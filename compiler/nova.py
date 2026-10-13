#!/usr/bin/env python3
"""
Nova 0.2.0 - a tiny language that compiles to a modern, Mac-smooth website.

Usage:
    python nova.py site.nova [output.html]
"""

import html
import os
import re
import sys
from urllib.parse import quote

VERSION = "0.2.0"
YES = ("yes", "true", "on", "1")


class NovaError(Exception):
    pass


def fail(num, msg):
    raise NovaError("line %d: %s" % (num, msg))


# ---------------------------------------------------------------- data

SYS = ('-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text",'
       '"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif')

THEMES = {
    "light": dict(bg="#f5f5f7", text="#1d1d1f", muted="#6e6e73", accent="#0071e3",
                  card="rgba(255,255,255,.72)", border="rgba(0,0,0,.08)", scheme="light"),
    "dark": dict(bg="#000000", text="#f5f5f7", muted="#a1a1a6", accent="#2997ff",
                 card="rgba(44,44,46,.60)", border="rgba(255,255,255,.12)", scheme="dark"),
    "ocean": dict(bg="linear-gradient(160deg,#021b2b,#04364f)", text="#e8f6ff",
                  muted="#8fb8cc", accent="#00b4d8",
                  card="rgba(255,255,255,.07)", border="rgba(255,255,255,.14)", scheme="dark"),
    "sunset": dict(bg="linear-gradient(160deg,#1b0a14,#4a1230)", text="#fff1ea",
                   muted="#d6a79b", accent="#ff6b4a",
                   card="rgba(255,255,255,.07)", border="rgba(255,255,255,.14)", scheme="dark"),
    "forest": dict(bg="linear-gradient(160deg,#07150e,#0f3a24)", text="#eaf6ee",
                   muted="#9ab8a5", accent="#3ddc84",
                   card="rgba(255,255,255,.07)", border="rgba(255,255,255,.14)", scheme="dark"),
    "rose": dict(bg="linear-gradient(160deg,#fff0f3,#ffd9e2)", text="#3a0a1a",
                 muted="#8a5566", accent="#e11d63",
                 card="rgba(255,255,255,.70)", border="rgba(225,29,99,.15)", scheme="light"),
}

FONTS = {
    "mac": (SYS, None),
    "system": (SYS, None),
    "serif": ('Georgia,"Times New Roman",serif', None),
    "mono": ('ui-monospace,"SF Mono",Menlo,Consolas,monospace', None),
    "inter": ('"Inter",' + SYS, "Inter:wght@400;700"),
    "poppins": ('"Poppins",' + SYS, "Poppins:wght@400;700"),
    "montserrat": ('"Montserrat",' + SYS, "Montserrat:wght@400;700"),
    "roboto": ('"Roboto",' + SYS, "Roboto:wght@400;700"),
    "opensans": ('"Open Sans",' + SYS, "Open+Sans:wght@400;700"),
    "playfair": ('"Playfair Display",Georgia,serif', "Playfair+Display:wght@400;700"),
    "lobster": ('"Lobster",cursive', "Lobster"),
    "pacifico": ('"Pacifico",cursive', "Pacifico"),
    "bebas": ('"Bebas Neue",Impact,sans-serif', "Bebas+Neue"),
    "orbitron": ('"Orbitron",' + SYS, "Orbitron:wght@400;700"),
    "caveat": ('"Caveat",cursive', "Caveat:wght@400;700"),
    "fira": ('"Fira Code",ui-monospace,monospace', "Fira+Code:wght@400;700"),
    # Arabic fonts
    "cairo": ('"Cairo",' + SYS, "Cairo:wght@400;700"),
    "tajawal": ('"Tajawal",' + SYS, "Tajawal:wght@400;700"),
    "almarai": ('"Almarai",' + SYS, "Almarai:wght@400;700"),
    "amiri": ('"Amiri",Georgia,serif', "Amiri:wght@400;700"),
    "changa": ('"Changa",' + SYS, "Changa:wght@400;700"),
}
FONTS["playfairdisplay"] = FONTS["playfair"]
FONTS["bebasneue"] = FONTS["bebas"]
FONTS["firacode"] = FONTS["fira"]

ENTRANCE = ("fade", "slide-up", "slide-down", "slide-left", "slide-right",
            "zoom", "flip", "blur")
