#!/usr/bin/env python3
"""Report off-origin loads. Citation anchors are not loads."""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
fail = []
load_patterns = [
    (r'<(?:script|img|iframe|source|video|audio)[^>]+\bsrc="(https?://[^"]+)"', "html src"),
    (r'<link[^>]+href="(https?://[^"]+)"', "html link"),
    (r'url\(\s*["\']?(https?://[^)"\']+)', "css url()"),
    (r'@import\s+["\'](https?://[^"\']+)', "css @import"),
    (r'\bimport\s*(?:\(|[^;]*from\s*)["\'](https?://[^"\']+)', "js import"),
    (r'\bfetch\(\s*["\'`](https?://[^"\'`]+)', "js fetch"),
    (r'new (?:Worker|WebSocket|EventSource)\(\s*["\'`](https?://[^"\'`]+)', "js net"),
]
files = []
for pattern in ("*.html",):
    files.extend(ROOT.glob(pattern))
    files.extend((ROOT / "rooms").glob(pattern))
    files.extend((ROOT / "tracks").glob(pattern))
files.extend((ROOT / "assets").rglob("*.css"))
files.extend((ROOT / "assets").rglob("*.js"))
files.extend((ROOT / "guide").glob("*.js"))
files.extend((ROOT / "shared").rglob("*.js"))
files.append(ROOT / "sw.js")
seen = set()
for f in files:
    if not f.is_file() or f in seen:
        continue
    seen.add(f)
    text = f.read_text(errors="replace")
    for pat, kind in load_patterns:
        for m in re.finditer(pat, text):
            fail.append(f"{f.relative_to(ROOT)}: off-origin {kind}: {m.group(1)}")
for x in fail:
    print("FAIL", x)
print("csp_check:", len(fail), "off-origin loads")
sys.exit(1 if fail else 0)
