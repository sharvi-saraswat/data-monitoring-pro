"""MEMBER 3 - Data Monitoring Tool: sign-up / login + themed Streamlit dashboard."""
import time
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from monitor import alerts, auth, checks, ingest, sample, storage
from monitor.themes import THEMES, build_css

BASE = Path(__file__).resolve().parent
st.set_page_config(page_title="Data Monitoring Tool", page_icon="📊", layout="wide")

ss = st.session_state
ss.setdefault("theme_name", "Ocean")
if ss["theme_name"] not in THEMES:
    ss["theme_name"] = "Ocean"
A1, A2 = THEMES[ss["theme_name"]]["a1"], THEMES[ss["theme_name"]]["a2"]
GREEN, AMBER, RED = "#22c55e", "#f59e0b", "#ef4444"
STATUS_COLOR = {"PASS": GREEN, "WARN": AMBER, "FAIL": RED}
BADGE = {"PASS": "🟢 PASS", "WARN": "🟡 WARN", "FAIL": "🔴 FAIL"}

st.markdown(build_css(ss["theme_name"]), unsafe_allow_html=True)


def theme_label(name):
    return f"{THEMES[name]['icon']} {name}"


# ============================ LOGIN / SIGN-UP ============================
def _login_theme_changed():
    ss["theme_name"] = ss["theme_login"]


def _start_session(username, guest=False):
    ss["auth"], ss["user"], ss["guest"] = True, username, guest
    saved = None if guest else auth.get_theme(username)
    if saved in THEMES:
        ss["theme_name"] = saved
    ss.pop("last", None)
    st.rerun()


def login_page():
    st.markdown("""<style>
    section[data-testid="stSidebar"], div[data-testid="collapsedControl"] {display: none;}
    </style>""", unsafe_allow_html=True)
    left, right = st.columns([1.2, 1], gap="large")

    with left:
        st.write("")
        st.markdown("""
        <div class="login-hero">
          <div class="logo">📊</div>
          <h1>Keep your data <span class="grad">healthy</span>, automatically.</h1>
          <p>Catch quality problems, schema changes and drift before they reach your reports.</p>
          <div class="feat"><span class="ic">🧹</span> Missing values, duplicates &amp; outliers</div>
          <div class="feat"><span class="ic">📉</span> Distribution drift detection (PSI)</div>
          <div class="feat"><span class="ic">⏱️</span> Freshness &amp; schema monitoring</div>
          <div class="feat"><span class="ic">🔔</span> Quality score, run history &amp; alerts</div>
        </div>""", unsafe_allow_html=True)

    with right:
        st.radio("🎨 Colour theme", list(THEMES), horizontal=True, key="theme_login",
                 index=list(THEMES).index(ss["theme_name"]), format_func=theme_label,
                 on_change=_login_theme_changed)
        tab_in, tab_up = st.tabs(["🔑 Sign in", "✨ Create account"])

        with tab_in:
            with st.form("signin"):
                st.markdown('<div class="login-title">Welcome back 👋</div>'
                            '<div class="login-sub">Sign in to open your dashboard</div>',
                            unsafe_allow_html=True)
                u = st.text_input("Username", key="si_user")
                p = st.text_input("Password", type="password", key="si_pass")
                go_in = st.form_submit_button("Sign in →", type="primary",
                                              use_container_width=True)
            if go_in:
                wait = ss.get("lock_until", 0) - time.time()
                if wait > 0:
                    st.error(f"Too many attempts. Try again in {int(wait) + 1} s.")
                else:
                    who = auth.verify_user(u, p)
                    if who:
                        ss["fails"] = 0
                        _start_session(who)
                    else:
                        ss["fails"] = ss.get("fails", 0) + 1
                        if ss["fails"] >= 5:
                            ss["lock_until"], ss["fails"] = time.time() + 30, 0
                        st.error("Incorrect username or password.")
            st.caption("New here? Open the **Create account** tab and set your own password.")
            if st.button("👀 Continue as guest (demo)", use_container_width=True):
                _start_session("guest", guest=True)

        with tab_up:
            with st.form("signup"):
                st.markdown('<div class="login-title">Create your account ✨</div>'
                            '<div class="login-sub">Choose a username and set your own password</div>',
                            unsafe_allow_html=True)
                nu = st.text_input("Username", key="su_user", placeholder="3-20 letters / numbers")
                n1 = st.text_input("Password", type="password", key="su_p1")
                n2 = st.text_input("Confirm password", type="password", key="su_p2")
                st.caption("Password: at least 8 characters, with a letter and a number.")
                go_up = st.form_submit_button("Create account", type="primary",
                                              use_container_width=True)
            if go_up:
                if n1 != n2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = auth.create_user(nu, n1)
                    if ok:
                        _start_session(msg)
                    else:
                        st.error(msg)


