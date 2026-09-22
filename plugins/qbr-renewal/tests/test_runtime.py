from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


server = load("qbr_delivery_test", ROOT / "mcp/server.py")
installer = load("qbr_installer_test", ROOT / "scripts/install.py")
extractor = load("qbr_extractor_test", ROOT / "skills/prepare-qbr-renewal/scripts/extract_qbr.py")


def response(body, start=0, total=None, status=206, headers=None):
    result = MagicMock(status_code=status)
    result.__enter__.return_value = result
    result.headers = {"Content-Type": "application/zip", "Content-Range": f"bytes {start}-{start+len(body)-1}/{total or len(body)}"}
    if headers:
        result.headers.update(headers)
    result.iter_content.return_value = [body]
    return result


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.home = patch.object(server.Path, "home", return_value=self.directory)
        self.home.start()
        self.addCleanup(self.home.stop)
        self.auth = patch.object(server, "pomerium_token", return_value="test-token")
        self.auth.start()
        self.addCleanup(self.auth.stop)

    def test_multirange_hash_and_nonoverwriting_delivery(self):
        body = b"PK\x03\x04abcdefgh"
        chunks = [response(body[i:i+4], i, len(body)) for i in range(0, len(body), 4)]
        directory = self.directory / "Generated QBRs"
        directory.mkdir()
        (directory / "deck.pptx").write_bytes(b"existing")
        with patch.object(server, "RANGE_SIZE", 4), patch.object(server.requests, "get", side_effect=chunks) as get:
            result = server.save_qbr_artifact("a" * 32, "../../deck.pptx", len(body))
        self.assertEqual(body, Path(result["path"]).read_bytes())
        self.assertEqual(b"existing", (directory / "deck.pptx").read_bytes())
        self.assertEqual("deck (1).pptx", result["filename"])
        self.assertEqual(hashlib.sha256(body).hexdigest(), result["sha256"])
        self.assertEqual(["bytes=0-3", "bytes=4-7", "bytes=8-11"], [c.kwargs["headers"]["Range"] for c in get.call_args_list])
        for call in get.call_args_list:
            self.assertFalse(call.kwargs["allow_redirects"])
            self.assertEqual({"_pomerium": "test-token"}, call.kwargs["cookies"])
        self.assertFalse(list(directory.glob("*.partial")))

    def test_size_can_be_discovered_from_server(self):
        body = b"%PDF-1.7 test"
        with patch.object(server.requests, "get", return_value=response(body)):
            result = server.save_qbr_artifact("b" * 32, "report.pdf")
        self.assertEqual(len(body), result["size"])

    def test_rejects_bad_transfers_and_removes_partial_files(self):
        cases = [
            response(b"PK\x03\x04data", status=302),
            response(b"<html>bad", headers={"Content-Type": "text/html"}),
            response(b"PK\x03\x04data", headers={"Content-Range": "bytes 2-9/10"}),
            response(b"PK\x03\x04data", headers={"Content-Range": "bytes 0-9/10"}),
            response(b"PK\x03\x04data", headers={"Content-Range": "bytes 0-3/4"}),
            response(b"not-an-artifact"),
            response(b"PK\x03\x04data", headers={"Content-Range": f"bytes 0-7/{server.MAX_SIZE+1}"}),
        ]
        for item in cases:
            with self.subTest(headers=item.headers, status=item.status_code):
                with patch.object(server.requests, "get", return_value=item), self.assertRaises(RuntimeError):
                    server.save_qbr_artifact("c" * 32, "report.pptx")
                self.assertEqual([], list((self.directory / "Generated QBRs").iterdir()))

    def test_explicit_size_mismatch_fails(self):
        with patch.object(server.requests, "get", return_value=response(b"PK\x03\x04data")), self.assertRaises(RuntimeError):
            server.save_qbr_artifact("d" * 32, "report.pptx", 10)

    def test_rejects_invalid_job_without_network(self):
        with patch.object(server.requests, "get") as get:
            for value in ("../../escape", "https://example.com", "x" * 32):
                with self.assertRaises(ValueError):
                    server.save_qbr_artifact(value)
            get.assert_not_called()

    def test_atomic_publish_handles_collision_during_creation(self):
        partial = self.directory / "temporary"
        partial.write_bytes(b"report")
        actual_link = server.os.link

        def racing_link(source, destination):
            if destination.name == "deck.pptx":
                destination.write_bytes(b"other download")
            return actual_link(source, destination)

        with patch.object(server.os, "link", side_effect=racing_link):
            result = server.publish_unique(partial, self.directory, "deck.pptx")
        self.assertEqual("deck (1).pptx", result.name)
        self.assertEqual(b"other download", (self.directory / "deck.pptx").read_bytes())


