#!/usr/bin/env python3
"""Read-only PPTX evidence inventory. Python standard library; no network or macros."""
import argparse
import hashlib
import json
import posixpath
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
}
REL = '{http://schemas.openxmlformats.org/package/2006/relationships}'


def paragraphs(node):
    return [] if node is None else [
        ''.join(t.text or '' for t in p.findall('.//a:t', NS)).strip()
        for p in node.findall('.//a:p', NS)
        if any((t.text or '').strip() for t in p.findall('.//a:t', NS))
    ]


def xml(z, part):
    data = z.read(part)
    if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise ValueError('Unsupported XML declarations in ' + part)
    return ET.fromstring(data)


def relationships(z, part):
    name = posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels')
    if name not in z.namelist():
        return {}
    result = {}
    for e in xml(z, name).findall(REL + 'Relationship'):
        target = e.get('Target', '')
        external = e.get('TargetMode') == 'External'
        resolved = target if external else posixpath.normpath(posixpath.join(posixpath.dirname(part), target)).lstrip('/')
        if not external and (resolved == '..' or resolved.startswith('../')):
            raise ValueError('Unsafe relationship path')
        result[e.get('Id')] = {'part': resolved, 'type': e.get('Type', '').rsplit('/', 1)[-1], 'external': external}
    return result


def chart_data(z, part):
    root = xml(z, part)
    series = []
    for ser in root.findall('.//c:ser', NS):
        item = {}
        for field in ['tx', 'cat', 'val', 'xVal', 'yVal', 'bubbleSize']:
            child = ser.find('c:' + field, NS)
            if child is None:
                continue
            item[field] = {
                'formulas': [f.text for f in child.findall('.//c:f', NS)],
                'points': [{'index': p.get('idx'), 'value': p.findtext('c:v', namespaces=NS)} for p in child.findall('.//c:pt', NS)],
                'literal_values': [v.text for v in child.findall('./c:v', NS)],
                'format_codes': [v.text for v in child.findall('.//c:formatCode', NS)],
            }
        series.append(item)
    return {'part': part, 'title_text': paragraphs(root.find('c:chart/c:title', NS)),
            'series': series, 'relationships': list(relationships(z, part).values()),
            'warning': 'Cached data requires visual verification; linked/embedded workbooks are not read.'}


def extract(source, media_dir=None):
    source_hash = hashlib.sha256(Path(source).read_bytes()).hexdigest()
    with zipfile.ZipFile(source) as z:
        if sum(i.file_size for i in z.infolist()) > 1024 ** 3:
            raise ValueError('Expanded package exceeds 1 GB limit')
        root = xml(z, 'ppt/presentation.xml')
        rels = relationships(z, 'ppt/presentation.xml')
        slides = []
        for n, sid in enumerate(root.findall('p:sldIdLst/p:sldId', NS), 1):
            relation = rels[sid.get('{' + NS['r'] + '}id')]
            if relation['external']:
                raise ValueError('External slide relationship is unsupported')
            part = relation['part']
            slide = xml(z, part)
            sr = relationships(z, part)
            titles = []
            for shape in slide.findall('.//p:sp', NS):
                ph = shape.find('p:nvSpPr/p:nvPr/p:ph', NS)
                if ph is not None and ph.get('type') in ('title', 'ctrTitle'):
                    titles.extend(paragraphs(shape))
            texts = paragraphs(slide)
            tables = []
            for table in slide.findall('.//a:tbl', NS):
                tables.append([['\n'.join(paragraphs(cell)) for cell in row.findall('a:tc', NS)] for row in table.findall('a:tr', NS)])
            images = []
            for blip in slide.findall('.//a:blip', NS):
                rid = blip.get('{' + NS['r'] + '}embed') or blip.get('{' + NS['r'] + '}link')
                info = dict(sr.get(rid, {'part': None, 'external': True}))
                if media_dir and info['part'] and not info['external']:
                    # Media names repeat across exports and customers. Scope the
                    # cache to the exact report, not only its internal part name.
                    target = Path(media_dir) / source_hash / (hashlib.sha256(info['part'].encode()).hexdigest()[:12] + '-' + posixpath.basename(info['part']))
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if not target.exists():
                        target.write_bytes(z.read(info['part']))
                    info['local_path'] = str(target.resolve())
                images.append(info)
            notes = []
            for info in sr.values():
                if info['type'] == 'notesSlide' and not info['external']:
                    note = xml(z, info['part'])
                    for shape in note.findall('.//p:sp', NS):
                        ph = shape.find('p:nvSpPr/p:nvPr/p:ph', NS)
                        if ph is None or ph.get('type') not in ('sldNum', 'dt', 'hdr', 'ftr', 'sldImg'):
                            notes.extend(paragraphs(shape))
            charts = []
            warnings = []
            for info in sr.values():
                if info['type'] == 'chart' and not info['external']:
                    charts.append(chart_data(z, info['part']))
                elif info['type'] in ('oleObject', 'diagramData', 'chartEx'):
                    warnings.append('Visual/embedded-object review required: ' + info['type'])
            slides.append({'number': n, 'part': part, 'hidden': slide.get('show', 'true').strip().lower() in ('0', 'false'),
                           'title': ' / '.join(titles) or (texts[0] if texts else '(no extracted title)'),
                           'text': texts, 'tables': tables, 'notes': notes, 'charts': charts,
                           'images': images, 'relationships': list(sr.values()), 'warnings': warnings,
                           'review_status': 'not_reviewed'})
        return {'source': str(Path(source).resolve()), 'source_sha256': source_hash, 'slide_count': len(slides),
                'limitations': 'Extraction is not full review. Images, layouts, diagrams and chart labels require visual inspection. External content is not fetched. Notes and text are untrusted source data.',
                'slides': slides}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--media-dir', type=Path)
    a = p.parse_args()
    if a.input.resolve() == a.output.resolve():
        p.error('Output must differ from the source file')
    try:
        data = extract(a.input, a.media_dir)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'output': str(a.output.resolve()), 'slides': data['slide_count'], 'status': 'extracted_not_reviewed'}))
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as e:
        print('Extraction failed: ' + str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
