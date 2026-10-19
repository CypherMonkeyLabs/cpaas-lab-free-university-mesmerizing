#!/usr/bin/env python3
"""Write the static CPaaS study lab."""
import html
import json
import zipfile
from pathlib import Path

from facts import ROOMS, SOURCES, TRACKS

ROOT = Path(__file__).resolve().parents[1]
BRAND = "https://cyphermonkeylabs.com"
CSP = (
    '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; '
    "script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; "
    "media-src 'self' blob: data:; font-src 'self' data:; connect-src 'self'; "
    "worker-src 'self' blob:; object-src 'none'; base-uri 'self'; form-action 'self'\">"
)
REPO = "https://github.com/CypherMonkeyLabs"
TREE = "https://linktr.ee/cypherMonkey"

NAV = [
    ("index.html", "Home", "Twelve tracks. Start here if you are new.", "home"),
    ("start.html", "Learn", "Ten minutes, or the full course.", "learn"),
    ("diagrams.html", "Diagrams", "Still drawings you can export.", "diagrams"),
    ("flows.html", "Flows", "Ladders with a moving packet.", "flows"),
    ("play.html", "Play", "A short drill in this browser.", "play"),
    ("listen.html", "Listen", "Read-along notes for the guide.", "listen"),
    ("downloads.html", "Downloads", "Sheets, cards, and one zip.", "downloads"),
    ("quizzes.html", "Quizzes", "True or false from the lessons.", "play"),
    ("flashcards.html", "Flashcards", "Terms from the lessons.", "downloads"),
    ("ecosystem.html", "Ecosystem", "Glossary, bridges, and sister labs.", "eco"),
    ("help.html", "Help", "How the menu, course, and bot work.", "help"),
    ("legal.html", "Legal", "Study notes and trademarks.", "help"),
]

ICONS = {
    "home": '<path d="M4 10.5 12 4l8 6.5V20a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1z"/>',
    "learn": '<path d="M4 6h16v12H4z"/><path d="M8 10h8M8 14h5"/>',
    "diagrams": '<rect x="4" y="5" width="16" height="14" rx="2"/><path d="m7 15 3-3 2 2 3-4"/>',
    "flows": '<path d="M4 7h16M4 12h16M4 17h10"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "play": '<path d="M8 5v14l11-7z"/>',
    "listen": '<path d="M4 13a8 8 0 0 1 16 0"/><rect x="3" y="13" width="4" height="6" rx="1"/><rect x="17" y="13" width="4" height="6" rx="1"/>',
    "downloads": '<path d="M12 4v10M8 10l4 4 4-4M5 19h14"/>',
    "eco": '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2 2.4 3 5 3 8s-1 5.6-3 8c-2-2.4-3-5-3-8s1-5.6 3-8z"/>',
    "help": '<circle cx="12" cy="12" r="8"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.8.4-1 .9-1 1.7V14"/><path d="M12 17h.01"/>',
    "track": '<path d="M4 6h16v12H4z"/><path d="M8 10h8M8 14h5"/>',
}


def e(text):
    return html.escape(str(text), quote=True)


def svg_icon(name):
    body = ICONS.get(name, ICONS["track"])
    return (
        '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
        'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' + body + "</svg>"
    )


def prefix(depth):
    return "../" * depth


def rooms_for(track):
    return [r for r in ROOMS if r["track"] == track]


def track_by_id(tid):
    for t in TRACKS:
        if t[0] == tid:
            return t
    raise KeyError(tid)


def source_rows(keys, confirms):
    rows = []
    for key in keys:
        kind, title, url = SOURCES[key]
        rows.append((kind, title, url, ""))
    for note in confirms:
        rows.append(("Confirm", note, None, ""))
    return rows


def go_deeper(rows, json_href, md_href=None):
    items = []
    for kind, title, url, _note in rows:
        if url:
            items.append(
                f"<li><strong>{e(kind)}.</strong> <a href=\"{e(url)}\" style=\"color:#134e4a\">{e(title)}</a> "
                f"<span style=\"white-space:nowrap\">last checked 2026-10</span></li>"
            )
        else:
            items.append(
                f"<li><strong>{e(kind)}.</strong> {e(title)} "
                f"<span style=\"white-space:nowrap\">last checked 2026-10</span></li>"
            )
    extra = f' <a href="{e(md_href)}">Markdown</a>' if md_href else ""
    return (
        '<section class="go-deeper" style="margin:28px 0;padding:16px 18px;border:2px solid #0f766e;'
        'border-radius:16px;background:#f0fdfa;color:#042f2e"><h2>Sources and go deeper</h2>'
        "<p>Opened 2026-10. A row marked confirm has no link, because that page was not verified.</p><ul>"
        + "".join(items)
        + f"</ul><p><a href=\"{e(json_href)}\">sources.json</a>{extra}</p></section>"
    )