if not ss.get("auth"):
    login_page()
    st.stop()


# ============================ HELPERS ============================
def style_fig(fig, h=330):
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", height=h, colorway=[A1, A2, AMBER, GREEN],
                      margin=dict(l=20, r=20, t=50, b=20), font=dict(color="#e2e8f0"))
    return fig


def kpi(label, value, sub, color):
    return (f'<div class="kpi" style="--c:{color}"><div class="kpi-l">{label}</div>'
            f'<div class="kpi-v">{value}</div><div class="kpi-s">{sub}</div></div>')


def score_color(s):
    return GREEN if s >= 80 else AMBER if s >= 50 else RED


def store_result(source, data, res, cfg):
    score = checks.quality_score(res)
    storage.save_run(source, data, res, score)
    ss["last"] = dict(res=res, score=score, name=source, df=data, cfg=cfg,
                      alerted=alerts.send_alerts(source, res, score))


def run_demo():
    clean, dirty = sample.make_sample(False), sample.make_sample(True)
    storage.save_baseline(checks.build_baseline(clean))
    cfg = {"timestamp_column": "order_date"}
    store_result("demo: sample (with issues)", dirty,
                 checks.run_all_checks(dirty, storage.load_baseline(), cfg),
                 {**checks.DEFAULT_CONFIG, **cfg})


def _sb_theme_changed():
    ss["theme_name"] = ss["theme_sb"]
    if not ss.get("guest"):
        auth.set_theme(ss["user"], ss["theme_name"])


# ============================ SIDEBAR ============================
with st.sidebar:
    st.markdown('<div class="brand">📊 DataMonitor</div>', unsafe_allow_html=True)
    badge = "👤 Guest (demo)" if ss.get("guest") else f"👤 {ss['user']}"
    st.markdown(f'<div class="user-chip">{badge}</div>', unsafe_allow_html=True)
    if st.button("Log out", use_container_width=True):
        for k in ("auth", "user", "guest", "last"):
            ss.pop(k, None)
        st.rerun()

    st.selectbox("🎨 Colour theme", list(THEMES), key="theme_sb",
                 index=list(THEMES).index(ss["theme_name"]), format_func=theme_label,
                 on_change=_sb_theme_changed)

    if not ss.get("guest"):
        with st.expander("🔐 Change password"):
            with st.form("chgpw", clear_on_submit=True):
                old = st.text_input("Current password", type="password")
                new = st.text_input("New password", type="password")
                new2 = st.text_input("Confirm new password", type="password")
                go_pw = st.form_submit_button("Update password", use_container_width=True)
            if go_pw:
                if new != new2:
                    st.error("New passwords do not match.")
                else:
                    ok, msg = auth.change_password(ss["user"], old, new)
                    (st.success if ok else st.error)(msg)
    st.divider()

    st.subheader("1 · Data source")
    src = st.radio("Source", ["Upload file", "Sample (clean)", "Sample (with issues)",
                              "File path"], label_visibility="collapsed")
    df, name = None, None
    if src == "Upload file":
        up = st.file_uploader("CSV / Excel / JSON", type=["csv", "xlsx", "xls", "json"])
        if up:
            df, name = ingest.load_file(up, up.name), up.name
    elif src.startswith("Sample"):
        dirty_flag = "issues" in src
        df, name = sample.make_sample(dirty_flag), f"sample ({'with issues' if dirty_flag else 'clean'})"
    else:
        path = st.text_input("File path", str(BASE / "data" / "sample_dirty.csv"))
        try:
            df, name = ingest.load_file(path, path), path
        except Exception as e:
            st.warning(str(e))

    st.subheader("2 · Thresholds")
    with st.expander("Adjust limits"):
        cfg = {
            "missing_warn": st.slider("Missing WARN %", 0, 50, 5) / 100,
            "missing_fail": st.slider("Missing FAIL %", 0, 100, 20) / 100,
            "psi_warn": st.slider("Drift PSI WARN", 0.0, 1.0, 0.10),
            "psi_fail": st.slider("Drift PSI FAIL", 0.0, 1.0, 0.25),
            "freshness_hours": st.number_input("Freshness limit (hours)", 1, 720, 24),
        }
    if df is not None:
        options = ["(none)"] + list(df.columns)
        guess = next((i + 1 for i, c in enumerate(df.columns)
                      if "date" in c.lower() or "time" in c.lower()), 0)
        ts = st.selectbox("Timestamp column", options, index=guess)
        cfg["timestamp_column"] = None if ts == "(none)" else ts

# ============================ MAIN ============================
hello = "Guest" if ss.get("guest") else ss["user"]
st.markdown(f'<div class="hero"><h1>📊 Data Monitoring Tool</h1>'
            f'<p>Welcome, {hello}. Track data quality, schema changes and drift in one place.</p></div>',
            unsafe_allow_html=True)