LOOPS = ("float", "pulse", "spin", "bounce", "shake", "glow", "wiggle", "rainbow")
HOVERS = ("lift", "grow", "shrink", "glow", "tilt", "none")
SHADOWS = {
    "none": "none",
    "soft": "0 6px 20px rgba(0,0,0,.10)",
    "medium": "0 12px 34px rgba(0,0,0,.18)",
    "big": "0 24px 60px rgba(0,0,0,.28)",
}

ARITY = {
    "title": (1, 1), "subtitle": (1, 1), "paragraph": (1, 1),
    "button": (1, 2), "link": (2, 2), "image": (1, 2), "sticker": (1, 1),
    "card": (2, 3), "list": (1, None), "divider": (0, 0), "space": (0, 1),
    "hero": (1, 2), "navbar": (2, None), "footer": (1, 1), "video": (1, 1),
    "box": (0, 0), "grid": (0, 1), "end": (0, 0),
}
GLOBAL_ARITY = {
    "page": (1, 1), "icon": (1, 1), "lang": (1, 1), "direction": (1, 1),
    "theme": (1, 1), "textcolor": (1, 1), "accent": (1, 1), "background": (1, 1),
    "gradient": (2, None), "font": (1, 1), "headingfont": (1, 1),
    "width": (1, 1), "animate": (1, 1),
}
EXAMPLES = {
    "title": 'title "Hello"', "subtitle": 'subtitle "Welcome"',
    "paragraph": 'paragraph "Some text"', "button": 'button "Click" "#section"',
    "link": 'link "Google" "https://google.com"', "image": 'image "photo.jpg" "description"',
    "sticker": 'sticker "🚀" size=80 animate=float', "card": 'card "Title" "Text" "🎨"',
    "list": 'list "One" "Two" "Three"', "divider": "divider", "space": "space 40",
    "hero": 'hero "Big title" "Subtitle"', "navbar": 'navbar "Brand" "Home|#top" "About|#about"',
    "footer": 'footer "Made with Nova"', "video": 'video "clip.mp4"',
    "box": "box", "grid": "grid 3", "end": "end",
    "page": 'page "My Site"', "icon": 'icon "🚀"', "lang": "lang ar", "direction": "direction rtl",
    "theme": "theme dark", "textcolor": "textcolor #ffffff", "accent": "accent #ff3366",
    "background": "background #111111   (or an image: background wall.jpg)",
    "gradient": "gradient #667eea #764ba2 135 animated=yes", "font": "font Poppins",
    "headingfont": 'headingfont "Playfair Display"', "width": "width 1000",
    "animate": "animate slide-up   (default entrance for all elements, or: none)",
}

STYLE_OPTS = {"color", "bg", "size", "font", "weight", "radius", "shadow", "padding",
              "margin", "width", "height", "border", "gap", "fit", "spacing",
              "textgradient"}
OTHER_OPTS = {"animate", "delay", "duration", "hover", "glass", "align", "id",
              "look", "drag", "autoplay", "inline"}
ALLOWED = STYLE_OPTS | OTHER_OPTS

SAFE = re.compile(r"^[#\w\s(),.%/+\-]+$")
NUM = re.compile(r"^\d+(\.\d+)?$")
IMG_EXT = re.compile(r"\.(png|jpe?g|gif|webp|svg|avif)$", re.I)
IMG_PATH = re.compile(r"^(https?://[^\s'\"()\\<>;]+|[\w./\- %]+)$")
TOKEN = re.compile(r'([\w-]+)=("[^"]*"|\S+)|"([^"]*)"|(\S+)')


class Ctx:
    def __init__(self):
        self.settings = {}
        self.fonts = set()


# ---------------------------------------------------------------- helpers

def txt(s):
    return html.escape(s).replace("\\n", "<br>")


def val(v, num, name):
    v = v.strip()
    if not v or not SAFE.match(v):
        fail(num, "invalid value for %s: %r" % (name, v))
    return v


def px(v, num, name):
    v = v.strip()
    return v + "px" if NUM.match(v) else val(v, num, name)


def secs(v, num, name):
    v = v.strip()
    if v.endswith("s"):
        v = v[:-1]
    if not NUM.match(v):
        fail(num, "%s must be a number of seconds, e.g. %s=0.5" % (name, name))
    return v + "s"


