import os
import re
from urllib.parse import urlparse

def is_external(url):
    parsed = urlparse(url)
    return bool(parsed.scheme or parsed.netloc)

def check_file_exists(filepath, base_dir):
    if filepath.startswith('/'):
        filepath = filepath[1:]
    path = os.path.join(base_dir, filepath)
    # Remove fragment and query string
    path = path.split('#')[0].split('?')[0]
    return os.path.exists(path)

def extract_hrefs(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all href attributes in anchor, link, area, etc.
    # Pattern: href="..." or href='...'
    pattern = r'''(?:href|src)\s*=\s*["']([^"']+)["']'''
    matches = re.findall(pattern, content, re.IGNORECASE)
    return matches

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
                hrefs = extract_hrefs(html_file)
            except Exception as e:
                print(f"Error parsing {rel_path}: {e}")
                continue
            for url in hrefs:
                if is_external(url):
                    continue
                total_checked += 1
                base_dir = os.path.dirname(html_file)
                if not check_file_exists(url, base_dir):
                    if not check_file_exists(url, root_dir):
                        # Get line number
                        with open(html_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        line_num = None
                        for i, line in enumerate(lines, 1):
                            if url in line:
                                line_num = i
                                break
                        broken.append((rel_path, line_num, url))
    print(f"Checked {total_checked} internal links.")
    if broken:
        print("\nBroken links found:")
        for file, line, url in broken:
            print(f"  {file}" + (f" (line {line})" if line else "") + f": {url}")
    else:
        print("No broken links found.")

if __name__ == '__main__':
    main()
