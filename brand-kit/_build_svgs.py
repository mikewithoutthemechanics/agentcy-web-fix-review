import re, os

BASE = os.path.expanduser("~") + "/agentcy-site-live"
OUT = BASE + "/brand-kit"

# ---- REAL palette from live site (agentcy.html computed styles) ----
INK = "#1A1A1A"          # page background
WHITE = "#FFFFFF"
MUTED = "#525252"
PERI = "#839AFF"          # periwinkle anchor
# signature gradient 270deg:
GRAD = "linear-gradient(270deg, #C9AAFF 0%, #FEFFBC 25%, #FFCDFD 50%, #B3E2FF 75%, #839AFF 100%)"
GRAD_STOPS = ["#C9AAFF", "#FEFFBC", "#FFCDFD", "#B3E2FF", "#839AFF"]

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

# --- marks: the logo is WHITE on the live site ---
w("svg/agentcy-mark-white-on-ink.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">'
  '<rect width="28" height="28" rx="6.2" fill="' + INK + '"/>'
  '<clipPath id="r"><rect width="28" height="28" rx="6.2"/></clipPath>'
  '<g clip-path="url(#r)">' + mark("#FFFFFF", 28) + "</g></svg>")

w("svg/agentcy-mark-white.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">' + mark("#FFFFFF", 28) + "</svg>")

w("svg/agentcy-mark-ink.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">' + mark(INK, 28) + "</svg>")

# gradient mark for feature use (SVG userSpaceOnUse gradient over the mark)
w("svg/agentcy-mark-gradient.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">'
  '<defs><linearGradient id="ag" x1="28" y1="0" x2="0" y2="28" gradientUnits="userSpaceOnUse">'
  '<stop offset="0" stop-color="#C9AAFF"/><stop offset=".25" stop-color="#FEFFBC"/>'
  '<stop offset=".5" stop-color="#FFCDFD"/><stop offset=".75" stop-color="#B3E2FF"/>'
  '<stop offset="1" stop-color="#839AFF"/></linearGradient></defs>'
  + mark("url(#ag)", 28) + "</svg>")

# --- horizontal light (ink chip bg, white art) ---
w("svg/agentcy-logo-horizontal-light.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 72">'
  '<rect width="300" height="72" rx="16" fill="' + INK + '"/>'
  '<g transform="translate(24,22)">' + spark("#FFFFFF") + gridf("#FFFFFF") + "</g>"
  '<text x="76" y="46.5" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" letter-spacing="-1.8" fill="' + WHITE + '">agentcy</text>'
  '<text x="76" y="60.5" font-family="Arial, Helvetica, sans-serif" font-size="7.5" letter-spacing="3.4" fill="' + PERI + '">AI ENGINEERS ON SITE</text>'
  "</svg>")

# --- horizontal dark (transparent bg, ink art for white surfaces) ---
w("svg/agentcy-logo-horizontal-dark.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 72">'
  '<g transform="translate(24,22)">' + spark(INK) + gridf(INK) + "</g>"
  '<text x="76" y="46.5" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" letter-spacing="-1.8" fill="' + INK + '">agentcy</text>'
  '<text x="76" y="60.5" font-family="Arial, Helvetica, sans-serif" font-size="7.5" letter-spacing="3.4" fill="' + PERI + '">AI ENGINEERS ON SITE</text>'
  "</svg>")

# --- stacked (ink bg) ---
w("svg/agentcy-logo-stacked-white-on-ink.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 220">'
  '<rect width="320" height="220" rx="20" fill="' + INK + '"/>'
  '<g transform="translate(118,40) scale(3)">' + spark("#FFFFFF") + gridf("#FFFFFF") + "</g>"
  '<text x="160" y="172" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="700" letter-spacing="-2.6" fill="' + WHITE + '">agentcy</text>'
  '<text x="160" y="194" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="10" letter-spacing="4.6" fill="' + PERI + '">AI ENGINEERS ON SITE</text>'
  "</svg>")

# --- favicon: white spark on ink tile (matches live logo) ---
w("favicon/favicon.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
  '<rect width="64" height="64" rx="14" fill="' + INK + '"/>'
  '<g transform="translate(7,7) scale(1.7857)">' + spark("#FFFFFF") + gridf("#FFFFFF") + "</g></svg>")

# --- email mark chip ---
os.makedirs(OUT + "/_render", exist_ok=True)
chip = ('<div style="width:96px;height:96px;border-radius:22px;background:' + INK + ';'
        'display:flex;align-items:center;justify-content:center">'
        '<svg width="62" height="62" viewBox="0 0 28 28">' + spark("#FFFFFF") + gridf("#FFFFFF") + "</svg></div>")
w("_render/email-mark.html",
  '<!DOCTYPE html><html><head><style>html,body{margin:0;padding:0}</style></head>'
  '<body style="margin:0">' + chip + "</body></html>")
print("done")
