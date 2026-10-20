"""Render the logo SVGs to PNG with headless Chromium (Playwright), so PNGs never drift from the SVG master.

Usage:
  python tools/render_assets.py sheet            # assets/drafts/sheet.png: every draft at 512/64/32 on dark and light
  python tools/render_assets.py export           # assets/*.png from assets/logo.svg + assets/social-preview.svg
Needs: pip install playwright && python -m playwright install chromium
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def _svg(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_svg(page, svg: str, width: int, height: int, out: Path) -> None:
    page.set_viewport_size({"width": width, "height": height})
    page.set_content(
        "<html><body style='margin:0;background:transparent'>"
        f"<div style='width:{width}px;height:{height}px'>{svg.replace('<svg ', f'<svg style=\"width:{width}px;height:{height}px;display:block\" ', 1)}</div>"
        "</body></html>"
    )
    page.screenshot(path=str(out), omit_background=True, clip={"x": 0, "y": 0, "width": width, "height": height})


def sheet(page) -> Path:
    drafts = sorted((ASSETS / "drafts").glob("*.svg"))
    rows = []
    for d in drafts:
        svg = _svg(d)
        cells = "".join(
            f"<div class='c {bg}'>"
            + "".join(f"<img src='data:image/svg+xml;utf8,{_uri(svg)}' width='{s}' height='{s}'>" for s in (256, 64, 32))
            + "</div>"
            for bg in ("dark", "light")
        )
        rows.append(f"<div class='r'><h2>{d.stem}</h2>{cells}</div>")
    html = (
        "<html><head><style>body{margin:0;font:600 20px system-ui;background:#fff;padding:24px}"
        ".r{display:flex;align-items:center;gap:24px;margin-bottom:24px}h2{width:200px;font-size:18px}"
        ".c{display:flex;align-items:center;gap:24px;padding:20px;border-radius:16px}"
        ".dark{background:#0d1117}.light{background:#f6f8fa}</style></head><body>"
        + "".join(rows)
        + "</body></html>"
    )
    page.set_viewport_size({"width": 1240, "height": 120 + 330 * len(drafts)})
    page.set_content(html)
    out = ASSETS / "drafts" / "sheet.png"
    page.screenshot(path=str(out), full_page=True)
    return out


def _uri(svg: str) -> str:
    from urllib.parse import quote

    return quote(svg)


def export(page) -> list[Path]:
    logo = _svg(ASSETS / "logo.svg")
    outs = []
    for name, size in (("logo.png", 512), ("icon-1024.png", 1024), ("icon-64.png", 64), ("icon-32.png", 32)):
        out = ASSETS / name
        render_svg(page, logo, size, size, out)
        outs.append(out)
    social = ASSETS / "social-preview.svg"
    if social.exists():
        out = ASSETS / "social-preview.png"
        render_svg(page, _svg(social), 1280, 640, out)
        outs.append(out)
    return outs


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        result = sheet(page) if mode == "sheet" else export(page)
        browser.close()
    print(result)


if __name__ == "__main__":
    main()