tab_run, tab_prof, tab_hist, tab_help = st.tabs(
    ["🔍 Monitor", "🧬 Data profile", "📈 History", "ℹ️ Help"])

# ---------------------------- Monitor ----------------------------
with tab_run:
    b1, b2, b3, b4 = st.columns([1.2, 1, 1, 1.6])
    if b1.button("⚡ One-click demo", use_container_width=True):
        run_demo()
    if b2.button("📌 Set baseline", use_container_width=True, disabled=df is None):
        storage.save_baseline(checks.build_baseline(df))
        st.toast("Baseline saved (schema + distributions)", icon="✅")
    run = b3.button("▶ Run monitoring", type="primary", use_container_width=True,
                    disabled=df is None)
    auto = b4.checkbox("Auto re-run every 30 s (best with File path)")

    tick = ss.pop("_tick", False)
    if df is not None and (run or tick):
        store_result(name, df, checks.run_all_checks(df, storage.load_baseline(), cfg), cfg)

    last = ss.get("last")
    if not last:
        st.info("👆 Press **⚡ One-click demo** to see the tool in action, or pick a data source "
                "in the sidebar → **Set baseline** → **Run monitoring**.")
    else:
        res, score, d, lcfg = last["res"], last["score"], last["df"], last["cfg"]
        r = pd.DataFrame(res)
        nf, nw = int((r.status == "FAIL").sum()), int((r.status == "WARN").sum())
        npass = int((r.status == "PASS").sum())
        st.caption(f"Results for: **{last['name']}**")

        k = st.columns(5)
        k[0].markdown(kpi("Quality score", f"{score}/100",
                          "Healthy" if score >= 80 else "Needs attention" if score >= 50
                          else "Critical", score_color(score)), unsafe_allow_html=True)
        k[1].markdown(kpi("Rows", f"{len(d):,}", "records scanned", A1), unsafe_allow_html=True)
        k[2].markdown(kpi("Columns", d.shape[1], "fields checked", A2), unsafe_allow_html=True)
        k[3].markdown(kpi("Failures", nf, "critical issues", RED), unsafe_allow_html=True)
        k[4].markdown(kpi("Warnings", nw, "to review", AMBER), unsafe_allow_html=True)
        st.write("")
        if last["alerted"]:
            st.warning("🔔 Alert logged to data/alerts.log (email sent if SMTP is configured).")

        c1, c2 = st.columns(2)
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=score, title={"text": "Quality score"},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": score_color(score)},
                   "bgcolor": "rgba(255,255,255,.05)",
                   "steps": [{"range": [0, 50], "color": "rgba(239,68,68,.18)"},
                             {"range": [50, 80], "color": "rgba(245,158,11,.18)"},
                             {"range": [80, 100], "color": "rgba(34,197,94,.18)"}]}))
        c1.plotly_chart(style_fig(gauge))
        donut = go.Figure(go.Pie(labels=["PASS", "WARN", "FAIL"], values=[npass, nw, nf],
                                 hole=.62, sort=False, textinfo="label+value",
                                 marker=dict(colors=[GREEN, AMBER, RED])))
        donut.update_layout(title="Check results", showlegend=False)
        c2.plotly_chart(style_fig(donut))

        c3, c4 = st.columns(2)
        miss = (d.isna().mean() * 100).round(1).reset_index()
        miss.columns = ["column", "missing %"]
        fig = px.bar(miss, x="missing %", y="column", orientation="h",
                     title="Missing values by column (%)", color="missing %",
                     color_continuous_scale=[GREEN, AMBER, RED], range_color=[0, 30])
        fig.update_layout(coloraxis_showscale=False)
        c3.plotly_chart(style_fig(fig))

        out = r[r.check == "outliers_iqr"]
        if out.empty:
            c4.info("No numeric columns to check for outliers.")
        else:
            fig = px.bar(out, x="column", y="value", title="Outlier share by column",
                         color="status", color_discrete_map=STATUS_COLOR)
            fig.update_layout(showlegend=False, yaxis_title="share of rows")
            c4.plotly_chart(style_fig(fig))

        drift = r[r.check == "drift_psi"]
        if not drift.empty:
            fig = px.bar(drift, x="column", y="value", title="Distribution drift (PSI) by column",
                         color="status", color_discrete_map=STATUS_COLOR)
            fig.add_hline(y=lcfg["psi_fail"], line_dash="dash", line_color=RED,
                          annotation_text="FAIL limit")
            fig.add_hline(y=lcfg["psi_warn"], line_dash="dot", line_color=AMBER,
                          annotation_text="WARN limit")
            fig.update_layout(showlegend=False, yaxis_title="PSI")
            st.plotly_chart(style_fig(fig, 300))
        else:
            st.caption("💡 Set a baseline first to unlock schema and drift checks.")

        st.markdown('<div class="sec">Issues found</div>', unsafe_allow_html=True)
        flt = st.multiselect("Show status", ["FAIL", "WARN", "PASS"], ["FAIL", "WARN"])
        show = r[r.status.isin(flt)].copy()
        show["status"] = show["status"].map(BADGE)
        st.dataframe(show, use_container_width=True, hide_index=True)
        with st.expander("Data preview"):
            st.dataframe(d.head(100), use_container_width=True)
        st.download_button("⬇ Download report (CSV)", r.to_csv(index=False), "monitor_report.csv")

        if auto and df is not None:
            ss["_tick"] = True
            time.sleep(30)
            st.rerun()

