"""Renders the 1920x1080 newsletter cover images (LLM and Quantum) into 99. Image/<name>/<name>-curated-cover.png.

Needs Chromium (path in CHROME below, or set CHROME_BIN), Pillow and the Inter font.
Edit COVERS at the bottom to change titles, taglines, chips and colors, then run: python3 "99. Image/make_covers.py"
"""
import random, math, subprocess, sys, os, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = os.environ.get("CHROME_BIN", "/opt/pw-browsers/chromium")

def llm_motif():
    rnd = random.Random(7)
    pts = []
    while len(pts) < 70:
        x, y = rnd.uniform(0, 1920), rnd.uniform(0, 1080)
        if all((x-a)**2 + (y-b)**2 > 130**2 for a, b in pts):
            pts.append((x, y))
    edges = []
    for i, (x, y) in enumerate(pts):
        near = sorted(range(len(pts)), key=lambda j: (pts[j][0]-x)**2 + (pts[j][1]-y)**2)[1:3]
        for j in near:
            if (j, i) not in edges: edges.append((i, j))
    lines = "".join(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[j][0]:.0f}" y2="{pts[j][1]:.0f}" stroke="#6f86ff" stroke-opacity=".16" stroke-width="2"/>' for i, j in edges)
    dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([4,5,6])}" fill="#8fa2ff" fill-opacity=".35"/>' for x, y in pts)
    # one highlighted "story thread" through three papers
    thread = [(150, 905), (560, 960), (1010, 930), (1480, 985), (1790, 900)]
    path = " ".join(f"{x},{y}" for x, y in thread)
    glow = f'<polyline points="{path}" fill="none" stroke="#5ee0ff" stroke-width="5" stroke-linejoin="round" stroke-opacity=".9" filter="url(#glow)"/>'
    tdots = "".join(f'<circle cx="{x}" cy="{y}" r="13" fill="#0a1128" stroke="#5ee0ff" stroke-width="4" filter="url(#glow)"/><circle cx="{x}" cy="{y}" r="5" fill="#fff"/>' for x, y in thread)
    return lines + dots + glow + tdots

def quantum_motif():
    rnd = random.Random(11)
    cx, cy = 960, 540
    rings = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#b69cff" stroke-opacity="{op}" stroke-width="2" transform="rotate({rot} {cx} {cy})"/>'
        for rx, ry, rot, op in [(900, 250, -18, .22), (820, 220, 24, .20), (980, 330, 60, .14), (700, 170, -52, .20)])
    # qubit lattice along the bottom: a row of nodes with a highlighted error-check path
    lattice = ""
    cols, rows, x0, y0, dx, dy = 15, 3, 160, 880, 112, 62
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c*dx, y0 + r*dy
            lattice += f'<circle cx="{x}" cy="{y}" r="5" fill="#b69cff" fill-opacity=".35"/>'
            if c < cols-1: lattice += f'<line x1="{x}" y1="{y}" x2="{x+dx}" y2="{y}" stroke="#b69cff" stroke-opacity=".12" stroke-width="2"/>'
            if r < rows-1: lattice += f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+dy}" stroke="#b69cff" stroke-opacity=".12" stroke-width="2"/>'
    hot = [(0,0),(1,0),(2,1),(3,1),(4,1),(5,2),(6,2),(7,1),(8,1),(9,0),(10,0),(11,1),(12,1),(13,2),(14,2)]
    pts = " ".join(f"{x0+c*dx},{y0+r*dy}" for c, r in hot)
    path = f'<polyline points="{pts}" fill="none" stroke="#3ff0c8" stroke-width="4" stroke-opacity=".85" stroke-linejoin="round" filter="url(#glow)"/>'
    hotd = "".join(f'<circle cx="{x0+c*dx}" cy="{y0+r*dy}" r="9" fill="#0b0820" stroke="#3ff0c8" stroke-width="3.5" filter="url(#glow)"/>' for c, r in hot[::3])
    stars = "".join(f'<circle cx="{rnd.uniform(0,1920):.0f}" cy="{rnd.uniform(0,820):.0f}" r="{rnd.choice([1.5,2,2.5])}" fill="#fff" fill-opacity="{rnd.choice([.2,.35,.5])}"/>' for _ in range(90))
    return stars + rings + lattice + path + hotd

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1920px;height:1080px;overflow:hidden;font-family:'Inter',sans-serif}}
body{{background:{bg};position:relative;color:#fff}}
svg.bg{{position:absolute;inset:0}}
.veil{{position:absolute;inset:0;background:radial-gradient(ellipse 62% 44% at 50% 45%, {veil} 0%, rgba(0,0,0,0) 100%)}}
.wrap{{position:absolute;left:0;right:0;top:250px;text-align:center}}
.kicker{{font-size:30px;font-weight:600;letter-spacing:.34em;text-transform:uppercase;color:{accent};margin-bottom:34px}}
h1{{font-size:{h1}px;font-weight:800;letter-spacing:-.025em;line-height:1.02}}
.sub{{margin-top:38px;font-size:48px;font-weight:500;color:rgba(255,255,255,.88);letter-spacing:-.005em}}
.chips{{margin-top:56px;display:flex;gap:22px;justify-content:center}}
.chip{{font-size:25px;font-weight:700;letter-spacing:.2em;padding:15px 30px;border-radius:999px;border:2px solid {chip};color:#fff;background:rgba(255,255,255,.05)}}
</style></head><body>
<svg class="bg" width="1920" height="1080" viewBox="0 0 1920 1080"><defs><filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>{motif}</svg>
<div class="veil"></div>
<div class="wrap"><div class="kicker">{kicker}</div><h1>{title}</h1><div class="sub">{sub}</div>
<div class="chips">{chips}</div></div>
</body></html>"""

COVERS = {
 "llm": dict(bg="radial-gradient(ellipse at 30% 20%, #16245a 0%, #0a1030 55%, #060918 100%)", veil="rgba(6,9,24,.92)",
             accent="#5ee0ff", chip="rgba(94,224,255,.7)", h1=148, kicker="Weekly · arXiv research", title="LLM Research Weekly",
             sub="One story. The papers behind it. An honest take.", chips=["THE STORY","THE PAPERS","EDITOR&rsquo;S TAKE"], motif=llm_motif()),
 "quantum": dict(bg="radial-gradient(ellipse at 70% 15%, #2a1670 0%, #120b3a 50%, #070617 100%)", veil="rgba(7,6,23,.92)",
             accent="#3ff0c8", chip="rgba(63,240,200,.7)", h1=112, kicker="Weekly · arXiv research", title="Quantum Computing Weekly",
             sub="What changed. Is it real. What to watch.", chips=["WHAT CHANGED","THE PAPERS","EDITOR&rsquo;S TAKE"], motif=quantum_motif()),
}
for name, c in COVERS.items():
    c = dict(c); c["chips"] = "".join(f'<span class="chip">{t}</span>' for t in c["chips"])
    html = os.path.join(tempfile.gettempdir(), f"cover_{name}.html"); open(html, "w", encoding="utf-8").write(PAGE.format(**c))
    png = os.path.join(HERE, name, f"{name}-curated-cover.png")
    os.makedirs(os.path.dirname(png), exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1920,1167", f"--screenshot={png}", f"file://{html}"],
                   check=True, capture_output=True)
    from PIL import Image
    im = Image.open(png).convert("RGB")
    im.crop((0, 0, 1920, 1080)).save(png, optimize=True)   # headless window includes ~87px of browser chrome
    print("wrote", png)
