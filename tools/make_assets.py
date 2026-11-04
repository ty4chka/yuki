import math, os, re, html
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)
FONT = "Roboto, 'Segoe UI', 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
MONO = "'JetBrains Mono','DejaVu Sans Mono',Consolas,Menlo,monospace"

LIGHT = dict(bg="#f4eeff", card="#ece4fb", card2="#e6deff", prim="#6b4fd8", onprim="#ffffff",
             pc="#e6deff", onpc="#21005d", sec="#e8def8", onsec="#1d192b", ter="#c8f2ee", onter="#00201f",
             text="#1d1b20", textv="#49454f", outline="#7a757f", warn="#ffe9b0", onwarn="#4a3400")
DARK = dict(bg="#1d1a22", card="#2b2930", card2="#36343b", prim="#cfbcff", onprim="#381e72",
            pc="#4f378b", onpc="#eaddff", sec="#4a4458", onsec="#e8def8", ter="#00504d", onter="#c8f2ee",
            text="#e6e0e9", textv="#cac4d0", outline="#948f99", warn="#5c4300", onwarn="#ffdf9a")
THEMES = {"light": LIGHT, "dark": DARK}

def esc(s): return html.escape(s, quote=False)
def tw(s, size, k=0.56): return int(len(s) * size * k)

def shape(cx, cy, R, n, amp, rot=0.0, pts=260):
    out = []
    for i in range(pts):
        t = 2 * math.pi * i / pts
        r = R * (1 + amp * math.cos(n * t + rot))
        out.append("%.1f,%.1f" % (cx + r * math.cos(t), cy + r * math.sin(t)))
    return "M" + " L".join(out) + "Z"

def blob(cx, cy, R, seed=0.0, pts=260):
    out = []
    for i in range(pts):
        t = 2 * math.pi * i / pts
        r = R * (1 + 0.09 * math.sin(2 * t + seed) + 0.06 * math.sin(3 * t + 2 * seed) + 0.04 * math.sin(5 * t + 1))
        out.append("%.1f,%.1f" % (cx + r * math.cos(t), cy + r * math.sin(t)))
    return "M" + " L".join(out) + "Z"

def svg(w, h, body, title=""):
    t = f"<title>{esc(title)}</title>" if title else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">{t}{body}</svg>'

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

def chip(x, y, label, fill, fg, size=19, h=40, bold=600):
    w = tw(label, size) + 36
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h//2}" fill="{fill}"/>'
            f'<text x="{x + w/2}" y="{y + h/2 + size*0.35}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="{bold}" fill="{fg}">{esc(label)}</text>'), w

# ───────── banner ─────────
def banner(c):
    W, H = 1200, 440
    b = f'<defs><clipPath id="r"><rect width="{W}" height="{H}" rx="56"/></clipPath></defs><g clip-path="url(#r)">'
    b += f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>'
    b += f'<path d="{shape(1090, 40, 270, 9, 0.06, 0.3)}" fill="{c["pc"]}" opacity=".85"/>'
    b += f'<path d="{blob(60, 450, 190, 1.2)}" fill="{c["ter"]}" opacity=".9"/>'
    b += f'<path d="{shape(640, 78, 34, 12, 0.10)}" fill="{c["prim"]}"/>'
    b += f'<path d="{shape(40, 60, 22, 4, 0.18, 0.4)}" fill="{c["sec"]}"/>'
    b += (f'<text x="60" y="226" font-family="{FONT}" font-size="176" font-weight="800" letter-spacing="-6" fill="{c["text"]}">yu'
          f'<tspan fill="{c["prim"]}">ki</tspan></text>')
    b += f'<text x="64" y="304" font-family="{FONT}" font-size="36" font-weight="700" fill="{c["text"]}">Менеджер пакетов для Yukino</text>'
    b += f'<text x="64" y="344" font-family="{FONT}" font-size="25" fill="{c["textv"]}">без своих серверов · с подписями · с откатом</text>'
    x = 64
    for label in ("Yukino", "Ed25519", "BLAKE3", "pacman-style"):
        s, w = chip(x, 372, label, c["sec"], c["onsec"], 19)
        b += s; x += w + 10
    # терминал
    tx, ty, tw_, th = 700, 70, 440, 300
    b += (f'<path d="M{tx+44},{ty} H{tx+tw_-44} Q{tx+tw_},{ty} {tx+tw_},{ty+44} V{ty+th-44} Q{tx+tw_},{ty+th} {tx+tw_-44},{ty+th} '
          f'H{tx+14} Q{tx},{ty+th} {tx},{ty+th-14} V{ty+44} Q{tx},{ty} {tx+44},{ty} Z" fill="#1e1e2e" stroke="#313244" stroke-width="2"/>')
    for i, col in enumerate(("#45475a", "#45475a", "#45475a")):
        b += f'<circle cx="{tx+30+i*20}" cy="{ty+28}" r="6" fill="{col}"/>'
    lines = [
        [("$ ", "#6c7086"), ("sudo yuki install ripgrep", "#cdd6f4")],
        [("[1/5] ", "#6c7086"), ("verifying as root", "#cdd6f4")],
        [("  ", ""), ("ok ", "#a6e3a1"), ("ripgrep ", "#cdd6f4"), ("14.1.0", "#a6e3a1")],
        [("  ", ""), ("!! ", "#f9e2af"), ("pcre2 ", "#cdd6f4"), ("build from source", "#f9e2af")],
        [("[4/5] ", "#6c7086"), ("re-verifying files", "#cdd6f4")],
        [("[5/5] ", "#6c7086"), ("applying transaction", "#cdd6f4")],
        [("  ", ""), ("ok ", "#a6e3a1"), ("done in 12.4s", "#cdd6f4")],
    ]
    for i, parts in enumerate(lines):
        y = ty + 70 + i * 32
        spans = "".join(f'<tspan fill="{col or "#cdd6f4"}">{esc(t).replace(" ", "&#160;")}</tspan>' for t, col in parts)
        b += f'<text x="{tx+28}" y="{y}" font-family="{MONO}" font-size="17" xml:space="preserve">{spans}</text>'
    b += "</g>"
    return svg(W, H, b, "yuki: package manager for Yukino")