def url_ok(u, num):
    u = u.strip()
    if re.match(r"^(javascript|data|vbscript):", u, re.I):
        fail(num, "this kind of link is not allowed")
    return html.escape(u, quote=True)


def href(u, num):
    out = ' href="%s"' % url_ok(u, num)
    if re.match(r"^https?://", u.strip(), re.I):
        out += ' target="_blank" rel="noopener"'
    return out


def bg_css(v, num):
    v = v.strip()
    if IMG_EXT.search(v):
        if not IMG_PATH.match(v):
            fail(num, "invalid image path: %r" % v)
        return "url('%s') center/cover no-repeat" % v
    return val(v, num, "background")


def font_css(name, ctx, num):
    key = name.strip().lower().replace(" ", "")
    if key in FONTS:
        fam, gf = FONTS[key]
        if gf:
            ctx.fonts.add(gf)
        return fam
    n = name.strip()
    if not re.fullmatch(r"[\w ]+", n):
        fail(num, "invalid font name: %r" % name)
    ctx.fonts.add(n.replace(" ", "+"))
    return '"%s",%s' % (n, SYS)


def anim_names(opts, num):
    names = [a.strip().lower() for a in opts.get("animate", "").split(",") if a.strip()]
    for a in names:
        if a not in ENTRANCE and a not in LOOPS and a != "none":
            fail(num, "unknown animation '%s'. Available: %s, %s"
                 % (a, ", ".join(ENTRANCE), ", ".join(LOOPS)))
    return names


def style_of(opts, num, ctx):
    s = []
    if "color" in opts:
        s.append("color:" + val(opts["color"], num, "color"))
    if "bg" in opts:
        s.append("background:" + bg_css(opts["bg"], num))
    if "size" in opts:
        s.append("font-size:" + px(opts["size"], num, "size"))
    if "font" in opts:
        s.append("font-family:" + font_css(opts["font"], ctx, num))
    if "weight" in opts:
        w = opts["weight"].lower()
        if w == "bold":
            w = "700"
        if not re.fullmatch(r"normal|[1-9]00", w):
            fail(num, "weight must be normal, bold, or 100-900")
        s.append("font-weight:" + w)
    if "radius" in opts:
        s.append("border-radius:" + px(opts["radius"], num, "radius"))
    if "shadow" in opts:
        sh = opts["shadow"].lower()
        if sh not in SHADOWS:
            fail(num, "shadow must be one of: " + ", ".join(SHADOWS))
        s.append("box-shadow:" + SHADOWS[sh])
    for key, prop in (("padding", "padding"), ("margin", "margin"), ("width", "width"),
                      ("height", "height"), ("gap", "gap"), ("spacing", "letter-spacing")):
        if key in opts:
            s.append("%s:%s" % (prop, px(opts[key], num, key)))
    if "border" in opts:
        s.append("border:" + val(opts["border"], num, "border"))
    if "fit" in opts:
        f = opts["fit"].lower()
        if f not in ("cover", "contain", "fill"):
            fail(num, "fit must be cover, contain, or fill")
        s.append("object-fit:" + f)
    if "textgradient" in opts:
        cols = [val(c, num, "textgradient") for c in opts["textgradient"].split(",")]
        if len(cols) < 2:
            fail(num, "textgradient needs 2 colors, e.g. textgradient=#ff0080,#7928ca")
        s.append("display:inline-block;background:linear-gradient(90deg,%s);"
                 "-webkit-background-clip:text;background-clip:text;"
                 "-webkit-text-fill-color:transparent;color:transparent" % ",".join(cols))
    return s


def attrs(opts, num, ctx, classes=(), hover=None, extra_style=None):
    cls = list(classes)
    for a in anim_names(opts, num):
        if a in LOOPS:
            cls.append("a-" + a)
    hv = opts.get("hover", hover)
    if hv:
        hv = hv.lower()
        if hv not in HOVERS:
            fail(num, "hover must be one of: " + ", ".join(HOVERS))
        if hv != "none":
            cls.append("h-" + hv)
    if opts.get("glass", "").lower() in YES:
        cls.append("glass")
    if opts.get("drag", "").lower() in YES:
        cls.append("drag")
    st = list(extra_style or []) + style_of(opts, num, ctx)
    out = ""
    if cls:
        out += ' class="%s"' % " ".join(cls)
    if st:
        out += ' style="%s"' % html.escape(";".join(st), quote=True)
    return out


