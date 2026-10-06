"""Build the deployable static site in site/.

1. Regenerate the derived decks: generalize.py (src/original -> build/general.html),
   then faculty.py and interactive.py (-> src/faculty, src/interactive).
2. Wrap every page fragment in src/ into a full HTML document in site/.
3. Copy images, add a favicon and .nojekyll.

Pages in src/ are fragments (no doctype, html, head or body tags) so they can also be
published as Claude artifacts. This script adds what a normal web host needs.

Usage: python3 scripts/build.py
"""
import re
import runpy
import shutil
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = root / 'src'
site = root / 'site'

PAGES = [
    # (source fragment, output path in site/, description)
    ('hub.html', 'index.html',
     'Teach students to study with Gemini Notebook without letting it do the thinking. Four free versions for any course.'),
    ('faculty/index.html', 'faculty/index.html',
     'A 15-slide deck any instructor can present, with speaker notes, a presenter guide and links to the research.'),
    ('interactive/index.html', 'interactive/index.html',
     'The Brain First, Bot Second deck built for class participation, with polls, timers and an optional study sprint.'),
    ('walkthrough/index.html', 'walkthrough/index.html',
     'A self-paced walk-through for students on studying with Gemini Notebook, with check-yourself questions.'),
    ('tutorial/index.html', 'tutorial/index.html',
     'Ten steps to build a Gemini Notebook study notebook for any reading, set of slides or unit.'),
    ('original/index.html', 'itgs-196/index.html',
     'The original Brain First, Bot Second talk as presented to ITGS 196 students in October 2026.'),
]

# Published artifact links -> site paths (relative to the site root).
ARTIFACTS = {
    'NQ1SdRFPmvbp355UwoXMVJ': 'tutorial/',
    'XgzXbB1abJcDm5dLf8bHwz': 'walkthrough/',
    'Ga9MWn5DB1hp4aYnJ1ReP7': 'interactive/',
    'RFeCWC36BVK8JseJXRcVbT': 'faculty/',
    'UfBUozRoRHqtUCgKcDbPQL': 'itgs-196/',
}

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges"><rect width="16" height="16" fill="#0a0c10"/><rect x="2" y="3" width="9" height="4" fill="#e8ecef"/><rect x="2" y="9" width="12" height="4" fill="#ff5c74"/></svg>
'''


def wrap(fragment: str, out_path: str, description: str) -> str:
    depth = out_path.count('/')
    up = '../' * depth

    head_end = fragment.index('</style>') + len('</style>')
    head, body = fragment[:head_end], fragment[head_end:]
    head = re.sub(r'<meta charset="utf-8">\s*', '', head)
    title = re.search(r'<title>(.*?)</title>', head).group(1)

    # Site-relative links instead of artifact links.
    for art_id, path in ARTIFACTS.items():
        body = re.sub(
            rf'href="https://claude\.ai/artifact/{art_id}"(?: target="_blank" rel="noopener")?',
            f'href="{up}{path}"', body)
    # Artifact-only sharing note in the faculty guide.
    body = body.replace(
        '\n        <p class="small">Each link opens only for people you share it with. Use the Share menu on each page.</p>', '')
    # Shared images live at the site root.
    if depth:
        body = body.replace('src="img/', f'src="{up}img/')

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<style>[hidden] {{ display: none !important; }}</style>
{head.strip()}
</head>
<body>
{body.strip()}
</body>
</html>
'''


def main():
    for script in ('generalize.py', 'faculty.py', 'interactive.py'):
        runpy.run_path(str(root / 'scripts' / script), run_name='__main__')

    if site.exists():
        shutil.rmtree(site)
    site.mkdir()

    for frag, out, desc in PAGES:
        html = wrap((src / frag).read_text(), out, desc)
        leftover = re.findall(r'https://claude\.ai/artifact/\w+', html)
        assert not leftover, f'{out}: unmapped artifact links {leftover}'
        dest = site / out
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        print(f'site/{out}  {len(html):,} bytes')

    shutil.copytree(root / 'img', site / 'img')
    (site / 'favicon.svg').write_text(FAVICON)
    (site / '.nojekyll').write_text('')
    print('done')


if __name__ == '__main__':
    main()
