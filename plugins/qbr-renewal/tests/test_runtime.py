from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load("qbr_installer_test", ROOT / "scripts/install.py")
extractor = load("qbr_extractor_test", ROOT / "skills/prepare-qbr-renewal/scripts/extract_qbr.py")


class MarketplaceTests(unittest.TestCase):
    def test_managed_snapshot_installs_without_git_and_refreshes_removed_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            snapshot = root / "download"
            (snapshot / ".agents/plugins").mkdir(parents=True)
            (snapshot / ".agents/plugins/marketplace.json").write_text('{"name":"zendesk-scaled-cs","plugins":[]}')
            (snapshot / "release.txt").write_text("first")
            data = root / "data"
            managed = data / "marketplace"
            with patch.object(installer, "run", side_effect=[json.dumps({"marketplaces": []}), json.dumps({"installedRoot": str(managed)})]) as run:
                self.assertEqual(managed, installer.prepare_marketplace("codex", snapshot=snapshot, data_root=data))
            self.assertFalse(any(call.args[0] == "git" for call in run.call_args_list))
            (managed / "removed.txt").write_text("old")
            (snapshot / "release.txt").write_text("second")
            with patch.object(installer, "run", return_value=self.listing(managed)):
                installer.prepare_marketplace("codex", snapshot=snapshot, data_root=data)
            self.assertEqual("second", (managed / "release.txt").read_text())
            self.assertFalse((managed / "removed.txt").exists())

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


class MigrationTests(unittest.TestCase):
    def test_different_endpoint_and_shared_marketplace_are_preserved(self):
        installed = {"installed": [{"pluginId": "another@qbr-express-local-delivery", "marketplaceName": "qbr-express-local-delivery"}]}
        markets = {"marketplaces": [{"name": "qbr-express-local-delivery"}]}
        servers = [{"name": "qbr-express", "transport": {"url": "https://other.example/mcp"}}]
        with tempfile.TemporaryDirectory() as temp, patch.object(installer, "run", side_effect=[json.dumps(installed), json.dumps(markets), json.dumps(servers)]) as run:
            installer.retire_legacy_qbr("codex", Path(temp))
        self.assertFalse(any("remove" in call.args for call in run.call_args_list))

    def test_cleanup_does_not_follow_symlinks_into_shared_tools(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = root / "data"
            shared = root / "shared"
            data.mkdir()
            shared.mkdir()
            (shared / "pomerium-cli").write_text("shared tool")
            (shared / "qbr-requirements.txt").write_text("shared runtime")
            (data / "bin").symlink_to(shared, target_is_directory=True)
            (data / "runtime-v1").symlink_to(shared, target_is_directory=True)
            with patch.object(installer, "run", side_effect=['{"installed":[]}', '{"marketplaces":[]}', '[]']):
                installer.retire_legacy_qbr("codex", data)
            self.assertEqual("shared tool", (shared / "pomerium-cli").read_text())
            self.assertEqual("shared runtime", (shared / "qbr-requirements.txt").read_text())
            self.assertFalse((data / "runtime-v1").is_symlink())


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