def wrap(inner, opts, num, ctx, frame, align=None, extra=""):
    names = anim_names(opts, num)
    ent = [a for a in names if a in ENTRANCE]
    if "none" in names:
        ent = []
    elif not ent:
        d = ctx.settings.get("animate", "slide-up")
        if d != "none":
            ent = [d]
    cls = ["n"]
    if extra:
        cls.append(extra)
    if opts.get("inline", "").lower() in YES:
        cls.append("inl")
    st = []
    a = opts.get("align", align)
    if a:
        if a not in ("left", "center", "right"):
            fail(num, "align must be left, center, or right")
        st.append("text-align:" + a)
    if "duration" in opts:
        st.append("--dur:" + secs(opts["duration"], num, "duration"))
    if "delay" in opts:
        st.append("--delay:" + secs(opts["delay"], num, "delay"))
    elif ent and frame.get("stagger"):
        st.append("--delay:%.2fs" % min(frame["count"] * 0.08, 0.8))
        frame["count"] += 1
    if ent:
        cls += ["rv"] + ent
    wid = ""
    if "id" in opts:
        if not re.fullmatch(r"[\w-]+", opts["id"]):
            fail(num, "id may only contain letters, numbers, - and _")
        wid = ' id="%s"' % opts["id"]
    sattr = ' style="%s"' % html.escape(";".join(st), quote=True) if st else ""
    return '<div class="%s"%s%s>%s</div>' % (" ".join(cls), wid, sattr, inner)


# ---------------------------------------------------------------- elements

def render(cmd, args, opts, num, ctx, frame):
    def W(inner, **kw):
        return wrap(inner, opts, num, ctx, frame, **kw)

    if cmd == "title":
        return W("<h1%s>%s</h1>" % (attrs(opts, num, ctx), txt(args[0])))
    if cmd == "subtitle":
        return W("<h2%s>%s</h2>" % (attrs(opts, num, ctx, ["sub"]), txt(args[0])))
    if cmd == "paragraph":
        return W("<p%s>%s</p>" % (attrs(opts, num, ctx), txt(args[0])))

    if cmd == "button":
        look = opts.get("look", "solid").lower()
        if look not in ("solid", "outline", "soft"):
            fail(num, "look must be solid, outline, or soft")
        cl = ["btn"] + ([] if look == "solid" else ["btn-" + look])
        a = attrs(opts, num, ctx, cl)
        if len(args) == 2:
            return W("<a%s%s>%s</a>" % (a, href(args[1], num), txt(args[0])))
        return W('<button%s type="button">%s</button>' % (a, txt(args[0])))

    if cmd == "link":
        return W("<a%s%s>%s</a>" % (attrs(opts, num, ctx, ["lnk"]),
                                    href(args[1], num), txt(args[0])))

    if cmd == "image":
        alt = args[1] if len(args) == 2 else ""
        return W('<img%s src="%s" alt="%s" loading="lazy">'
                 % (attrs(opts, num, ctx, ["img"]), url_ok(args[0], num),
                    html.escape(alt, quote=True)))

    if cmd == "sticker":
        s = args[0]
        if IMG_EXT.search(s):
            o2 = dict(opts)
            if "size" in o2:
                o2["height"] = o2.pop("size")
            return W('<img%s src="%s" alt="" draggable="false">'
                     % (attrs(o2, num, ctx, ["sticker-img"]), url_ok(s, num)))
        return W('<span%s role="img" aria-label="sticker">%s</span>'
                 % (attrs(opts, num, ctx, ["sticker"]), html.escape(s)))

    if cmd == "card":
        ic = '<div class="ic">%s</div>' % txt(args[2]) if len(args) == 3 else ""
        return W("<div%s>%s<h3>%s</h3><p>%s</p></div>"
                 % (attrs(opts, num, ctx, ["card"], hover="lift"), ic,
                    txt(args[0]), txt(args[1])))

    if cmd == "list":
        items = "".join("<li>%s</li>" % txt(i) for i in args)
        return W("<ul%s>%s</ul>" % (attrs(opts, num, ctx, ["list"]), items))

    if cmd == "divider":
        return W("<hr%s>" % attrs(opts, num, ctx, ["hr"]))

    if cmd == "space":
        n = args[0] if args else "40"
        if not NUM.match(n):
            fail(num, "space needs a number, e.g. space 40")
        return '<div style="height:%spx"></div>' % n

    if cmd == "hero":
        sub = "<p>%s</p>" % txt(args[1]) if len(args) == 2 else ""
        return W("<section%s><h1>%s</h1>%s</section>"
                 % (attrs(opts, num, ctx, ["hero"]), txt(args[0]), sub), align="center")

    if cmd == "navbar":
        links = []
        for item in args[1:]:
            if "|" not in item:
                fail(num, 'navbar items look like "Home|#top"  (text|link)')
            label, url = item.rsplit("|", 1)
            links.append("<a%s>%s</a>" % (href(url, num), txt(label)))
        return W('<nav%s><b>%s</b><div class="links">%s</div></nav>'
                 % (attrs(opts, num, ctx, ["nav"]), txt(args[0]), "".join(links)),
                 extra="sticky")

    if cmd == "footer":
        return W("<footer%s>%s</footer>" % (attrs(opts, num, ctx, ["footer"]), txt(args[0])))

    if cmd == "video":
        flags = (" autoplay muted loop playsinline"
                 if opts.get("autoplay", "").lower() in YES else " controls playsinline")
        return W('<video%s src="%s"%s></video>'
                 % (attrs(opts, num, ctx, ["img"]), url_ok(args[0], num), flags))

    fail(num, "unknown command: " + cmd)


