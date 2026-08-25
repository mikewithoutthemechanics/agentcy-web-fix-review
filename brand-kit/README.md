# Agentcy Brand Kit

Generated from the live logo (`uploads/logoicon.svg` — 8-point spark) and site palette.

## Palette
| Token | Hex |
|---|---|
| Ink (bg) | `#111820` / deep `#0B1118` |
| Teal (primary accent) | `#61DCCF` (print-safe dark: `#0E7C74`) |
| Blue (secondary) | `#5F8CFF` |
| Off-white | `#F4F5F2` |
| Wordmark | Arial Bold, tracking −0.06em, lowercase "agentcy" |

## Contents
- **svg/** — logo marks (teal-on-ink, white, ink) + horizontal & stacked lockups
- **favicon/** — favicon.svg/.ico, PNGs 16→512, apple-touch, mstile, site.webmanifest
- **banners-*.png** — LinkedIn 1584×396 · X 1500×500 · Facebook 851×315 · YouTube 2560×1440 (safe-area centered) · OG 1200×630
- **templates-*.png** — IG quote 1080×1080 · IG services 1080×1080 · Story 1080×1920
- **email-signature/** — light + dark HTML (table-based, Outlook/Gmail-safe) + 96px mark PNG.
  Logo is hot-linked from `https://agentcy.co.za/favicon/icon-192.png` (live).

## Editing / regenerating
- Layouts live as HTML in `_render/` — edit text there, then:
  `python _render_all.py` (headless Edge screenshots every page at exact size)
- SVG lockups regenerate via `_build_svgs.py`; pages via `_gen_pages.py`

## Favicon deployment (done 2026-08-25)
Files live at repo root AND `/favicon/` subfolder; `<head>` links injected in both
`agentcy.html` and `index.html`; deployed with `vercel deploy --prod`.
