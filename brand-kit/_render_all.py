import os, subprocess, sys

BASE = os.path.expanduser("~") + "/agentcy-site-live"
OUT = BASE + "/brand-kit"
EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

def shot(html_path, w, h, png_path):
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--force-device-scale-factor=1",
           "--window-size=%d,%d" % (w, h),
           "--screenshot=" + png_path,
           "file:///" + html_path.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    ok = os.path.exists(png_path) and os.path.getsize(png_path) > 5000
    print(("OK  " if ok else "FAIL") + " " + os.path.basename(png_path),
          os.path.getsize(png_path) if os.path.exists(png_path) else r.stderr[-200:])
    return ok

SIZES = {
    "banners/linkedin-banner": (1584, 396),
    "banners/x-header": (1500, 500),
    "banners/facebook-cover": (851, 315),
    "banners/youtube-banner": (2560, 1440),
    "banners/og-image": (1200, 630),
    "templates/instagram-square-a-quote": (1080, 1080),
    "templates/instagram-square-b-services": (1080, 1080),
    "templates/story-1080x1920": (1080, 1920),
}

fails = []
for name, (w, h) in SIZES.items():
    src = OUT + "/_render/" + name + ".html"
    dst = OUT + "/" + name.replace("/", "-") + ".png"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not shot(src, w, h, dst):
        fails.append(name)

# favicon rasters from favicon.svg
FAV_IN = OUT + "/favicon/favicon.svg"
fav_sizes = [(16, "favicon/favicon-16.png"), (32, "favicon/favicon-32.png"),
             (48, "favicon/favicon-48.png"), (180, "favicon/apple-touch-icon.png"),
             (192, "favicon/icon-192.png"), (270, "favicon/mstile-270x270.png"),
             (512, "favicon/icon-512.png")]
for s, rel in fav_sizes:
    dst = OUT + "/" + rel
    if not shot(FAV_IN, s, s, dst):
        fails.append(rel)

print("FAILS:", fails if fails else "none")
sys.exit(1 if fails else 0)