# ───────── кнопки ─────────
def button(label, kind, c, w=None, size=21):
    h = 60
    w = w or tw(label, size, 0.58) + 96
    if kind == "filled":
        bg, fg, stroke = c["prim"], c["onprim"], "none"
    elif kind == "tonal":
        bg, fg, stroke = c["sec"], c["onsec"], "none"
    else:
        bg, fg, stroke = "none", c["prim"], c["outline"]
    body = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="30" fill="{bg}" stroke="{stroke}" stroke-width="{2 if stroke!="none" else 0}"/>'
    # маленькая выразительная фигура слева
    shape_fill = fg if kind != "outlined" else c["pc"]
    body += f'<path d="{shape(34, 30, 11, 8, 0.12)}" fill="{shape_fill}" opacity="{0.95 if kind!="outlined" else 1}"/>'
    body += f'<text x="{w/2 + 14}" y="{h/2 + size*0.35}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="700" fill="{fg}">{esc(label)}</text>'
    return svg(w, h, body, label)

# ───────── плитки с цифрами ─────────
def stat(num, label, c, tone):
    W, H = 280, 170
    fills = {"a": (c["pc"], c["onpc"]), "b": (c["ter"], c["onter"]), "c": (c["sec"], c["onsec"]), "d": (c["card"], c["text"])}
    bg, fg = fills[tone]
    b = f'<defs><clipPath id="s"><rect width="{W}" height="{H}" rx="44"/></clipPath></defs><g clip-path="url(#s)"><rect width="{W}" height="{H}" fill="{bg}"/>'
    shapes = {"a": shape(240, 20, 70, 9, 0.08), "b": blob(250, 150, 80, 0.7), "c": shape(236, 150, 74, 6, 0.12), "d": blob(244, 28, 72, 2.0)}
    b += f'<path d="{shapes[tone]}" fill="{fg}" opacity=".13"/>'
    b += f'<text x="26" y="98" font-family="{FONT}" font-size="76" font-weight="800" letter-spacing="-2" fill="{fg}">{esc(num)}</text>'
    b += f'<text x="28" y="140" font-family="{FONT}" font-size="21" font-weight="600" fill="{fg}" opacity=".85">{esc(label)}</text></g>'
    return svg(W, H, b, f"{num} {label}")

