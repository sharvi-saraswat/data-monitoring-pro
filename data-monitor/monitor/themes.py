"""MEMBER 3 - Colour themes and the CSS that styles the whole app."""

THEMES = {
    "Ocean":   dict(icon="🔵", a1="#6366f1", a2="#06b6d4", bg1="#1e1b4b", bg2="#083344", base="#0b1020", side="#0f1530"),
    "Emerald": dict(icon="🟢", a1="#10b981", a2="#a3e635", bg1="#052e16", bg2="#064e3b", base="#07130e", side="#0a1f16"),
    "Sunset":  dict(icon="🟠", a1="#f97316", a2="#ec4899", bg1="#431407", bg2="#500724", base="#120a0a", side="#1c1010"),
    "Violet":  dict(icon="🟣", a1="#8b5cf6", a2="#ec4899", bg1="#2e1065", bg2="#4a044e", base="#0e0a1a", side="#150f26"),
    "Gold":    dict(icon="🟡", a1="#eab308", a2="#f97316", bg1="#422006", bg2="#451a03", base="#0f0c06", side="#1a1409"),
    "Slate":   dict(icon="⚪", a1="#38bdf8", a2="#94a3b8", bg1="#0f172a", bg2="#1e293b", base="#020617", side="#0b1220"),
}

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, .stApp, [class*="css"] {font-family: 'Inter', sans-serif;}
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}
.stApp {
    background: radial-gradient(1200px 600px at 8% -10%, __BG1__ 0%, transparent 60%),
                radial-gradient(1000px 520px at 100% 0%, __BG2__ 0%, transparent 55%),
                __BASE__;
}
.block-container {padding-top: 2rem; max-width: 1300px;}

/* ---------- hero ---------- */
.hero {
    background: linear-gradient(120deg, __A1__ 0%, __A2__ 100%);
    border-radius: 22px; padding: 28px 34px; margin-bottom: 22px;
    box-shadow: 0 12px 44px rgba(__A1_RGB__, .38);
}
.hero h1 {margin: 0; font-size: 2rem; color: #fff;}
.hero p {margin: 6px 0 0; color: rgba(255,255,255,.9); font-size: 1rem;}

/* ---------- KPI cards ---------- */
.kpi {
    background: rgba(255,255,255,.045); border: 1px solid rgba(255,255,255,.08);
    border-left: 4px solid var(--c); border-radius: 16px; padding: 16px 18px;
    backdrop-filter: blur(6px); transition: transform .15s ease, box-shadow .15s ease;
}
.kpi:hover {transform: translateY(-3px); box-shadow: 0 10px 28px rgba(0,0,0,.35);}
.kpi-l {font-size: .75rem; text-transform: uppercase; letter-spacing: .09em; color: #94a3b8;}
.kpi-v {font-size: 2rem; font-weight: 700; color: #fff; line-height: 1.25;}
.kpi-s {font-size: .8rem; color: var(--c);}
.sec {font-size: 1.1rem; font-weight: 600; margin: 10px 0 4px; color: #e2e8f0;}

/* ---------- chart panels ---------- */
div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.07);
    border-radius: 16px; padding: 6px;
}

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {background: rgba(255,255,255,.045); border-radius: 10px; padding: 8px 18px;}
.stTabs [aria-selected="true"] {background: rgba(__A1_RGB__, .30) !important;}

/* ---------- buttons ---------- */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    border-radius: 12px; font-weight: 600; border: 1px solid rgba(255,255,255,.16);
}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(120deg, __A1__, __A2__); border: none; color: #fff;
}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {
    filter: brightness(1.1); box-shadow: 0 6px 22px rgba(__A1_RGB__, .5);
}

/* ---------- inputs ---------- */
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.06); border-radius: 12px;
}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {background: __SIDE__; border-right: 1px solid rgba(255,255,255,.07);}
section[data-testid="stSidebar"] div[data-testid="stForm"] {
    padding: 12px; border-radius: 14px; box-shadow: none;
}
.brand {font-size: 1.3rem; font-weight: 700; color: #fff;}
.user-chip {
    background: rgba(__A1_RGB__, .2); border-radius: 12px; padding: 8px 12px;
    color: #fff; font-size: .9rem; margin: 6px 0 10px;
}

/* ---------- login ---------- */
.logo {
    width: 64px; height: 64px; border-radius: 18px; display: flex; align-items: center;
    justify-content: center; font-size: 2rem;
    background: linear-gradient(135deg, __A1__, __A2__); box-shadow: 0 10px 30px rgba(__A1_RGB__, .45);
}
.login-hero h1 {font-size: 2.7rem; line-height: 1.15; color: #fff; margin: 18px 0 10px;}
.login-hero .grad {
    background: linear-gradient(120deg, __A1__, __A2__, __A1__); background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 5s linear infinite;
}
@keyframes shine {to {background-position: 200% center;}}
.login-hero p {color: #94a3b8; font-size: 1.05rem; margin-bottom: 18px;}
.feat {display: flex; gap: 12px; align-items: center; margin: 12px 0; color: #e2e8f0;}
.feat .ic {background: rgba(__A1_RGB__, .22); border-radius: 10px; padding: 7px 10px;}
div[data-testid="stForm"] {
    background: rgba(255,255,255,.055); border: 1px solid rgba(255,255,255,.11);
    border-radius: 22px; padding: 26px; backdrop-filter: blur(10px);
    box-shadow: 0 20px 60px rgba(0,0,0,.45);
}
.login-title {font-size: 1.5rem; font-weight: 700; color: #fff; margin-bottom: 2px;}
.login-sub {color: #94a3b8; margin-bottom: 6px;}
</style>
"""


def _rgb(hex_color):
    h = hex_color.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def build_css(name):
    t = THEMES[name]
    css = _CSS.replace("__A1_RGB__", _rgb(t["a1"]))
    for key in ("a1", "a2", "bg1", "bg2", "base", "side"):
        css = css.replace(f"__{key.upper()}__", t[key])
    return css
