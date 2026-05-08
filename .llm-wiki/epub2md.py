"""Convert EPUB to clean Markdown, preserving paragraph structure.
Usage: python epub2md.py <epub_path>
       python epub2md.py --all   # convert all EPUBs in sources/books/
"""
import zipfile, re, sys, os, glob as globmod
from xml.etree import ElementTree as ET

NS = {
    'opf': 'http://www.idmp.org/2007/opf',
    'dc': 'http://purl.org/dc/elements/1.1/',
}

def strip_html(text):
    """Strip HTML tags and CSS bloat, preserve paragraph breaks."""
    text = re.sub(r':root\s*\{[^}]*\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\[imt-[^\]]*\]\s*\{[^}]*\}', '', text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    for tag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'br',
                'tr', 'section', 'article', 'blockquote']:
        text = re.sub(rf'</?{tag}[^>]*>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&apos;', "'").replace('&#39;', "'")
    text = text.replace('&nbsp;', ' ').replace('\xa0', ' ')
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = [line.strip() for line in text.split('\n')]
    return '\n'.join(lines)

def derive_title_authors(filename):
    """Derive title and authors from EPUB filename."""
    name = os.path.splitext(filename)[0]
    name = re.sub(r'机翻\w*$', '', name).strip()

    authors = []
    m = re.search(r'\(([^)]+)\)$', name)
    if m:
        authors = [a.strip() for a in m.group(1).split(',') if a.strip()]
        name = name[:m.start()].strip()

    return name.strip(), authors

def extract_epub(epub_path):
    """Extract EPUB to Markdown. Writes .md alongside the .epub."""
    output_path = re.sub(r'\.epub$', '.md', epub_path)
    title, authors = derive_title_authors(os.path.basename(epub_path))

    with zipfile.ZipFile(epub_path) as z:
        all_names = z.namelist()

        container = ET.parse(z.open('META-INF/container.xml'))
        rootfile = container.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
        opf_path = rootfile.get('full-path')
        opf_dir = os.path.dirname(opf_path)

        opf = ET.parse(z.open(opf_path))

        # Better metadata from OPF if valid AND more complete than filename
        opf_title = opf.getroot().find('.//dc:title', NS)
        if opf_title is not None and opf_title.text and len(opf_title.text.strip()) > 2:
            t = opf_title.text.strip()
            if re.search(r'[一-鿿぀-ゟァ-ヺa-zA-Z0-9]', t) and len(t) > len(title):
                title = t

        opf_authors = []
        for creator in opf.getroot().findall('.//dc:creator', NS):
            if creator.text and creator.text.strip():
                opf_authors.append(creator.text.strip())
        if opf_authors:
            authors = opf_authors

        # Build manifest
        manifest = {}
        for item in opf.getroot().findall('.//opf:item', NS):
            manifest[item.get('id')] = item.get('href')

        # Determine chapter order: spine, then fallback to sorted XHTML
        chapters = []
        spine = opf.getroot().find('.//opf:spine', NS)
        if spine is not None:
            for itemref in spine.findall('opf:itemref', NS):
                href = manifest.get(itemref.get('idref'))
                if href:
                    full = os.path.normpath(
                        os.path.join(opf_dir, href)).replace('\\', '/')
                    if full in all_names:
                        chapters.append(full)

        if not chapters:
            xhtml_files = [n for n in all_names
                          if n.endswith(('.xhtml', '.html'))
                          and 'cover' not in n.lower()
                          and 'toc' not in n.lower()
                          and 'nav' not in n.lower()]
            def sort_key(p):
                bn = os.path.basename(p)
                if 'book-part' in bn or 'chapter' in bn:
                    return (0, bn)
                elif 'front' in bn:
                    return (1, bn)
                elif 'index' in bn or 'ref' in bn:
                    return (3, bn)
                else:
                    return (2, bn)
            chapters = sorted(xhtml_files, key=sort_key)

    # Write Markdown
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write('---\n')
        out.write(f'title: "{title}"\n')
        out.write(f'author: "{", ".join(authors)}"\n')
        out.write(f'source: "{os.path.basename(epub_path)}"\n')
        out.write(f'format: epub2md\n')
        out.write('---\n\n')
        out.write(f'# {title}\n\n')
        if authors:
            out.write(f'**作者**: {", ".join(authors)}\n\n')
        out.write('---\n\n')

        with zipfile.ZipFile(epub_path) as z:
            written = 0
            for i, ch_path in enumerate(chapters):
                content = z.read(ch_path).decode('utf-8', errors='replace')
                cleaned = strip_html(content)
                if len(cleaned.strip()) < 100:
                    continue
                if written > 0:
                    out.write('\n\n---\n\n')
                out.write(cleaned)
                written += 1

    return title, authors, output_path, written

def convert_all():
    """Convert all EPUBs in sources/books/."""
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    books_dir = os.path.join(repo, 'sources', 'books')
    epubs = globmod.glob(os.path.join(books_dir, '*.epub'))
    results = []
    for epub in epubs:
        try:
            title, authors, path, n = extract_epub(epub)
            results.append((os.path.basename(epub), title, authors, n))
        except Exception as e:
            results.append((os.path.basename(epub), f'ERROR: {e}', [], 0))

    # Write summary to a file to avoid console encoding issues
    summary_path = os.path.join(repo, 'temp_epub2md_summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write('EPUB to MD Conversion Summary\n')
        f.write('=' * 60 + '\n\n')
        for epub, title, authors, n in results:
            f.write(f'EPUB: {epub}\n')
            f.write(f'Title: {title}\n')
            f.write(f'Authors: {", ".join(authors)}\n')
            f.write(f'Chapters: {n}\n')
            f.write(f'{"-" * 40}\n')
    print(f'Summary written to: {summary_path}')
    return results

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        convert_all()
    elif len(sys.argv) > 1:
        # Single file mode — write output path to file to avoid console encoding
        title, authors, path, n = extract_epub(sys.argv[1])
        summary = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'temp_epub2md_summary.txt')
        with open(summary, 'w', encoding='utf-8') as f:
            f.write(f'Title: {title}\n')
            f.write(f'Authors: {", ".join(authors)}\n')
            f.write(f'Chapters: {n}\n')
            f.write(f'Output: {path}\n')
        print(f'Done. See: {summary}')
    else:
        print("Usage: python epub2md.py <epub_path>")
        print("       python epub2md.py --all")