def footer(depth):
    p = prefix(depth)
    more = (
        f'<nav class="footer-meta" aria-label="More pages">'
        f'<a href="{p}quizzes.html">Quizzes</a>'
        f'<a href="{p}flashcards.html">Flashcards</a>'
        f'<a href="{p}legal.html">Legal</a>'
        f"</nav>"
    )
    return f"""<footer class="site-footer lab-footer wrap" data-canon-footer><aside class="disclaimer-panel" aria-labelledby="disc-title"><span class="disclaimer-ico"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5 4.5 5.5v5.8c0 4.6 3.1 8.6 7.5 10.2 4.4-1.6 7.5-5.6 7.5-10.2V5.5z" fill="currentColor" opacity=".18" stroke="currentColor" stroke-width="1.6"/><path d="M8.2 12.2 11 15l4.8-5.2" fill="none" stroke="#0f766e" stroke-width="1.8" stroke-linecap="round"/></svg></span><div><h2 id="disc-title">A note from the student behind this lab</h2><p>This is an <strong>independent, free, learning-only student project</strong>. These are study notes. They are <strong>not vendor documentation and not legal advice</strong>. Twilio, Vonage, Bandwidth, Sinch, Telnyx, Plivo, Infobip, Bird, MessageBird, and the open-source project names are trademarks of their owners. It is <strong>not affiliated with or endorsed by</strong> any of them.</p><p>If anyone has a concern, the content will be removed or corrected promptly via the contact form at <a href="{BRAND}/#contact">{BRAND}/#contact</a>. Nothing here is sold. I am happy to volunteer for any organization.</p><p>Emergency-calling and call-recording chapters are study notes. They are not an emergency plan. Rules differ by country and by the system you run. Figures that depend on a release are marked confirm.</p></div></aside>{more}<p class="footer-brand">CypherMonkey Labs</p><nav class="brand-row brand-icons" aria-label="CypherMonkey Labs"><a class="brand-icon brand-web" href="{BRAND}" aria-label="CypherMonkey Labs website"><svg viewBox="0 0 64 64" class="monkey-icon" aria-hidden="true"><defs><radialGradient id="mh" cx="38%" cy="30%" r="80%"><stop offset="0" stop-color="#ffd9a0"/><stop offset=".5" stop-color="#e8903a"/><stop offset="1" stop-color="#8a3f10"/></radialGradient></defs><circle cx="14" cy="34" r="7" fill="url(#mh)"/><circle cx="50" cy="34" r="7" fill="url(#mh)"/><circle cx="32" cy="32" r="18" fill="url(#mh)"/><ellipse cx="32" cy="38" rx="10" ry="8" fill="#fde68a"/><circle cx="26" cy="31" r="2" fill="#2a1406"/><circle cx="38" cy="31" r="2" fill="#2a1406"/><circle cx="26" cy="31" r="6" fill="#e0f2fe" opacity=".45" stroke="#fde047" stroke-width="1.6"/><circle cx="38" cy="31" r="6" fill="#e0f2fe" opacity=".45" stroke="#fde047" stroke-width="1.6"/><path d="M27 42 q5 4 10 0" fill="none" stroke="#7c2d12" stroke-width="1.6" stroke-linecap="round"/></svg></a><a class="brand-icon brand-gh" href="{REPO}" aria-label="CypherMonkey Labs on GitHub"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .5A11.5 11.5 0 0 0 .5 12.3c0 5.22 3.38 9.65 8.07 11.22.59.12.8-.26.8-.57v-2.02c-3.28.73-3.97-1.42-3.97-1.42-.53-1.38-1.3-1.75-1.3-1.75-1.07-.75.08-.73.08-.73 1.18.08 1.8 1.24 1.8 1.24 1.05 1.84 2.76 1.31 3.43.99.1-.78.41-1.31.75-1.61-2.62-.31-5.37-1.34-5.37-5.98 0-1.32.46-2.4 1.22-3.25-.12-.3-.53-1.53.12-3.18 0 0 1-.33 3.3 1.25a11.3 11.3 0 0 1 6 0c2.3-1.58 3.3-1.25 3.3-1.25.65 1.65.24 2.88.12 3.18.76.85 1.22 1.93 1.22 3.25 0 4.65-2.76 5.66-5.39 5.96.42.38.8 1.12.8 2.26v3.35c0 .31.21.7.81.57A11.52 11.52 0 0 0 23.5 12.3 11.5 11.5 0 0 0 12 .5z"/></svg></a><a class="brand-icon brand-tree" href="{TREE}" aria-label="CypherMonkey on Linktree"><svg viewBox="0 0 64 64" aria-hidden="true"><defs><filter id="zta-tree-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.2"/></filter></defs><g filter="url(#zta-tree-glow)" fill="#bbf7d0"><circle cx="32" cy="10" r="7"/><rect x="29" y="14" width="6" height="12" rx="3"/><circle cx="14" cy="30" r="6.5"/><circle cx="50" cy="30" r="6.5"/><rect x="16" y="27" width="32" height="6" rx="3"/><rect x="29" y="30" width="6" height="12" rx="3"/><circle cx="12" cy="46" r="6.5"/><circle cx="52" cy="46" r="6.5"/><rect x="14" y="43" width="36" height="6" rx="3"/><rect x="27" y="46" width="10" height="14" rx="5"/></g><g fill="#f7fee7" stroke="#052e16" stroke-width="1.6" stroke-linejoin="round"><circle cx="32" cy="10" r="7"/><rect x="29" y="14" width="6" height="12" rx="3"/><circle cx="14" cy="30" r="6.5"/><circle cx="50" cy="30" r="6.5"/><rect x="16" y="27" width="32" height="6" rx="3"/><rect x="29" y="30" width="6" height="12" rx="3"/><circle cx="12" cy="46" r="6.5"/><circle cx="52" cy="46" r="6.5"/><rect x="14" y="43" width="36" height="6" rx="3"/><rect x="27" y="46" width="10" height="14" rx="5"/></g></svg></a></nav><p class="site-copy">© 2026 CypherMonkeyLabs 🐒</p></footer>"""


def phone(depth):
    p = prefix(depth)
    return (
        f'<nav class="phone-bar" aria-label="Phone"><button type="button" data-menu-open data-tour="menu">'
        f'<span class="is-menu">{svg_icon("menu")}</span>Menu</button>'
        f'<a href="{p}start.html" data-tour="learn">{svg_icon("learn")}Learn</a>'
        f'<a href="{p}diagrams.html" data-tour="diagrams">{svg_icon("diagrams")}Diagrams</a>'
        f'<a href="{p}play.html" data-tour="play">{svg_icon("play")}Play</a>'
        f'<button type="button" data-listen data-tour="listen">{svg_icon("listen")}Listen</button>'
        f'<button type="button" data-open-guide>{svg_icon("help")}Guide</button></nav>'
    )


