# agentcy.co.za — Production Site (AEO build)

Source of truth for **https://agentcy.co.za** as of 2026-08-25.

Deployed to Vercel project `agon-agent-master` (custom domain `agentcy.co.za`).

## Architecture
- `index.html` — outer shell: SEO meta, OG/Twitter cards, JSON-LD (`ProfessionalService`), loads the app bundle
- `assets/index-B8demhiE.js` + CSS — React shell that renders `/agentcy.html` in an iframe
- `agentcy.html` — the actual site (Conicorn template): hero, services, process, case studies, integrations, testimonials, pricing, team, FAQs, booking modal, footer
- `api/contact.js` — Vercel serverless function: booking/contact form → Resend email
- `uploads/` — self-hosted images (team photos, emblem SVG)
- `llms.txt`, `robots.txt`, `sitemap.xml` — AI/SEO discoverability

## Environment variables (Vercel → agon-agent-master)
| Var | Purpose |
|---|---|
| `RESEND_API_KEY` | Email sending (Resend) |
| `CONTACT_TO` | Optional comma-separated recipients override |

Email sender: `bookings@concierge.agentcy.co.za` (SPF/DKIM verified via Vercel DNS).

## Deploy
```bash
vercel link --project agon-agent-master --scope michael-s-projects-1c4584cf
vercel deploy --prod
```

## History note
This replaces the previous production deploy, which was an uncommitted
[Design Arena](https://designarena.ai) tournament generation pushed via CLI and
never committed anywhere (now lost). It was recovered byte-for-byte from the live
deployment and repaired on 2026-08-25:
- removed 2 duplicate/experimental footers (kept `agentcy-footer-final`)
- fixed double-encoded mojibake (`Ãƒ-`) → brand emblem logo in footer wordmark
- removed Design Arena session recorder / page-view beacons / element picker
- hoisted meta description, OG/Twitter, JSON-LD into the outer shell
- wired booking form to real email delivery (was console.log)
- restored missing `llms.txt`; unmasked JSON-LD phone number