def apply_global(cmd, args, opts, num, ctx):
    S = ctx.settings
    a = args[0] if args else ""
    if opts and not (cmd == "gradient" and set(opts) == {"animated"}):
        fail(num, '"%s" does not take options' % cmd)
    if cmd == "page":
        S["title"] = a
    elif cmd == "icon":
        S["icon"] = a
    elif cmd == "lang":
        if not re.fullmatch(r"[A-Za-z-]{2,10}", a):
            fail(num, "lang example: lang ar")
        S["lang"] = a
    elif cmd == "direction":
        if a.lower() not in ("rtl", "ltr"):
            fail(num, "direction must be rtl or ltr")
        S["dir"] = a.lower()
    elif cmd == "theme":
        if a.lower() not in THEMES:
            fail(num, "unknown theme. Available: " + ", ".join(THEMES))
        S["theme"] = a.lower()
    elif cmd == "textcolor":
        S["text"] = val(a, num, "textcolor")
    elif cmd == "accent":
        S["accent"] = val(a, num, "accent")
    elif cmd == "background":
        S["bg"] = bg_css(a, num)
        S["bg_anim"] = False
    elif cmd == "gradient":
        cols = list(args)
        angle = "135deg"
        if NUM.match(cols[-1]):
            angle = cols.pop() + "deg"
        if len(cols) < 2:
            fail(num, "gradient needs at least 2 colors")
        cols = [val(c, num, "gradient") for c in cols]
        S["bg"] = "linear-gradient(%s,%s)" % (angle, ",".join(cols))
        S["bg_anim"] = opts.get("animated", "").lower() in YES
    elif cmd == "font":
        S["font"] = font_css(a, ctx, num)
    elif cmd == "headingfont":
        S["hfont"] = font_css(a, ctx, num)
    elif cmd == "width":
        S["maxw"] = px(a, num, "width")
    elif cmd == "animate":
        if a.lower() != "none" and a.lower() not in ENTRANCE:
            fail(num, "animate must be none or one of: " + ", ".join(ENTRANCE))
        S["animate"] = a.lower()


# ---------------------------------------------------------------- parsing

def parse_line(line):
    parts = line.split(None, 1)
    cmd = parts[0].lower()
    rest = parts[1] if len(parts) > 1 else ""
    args, opts = [], {}
    for m in TOKEN.finditer(rest):
        if m.group(1):
            v = m.group(2)
            if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
                v = v[1:-1]
            opts[m.group(1).lower()] = v
        elif m.group(3) is not None:
            args.append(m.group(3))
        else:
            args.append(m.group(4))
    return cmd, args, opts


def check_arity(cmd, args, table, num):
    lo, hi = table[cmd]
    if len(args) < lo or (hi is not None and len(args) > hi):
        fail(num, 'wrong number of values for "%s". Example: %s' % (cmd, EXAMPLES[cmd]))