class AuthenticationTests(unittest.TestCase):
    def test_scoped_credential_and_no_output_leak(self):
        with patch.object(server.shutil, "which", return_value="/bin/pomerium-cli"), patch.object(server.subprocess, "run") as run:
            run.return_value.stdout = json.dumps({"status": {"token": "Pomerium-example"}})
            self.assertEqual("example", server.pomerium_token())
            self.assertEqual(server.QBR_URL, run.call_args.args[0][-1])
            run.side_effect = subprocess.CalledProcessError(1, ["cli"], stderr="private auth data")
            with self.assertRaises(RuntimeError) as error:
                server.pomerium_token()
            self.assertNotIn("private auth data", str(error.exception))


class MarketplaceTests(unittest.TestCase):
    def listing(self, root, kind="local", source=None):
        return json.dumps({"marketplaces": [{"name": installer.MARKETPLACE, "root": str(root), "marketplaceSource": {"sourceType": kind, "source": source or str(root)}}]})

    def test_new_marketplace_uses_codex_without_removal(self):
        with patch.object(installer, "run", side_effect=[json.dumps({"marketplaces": []}), json.dumps({"installedRoot": "/cache/market"})]) as run:
            self.assertEqual(Path("/cache/market"), installer.prepare_marketplace("codex"))
        self.assertEqual("add", run.call_args_list[1].args[3])

    def test_existing_git_marketplace_is_upgraded(self):
        with patch.object(installer, "run", side_effect=[self.listing("/cache/market", "git", installer.REPOSITORY), ""]) as run:
            installer.prepare_marketplace("codex")
        self.assertEqual(("codex", "plugin", "marketplace", "upgrade", installer.MARKETPLACE), run.call_args.args)

    def test_different_repository_is_preserved(self):
        with patch.object(installer, "run", return_value=self.listing("/cache/market", "git", "https://example.com/other.git")) as run:
            with self.assertRaisesRegex(RuntimeError, "different repository"):
                installer.prepare_marketplace("codex")
        self.assertEqual(1, run.call_count)

    def test_dirty_local_checkout_is_not_fetched_or_changed(self):
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / ".git").mkdir()
            with patch.object(installer, "run", side_effect=[self.listing(temp), installer.REPOSITORY, " M existing-file"]) as run:
                with self.assertRaisesRegex(RuntimeError, "local changes"):
                    installer.prepare_marketplace("codex")
            self.assertEqual(3, run.call_count)

    def test_clean_local_main_is_only_fast_forwarded(self):
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / ".git").mkdir()
            with patch.object(installer, "run", side_effect=[self.listing(temp), installer.REPOSITORY, "", "main", "", ""]) as run:
                installer.prepare_marketplace("codex")
            self.assertEqual(("git", "-C", temp, "merge", "--ff-only", "origin/main"), run.call_args.args)


class ExtractionTests(unittest.TestCase):
    def test_package_order_hidden_notes_and_external_image(self):
        import zipfile
        p = extractor.NS["p"]
        a = extractor.NS["a"]
        r = extractor.NS["r"]
        relationship_ns = extractor.REL[1:-1]
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "synthetic.pptx"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("ppt/presentation.xml", f'<p:presentation xmlns:p="{p}" xmlns:r="{r}"><p:sldIdLst><p:sldId id="1" r:id="s2"/><p:sldId id="2" r:id="s1"/></p:sldIdLst></p:presentation>')
                archive.writestr("ppt/_rels/presentation.xml.rels", f'<Relationships xmlns="{relationship_ns}"><Relationship Id="s1" Type="slide" Target="slides/slide1.xml"/><Relationship Id="s2" Type="slide" Target="slides/slide2.xml"/></Relationships>')
                for num in (1, 2):
                    archive.writestr(f"ppt/slides/slide{num}.xml", f'<p:sld xmlns:p="{p}" xmlns:a="{a}" xmlns:r="{r}" show="{0 if num==2 else 1}"><p:cSld><p:spTree><p:sp><a:p><a:r><a:t>Slide {num}</a:t></a:r></a:p></p:sp><a:blip r:link="external"/></p:spTree></p:cSld></p:sld>')
                archive.writestr("ppt/slides/_rels/slide2.xml.rels", f'<Relationships xmlns="{relationship_ns}"><Relationship Id="note" Type="notesSlide" Target="../notesSlides/notesSlide2.xml"/><Relationship Id="external" Type="image" Target="https://example.invalid/never-fetch" TargetMode="External"/></Relationships>')
                archive.writestr("ppt/notesSlides/notesSlide2.xml", f'<p:notes xmlns:p="{p}" xmlns:a="{a}"><p:sp><a:p><a:r><a:t>Dated context only</a:t></a:r></a:p></p:sp></p:notes>')
            evidence = extractor.extract(source, Path(temp) / "media")
            self.assertEqual(["Slide 2", "Slide 1"], [slide["title"] for slide in evidence["slides"]])
            self.assertTrue(evidence["slides"][0]["hidden"])
            self.assertEqual(["Dated context only"], evidence["slides"][0]["notes"])
            self.assertTrue(evidence["slides"][0]["images"][0]["external"])
            self.assertEqual("not_reviewed", evidence["slides"][0]["review_status"])
            self.assertFalse((Path(temp) / "media").exists())


if __name__ == "__main__":
    unittest.main()