# ───────── иконки ─────────
def glyph(kind, cx, cy, col):
    s = f'stroke="{col}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    if kind == "sign":
        return f'<path d="M{cx-13},{cy+1} L{cx-4},{cy+10} L{cx+14},{cy-11}" {s}/>'
    if kind == "priv":
        return (f'<rect x="{cx-14}" y="{cy-15}" width="28" height="11" rx="4" {s}/>'
                f'<rect x="{cx-14}" y="{cy+3}" width="28" height="11" rx="4" fill="{col}" stroke="none"/>')
    if kind == "undo":
        return (f'<path d="M{cx+12},{cy+8} A14,14 0 1 0 {cx-12},{cy-2}" {s}/>'
                f'<path d="M{cx-17},{cy-14} L{cx-10},{cy-2} L{cx-22},{cy+2}" {s}/>')
    if kind == "build":
        return (f'<path d="{shape(cx, cy, 14, 8, 0.2)}" fill="{col}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="5" fill="none" stroke="none"/>')
    if kind == "graph":
        return (f'<path d="M{cx-12},{cy+10} L{cx},{cy-11} L{cx+12},{cy+10}" {s}/>'
                f'<circle cx="{cx-12}" cy="{cy+10}" r="6" fill="{col}"/><circle cx="{cx+12}" cy="{cy+10}" r="6" fill="{col}"/><circle cx="{cx}" cy="{cy-11}" r="6" fill="{col}"/>')
    if kind == "palette":
        return (f'<circle cx="{cx-9}" cy="{cy+4}" r="9" fill="{col}" opacity=".9"/><circle cx="{cx+9}" cy="{cy+4}" r="9" fill="{col}" opacity=".6"/>'
                f'<circle cx="{cx}" cy="{cy-9}" r="9" fill="{col}" opacity=".8"/>')
    if kind == "arrow":
        return f'<path d="M{cx-9},{cy-12} L{cx+11},{cy} L{cx-9},{cy+12} Z" fill="{col}"/>'
    if kind == "grid":
        return "".join(f'<rect x="{cx-14+dx*16}" y="{cy-14+dy*16}" width="12" height="12" rx="4" fill="{col}"/>' for dx in (0, 1) for dy in (0, 1))
    if kind == "q":
        return f'<text x="{cx}" y="{cy+11}" text-anchor="middle" font-family="{FONT}" font-size="32" font-weight="800" fill="{col}">?</text>'
    return ""

def icon_shape(kind, size, shape_fill, glyph_col, n=9, amp=0.07, rot=0.0):
    c = size / 2
    return svg(size, size, f'<path d="{shape(c, c, size*0.4, n, amp, rot)}" fill="{shape_fill}"/>{glyph(kind, c, c, glyph_col)}'.replace("cx=", "cx="), kind)

# ───────── карточки ─────────
def card(title, lines, icon, c, tone):
    W, H = 388, 232
    fills = {"a": (c["pc"], c["onpc"], c["prim"], c["onprim"]), "b": (c["ter"], c["onter"], c["onter"], c["ter"]),
             "c": (c["card"], c["text"], c["prim"], c["onprim"]), "d": (c["sec"], c["onsec"], c["onsec"], c["sec"])}
    bg, fg, ic_bg, ic_fg = fills[tone]
    b = f'<defs><clipPath id="k"><rect width="{W}" height="{H}" rx="40"/></clipPath></defs><g clip-path="url(#k)"><rect width="{W}" height="{H}" fill="{bg}"/>'
    b += f'<path d="{blob(W-20, H+10, 90, 0.9)}" fill="{fg}" opacity=".07"/></g>'
    b += f'<path d="{shape(64, 62, 36, 9, 0.07)}" fill="{ic_bg}"/>' + glyph(icon, 64, 62, ic_fg)
    b += f'<text x="30" y="132" font-family="{FONT}" font-size="25" font-weight="800" fill="{fg}">{esc(title)}</text>'
    for i, ln in enumerate(lines):
        b += f'<text x="30" y="{164 + i*26}" font-family="{FONT}" font-size="18" fill="{fg}" opacity=".88">{esc(ln)}</text>'
    return svg(W, H, b, title)

# ───────── прочее ─────────
def divider(c):
    W, H = 1200, 28
    d = ""
    x = 0
    while x < W:
        d += f'<circle cx="{x+14}" cy="14" r="9" fill="{c["pc"]}"/>'
        x += 32
    return svg(W, H, d, "divider")

def status_chip(c):
    label = "статус: ещё не собирался: начните с yuki selftest"
    w = tw(label, 18, 0.54) + 60
    b = f'<rect width="{w}" height="44" rx="22" fill="{c["warn"]}"/><path d="{shape(26, 22, 8, 8, 0.15)}" fill="{c["onwarn"]}"/>'
    b += f'<text x="{w/2 + 10}" y="29" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="600" fill="{c["onwarn"]}">{esc(label)}</text>'
    return svg(w, 44, b, label)