def build(src, out):
    ctx = Ctx()
    root = {"kids": [], "stagger": False, "count": 0}
    stack = [root]

    with open(src, encoding="utf-8-sig") as f:
        for num, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.count('"') % 2:
                fail(num, "missing closing quote (\")")
            cmd, args, opts = parse_line(line)

            if cmd in GLOBAL_ARITY:
                check_arity(cmd, args, GLOBAL_ARITY, num)
                apply_global(cmd, args, opts, num, ctx)
                continue
            if cmd not in ARITY:
                fail(num, "unknown command '%s'. Commands: %s"
                     % (cmd, ", ".join(list(GLOBAL_ARITY) + list(ARITY))))
            check_arity(cmd, args, ARITY, num)
            bad = set(opts) - ALLOWED
            if bad:
                fail(num, "unknown option(s): %s" % ", ".join(sorted(bad)))

            frame = stack[-1]
            if cmd == "box":
                stack.append({"kids": [], "stagger": False, "count": 0, "opts": opts,
                              "num": num,
                              "open": "<div%s>" % attrs(opts, num, ctx, ["box"])})
            elif cmd == "grid":
                cols = args[0] if args else "3"
                if not re.fullmatch(r"[1-6]", cols):
                    fail(num, "grid columns must be a number from 1 to 6")
                stack.append({"kids": [], "stagger": True, "count": 0, "opts": opts,
                              "num": num,
                              "open": "<div%s>" % attrs(opts, num, ctx, ["grid"],
                                                        extra_style=["--cols:" + cols])})
            elif cmd == "end":
                if len(stack) == 1:
                    fail(num, '"end" without a matching "box" or "grid"')
                fr = stack.pop()
                inner = fr["open"] + "".join(fr["kids"]) + "</div>"
                parent = stack[-1]
                parent["kids"].append(wrap(inner, fr["opts"], fr["num"], ctx, parent))
            else:
                frame["kids"].append(render(cmd, args, opts, num, ctx, frame))

    if len(stack) > 1:
        fail(stack[-1]["num"], 'this "box"/"grid" is never closed with "end"')

    with open(out, "w", encoding="utf-8") as f:
        f.write(page_html(ctx, "".join(root["kids"])))
    print("Done! Built: " + out)


# ---------------------------------------------------------------- output

