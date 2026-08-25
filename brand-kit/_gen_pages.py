import re, os

BASE = os.path.expanduser("~") + "/agentcy-site-live"
OUT = BASE + "/brand-kit"
os.makedirs(OUT + "/_render/banners", exist_ok=True)
os.makedirs(OUT + "/_render/templates", exist_ok=True)

# ---- REAL palette (live site computed styles) ----
INK = "#1A1A1A"
WHITE = "#FFFFFF"
MUTED = "#525252"
PERI = "#839AFF"
GRAD_CSS = ("linear-gradient(270deg,#C9AAFF 0%,#FEFFBC 25%,#FFCDFD 50%,"
            "#B3E2FF 75%,#839AFF 100%)")
GRAD_TEXT = ("background:" + GRAD_CSS + ";-webkit-background-clip:text;"
             "background-clip:text;color:transparent;-webkit-text-fill-color:transparent")

logo = open(BASE + "/uploads/logoicon.svg", encoding="utf-8").read()
paths = re.findall(r'<path [^>]+/>|<line [^>]+/>', logo)

def spark(f):
    return "".join(p.replace('fill="white"', 'fill="' + f + '"') for p in paths[:8])

def gridf(f):
    return "".join(p.replace('stroke="white"', 'stroke="' + f + '"')
                    .replace('fill="white"', 'fill="' + f + '"') for p in paths[8:])

SPARK_W, GRID_W = spark("#FFFFFF"), gridf("#FFFFFF")

def page(body):
    return ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<style>html,body{margin:0;padding:0}</style></head>'
            '<body style="margin:0">' + body + "</body></html>")

def base(w, h):
    s = ('<div style="width:WWpx;height:HHpx;position:relative;overflow:hidden;'
         'font-family:Arial,Helvetica,sans-serif;background:INK;color:WHITE">'
         '<div style="position:absolute;inset:0;'
         'background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),'
         'linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);'
         'background-size:72px 72px"></div>')
    return s.replace("WW", str(w)).replace("HH", str(h)).replace("INK", INK).replace("WHITE", WHITE)

CLOSE = "</div>"

def markchip(size, radius, inner):
    return ('<div style="width:' + str(size) + 'px;height:' + str(size) + 'px;border-radius:' +
            str(radius) + 'px;background:#222222;display:flex;align-items:center;'
            'justify-content:center;box-shadow:0 0 0 1px rgba(255,255,255,.22)">'
            '<svg width="' + str(inner) + '" height="' + str(inner) +
            '" viewBox="0 0 28 28">' + SPARK_W + GRID_W + '</svg></div>')

def lockup(msize, mr, ssize, wsize, tsize=10):
    return ('<div style="display:flex;align-items:center;gap:16px">' +
            markchip(msize, mr, int(ssize * 0.72)) +
            '<div><div style="font-weight:700;font-size:' + str(wsize) +
            'px;letter-spacing:-0.06em;line-height:1">agentcy</div>'
            '<div style="letter-spacing:.42em;font-size:' + str(tsize) +
            'px;color:' + PERI + ';text-transform:uppercase;margin-top:7px">AI engineers on site</div></div></div>')

def pill(text, pad="16px 30px", fs=20):
    return ('<span style="display:inline-flex;align-items:center;gap:12px;'
            'background:rgba(255,255,255,.85);color:' + INK + ';font-weight:700;'
            'border-radius:999px;padding:' + pad + ';font-size:' + str(fs) + 'px">' + text + '</span>')

def ghost(text, fs=12, pad="10px 22px"):
    return ('<span style="display:inline-block;padding:' + pad + ';'
            'border:1px solid rgba(255,255,255,.22);border-radius:999px;'
            'letter-spacing:.28em;color:#FFFFFF;font-size:' + str(fs) +
            'px;text-transform:uppercase">' + text + '</span>')

pages = {}

# ---------- 1 LINKEDIN BANNER 1584x396 ----------
b = base(1584, 396)
b += ('<svg style="position:absolute;right:-140px;top:-170px;width:760px;height:760px;opacity:.10" viewBox="-40 -40 108 108">' + SPARK_W + GRID_W + '</svg>')
b += ('<svg style="position:absolute;right:520px;bottom:-90px;width:280px;height:280px;opacity:.06" viewBox="0 0 28 28">' + SPARK_W + GRID_W + '</svg>')
b += '<div style="position:absolute;left:84px;top:72px">' + lockup(46, 11, 30, 34) + "</div>"
b += ('<div style="position:absolute;left:84px;top:196px">'
      '<div style="font-size:52px;font-weight:700;letter-spacing:-0.03em">Intelligent Automation <span style="' + GRAD_TEXT + '">for Modern Teams</span></div>'
      '<div style="margin-top:18px;font-size:19px;color:#A6A6A6">Forward-deployed AI engineers &nbsp;&middot;&nbsp; agentcy.co.za</div></div>')