def palette():
    sw = [("accent", "#89b4fa"), ("good", "#a6e3a1"), ("warn", "#f9e2af"), ("bad", "#f38ba8"), ("logo", "#cba6f7"), ("speed", "#94e2d5")]
    W, H = 1100, 150
    b = ""
    for i, (n, col) in enumerate(sw):
        cx = 90 + i * 184
        b += f'<path d="{shape(cx, 62, 52, [9, 6, 8, 12, 5, 10][i], 0.08, i)}" fill="{col}"/>'
        b += f'<text x="{cx}" y="140" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#888">{n}</text>'
    return svg(W, H, b, "theme colors")

def num_badge(n):
    shapes = {1: (9, .07), 2: (6, .10), 3: (12, .08), 4: (8, .09), 5: (10, .08)}
    k, a = shapes[n]
    b = f'<path d="{shape(40, 40, 32, k, a, n)}" fill="#6b4fd8"/>'
    b += f'<text x="40" y="52" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="800" fill="#ffffff">{n}</text>'
    return svg(80, 80, b, f"step {n}")

def who(label, bg):
    w = tw(label, 18, 0.6) + 34
    return svg(w, 34, f'<rect width="{w}" height="34" rx="17" fill="{bg}"/><text x="{w/2}" y="23" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="700" fill="#fff">{label}</text>', label)

def section_icon(kind, n=9, amp=.07):
    return icon_shape(kind, 48, "#6b4fd8", "#ffffff", n, amp)

# ───────── числа из реального кода ─────────
src = os.path.join(os.path.dirname(OUT), "yuki", "src")
def count_cmds():
    try:
        t = open(os.path.join(src, "cmdlist.ykn"), encoding="utf-8").read()
        m = re.search(r'fun all_commands\(\) -> string\[\] \{\s*return \[(.*?)\]', t, re.S)
        return len(re.findall(r'"[^"]+"', m.group(1)))
    except Exception:
        return 44
def count_codes():
    try:
        t = open(os.path.join(src, "explain.ykn"), encoding="utf-8").read()
        return len(set(re.findall(r'code == (\d+)', t)))
    except Exception:
        return 60
NCMD, NERR = count_cmds(), count_codes()

for name, c in THEMES.items():
    write(f"banner-{name}.svg", banner(c))
    write(f"btn-start-{name}.svg", button("Быстрый старт", "filled", c, 290))
    write(f"btn-tutorial-{name}.svg", button("Свой индекс: туториал", "tonal", c, 360))
    write(f"btn-security-{name}.svg", button("Модель защиты", "outlined", c, 290))
    write(f"btn-commands-{name}.svg", button("Все команды", "outlined", c, 250))
    write(f"stat-cmds-{name}.svg", stat(str(NCMD), "команд", c, "a"))
    write(f"stat-errors-{name}.svg", stat(str(NERR), "ошибок с разбором", c, "b"))
    write(f"stat-servers-{name}.svg", stat("0", "своих серверов", c, "c"))
    write(f"stat-modes-{name}.svg", stat("3", "режима терминала", c, "d"))
    write(f"card-signed-{name}.svg", card("Подписанный индекс", ["Ed25519 + BLAKE3, роли ключей,", "порог издателей, защита от отката"], "sign", c, "a"))
    write(f"card-priv-{name}.svg", card("Без root до конца", ["сеть и сборка от nobody, root", "проверяет всё заново"], "priv", c, "c"))
    write(f"card-fast-{name}.svg", card("Параллельные загрузки", ["до 16 потоков, хеш прямо в воркере,", "панель не замирает"], "grid", c, "b"))
    write(f"card-tx-{name}.svg", card("Транзакции и откат", ["журнал на диск, автооткат после", "сбоя, один upgrade = одна транзакция"], "undo", c, "d"))
    write(f"card-build-{name}.svg", card("Нет бинарника? Соберём", ["песочница, без сети, результат", "сверяется с подписанным хешем"], "build", c, "a"))
    write(f"card-graph-{name}.svg", card("Связи пакетов", ["why, tree, rdeps, related, graph,", "orphans и autoremove"], "graph", c, "c"))
    write(f"divider-{name}.svg", divider(c))
    write(f"status-{name}.svg", status_chip(c))

write("palette.svg", palette())
for i in range(1, 6): write(f"num-{i}.svg", num_badge(i))
write("who-nobody.svg", who("nobody", "#625b71"))
write("who-root.svg", who("root", "#b3261e"))
for kind, n, a in [("arrow", 9, .07), ("priv", 6, .10), ("grid", 12, .08), ("sign", 8, .09), ("palette", 10, .08), ("q", 5, .12), ("graph", 9, .07), ("undo", 6, .1)]:
    write(f"sec-{kind}.svg", section_icon(kind, n, a))
print("assets:", len(os.listdir(OUT)), "cmds", NCMD, "errors", NERR)
