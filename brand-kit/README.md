# Agentcy Brand Kit

Built from the live site's real design system (extracted from computed styles on agentcy.co.za).

## Palette (live-site accurate)
| Token | Value |
|---|---|
| Ink (page bg) | `#1A1A1A` |
| Text | `#FFFFFF`, muted `#525252` / `#A6A6A6` on dark |
| Signature gradient | `#C9AAFF → #FEFFBC → #FFCDFD → #B3E2FF → #839AFF` (270deg) |
| Periwinkle anchor | `#839AFF` (taglines, dividers, links) |
| Buttons | white pill `rgba(255,255,255,.85)` + ghost pills `border: 1px solid rgba(255,255,255,.22)` |
| Wordmark | Arial Bold, tracking −0.06em, lowercase "agentcy" |
| Logo mark | WHITE spark (uploads/logoicon.svg) on `#1A1A1A`/`#222` chip |

## Contents
- **svg/** — marks (white-on-ink, white, ink, gradient) + horizontal & stacked lockups
- **favicon/** — favicon.svg/.ico, PNGs 16→512, apple-touch, mstile, site.webmanifest
- **banners-*.png** — LinkedIn 1584×396 · X 1500×500 · Facebook 851×315 · YouTube 2560×1440 (safe-area centered) · OG 1200×630
- **templates-*.png** — IG quote 1080×1080 · IG services 1080×1080 · Story 1080×1920
- **email-signature/** — light + dark HTML (table-based, Outlook/Gmail-safe) + 96px mark PNG.
  Logo hot-links from `https://agentcy.co.za/favicon/icon-192.png` (live).

## Editing / regenerating
- Layouts live as HTML in `_render/` — edit text there, then:
  `python _render_all.py` (headless Edge screenshots every page at exact size)
- SVG lockups regenerate via `_build_svgs.py`; pages via `_gen_pages.py`

## Deployment history
- 2026-08-25 v1: teal palette (wrong — from old placeholder favicon)
- 2026-08-25 v2: corrected to live palette (#1A1A1A + pastel gradient + periwinkle);
  favicons redeployed, hash-verified live