BASE_CSS = """
:root{--ease:cubic-bezier(.16,1,.3,1);--spring:cubic-bezier(.34,1.56,.64,1)}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;min-height:100vh;color:var(--text);font-family:var(--font);line-height:1.55;
-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;animation:pageIn .9s var(--ease) both}
::selection{background:var(--accent);color:#fff}
.page{max-width:var(--maxw);margin:0 auto;padding:24px 24px 96px}
.n{display:block}
.n.inl{display:inline-block;vertical-align:middle;margin:6px}
.n[id]{scroll-margin-top:96px}
h1,h2,h3{font-family:var(--hfont,var(--font));margin:0 0 .4em;letter-spacing:-.02em;line-height:1.1}
h1{font-size:clamp(2.2rem,6vw,4rem);font-weight:700}
h2{font-size:clamp(1.5rem,3.5vw,2.2rem);font-weight:700}
h2.sub{font-weight:400;color:var(--muted)}
h3{font-size:1.3rem;font-weight:700}
p{margin:0 0 1em;font-size:1.1rem}
.btn{display:inline-block;font:inherit;font-weight:600;font-size:1rem;padding:.8em 1.7em;
border:2px solid var(--accent);border-radius:980px;background:var(--accent);color:#fff;
text-decoration:none;cursor:pointer;transition:transform .45s var(--spring),box-shadow .45s var(--ease),filter .3s}
.btn:hover{transform:scale(1.05);filter:brightness(1.1)}
.btn:active{transform:scale(.96)}
.btn-outline{background:transparent;color:var(--accent)}
.btn-soft{background:var(--card);color:var(--accent);border-color:transparent}
.lnk{color:var(--accent);text-decoration:none;font-weight:500;transition:opacity .3s}
.lnk:hover{opacity:.65}
.img{display:inline-block;max-width:100%;height:auto;border-radius:20px;vertical-align:middle}
.sticker{display:inline-block;font-size:64px;line-height:1;user-select:none}
.sticker-img{display:inline-block;height:90px;width:auto;user-select:none;-webkit-user-drag:none}
.drag{cursor:grab;touch-action:none}
.card{background:var(--card);border:1px solid var(--border);border-radius:22px;padding:28px;
backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%)}
.card h3{margin-bottom:.35em}
.card p{margin:0;color:var(--muted);font-size:1rem}
.card .ic{font-size:2.2rem;line-height:1;margin-bottom:.4em}
.glass{background:var(--card);border:1px solid var(--border);border-radius:22px;
backdrop-filter:blur(24px) saturate(180%);-webkit-backdrop-filter:blur(24px) saturate(180%)}
.box{padding:4px 0}
.glass.box{padding:28px}
.grid{display:grid;grid-template-columns:repeat(var(--cols,3),1fr);gap:20px}
.grid>.n{display:flex;flex-direction:column}
.grid>.n>*{flex:1}
@media(max-width:720px){.grid{grid-template-columns:1fr}}
.hero{padding:clamp(48px,12vh,120px) 24px;border-radius:28px}
.hero h1{font-size:clamp(2.6rem,8vw,5.2rem)}
.hero p{font-size:clamp(1.1rem,2.4vw,1.5rem);color:var(--muted);max-width:46ch;margin:.5em auto 0}
.sticky{position:sticky;top:12px;z-index:50;margin-bottom:16px}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;
padding:12px 22px;border-radius:30px;background:var(--card);border:1px solid var(--border);
backdrop-filter:blur(24px) saturate(180%);-webkit-backdrop-filter:blur(24px) saturate(180%);
box-shadow:0 8px 30px rgba(0,0,0,.10)}
.nav b{font-size:1.05rem}
.nav .links{display:flex;gap:4px;flex-wrap:wrap}
.nav a{color:var(--text);text-decoration:none;padding:6px 14px;border-radius:980px;font-size:.95rem;
transition:background .3s}
.nav a:hover{background:var(--border)}
.footer{text-align:center;color:var(--muted);font-size:.9rem;padding:48px 0 0}
.hr{border:0;height:1px;background:var(--border);margin:32px 0}
.list{padding-inline-start:1.3em;font-size:1.1rem}
.list li{margin:.35em 0}
.h-lift,.h-grow,.h-shrink,.h-glow,.h-tilt{transition:transform .5s var(--spring),box-shadow .5s var(--ease),filter .4s var(--ease)}
.h-lift:hover{transform:translateY(-8px);box-shadow:0 18px 40px rgba(0,0,0,.20)}
.h-grow:hover{transform:scale(1.07)}
.h-shrink:hover{transform:scale(.94)}
.h-glow:hover{box-shadow:0 0 34px var(--accent);filter:brightness(1.1)}
.h-tilt:hover{transform:rotate(-3deg) scale(1.06)}
.rv{opacity:0;transition:opacity var(--dur,.9s) var(--ease) var(--delay,0s),
transform var(--dur,.9s) var(--ease) var(--delay,0s),filter var(--dur,.9s) var(--ease) var(--delay,0s)}
.rv.slide-up{transform:translateY(40px)}
.rv.slide-down{transform:translateY(-40px)}
.rv.slide-left{transform:translateX(60px)}
.rv.slide-right{transform:translateX(-60px)}
.rv.zoom{transform:scale(.88)}
.rv.flip{transform:perspective(800px) rotateX(25deg) translateY(30px)}
.rv.blur{filter:blur(14px);transform:scale(1.04)}
.rv.in{opacity:1;transform:none;filter:none}
.a-float{animation:float var(--dur,3.4s) ease-in-out var(--delay,0s) infinite}
.a-pulse{animation:pulse var(--dur,2.2s) ease-in-out var(--delay,0s) infinite}
.a-spin{animation:spin var(--dur,8s) linear var(--delay,0s) infinite}
.a-bounce{animation:bounce var(--dur,1.4s) ease-in-out var(--delay,0s) infinite}
.a-shake{animation:shake var(--dur,.8s) ease-in-out var(--delay,0s) infinite}
.a-glow{animation:glow var(--dur,2.4s) ease-in-out var(--delay,0s) infinite alternate}
.a-wiggle{animation:wiggle var(--dur,1.6s) ease-in-out var(--delay,0s) infinite}
.a-rainbow{animation:rainbow var(--dur,6s) linear var(--delay,0s) infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.09)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes bounce{0%,100%{transform:translateY(0)}40%{transform:translateY(-24px)}60%{transform:translateY(-12px)}}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-8px)}40%{transform:translateX(8px)}60%{transform:translateX(-5px)}80%{transform:translateX(5px)}}
@keyframes glow{from{filter:drop-shadow(0 0 2px var(--accent))}to{filter:drop-shadow(0 0 18px var(--accent))}}
@keyframes wiggle{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}
@keyframes rainbow{to{filter:hue-rotate(360deg)}}
@keyframes pageIn{from{opacity:0}to{opacity:1}}
@keyframes gradientShift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
@media(prefers-reduced-motion:reduce){
*{animation:none!important;transition:none!important;scroll-behavior:auto!important}
.rv{opacity:1!important;transform:none!important;filter:none!important}}
"""

