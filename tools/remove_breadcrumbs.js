// Automated removal of breadcrumb markup from all HTML files under the repository.
// This is a one-time utility to fully remove breadcrumb elements and any breadcrumb-like navs.
// Usage: node tools/remove_breadcrumbs.js

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

function walk(dir, fileList = []) {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      walk(full, fileList);
    } else if (stat.isFile() && full.endsWith('.html')) {
      fileList.push(full);
    }
  }
  return fileList;
}

function removeBreadcrumbsFrom(content) {
  // Remove <nav class="breadcrumb" ...>...</nav> and <nav class="breadcrumb-pill" ...>...</nav>
  content = content.replace(/<nav\s+class=["']breadcrumb[^>]*>[\s\S]*?<\/nav>/gi, '');
  content = content.replace(/<nav\s+class=["']breadcrumb-pill[^>]*>[\s\S]*?<\/nav>/gi, '');
  // Remove standalone breadcrumb pills if any
  content = content.replace(/<div\s+class=["']breadcrumb[^>]*>[\s\S]*?<\/div>/gi, '');
  return content;
}

function main() {
  // Target all HTML files under the repository (recursively)
  const files = walk(path.resolve(__dirname, '..'));
  let count = 0;
  for (const file of files) {
    let content = fs.readFileSync(file, 'utf8');
    const original = content;
    content = removeBreadcrumbsFrom(content);
    if (content !== original) {
      fs.writeFileSync(file, content, 'utf8');
      count++;
      console.log(`Updated: ${file}`);
    }
  }
  console.log(`Breadcrumbs removed from ${count} files.`);
}

main();
