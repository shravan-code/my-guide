import os
import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

def is_external(url):
    parsed = urlparse(url)
    return bool(parsed.scheme or parsed.netloc)

def check_file_exists(filepath, base_dir):
    """Check if file exists relative to base_dir."""
    if filepath.startswith('/'):
        # root-relative path: treat as relative to repo root
        filepath = filepath[1:]
    path = os.path.join(base_dir, filepath)
    # Remove fragment and query string
    path = path.split('#')[0].split('?')[0]
    return os.path.exists(path)

def extract_links(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    links = []
    # anchor tags
    for a in soup.find_all('a', href=True):
        links.append(('a', a['href'], a))
    # link tags
    for link in soup.find_all('link', href=True):
        links.append(('link', link['href'], link))
    # area tags (if any)
    for area in soup.find_all('area', href=True):
        links.append(('area', area['href'], area))
    # script tags with src (not href but still a resource)
    for script in soup.find_all('script', src=True):
        links.append(('script', script['src'], script))
    # img tags with src
    for img in soup.find_all('img', src=True):
        links.append(('img', img['src'], img))
    return links

def main():
    root_dir = os.getcwd()
    broken = []
    total_checked = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fname in filenames:
            if not fname.endswith('.html'):
                continue
            html_file = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(html_file, root_dir)
            try:
                links = extract_links(html_file)
            except Exception as e:
                print(f"Error parsing {rel_path}: {e}")
                continue
            for tag, url, element in links:
                if is_external(url):
                    continue
                total_checked += 1
                # Determine base directory for this file
                base_dir = os.path.dirname(html_file)
                if not check_file_exists(url, base_dir):
                    # Try relative to root
                    if not check_file_exists(url, root_dir):
                        # Get line number (approx)
                        # Find the line containing this href in original file
                        with open(html_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        for i, line in enumerate(lines, 1):
                            # crude match
                            if url in line:
                                line_num = i
                                break
                        else:
                            line_num = None
                        broken.append((rel_path, line_num, tag, url))
    print(f"Checked {total_checked} internal links.")
    if broken:
        print("\nBroken links found:")
        for file, line, tag, url in broken:
            print(f"  {file}" + (f" (line {line})" if line else "") + f": <{tag} href=\"{url}\">")
    else:
        print("No broken links found.")

if __name__ == '__main__':
    main()
