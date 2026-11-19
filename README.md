# 📊 Data Monitoring Tool

Monitors datasets (CSV / Excel / JSON) for **missing values, duplicates, outliers, schema changes,
distribution drift (PSI) and stale data**. Includes sign-up / login, a themed Streamlit dashboard,
run history in SQLite, and email / log alerts.

🔗 **Live demo:** _paste your Streamlit link here_

## Features
- 🔐 Create your own account (salted PBKDF2 password hashing), change password, or continue as guest
- 🎨 6 colour themes (Ocean, Emerald, Sunset, Violet, Gold, Slate) - saved per user
- ⚡ One-click demo, quality score gauge, status donut, missing / outlier / drift charts
- 🧬 Data profile tab (types, null %, unique values, distributions)
- 📈 Run history with score trend; downloadable CSV report
- 🔔 Alerts to `data/alerts.log` (+ email if SMTP env vars are set)

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Optional: `python generate_sample_data.py` creates CSVs in `data/` for the *File path* source.
Headless / scheduled: `python monitor_cli.py data/sample_dirty.csv order_date`

## Project structure
```
app.py               dashboard + login UI            (Member 3)
monitor/themes.py    colour themes + CSS             (Member 3)
monitor/checks.py    all data-quality checks         (Member 2)
monitor/alerts.py    log / email alerts              (Member 2)
monitor/storage.py   SQLite: runs, issues, baseline  (Member 1)
monitor/auth.py      accounts + password hashing     (Member 1)
monitor/ingest.py    CSV / Excel / JSON loaders      (Member 1)
monitor/sample.py    built-in demo data              (Member 1)
tests/               unit tests                      (Member 2)
```

## Team roles
| Member | Role | Responsibilities |
|---|---|---|
| 1 | Data & Security Engineer | File ingestion, SQLite schema, user accounts / password hashing, sample data, add DB/API connectors |
| 2 | Monitoring & Alerts Engineer | Quality checks, thresholds, scoring, alerts, scheduling (`monitor_cli.py`), unit tests |
| 3 | UI, Integration & Docs Lead | Streamlit dashboard, login page, themes, charts, deployment, README / report / demo |

## Notes
- On Streamlit Community Cloud the SQLite file resets when the app restarts, so accounts and history
  can disappear. For permanent storage use an external database (e.g. PostgreSQL).
- Login is suitable for a project demo; production apps should use OAuth / SSO.