b += CLOSE
pages["banners/linkedin-banner"] = page(b)

# ---------- 2 X HEADER 1500x500 ----------
b = base(1500, 500)
b += ('<svg style="position:absolute;left:-160px;bottom:-190px;width:700px;height:700px;opacity:.08" viewBox="-40 -40 108 108">' + SPARK_W + GRID_W + '</svg>')
b += ('<svg style="position:absolute;right:-120px;top:-130px;width:640px;height:640px;opacity:.10" viewBox="-40 -40 108 108">' + SPARK_W + GRID_W + '</svg>')
b += ('<div style="position:absolute;left:96px;top:88px">' +
      ghost("Forward-deployed AI engineering") +
      '<div style="margin-top:32px;font-size:58px;font-weight:700;letter-spacing:-0.03em;line-height:1.08">AI engineers,<br/><span style="' + GRAD_TEXT + '">on-site anywhere</span> in South Africa</div></div>')
b += ('<div style="position:absolute;left:96px;top:396px;display:flex;align-items:center;gap:14px">' +
      markchip(38, 9, 24) +
      '<div style="font-weight:700;font-size:26px;letter-spacing:-0.06em">agentcy<span style="color:' + PERI + '"></span></div></div>')
b += CLOSE
pages["banners/x-header"] = page(b)

# ---------- 3 FACEBOOK COVER 851x315 ----------
b = base(851, 315)
b += ('<svg style="position:absolute;right:-90px;top:-110px;width:430px;height:430px;opacity:.10" viewBox="-40 -40 108 108">' + SPARK_W + GRID_W + '</svg>')
b += ('<div style="position:absolute;left:56px;top:44px">'
      '<div style="font-size:38px;font-weight:700;letter-spacing:-0.03em;line-height:1.12">AI engineers,<br/><span style="' + GRAD_TEXT + '">on-site</span> in South Africa</div></div>')
b += ('<div style="position:absolute;left:56px;top:214px;display:flex;align-items:center;gap:12px">' +
      markchip(36, 8, 22) +
      '<div style="font-weight:700;font-size:24px;letter-spacing:-0.06em">agentcy</div>'
      '<div style="color:#A6A6A6;font-size:15px">&nbsp;&middot;&nbsp; agentcy.co.za</div></div>')
b += CLOSE
pages["banners/facebook-cover"] = page(b)

# ---------- 4 YOUTUBE BANNER 2560x1440 ----------
b = base(2560, 1440)
b += ('<svg style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:1546px;height:1546px;opacity:.05" viewBox="0 0 28 28">' + SPARK_W + GRID_W + '</svg>')
b += '<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-54%);text-align:center;width:1400px">'
b += '<div style="display:flex;justify-content:center">' + lockup(64, 15, 42, 48) + "</div>"
b += ('<div style="margin-top:44px;font-size:74px;font-weight:700;letter-spacing:-0.03em">Intelligent Automation <span style="' + GRAD_TEXT + '">for Modern Teams</span></div>'
      '<div style="margin-top:26px;font-size:26px;color:#A6A6A6">Forward-deployed AI engineers &nbsp;&middot;&nbsp; agentcy.co.za</div></div>')
b += CLOSE
pages["banners/youtube-banner"] = page(b)

# ---------- 5 OG IMAGE 1200x630 ----------
b = base(1200, 630)
b += ('<svg style="position:absolute;right:-110px;top:-120px;width:540px;height:540px;opacity:.10" viewBox="-40 -40 108 108">' + SPARK_W + GRID_W + '</svg>')
b += '<div style="position:absolute;left:70px;top:60px">' + lockup(44, 11, 28, 32) + "</div>"
b += ('<div style="position:absolute;left:70px;top:198px;width:1000px">'
      '<div style="font-size:58px;font-weight:700;letter-spacing:-0.03em;line-height:1.14">Intelligent Automation<br/><span style="' + GRAD_TEXT + '">for Modern Teams</span></div>'
      '<div style="margin-top:24px;font-size:21px;color:#A6A6A6">Workflow automation &middot; AI integrations &middot; WhatsApp CRM &middot; Custom tools</div></div>')
b += CLOSE
pages["banners/og-image"] = page(b)

# ---------- 6 IG SQUARE A - QUOTE 1080x1080 ----------
quote = ("&ldquo;The businesses that win won&rsquo;t be the ones with the most "
         "AI &mdash; they&rsquo;ll be the ones with AI actually working on the ground.&rdquo;")
