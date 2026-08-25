import re, os

BASE = os.path.expanduser("~") + "/agentcy-site-live"
OUT = BASE + "/brand-kit"

logo = open(BASE + "/uploads/logoicon.svg", encoding="utf-8").read()
paths = re.findall(r'<path [^>]+/>|<line [^>]+/>', logo)

def spark(f):
    return "".join(p.replace('fill="white"', 'fill="' + f + '"') for p in paths[:8])

def gridf(f):
    # vertical bar is a fill path — recolor fills AND strokes
    return "".join(p.replace('stroke="white"', 'stroke="' + f + '"')
                    .replace('fill="white"', 'fill="' + f + '"') for p in paths[8:])

def mark(f, size=22):
    off = (28 - size) / 2
    return ('<g transform="translate(' + str(off) + ',' + str(off) + ') scale(' +
            str(size / 28) + ')">' + spark(f) + gridf(f) + "</g>")

def w(rel, content):
    open(OUT + "/" + rel, "w", encoding="utf-8").write(content)
    print("wrote", rel)

# --- marks ---
w("svg/agentcy-mark-teal-on-ink.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">'
  '<rect width="28" height="28" rx="6.2" fill="#111820"/>'
  '<clipPath id="r"><rect width="28" height="28" rx="6.2"/></clipPath>'
  '<g clip-path="url(#r)">' + mark("#61DCCF", 28) + "</g></svg>")

w("svg/agentcy-mark-white.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">' + mark("#FFFFFF", 28) + "</svg>")

w("svg/agentcy-mark-ink.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">' + mark("#111820", 28) + "</svg>")

# --- horizontal light (ink bg) ---
w("svg/agentcy-logo-horizontal-light.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 72">'
  '<rect width="300" height="72" rx="16" fill="#111820"/>'
  '<g transform="translate(24,22)">' + spark("#61DCCF") + gridf("#61DCCF") + "</g>"
  '<text x="76" y="46.5" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" letter-spacing="-1.8" fill="#F4F5F2">agentcy</text>'
  '<text x="76" y="60.5" font-family="Arial, Helvetica, sans-serif" font-size="7.5" letter-spacing="3.4" fill="#61DCCF">AI ENGINEERS ON SITE</text>'
  "</svg>")

# --- horizontal dark (transparent bg, ink art) ---
w("svg/agentcy-logo-horizontal-dark.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 72">'
  '<g transform="translate(24,22)">' + spark("#111820") + gridf("#111820") + "</g>"
  '<text x="76" y="46.5" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" letter-spacing="-1.8" fill="#111820">agentcy</text>'
  '<text x="76" y="60.5" font-family="Arial, Helvetica, sans-serif" font-size="7.5" letter-spacing="3.4" fill="#0E7C74">AI ENGINEERS ON SITE</text>'
  "</svg>")

# --- stacked (ink bg) ---
w("svg/agentcy-logo-stacked-teal-on-ink.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 220">'
  '<rect width="320" height="220" rx="20" fill="#111820"/>'
  '<g transform="translate(118,40) scale(3)">' + spark("#61DCCF") + gridf("#61DCCF") + "</g>"
  '<text x="160" y="172" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="700" letter-spacing="-2.6" fill="#F4F5F2">agentcy</text>'
  '<text x="160" y="194" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="10" letter-spacing="4.6" fill="#61DCCF">AI ENGINEERS ON SITE</text>'
  "</svg>")

# --- favicon ---
w("favicon/favicon.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
  '<rect width="64" height="64" rx="14" fill="#111820"/>'
  '<g transform="translate(7,7) scale(1.7857)">' + spark("#61DCCF") + gridf("#61DCCF") + "</g></svg>")

# --- email mark chip (render target) ---
os.makedirs(OUT + "/_render", exist_ok=True)
chip = ('<div style="width:96px;height:96px;border-radius:22px;background:#111820;'
        'display:flex;align-items:center;justify-content:center">'
        '<svg width="62" height="62" viewBox="0 0 28 28">' + spark("#61DCCF") + gridf("#61DCCF") + "</svg></div>")
w("_render/email-mark.html",
  '<!DOCTYPE html><html><head><style>html,body{margin:0;padding:0}</style></head>'
  '<body style="margin:0">' + chip + "</body></html>")
print("done")
