"""Check EPUB structure: metadata, spine, files."""
import zipfile, os, sys
from xml.etree import ElementTree as ET

NS = {
    'opf': 'http://www.idmp.org/2007/opf',
    'dc': 'http://purl.org/dc/elements/1.1/',
}

epub = sys.argv[1]
with zipfile.ZipFile(epub) as z:
    container = ET.parse(z.open('META-INF/container.xml'))
    rootfile = container.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
    opf_path = rootfile.get('full-path')
    print('OPF:', opf_path)

    opf_dir = os.path.dirname(opf_path)
    opf = ET.parse(z.open(opf_path))

    # Metadata
    for el in opf.getroot().findall('.//'):
        tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
        if tag in ('title', 'creator', 'language', 'date', 'identifier'):
            text = el.text.strip() if el.text else ''
            print(f'  {tag}: {text}')

    # Manifest
    manifest = {}
    for item in opf.getroot().findall('.//opf:item', NS):
        manifest[item.get('id')] = item.get('href')

    # Spine
    spine = opf.getroot().find('.//opf:spine', NS)
    print('\nSpine:')
    for itemref in spine.findall('opf:itemref', NS):
        ref_id = itemref.get('idref')
        href = manifest.get(ref_id)
        if href:
            full = os.path.normpath(os.path.join(opf_dir, href)).replace('\\', '/')
            print(f'  {ref_id}: {full}')
