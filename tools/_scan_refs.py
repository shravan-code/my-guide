import re
from pathlib import Path


def is_probably_file_ref(ref: str) -> bool:
    # Most broken refs are file-like (have an extension) or known asset types.
    return ("." in Path(ref).name) and not ref.endswith("/")


def main() -> None:
    repo_root = Path(r"d:\shra1\github\my-guide").resolve()
    html_files = list(repo_root.rglob("*.html"))

    ref_re = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']')

    missing: list[tuple[str, str, str]] = []

    for html in html_files:
        try:
            text = html.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = html.read_text(encoding="latin-1")

        for m in ref_re.finditer(text):
            ref = m.group(1).strip()
            if not ref:
                continue

            if ref.startswith(("#", "mailto:", "tel:", "http://", "https://")):
                continue
            if ref.startswith("?"):
                continue

            # Resolve relative references.
            if ref.startswith("/"):
                resolved = (repo_root / ref.lstrip("/")).resolve()
            elif ref.startswith(("./", "../")):
                resolved = (html.parent / ref).resolve()
            else:
                # Same-directory refs without ./ (e.g. "cheatsheets.js")
                resolved = (html.parent / ref).resolve()

            # Only check "file-like" refs.
            if not is_probably_file_ref(ref):
                continue

            # Keep it within repo; ignore anything else.
            try:
                resolved.relative_to(repo_root)
            except Exception:
                continue

            # Existence check.
            if not resolved.exists():
                missing.append((str(html.relative_to(repo_root)), ref, str(resolved.relative_to(repo_root))))

    print(f"HTML files scanned: {len(html_files)}")
    print(f"Missing local refs: {len(missing)}")
    for html_rel, ref, resolved_rel in missing[:120]:
        print(f"- {html_rel}: {ref} -> {resolved_rel} (MISSING)")


if __name__ == "__main__":
    main()