# ---------------------------- Data profile ----------------------------
with tab_prof:
    if df is None:
        st.info("Choose a data source in the sidebar to see its profile.")
    else:
        num_cols = df.select_dtypes(include="number").columns
        p = st.columns(4)
        p[0].markdown(kpi("Rows", f"{len(df):,}", "total records", A1), unsafe_allow_html=True)
        p[1].markdown(kpi("Columns", df.shape[1], "fields", A2), unsafe_allow_html=True)
        p[2].markdown(kpi("Numeric", len(num_cols), "number columns", GREEN),
                      unsafe_allow_html=True)
        p[3].markdown(kpi("Memory", f"{df.memory_usage(deep=True).sum() / 1e6:.2f} MB",
                          "in RAM", AMBER), unsafe_allow_html=True)
        st.write("")
        prof = pd.DataFrame({
            "column": df.columns,
            "type": [str(t) for t in df.dtypes],
            "non-null %": ((1 - df.isna().mean()) * 100).round(1).values,
            "unique": df.nunique().values,
            "example": [str(df[c].dropna().iloc[0]) if df[c].notna().any() else ""
                        for c in df.columns],
        })
        st.dataframe(prof, use_container_width=True, hide_index=True)

        pick = st.selectbox("Explore a column", list(df.columns))
        if pick in num_cols:
            fig = px.histogram(df, x=pick, nbins=30, title=f"Distribution of {pick}")
            fig.update_traces(marker_color=A1)
            st.plotly_chart(style_fig(fig, 320))
        elif df[pick].nunique() <= 50:
            vc = df[pick].value_counts().reset_index()
            vc.columns = [pick, "count"]
            fig = px.bar(vc, x=pick, y="count", title=f"Values in {pick}")
            fig.update_traces(marker_color=A2)
            st.plotly_chart(style_fig(fig, 320))
        else:
            st.info("This column has too many distinct values to chart.")

# ---------------------------- History ----------------------------
with tab_hist:
    runs = storage.load_runs()
    if runs.empty:
        st.info("No runs yet. Run monitoring once and it will appear here.")
    else:
        h = st.columns(3)
        h[0].markdown(kpi("Total runs", len(runs), "saved in database", A1),
                      unsafe_allow_html=True)
        h[1].markdown(kpi("Average score", f"{runs.score.mean():.0f}/100", "across all runs", A2),
                      unsafe_allow_html=True)
        latest = int(runs.iloc[0].score)
        h[2].markdown(kpi("Latest score", f"{latest}/100", runs.iloc[0].ts, score_color(latest)),
                      unsafe_allow_html=True)
        st.write("")
        fig = px.line(runs.sort_values("id"), x="ts", y="score", markers=True,
                      title="Quality score over time", range_y=[0, 100])
        fig.update_traces(line_color=A1, fill="tozeroy", fillcolor="rgba(120,120,255,.15)")
        st.plotly_chart(style_fig(fig, 320))
        st.dataframe(runs, use_container_width=True, hide_index=True)
        rid = st.selectbox("Inspect run", runs["id"])
        iss = storage.load_issues(rid)
        iss["status"] = iss["status"].map(BADGE)
        st.dataframe(iss, use_container_width=True, hide_index=True)

# ---------------------------- Help ----------------------------
with tab_help:
    st.markdown("""
### Quick start
1. Press **⚡ One-click demo** - it creates a baseline from clean data and checks a faulty dataset.
2. Or use your own data: load a **clean** file → **Set baseline** → load a **new** file → **Run monitoring**.
3. Every run is saved in **History**. Pick a **Colour theme** in the sidebar any time.

### Checks
| Check | What it finds |
|---|---|
| Missing values | Columns with too many empty cells |
| Duplicates | Repeated rows |
| Outliers (IQR) | Values far outside the normal range |
| Schema | Added / removed / retyped columns vs baseline |
| Drift (PSI) | Numeric distribution shifted from baseline |
| Freshness | Newest record older than the limit |

**Score** = 100 − 10 per FAIL − 3 per WARN.
**Scheduling:** `python monitor_cli.py data/file.csv order_date` (cron / Task Scheduler).
""")