BASE_JS = """
(function(){
var els=document.querySelectorAll('.rv');
if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});}
else{
var io=new IntersectionObserver(function(en){en.forEach(function(x){
if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},
{threshold:.12,rootMargin:'0px 0px -6% 0px'});
els.forEach(function(e){io.observe(e)});}
document.querySelectorAll('.drag').forEach(function(el){
var x=0,y=0,sx=0,sy=0,on=false;
el.addEventListener('pointerdown',function(e){on=true;sx=e.clientX-x;sy=e.clientY-y;
el.setPointerCapture(e.pointerId);el.style.cursor='grabbing';e.preventDefault();});
el.addEventListener('pointermove',function(e){if(!on)return;x=e.clientX-sx;y=e.clientY-sy;
el.style.translate=x+'px '+y+'px';});
var up=function(){on=false;el.style.cursor='grab';};
el.addEventListener('pointerup',up);el.addEventListener('pointercancel',up);
});
})();
"""


def page_html(ctx, body):
    S = ctx.settings
    th = THEMES[S.get("theme", "light")]
    text = S.get("text", th["text"])
    muted = S.get("text", th["muted"])
    accent = S.get("accent", th["accent"])
    font = S.get("font", SYS)
    maxw = S.get("maxw", "980px")
    direction = S.get("dir", "ltr")
    lang = S.get("lang", "ar" if direction == "rtl" else "en")
    title = html.escape(S.get("title", "Nova Site"))

    root = (":root{color-scheme:%s;--bg:%s;--text:%s;--muted:%s;--accent:%s;--card:%s;"
            "--border:%s;--font:%s;--maxw:%s;" % (th["scheme"], th["bg"], text, muted, accent,
                                                  th["card"], th["border"], font, maxw))
    if "hfont" in S:
        root += "--hfont:%s;" % S["hfont"]
    root += "}"
    dyn = "body{background:%s;background-attachment:fixed}" % (S.get("bg") or "var(--bg)")
    if S.get("bg_anim"):
        dyn += ("body{background-size:300% 300%;"
                "animation:pageIn .9s var(--ease) both,gradientShift 14s ease infinite}")

    fonts = ""
    if ctx.fonts:
        fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
                 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n')
        for g in sorted(ctx.fonts):
            fonts += ('<link rel="stylesheet" href="https://fonts.googleapis.com/'
                      'css2?family=%s&amp;display=swap">\n' % g)

    icon = ""
    if S.get("icon"):
        svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
               "<text y='.9em' font-size='90'>%s</text></svg>" % html.escape(S["icon"]))
        icon = '<link rel="icon" href="data:image/svg+xml,%s">\n' % quote(svg)

    return """<!DOCTYPE html>
<html lang="%s" dir="%s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
%s%s<style>%s%s%s</style>
<noscript><style>.rv{opacity:1!important;transform:none!important;filter:none!important}</style></noscript>
</head>
<body>
<div class="page">
%s
</div>
<script>%s</script>
</body>
</html>
""" % (lang, direction, title, icon, fonts, root, BASE_CSS, dyn, body, BASE_JS)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print("Nova %s\nUsage: python nova.py site.nova [output.html]" % VERSION)
        return
    src = args[0] if args else "index.nova"
    out = args[1] if len(args) > 1 else os.path.splitext(src)[0] + ".html"
    try:
        build(src, out)
    except NovaError as e:
        print("Nova error - " + str(e))
        sys.exit(1)
    except FileNotFoundError:
        print("File not found: " + src)
        sys.exit(1)


if __name__ == "__main__":
    main()
