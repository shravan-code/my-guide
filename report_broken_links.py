import sys
import re
from collections import defaultdict

lines = open('broken_links.txt', 'r').readlines()
unique = set()
for line in lines:
    line = line.strip()
    if not line:
        continue
    unique.add(line)

# Group by file
groups = defaultdict(list)
for entry in unique:
    # parse format: "  file (line XX): url"
    m = re.match(r'^\s+(.*?)\s+\(line (\d+)\):\s+(.*)$', entry)
    if m:
        file, line_num, url = m.groups()
        groups[file].append((int(line_num), url))
    else:
        groups[entry].append((None, ''))

print("=== BROKEN LINKS REPORT ===")
print(f"Total unique broken links: {len(unique)}")
print()
for file, entries in sorted(groups.items()):
    print(f"File: {file}")
    for line_num, url in sorted(entries, key=lambda x: x[0] if x[0] else 0):
        if line_num:
            print(f"  Line {line_num}: {url}")
        else:
            print(f"  {url}")
    print()