hl = 'actually working on the ground.'
quote = quote.replace(hl, '</span>' + hl + '<span style="' + GRAD_TEXT + '">')
quote = ('<span style="color:' + WHITE + '">' + quote + "</span>")
b = base(1080, 1080)
b += ('<svg style="position:absolute;right:-190px;top:-190px;width:640px;height:640px;opacity:.08" viewBox="-40 -40 108 108">' + SPARK_W + GRID_W + '</svg>')
b += ('<svg style="position:absolute;left:-170px;bottom:-170px;width:520px;height:520px;opacity:.07" viewBox="0 0 28 28">' + SPARK_W + GRID_W + '</svg>')
b += ('<div style="position:absolute;left:96px;top:96px">' + ghost("Field Notes", 15, "12px 26px") + "</div>")
b += ('<div style="position:absolute;left:96px;top:252px;width:888px;font-size:64px;font-weight:700;letter-spacing:-0.02em;line-height:1.24">' + quote + '</div>')
b += ('<div style="position:absolute;left:96px;top:900px;display:flex;align-items:center;gap:16px">' +
      markchip(44, 11, 28) +
      '<div><div style="font-weight:700;font-size:24px;letter-spacing:-0.05em">agentcy</div>'
      '<div style="color:#A6A6A6;font-size:17px;margin-top:2px">agentcy.co.za</div></div></div>')
b += CLOSE
pages["templates/instagram-square-a-quote"] = page(b)

# ---------- 7 IG SQUARE B - SERVICES 1080x1080 ----------
services = [("01", "Workflow Automation", "Audits, architecture and hands-on builds"),
            ("02", "AI Integrations", "LLMs wired into the systems you already run"),
            ("03", "WhatsApp CRM", "Pipelines your team actually answers")]
rows = ""
for num, title, sub in services:
    rows += ('<div style="display:flex;align-items:center;gap:28px;padding:30px 0;'
             'border-bottom:1px solid rgba(255,255,255,.14)">'
             '<div style="font-size:22px;font-weight:700;letter-spacing:.2em;width:64px;' + GRAD_TEXT + '">' + num + '</div>'
             '<div><div style="font-size:33px;font-weight:700;letter-spacing:-0.02em">' + title + '</div>'
             '<div style="color:#A6A6A6;font-size:19px;margin-top:6px">' + sub + '</div></div></div>')
b = base(1080, 1080)
b += ('<svg style="position:absolute;right:-160px;bottom:-160px;width:560px;height:560px;opacity:.08" viewBox="-40 -40 108 108">' + SPARK_W + GRID_W + '</svg>')
b += '<div style="position:absolute;left:96px;top:86px"><div style="font-size:52px;font-weight:700;letter-spacing:-0.03em">What we <span style="' + GRAD_TEXT + '">deploy</span></div></div>'
b += '<div style="position:absolute;left:96px;top:208px;width:888px">' + rows + "</div>"
b += ('<div style="position:absolute;left:96px;top:872px">' + pill("Book a workflow audit &rarr;") + '</div>'
      '<div style="position:absolute;left:96px;top:968px;color:#A6A6A6;font-size:19px">agentcy.co.za &nbsp;&middot;&nbsp; ai@agentcy.co.za</div>')
b += CLOSE
pages["templates/instagram-square-b-services"] = page(b)

# ---------- 8 STORY 1080x1920 ----------
b = base(1080, 1920)
b += ('<svg style="position:absolute;right:-260px;top:-260px;width:860px;height:860px;opacity:.08" viewBox="-40 -40 108 108">' + SPARK_W + GRID_W + '</svg>')
b += ('<svg style="position:absolute;left:-240px;bottom:-240px;width:800px;height:800px;opacity:.07" viewBox="0 0 28 28">' + SPARK_W + GRID_W + '</svg>')
b += '<div style="position:absolute;left:84px;top:116px">' + lockup(52, 13, 34, 30) + "</div>"
b += ('<div style="position:absolute;left:84px;top:580px;width:912px">'
      '<div style="font-size:96px;font-weight:700;letter-spacing:-0.03em;line-height:1.08">Your workflows,<br/><span style="' + GRAD_TEXT + '">on autopilot.</span></div>'
      '<div style="margin-top:44px;font-size:31px;color:#A6A6A6;line-height:1.5">We audit, architect and automate the systems slowing your business down &mdash; then hand you the keys.</div></div>')
b += ('<div style="position:absolute;left:84px;top:1552px">' + pill("Book a workflow audit &rarr;", "26px 48px", 27) + '</div>'
      '<div style="position:absolute;left:84px;top:1690px;color:#A6A6A6;font-size:23px">agentcy.co.za</div>')
b += CLOSE
pages["templates/story-1080x1920"] = page(b)

# ---------- TOKEN SUBSTITUTION ----------
for name, html in pages.items():
    path = OUT + "/_render/" + name + ".html"
    open(path, "w", encoding="utf-8").write(html)
    print("wrote", name, len(html))