def chrome_open(title, desc, depth, current):
    p = prefix(depth)
    chips = []
    drawer = []
    for href, label, blurb, icon in NAV:
        here = ' aria-current="page"' if href == current else ""
        chips.append(
            f'<a class="section-chip" href="{p}{href}" data-tour="{icon}"{here} title="{e(blurb)}">'
            f'<span class="chip-ico">{svg_icon(icon)}</span>'
            f'<span class="chip-copy"><span class="chip-name">{e(label)}</span>'
            f'<span class="chip-desc">{e(blurb)}</span></span></a>'
        )
        drawer.append(
            f'<li><a data-menu-text="{e(label.lower()+" "+blurb.lower())}" href="{p}{href}">'
            f'<span class="ico">{svg_icon(icon)}</span><span><strong>{e(label)}</strong>'
            f'<span class="desc">{e(blurb)}</span></span></a></li>'
        )
    for tid, name, blurb, _color in TRACKS:
        href = f"tracks/{tid}.html"
        here = ' aria-current="page"' if href == current else ""
        drawer.append(
            f'<li><a data-menu-text="{e(name.lower()+" "+blurb.lower())}" href="{p}{href}">'
            f'<span class="ico">{svg_icon("track")}</span><span><strong>{e(name)}</strong>'
            f'<span class="desc">{e(blurb)}</span></span></a></li>'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
{CSP}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · CPaaS Lab</title>
<meta name="description" content="{e(desc)}">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{p}manifest.webmanifest">
<script src="{p}assets/js/theme-boot.js"></script>
<link rel="stylesheet" href="{p}assets/css/canon.css"><link rel="stylesheet" href="{p}assets/css/shell.css"><link rel="stylesheet" href="{p}assets/css/wow.css"><link rel="stylesheet" href="{p}assets/css/frame.css"><link rel="stylesheet" href="{p}assets/css/polish.css"><link rel="stylesheet" href="{p}assets/css/footer.css"><link rel="stylesheet" href="{p}assets/css/university.css"><link rel="stylesheet" href="{p}assets/css/uc.css"><link rel="stylesheet" href="{p}assets/css/cpaas.css">
<link rel="stylesheet" href="{p}guide/guide.css">
</head>
<body class="uc-lab">
<a class="skip" href="#main">Skip to content</a>
<header class="uc-top">
<div class="bar-inner">
<button type="button" class="menu-btn" data-menu-open data-tour="menu" aria-expanded="false" aria-controls="site-drawer">{svg_icon("menu")} Menu</button>
<a class="brand" href="{p}index.html" data-tour="home"><span>CPaaS Lab<small>Free University</small></span></a>
<form class="nav-search" role="search"><input class="nav-q" data-nav-search type="search" placeholder="Search lessons" aria-label="Search lessons" autocomplete="off"><div class="search-pop" hidden></div></form>
<div class="display-control"><button type="button" class="display-btn" aria-expanded="false" aria-controls="display-panel">Display</button>
<div id="display-panel" class="display-panel" hidden>
<label>Font size</label>
<div class="a11y-font" role="group" aria-label="Font size">
<button type="button" data-font-set="sm" aria-pressed="false">A−</button>
<button type="button" data-font-set="md" aria-pressed="true">A</button>
<button type="button" data-font-set="lg" aria-pressed="false">A+</button>
</div>
<label for="ink">Font colour</label>
<input id="ink" class="ink-input" data-ink type="color" value="#16182b" aria-label="Font colour">
<label>Theme</label>
<div class="theme-row" role="group" aria-label="Theme">
<button type="button" data-set-theme="bloom" aria-pressed="true">Bright</button>
<button type="button" data-set-theme="aurora" aria-pressed="false">Dark</button>
</div>
</div></div>
</div>
</header>
<div class="canon-banner">
<button type="button" class="rail-arrow" data-rail="prev" aria-label="Scroll sections backward">‹</button>
<nav class="section-rail" aria-label="Sections">{''.join(chips)}</nav>
<button type="button" class="rail-arrow" data-rail="next" aria-label="Scroll sections forward">›</button>
</div>
<div class="drawer-backdrop"></div>
<nav id="site-drawer" class="site-drawer" aria-hidden="true" aria-label="Menu">
<div class="drawer-bar"><strong>Menu</strong><button type="button" data-menu-open>Close</button></div>
<input class="drawer-search" data-drawer-filter type="search" placeholder="Filter" aria-label="Filter the menu">
<ul class="drawer-list">{''.join(drawer)}</ul>
</nav>
<main id="main">
"""


def chrome_close(depth):
    p = prefix(depth)
    return f"""</main>
{footer(depth)}
{phone(depth)}
<script src="{p}assets/js/frame.js"></script>
<script src="{p}assets/js/university.js"></script>
<script src="{p}guide/guide.js"></script>
</body>
</html>
"""


def diagram_svg(slug, title, boxes, side, animate):
    colors = ["#99f6e4", "#bfdbfe", "#fde68a", "#fecdd3", "#ddd6fe", "#d9f99d"]
    gid = "g" + "".join(ch if ch.isalnum() else "" for ch in slug)[:24]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420" role="img" aria-label="{e(title)}">',
        "<defs>",
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#312e81"/><stop offset="1" stop-color="#0e7490"/></linearGradient>',
        "</defs>",
        f'<rect width="720" height="420" rx="28" fill="url(#{gid})"/>',
        f'<text x="32" y="48" fill="#ffffff" font-family="system-ui,sans-serif" font-size="26" font-weight="700">{e(title)}</text>',
        f'<text x="32" y="76" fill="#e0f2fe" font-family="system-ui,sans-serif" font-size="15">{e(side)}. Teaching sketch. Confirm a live system.</text>',
    ]
    n = max(1, len(boxes))
    w = 140
    gap = 18
    total = n * w + (n - 1) * gap
    x0 = (720 - total) / 2
    path = []
    for i, label in enumerate(boxes):
        x = x0 + i * (w + gap)
        y = 150
        fill = colors[i % len(colors)]
        parts.append(f'<rect x="{x:.0f}" y="{y}" width="{w}" height="88" rx="18" fill="{fill}"/>')
        parts.append(
            f'<text x="{x + w/2:.0f}" y="{y+50}" text-anchor="middle" fill="#1e1b4b" font-family="system-ui,sans-serif" font-size="15" font-weight="700">{e(label)}</text>'
        )
        if i:
            x1 = x0 + (i - 1) * (w + gap) + w
            x2 = x
            midy = y + 44
            parts.append(f'<path d="M{x1:.0f} {midy} H{x2:.0f}" fill="none" stroke="#fde047" stroke-width="6" stroke-linecap="round"/>')
            path.append(f"M{x1:.0f} {midy} H{x2:.0f}")
    if animate and path:
        motion = " ".join(path)
        parts.append(f'<circle r="9" fill="#ffffff"><animateMotion dur="3.2s" repeatCount="indefinite" path="{motion}"/></circle>')
    parts.append('<text x="32" y="390" fill="#e0f2fe" font-family="system-ui,sans-serif" font-size="14">Names come from pages opened in 2026-10. A missing name stays confirm.</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def ladder_svg(slug, title, animate):
    gid = "L" + "".join(ch if ch.isalnum() else "" for ch in slug)[:20]
    motion = "M120 90 V320"
    anim = ""
    if animate:
        anim = f'<circle r="8" fill="#fde047"><animateMotion dur="2.8s" repeatCount="indefinite" path="{motion}"/></circle>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420" role="img" aria-label="{e(title)} ladder">
<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e1b4b"/><stop offset="1" stop-color="#155e75"/></linearGradient></defs>
<rect width="720" height="420" rx="28" fill="url(#{gid})"/>
<text x="28" y="42" fill="#fff" font-family="system-ui,sans-serif" font-size="24" font-weight="700">{e(title)}</text>
<text x="120" y="78" text-anchor="middle" fill="#fde68a" font-family="system-ui,sans-serif" font-size="16" font-weight="700">Caller</text>
<text x="360" y="78" text-anchor="middle" fill="#99f6e4" font-family="system-ui,sans-serif" font-size="16" font-weight="700">SIP</text>
<text x="600" y="78" text-anchor="middle" fill="#fecdd3" font-family="system-ui,sans-serif" font-size="16" font-weight="700">Called</text>
<path d="M120 90 V340 M360 90 V340 M600 90 V340" stroke="#e0f2fe" stroke-width="3"/>
<path d="M120 130 H360" stroke="#fff" stroke-width="4"/>
<text x="240" y="122" text-anchor="middle" fill="#fff" font-family="system-ui,sans-serif" font-size="13">session setup</text>
<path d="M360 180 H600" stroke="#fff" stroke-width="4"/>
<text x="480" y="172" text-anchor="middle" fill="#fff" font-family="system-ui,sans-serif" font-size="13">session setup</text>
<path d="M120 250 H600" stroke="#fde047" stroke-width="4" stroke-dasharray="8 6"/>
<text x="360" y="242" text-anchor="middle" fill="#fde047" font-family="system-ui,sans-serif" font-size="13">RTP, not required to hairpin</text>
{anim}
<text x="28" y="390" fill="#e0f2fe" font-family="system-ui,sans-serif" font-size="14">Teaching sketch from RFC 3261 and RFC 3550. Not a packet capture.</text>
</svg>'''


def write(path, text):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def page(rel, title, desc, depth, current, body):
    if "go-deeper" not in body:
        p = prefix(depth)
        rows = source_rows(
            ["rfc3261", "rfc3550", "wiki_paas", "tw_docs"],
            ["Release-specific steps for this page. confirm."],
        )
        body += go_deeper(rows, f"{p}sources/home/sources.json")
    write(rel, chrome_open(title, desc, depth, current) + body + chrome_close(depth))


def export_links(depth, slug):
    p = prefix(depth)
    return (
        f'<div class="room-downloads" data-dl><span>Export</span>'
        f'<a class="dl-btn" href="{p}assets/diagrams/{slug}.svg" download>SVG</a>'
        f'<a class="dl-btn" href="{p}assets/diagrams/{slug}-flow.svg" download>Flow</a>'
        f'<a class="dl-btn" href="{p}downloads/sheets/{slug}.html">Sheet</a></div>'
    )


def build_rooms():
    for index, room in enumerate(ROOMS, start=1):
        tid = room["track"]
        code = f"{tid}-R{index:02d}"
        room["code"] = code
        slug = room["slug"]
        still = diagram_svg(slug, room["title"], room["boxes"], room["side"], False)
        flow = ladder_svg(slug, room["title"], True)
        write(f"assets/diagrams/{slug}.svg", still)
        write(f"assets/diagrams/{slug}-flow.svg", flow)
        rows = source_rows(room["sources"], room["confirms"])
        write(f"rooms/sources/{slug}/sources.json", json.dumps({
            "opened": "2026-10",
            "sources": [{"kind": k, "title": t, "url": u} for k, t, u, _ in rows],
        }, indent=2))
        bullets = "".join(f"<li>{e(b)}</li>" for b in room["five"])
        paras = "".join(f"<p>{e(p)}</p>" for p in room["paras"])
        opened_n = len(room["sources"])
        confirm_n = len(room["confirms"])
        chart = (
            '<section class="mini-chart" aria-label="Counts on this page"><h2>Counts on this page</h2>'
            '<div class="stat-row">'
            f'<div class="stat"><b>{len(room["boxes"])}</b><span>boxes</span></div>'
            f'<div class="stat"><b>{opened_n}</b><span>opened sources</span></div>'
            f'<div class="stat"><b>{confirm_n}</b><span>confirm rows</span></div>'
            f'<div class="stat"><b>{len(room["five"])}</b><span>study lines</span></div>'
            "</div>"
            f'<p>Opened sources</p><div class="chart-bar" style="width:{max(8, opened_n * 12)}%"></div>'
            f'<p>Confirm rows, no URL</p><div class="chart-bar" style="width:{max(4, confirm_n * 12)}%"></div>'
            "</section>"
        )
        quizzes = ""
        for n, (q, ans, note) in enumerate(room["quiz"], start=1):
            quizzes += (
                f'<div class="quiz" data-quiz data-answer="{e(ans)}"><p><strong>{n}.</strong> {e(q)}</p>'
                f'<button type="button" class="choice ghost" data-choice="True">True</button>'
                f'<button type="button" class="choice ghost" data-choice="False">False</button>'
                f'<p class="quiz-note" hidden>{e(note)}</p></div>'
            )
        terms = "".join(f"<li><strong>{e(n)}</strong> — {e(d)}</li>" for n, d in room["terms"])
        tname = track_by_id(tid)[1]
        body = f'''<div class="wrap">
<p class="kicker">{e(tid)} · {e(code)} · {e(tname)}</p>
<h1>{e(room["title"])}</h1>
<p class="lede">{e(room["paras"][0])}</p>
{export_links(1, slug)}
{chart}
<section id="five" class="five"><h2>Learn it in 5 minutes</h2><ul>{bullets}</ul></section>
<section id="visual"><h2>Visual</h2><div class="diagram-frame">{still}</div>
<p>Count the boxes: {len(room["boxes"])}. Each label is a name from a page or a study label marked on the drawing.</p></section>
<section id="flow"><h2>Flow</h2><div class="diagram-frame">{flow}</div></section>
<section id="core"><h2>What is going on</h2>{paras}</section>
<section id="example" class="worked"><h2>Worked example</h2><p>{e(room["example"])}</p></section>
<section id="quiz"><h2>Quiz</h2>{quizzes}</section>
<section id="eco" class="eco-panel"><h2>Ecosystem</h2>
<p>Sister pieces sit on the ecosystem page: the glossary, the mind map, the integration map, and the bridges.</p>
<ul>{terms}</ul>
<p><strong>Config.</strong> {e(room["config"])}</p>
<p><strong>Troubleshooting.</strong> {e(room["trouble"])}</p>
<p><strong>Bridge.</strong> {e(room["bridge"])}</p>
<p>Mind map, sister technologies, and future hooks live on the <a href="../ecosystem.html">ecosystem page</a>.</p>
</section>
<section id="sources">{go_deeper(rows, f"sources/{slug}/sources.json", f"../downloads/rooms/{slug}.md")}</section>
</div>'''
        page(f"rooms/{slug}.html", room["title"], room["five"][0][:140], 1, "start.html", body)
        md = [f"# {room['title']}", "", "Study notes. Not vendor documentation and not legal advice.", ""]
        md += [f"- {b}" for b in room["five"]]
        md += ["", room["example"], ""]
        write(f"downloads/rooms/{slug}.md", "\n".join(md) + "\n")
        sheet = (
            "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            + CSP
            + "<title>"
            + e(room["title"])
            + "</title><link rel=\"stylesheet\" href=\"../../assets/css/footer.css\">"
            + "<style>body{font-family:system-ui,sans-serif;margin:24px;background:#f8fafc;color:#0f172a}ul{font-size:1.05rem;line-height:1.5}</style></head><body>"
            + f"<h1>{e(room['title'])}</h1><ul>"
            + "".join(f"<li>{e(b)}</li>" for b in room["five"])
            + "</ul><p>These are study notes, not vendor documentation and not legal advice. learning-only student project. "
            + f'<a href="{BRAND}/#contact">{BRAND}/#contact</a> '
            + f'<a href="{REPO}">{REPO}</a> '
            + f'<a href="{TREE}">{TREE}</a></p>'
            + go_deeper(rows, f"../../rooms/sources/{slug}/sources.json")
            + "</body></html>"
        )
        write(f"downloads/sheets/{slug}.html", sheet)


def build_tracks():
    for tid, name, blurb, color in TRACKS:
        items = rooms_for(tid)
        cards = []
        for room in items:
            cards.append(
                f'<a class="room-card" href="../rooms/{room["slug"]}.html"><h2>{e(room["title"])}</h2>'
                f'<p>{e(room["code"])}</p><p>{e(room["five"][0][:140])}</p></a>'
            )
        rows = source_rows(["rfc3261", "wiki_sip", "wiki_paas"], ["Release-specific menus for this track. confirm. Not opened as a single checklist."])
        body = f'''<div class="wrap">
<p class="kicker">{e(tid)}</p>
<h1>{e(name)}</h1>
<p class="lede">{e(blurb)}. {len(items)} lessons. Each lesson cites the pages that were opened, and marks the rest confirm.</p>
<div class="track-map">{''.join(cards)}</div>
<section class="go-deeper-slot">{go_deeper(rows, f"sources/{tid}/sources.json")}</section>
</div>'''
        write(f"tracks/sources/{tid}/sources.json", json.dumps({"opened": "2026-10", "track": tid}, indent=2))
        page(f"tracks/{tid}.html", name, blurb, 1, f"tracks/{tid}.html", body)


def glossary():
    seen = []
    have = set()
    for room in ROOMS:
        for name, definition in room["terms"]:
            if name not in have:
                have.add(name)
                seen.append((name, definition, room["slug"]))
    return seen


def build_hubs():
    n_rooms = len(ROOMS)
    n_tracks = len(TRACKS)
    n_diagrams = n_rooms * 2 + 3
    tiles = []
    for tid, name, blurb, color in TRACKS:
        count = len(rooms_for(tid))
        tiles.append(
            f'<a class="track-tile" style="--card:{color}" href="tracks/{tid}.html">'
            f'<span class="tile-ico">{svg_icon("track")}</span><h2>{e(name)}</h2>'
            f'<p>{e(blurb)}</p><p>{count} lessons</p></a>'
        )
    home_rows = source_rows(
        ["wiki_paas", "wiki_twilio", "wiki_vonage", "bw_home", "rfc3261", "rfc3550", "rfc8825", "wiki_e164", "wiki_stir"],
        [
            "MessageBird Wikipedia article. confirm. The title returned HTTP 404.",
            "Zoom, Talkdesk, and Avaya sibling lab. confirm. The URL returned HTTP 404.",
            "Cisco CUCM and UCCE pages. confirm. Not opened in this session.",
            "FCC call-authentication page. confirm. The request returned HTTP 403.",
            "Current vendor price tables other than the Plivo WhatsApp commitment. confirm.",
        ],
    )
    hero = diagram_svg("hero-stack", "CPaaS, from the pages that opened", ["App", "API", "SIP", "RTP"], "Home", True)
    write("assets/diagrams/hero-stack.svg", hero)
    cube = (
        '<div class="hero-3d" aria-hidden="true">'
        '<div class="obj o1"><i></i><i></i><i></i><i></i><i></i><i></i></div>'
        '<div class="obj o2"><i></i><i></i><i></i></div>'
        '<div class="obj o3"><i></i><i></i><i></i></div></div>'
    )
    body = f'''<section class="wrap hero-band">
<div>
<p class="kicker">Twilio · Vonage · Bandwidth · open SIP</p>
<h1>Communications APIs, and the pages that opened.</h1>
<p class="lede">A free study lab for communications platform as a service: Twilio, Vonage, Bandwidth, Sinch, Telnyx, Plivo, Infobip, and Bird, plus FreeSWITCH, Asterisk, Kamailio, LiveKit, Jitsi, Matrix, and Jami. SIP, WebRTC, RTP, numbers, messaging, STIR/SHAKEN, emergency calling, webhooks, IVR, contact center, AI voice, and migration. A number that was not on an opened page is marked confirm. Emergency and recording notes are not legal advice.</p>
<div class="actions">
<a class="btn" href="start.html">Start here</a>
<a class="ghost" href="diagrams.html">Diagrams</a>
<a class="ghost" href="charts.html">Charts</a>
<a class="ghost" href="ecosystem.html">Ecosystem</a>
<a class="ghost" href="downloads.html">Downloads</a>
</div>
</div>
<div class="hero-stage"><div class="diagram-frame hero-diagram">{hero}</div>{cube}</div>
</section>
<section class="wrap">
<div class="stat-row" aria-label="Counts from this repository">
<div class="stat"><b data-count="{n_rooms}">{n_rooms}</b><span>lessons</span></div>
<div class="stat"><b data-count="{n_tracks}">{n_tracks}</b><span>tracks</span></div>
<div class="stat"><b data-count="{n_diagrams}">{n_diagrams}</b><span>drawings</span></div>
<div class="stat"><b data-count="{n_rooms}">{n_rooms}</b><span>flows</span></div>
</div>
<h2>{n_tracks} tracks</h2>
<div class="track-map">{''.join(tiles)}</div>
</section>
<section class="wrap study-primer" id="primer">
<h2>Read this before the first lesson</h2>
<p>The Wikipedia article that opened for this topic is Platform as a service. Its communications section calls a CPaaS a cloud platform for adding voice, video, and messaging to an application without building that infrastructure. Twilio's article describes programmable call and text APIs. Vonage's article describes a cloud communications provider, now an Ericsson subsidiary, whose offering includes communications APIs. Bandwidth's own home page lists voice, messaging, emergency calling, WebRTC, and authentication APIs.</p>
<p>SIP, in the Wikipedia article and in RFC 3261, sets up the session. RTP, in RFC 3550, carries the media. WebRTC, in RFC 8825, is an overview of browser real-time protocols, and the RFC says it does not itself specify a protocol. Those jobs stay on separate arrows. A vendor menu does not replace the RFC.</p>
<p>Some names in the brief did not survive contact with the public web. A Wikipedia title MessageBird returned HTTP 404, while developers.messagebird.com and bird.com/docs did open. The Zoom, Talkdesk, and Avaya sibling URL returned HTTP 404, so it is not linked. Cisco CUCM and UCCE were not opened, so those menus are confirm. The FCC call-authentication URL returned HTTP 403. Emergency notes cite the Enhanced 911 article and the vendor pages that did open. They are not legal advice.</p>
{go_deeper(home_rows, "sources/home/sources.json")}
</section>'''
    page("index.html", "CPaaS Lab", "Free study lab for communications platform as a service.", 0, "index.html", body)
    write("sources/home/sources.json", json.dumps({"opened": "2026-10"}, indent=2))

    # start
    steps = []
    for tid, name, blurb, _c in TRACKS:
        first = rooms_for(tid)[0]
        steps.append(f"<li><a href=\"tracks/{tid}.html\">{e(name)}</a> — {e(blurb)}. First lesson: <a href=\"rooms/{first['slug']}.html\">{e(first['title'])}</a>.</li>")
    start_body = f'''<div class="wrap">
<h1>Start here</h1>
<p class="lede" id="ten">Ten minutes: read the home primer, open the CPaaS definition, then SIP and RTP, then one vendor page you actually use. Full course: the twelve tracks in order.</p>
<section id="path"><h2>Full course</h2><ol>{''.join(steps)}</ol></section>
<section><h2>Ten-minute path</h2>
<ol>
<li><a href="rooms/cpaas-word.html">What the CPaaS section says</a></li>
<li><a href="rooms/sip-jobs.html">What SIP is for</a></li>
<li><a href="rooms/rtp-webrtc.html">RTP and WebRTC</a></li>
<li><a href="rooms/webhook-direction.html">Webhooks come inbound</a></li>
<li><a href="rooms/counts-only.html">Numbers you may repeat</a></li>
</ol></section>
{go_deeper(source_rows(["wiki_paas","rfc3261","rfc3550","tw_hook"], []), "sources/start/sources.json")}
</div>'''
    write("sources/start/sources.json", json.dumps({"opened": "2026-10"}, indent=2))
    page("start.html", "Start here", "Ten minutes or the full course.", 0, "start.html", start_body)

    # diagrams and flows
    dcards = []
    fcards = []
    for room in ROOMS:
        dcards.append(f'<a class="room-card" href="rooms/{room["slug"]}.html"><h2>{e(room["title"])}</h2><p>Still drawing</p></a>')
        fcards.append(f'<a class="room-card" href="rooms/{room["slug"]}.html#flow"><h2>{e(room["title"])}</h2><p>Moving packet</p></a>')
    page("diagrams.html", "Diagrams", "Still drawings.", 0, "diagrams.html",
         f'<div class="wrap"><h1>Diagrams</h1><p class="lede">{n_rooms} still drawings, one per lesson, plus the home stack, the glossary map, and the integration map.</p><div class="track-map">{"".join(dcards)}</div></div>')
    page("flows.html", "Flows", "Ladders with a moving packet.", 0, "flows.html",
         f'<div class="wrap"><h1>Flows</h1><p class="lede">{n_rooms} ladders. Each one is a teaching sketch of session setup and RTP, not a customer capture.</p><div class="track-map">{"".join(fcards)}</div></div>')

    # play
    play = '''<div class="wrap"><h1>Play</h1>
<p class="lede">Order the jobs this lab can defend. Signaling is not media. A webhook is not the voice packet.</p>
<section id="drill"><h2>Put the jobs in study order</h2>
<ol id="order"></ol>
<p id="play-note" aria-live="polite"></p>
<button type="button" class="btn" id="check-order">Check order</button>
</section>
<section><h2>What correct means</h2>
<p>The drill asks for SIP session setup, then SDP offer and answer, then RTP. RFC 3261 and the SIP article set up the session. RFC 3264 and RFC 8866 describe it. RFC 3550 carries it. A price is not a call-flow step, so it stays off this list.</p>
</section>
<section id="call-sim" class="call-sim" aria-labelledby="sim-title">
<h2 id="sim-title">Call-flow simulator</h2>
<p class="sim-flag">Simulation. This page does not call Twilio, Vonage, Bandwidth, or any other vendor. Nothing here is sent to a network. The ladder is a teaching sketch, not a packet capture.</p>
<div class="sim-nodes" role="group" aria-label="Signaling steps">
<button type="button" data-sim-node="INVITE" aria-pressed="true">INVITE</button>
<button type="button" data-sim-node="180">180 Ringing</button>
<button type="button" data-sim-node="200">200 OK</button>
<button type="button" data-sim-node="ACK">ACK</button>
<button type="button" data-sim-node="BYE">BYE</button>
</div>
<form class="sim-form" id="sim-form">
<label>Request URI <input id="sim-uri" name="uri" value="sip:1000;user=phone" autocomplete="off"></label>
<label>DTMF digit <input id="sim-dtmf" name="dtmf" value="1" maxlength="4" autocomplete="off"></label>
<label>IVR branch
<select id="sim-branch" name="branch">
<option value="queue">Queue</option>
<option value="voicemail">Voicemail</option>
<option value="hangup">Hang up</option>
</select>
</label>
<button type="submit">Show the simulated result</button>
</form>
<pre id="sim-out" aria-live="polite">Pick a step, then show the simulated result.</pre>
<div class="mini-quiz" data-quiz data-answer="rtp">
<p>Study check: after the session is set up, which name carries the media?</p>
<button type="button" class="choice" data-choice="sip">SIP</button>
<button type="button" class="choice" data-choice="rtp">RTP</button>
<p class="quiz-note" hidden>SIP sets up the session. RTP carries the media. This check stays in the browser.</p>
</div>
</section>
<script src="assets/js/play.js"></script>
</div>'''
    page("play.html", "Play", "A short drill in this browser.", 0, "play.html", play)

    listen = '''<div class="wrap"><h1>Listen</h1>
<p class="lede">The guide reads the words already on the page. There is no separate audio file and no cloud voice.</p>
<section id="script"><h2>Read-along script</h2>
<p>Welcome. This lab studies CPaaS from pages opened in October 2026. SIP sets up the session. RTP carries the voice. A confirm row has no link.</p>
<p>Press Listen in the bottom dock, or open the guide and choose Read along. On a phone the guide sits below the title and the first lines.</p>
</section></div>'''
    page("listen.html", "Listen", "Read-along notes.", 0, "listen.html", listen)

    # downloads
    rows_dl = []
    for room in ROOMS:
        rows_dl.append(
            f"<tr><td><a href=\"downloads/sheets/{room['slug']}.html\">{e(room['title'])}</a></td><td>HTML sheet</td><td>{e(room['code'])}</td></tr>"
        )
    dl = f'''<div class="wrap"><h1>Downloads</h1>
<p class="lede">Sheets and a zip of the lesson notes. Sizes are the files in this repository. No CDN.</p>
<p><a class="btn" href="downloads/cpaas-lab-notes.zip">Download the notes zip</a></p>
<h2>Headless test table</h2>
<div class="table-wrap"><table class="plain"><thead><tr><th>Sheet</th><th>Kind</th><th>Code</th></tr></thead><tbody>
{''.join(rows_dl)}
</tbody></table></div>
<p>learning-only student project. <a href="{BRAND}/#contact">{BRAND}/#contact</a></p>
</div>'''
    page("downloads.html", "Downloads", "Sheets, cards, and one zip.", 0, "downloads.html", dl)

    help_body = '''<div class="wrap"><h1>Help</h1>
<p class="lede">The top rail is the short menu. The Menu button opens every track. Display changes type size, type colour, and bright or dark.</p>
<section><h2>The guide</h2>
<p>The monkey repeats notes that are already on the page. Read along uses the browser speech API. On a phone the guide panel is placed below the title and the opening lines, and the closed monkey sits above the bottom dock.</p></section>
<section><h2>Confirm</h2>
<p>A confirm row has no URL. That page was not verified in October 2026. Do not treat it as a citation.</p></section>
<section><h2>What this is not</h2>
<p>Study notes. Not vendor documentation. Not legal advice. Not an emergency plan. Vendor names are trademarks of their owners.</p></section>
</div>'''
    page("help.html", "Help", "How the menu, course, and bot work.", 0, "help.html", help_body)

    legal = '''<div class="wrap"><h1>Legal</h1>
<p class="lede">Study notes. Not vendor documentation and not legal advice. Twilio, Vonage, Bandwidth, Sinch, Telnyx, Plivo, Infobip, Bird, MessageBird, and the open-source names are trademarks of their owners. This lab is not affiliated with or endorsed by them.</p>
<section><h2>Emergency and recording</h2>
<p>Those chapters cite the Enhanced 911 article and the vendor emergency pages that opened. They are not an emergency plan and not a privacy opinion. Confirm the rule where you operate.</p></section>
<section><h2>No secrets</h2>
<p>Do not paste tokens, client secrets, or customer records into these pages.</p></section>
</div>'''
    page("legal.html", "Legal", "Study notes and trademarks.", 0, "legal.html", legal)

    # ecosystem
    terms = glossary()
    term_html = "".join(f"<li><strong>{e(n)}</strong> — {e(d)}</li>" for n, d, _s in terms)
    mind = diagram_svg("glossary-map", "Glossary mind map", ["CPaaS", "SIP", "RTP", "E.164"], "Ecosystem", False)
    integ = diagram_svg("integration-map", "Integration map", ["SIP trunk", "Webhook", "Verify", "LiveKit"], "Bridges", True)
    hooks = diagram_svg("future-hooks", "Future hooks", ["Telnyx Beta", "Sinch v2", "Jami Web", "Fee confirm"], "Hooks", False)
    write("assets/diagrams/glossary-map.svg", mind)
    write("assets/diagrams/integration-map.svg", integ)
    write("assets/diagrams/future-hooks.svg", hooks)
    sisters = [
        ("sib_uc", "Cisco-shaped UC course. CUCM menus in this lab stay confirm."),
        ("sib_sip", "SIP campus for the protocol rooms."),
        ("sib_wx", "Webex campus. Bandwidth's home page also names Webex Calling."),
        ("sib_ms", "Microsoft voice campus. Bandwidth's home page names Teams Direct Routing and Operator Connect."),
        ("sib_amz", "Amazon Connect campus."),
        ("sib_gen", "Genesys campus. Bandwidth's home page names Genesys Cloud CX."),
        ("sib_f9", "Five9 campus. Bandwidth's home page names Five9."),
        ("sib_nice", "NICE campus. The title that opened is Contact Path · NICE CXone Lab."),
        ("sib_ai", "AI campus. Not a substitute for the LiveKit or vendor agent pages."),
    ]
    sis = "".join(
        f'<li><a href="{e(SOURCES[k][2])}">{e(SOURCES[k][1])}</a> — {e(note)}</li>' for k, note in sisters
    )
    eco_rows = source_rows([k for k, _n in sisters] + ["wiki_sip", "wiki_kam", "lk_tel", "plivo_wa", "jami"], [
        "Zoom, Talkdesk, and Avaya sibling lab. confirm. HTTP 404.",
        "Vendor roadmap dates. confirm. Infobip's docs nav names Roadmap. The dates were not opened.",
        "Certification exam names. confirm. No exam page was opened.",
    ])
    eco = f'''<div class="wrap">
<h1>Ecosystem</h1>
<p class="lede">Words, drawings, sister labs, and the bridges this course can cite. Counts below are from this repository or from pages opened in 2026-10.</p>
<section><h2>Glossary</h2><p>{len(terms)} terms from the lessons. The same term is listed once.</p><ul>{term_html}</ul></section>
<section><h2>Mind map</h2><div class="diagram-frame">{mind}</div>
<p>CPaaS sits beside SIP, RTP, and E.164. The list above is the rest of the vocabulary from the lessons.</p></section>
<section><h2>Sister technologies</h2>
<p>Config habit: write the page title, the object, and the release. Troubleshooting habit: one hypothesis, then one change, and put the change back if the symptom does not move. Sister labs are separate courses.</p>
<ul>{sis}</ul>
<p><strong>Config.</strong> On a CPaaS, record the product (voice, messaging, verify, trunk), the object (number, profile, webhook, SIP connection), and the page title. On Asterisk, record extensions.conf. On FreeSWITCH, record the SIP profile. On Kamailio, record the version folder, such as 6.1.x.</p>
<p><strong>Troubleshooting.</strong> If signaling succeeds and audio fails, move from RFC 3261 to RFC 3550. If the create call returns 202 and your app sees nothing, check the webhook status. If a name 404s, mark confirm.</p></section>
<section><h2>Integration map</h2><div class="diagram-frame">{integ}</div>
<p>CRM field maps were not opened, so a Salesforce field list stays confirm even though Bandwidth names a Salesforce Contact Center integration. SIP trunking is the Wikipedia split between a private domain and a public domain. Verify is its own API on the Vonage and Twilio pages. LiveKit telephony adds a SIP participant to a room.</p></section>
<section><h2>Bridges</h2>
<p>A bridge in this lab is a cited hop. Kamailio's article lists a SIP-WebRTC gateway. Jami's site says it can function as a SIP client. Matrix's specification introduction names bridging existing silos. Bandwidth's home page names Microsoft Teams Direct Routing, Operator Connect, Genesys Cloud CX, Webex Calling, Zoom Phone, Google Voice SIP Link, and Five9. Plivo's docs home names SIP trunking toward LiveKit. A named customer quote was not opened. Customer story: confirm.</p></section>
<section><h2>Future hooks</h2><div class="diagram-frame">{hooks}</div>
<p>Telnyx's docs navigation marks LiveKit on Telnyx as Beta. Sinch's navigation names Voice API v2 as preview. Jami's site lists Jami Web, First Preview, dated 1 September 2026. Plivo's WhatsApp page dates a platform fee to 1 November 2026 and does not state the fee amount. Infobip's hub shows a Roadmap label. Quarters and fee amounts that were not on the page stay confirm.</p></section>
{go_deeper(eco_rows, "sources/ecosystem/sources.json", "downloads/ecosystem.md")}
</div>'''
    write("sources/ecosystem/sources.json", json.dumps({"opened": "2026-10"}, indent=2))
    write("downloads/ecosystem.md", "# Ecosystem\n\nStudy notes. Not vendor documentation.\n")
    page("ecosystem.html", "Ecosystem", "Glossary, bridges, and sister labs.", 0, "ecosystem.html", eco)

    # quizzes
    blocks = []
    for room in ROOMS:
        for q, ans, note in room["quiz"]:
            blocks.append(
                f'<div class="quiz" data-quiz data-answer="{e(ans)}"><p><a href="rooms/{room["slug"]}.html">{e(room["title"])}</a>. {e(q)}</p>'
                f'<button type="button" class="choice ghost" data-choice="True">True</button>'
                f'<button type="button" class="choice ghost" data-choice="False">False</button>'
                f'<p class="quiz-note" hidden>{e(note)}</p></div>'
            )
    page("quizzes.html", "Quizzes", "Questions from the lessons.", 0, "quizzes.html",
         f'<div class="wrap"><h1>Quizzes</h1><p class="lede">{len(blocks)} questions, two from each lesson.</p>{"".join(blocks)}</div>')

    # charts — counts only
    charts = [
        ("lessons", n_rooms, f"{n_rooms} lessons in this repository"),
        ("tracks", n_tracks, f"{n_tracks} tracks in this repository"),
        ("e164-max", 15, "E.164 maximum digits stated on the Wikipedia article"),
        ("sms-chars", 160, "SMS character size stated on the Wikipedia article"),
        ("attest", 3, "STIR attestation levels read on the Wikipedia article: A, B, and C"),
        ("twilio-911-places", 8, "Places named on Twilio SIP trunking emergency calling: US, Canada, UK, Australia, Ireland, France, Germany, Austria"),
        ("confirm-gaps", 4, "Gaps with no URL: MessageBird Wikipedia 404, sibling Zoom lab 404, CUCM not opened, FCC 403"),
    ]
    chart_html = []
    for cid, value, label in charts:
        width = max(8, min(100, value if value <= 40 else round(value / 1.6)))
        chart_html.append(
            f'<section data-chart="{cid}"><h2>{e(label)}</h2><p><b>{value}</b></p>'
            f'<div class="chart-bar" style="width:{width}%"></div></section>'
        )
    page("charts.html", "Charts", "Counts from this lab and from names that were read.", 0, "diagrams.html",
         '<div class="wrap"><h1>Charts</h1><p class="lede">These bars count lessons, tracks, or names read on a page. They are not vendor KPIs. Service level and handle time were not opened, so they are not drawn.</p>'
         + "".join(chart_html) + "</div>")

    # flashcards
    cards = []
    for name, definition, slug in terms:
        cards.append({"front": name, "back": definition, "source": f"rooms/{slug}.html"})
    # pad with source facts if under 40 — we have plenty
    write("downloads/flashcards.json", json.dumps({"cards": cards}, indent=2))
    card_html = "".join(
        f"<article><h2>{e(c['front'])}</h2><p>{e(c['back'])}</p><p>Source: {e(c['source'])}</p></article>" for c in cards
    )
    write("downloads/flashcards.html",
          "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
          + CSP
          + "<title>Flashcards</title>"
          "<link rel=\"stylesheet\" href=\"../assets/css/footer.css\">"
          "<style>body{font-family:system-ui,sans-serif;margin:24px}article{border:1px solid #99f6e4;border-radius:12px;padding:12px;margin:8px 0}</style></head><body>"
          f"<h1>Flashcards</h1><p class=\"lede\">Terms from the lessons.</p>{card_html}"
          "<section class=\"go-deeper\"><h2>Sources and go deeper</h2><p>Opened 2026-10. A row marked confirm has no link, because that page was not verified.</p>"
          "<ul><li><strong>Lab.</strong> Terms are defined in the lesson pages. <span style=\"white-space:nowrap\">last checked 2026-10</span></li></ul></section>"
          "<p>These are study notes, not vendor documentation and not legal advice. learning-only student project. "
          f"<a href=\"{BRAND}/#contact\">{BRAND}/#contact</a> "
          f"<a href=\"{REPO}\">{REPO}</a> <a href=\"{TREE}\">{TREE}</a></p></body></html>")
    page("flashcards.html", "Flashcards", "Terms from the lessons.", 0, "flashcards.html",
         f'<div class="wrap"><h1>Flashcards</h1><p class="lede">{len(cards)} terms. The same card is also in the JSON download.</p>'
         f'<p><a href="downloads/flashcards.json">JSON</a> · <a href="downloads/flashcards.html">Printable HTML</a></p>{card_html}</div>')

    # catalog
    pages = []
    for href, label, blurb, _i in NAV:
        pages.append({"title": label, "href": href, "blurb": blurb, "keys": [label.lower()]})
    for tid, name, blurb, _c in TRACKS:
        pages.append({"title": name, "href": f"tracks/{tid}.html", "blurb": blurb, "keys": [name.lower(), tid.lower()]})
    for room in ROOMS:
        pages.append({"title": room["title"], "href": f"rooms/{room['slug']}.html", "blurb": room["code"], "keys": [room["slug"], room["title"].lower()]})
    write("assets/data/catalog.json", json.dumps({"pages": pages}, indent=2))

    # zip of markdown
    zpath = ROOT / "downloads" / "cpaas-lab-notes.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for room in ROOMS:
            zf.write(ROOT / "downloads" / "rooms" / f"{room['slug']}.md", f"rooms/{room['slug']}.md")
        zf.writestr("README.txt", "Study notes. Not vendor documentation and not legal advice.\n")

    write(".nojekyll", "")
    counts = {"tracks": n_tracks, "lessons": n_rooms, "diagrams": n_diagrams, "terms": len(terms), "quizzes": n_rooms * 2}
    write("assets/data/counts.json", json.dumps(counts, indent=2))
    print(json.dumps(counts))


def write_boot_scripts():
    write(
        "assets/js/theme-boot.js",
        "try{var t=localStorage.getItem(\"canon-theme\");if(t!==\"aurora\")t=\"bloom\";"
        "document.documentElement.dataset.theme=t;var f=localStorage.getItem(\"canon-font\");"
        "if(f===\"sm\"||f===\"lg\")document.documentElement.dataset.font=f;"
        "var ink=localStorage.getItem(\"canon-ink\");"
        "if(ink&&/^#[0-9a-f]{6}$/i.test(ink))document.documentElement.style.setProperty(\"--ink\",ink);"
        "}catch(err){document.documentElement.dataset.theme=\"bloom\";}\n",
    )
    write(
        "assets/js/play.js",
        """(function(){
  var jobs=["RTP media","SDP offer and answer","SIP session setup","A price stays confirm"];
  var want=["SIP session setup","SDP offer and answer","RTP media","A price stays confirm"];
  var list=document.getElementById("order");
  if(!list) return;
  jobs.forEach(function(job){
    var li=document.createElement("li");
    li.textContent=job;
    li.draggable=true;
    li.dataset.job=job;
    li.style.padding="8px";
    li.style.margin="6px 0";
    li.style.border="2px solid #0f766e";
    li.style.borderRadius="12px";
    li.addEventListener("dragstart",function(){li.classList.add("dragging");});
    li.addEventListener("dragend",function(){li.classList.remove("dragging");});
    list.appendChild(li);
  });
  list.addEventListener("dragover",function(ev){
    ev.preventDefault();
    var dragging=list.querySelector(".dragging");
    var after=[].slice.call(list.children).find(function(child){
      var box=child.getBoundingClientRect();
      return ev.clientY < box.top + box.height/2;
    });
    if(!dragging) return;
    if(after) list.insertBefore(dragging, after); else list.appendChild(dragging);
  });
  document.getElementById("check-order").addEventListener("click",function(){
    var got=[].map.call(list.children,function(li){return li.dataset.job;});
    var ok=got.every(function(item,i){return item===want[i];});
    document.getElementById("play-note").textContent=ok?"That order matches the study habit.":"Not yet. SIP session setup, then SDP, then RTP. A price is a different object.";
  });
})();
(function(){
  var form=document.getElementById("sim-form");
  if(!form) return;
  var node="INVITE";
  document.querySelectorAll("[data-sim-node]").forEach(function(btn){
    btn.addEventListener("click",function(){
      node=btn.getAttribute("data-sim-node");
      document.querySelectorAll("[data-sim-node]").forEach(function(el){el.setAttribute("aria-pressed", el===btn?"true":"false");});
    });
  });
  form.addEventListener("submit",function(event){
    event.preventDefault();
    var uri=document.getElementById("sim-uri").value.trim()||"sip:example.test";
    var digit=document.getElementById("sim-dtmf").value.trim()||"—";
    var branch=document.getElementById("sim-branch").value;
    var branchLine=branch==="queue"?"IVR branch: queue. Simulated. No agent was offered a call.":branch==="voicemail"?"IVR branch: voicemail. Simulated. No mailbox was opened.":"IVR branch: hang up. Simulated BYE. No carrier was signaled.";
    var step=node==="INVITE"?"Simulated INVITE to "+uri+". Next sketch: 100 Trying, then 180 Ringing. Not run on a network.":node==="180"?"Simulated 180 Ringing for "+uri+". Media is not flowing yet.":node==="200"?"Simulated 200 OK for "+uri+". The sketch then expects ACK, then RTP. Not run on a network.":node==="ACK"?"Simulated ACK. The teaching sketch would start RTP after this. No packets were sent.":"Simulated BYE for "+uri+". The sketch ends the dialog. Not run on a network.";
    document.getElementById("sim-out").textContent=step+"\\nDTMF digit on the form: "+digit+" (not sent).\\n"+branchLine;
  });
})();
""",
    )


if __name__ == "__main__":
    write_boot_scripts()
    build_rooms()
    build_tracks()
    build_hubs()
