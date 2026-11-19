📊 Data Monitoring Tool

A data-quality monitoring web app that automatically checks datasets for missing values, duplicate rows, outliers, schema changes, distribution drift and stale data, gives each run a quality score, saves a run history and raises alerts. Built with Python, Pandas, SQLite and Streamlit.

🔗 Live demo: Open the app  |  💻 Source code: GitHub

Tip: click Continue as guest (demo) on the login page, then press ⚡ One-click demo.

📸 Screenshots
Login page	Dashboard
add screenshot	add screenshot

(Upload images to a screenshots/ folder in the repo and link them here.)

❓ Problem Statement

Bad data (missing values, duplicates, sudden changes in format or distribution, old data) silently breaks reports and ML models. This tool monitors a dataset against a trusted baseline and flags problems early.

✨ Features
🔐 Sign-up / login - users create their own account and set their own password (salted PBKDF2 hashing); guest demo mode
🎨 6 colour themes (Ocean, Emerald, Sunset, Violet, Gold, Slate) - saved per user
🧹 Quality checks: missing values, duplicates, outliers (IQR), schema changes, drift (PSI), freshness
📊 Dashboard: quality-score gauge, PASS/WARN/FAIL donut, missing / outlier / drift charts, issues table
🧬 Data profile tab: column types, null %, unique values, distributions
📈 History: every run saved in SQLite with a score trend chart
🔔 Alerts: written to data/alerts.log (and emailed if SMTP is configured)
⏱️ Scheduling: monitor_cli.py can run from cron / Task Scheduler
⬇️ Downloadable CSV report; supports CSV, Excel and JSON input
🧠 How it works
Data file  →  Ingestion  →  Checks engine  →  Quality score  →  SQLite history
 (CSV/XLSX/JSON)              (6 checks)            ↓                 ↓
                                              Alerts (log/email)   Streamlit dashboard
Check	Method
Missing values	% of nulls per column vs WARN/FAIL limits
Duplicates	% of fully repeated rows
Outliers	Values outside Q1 − 1.5×IQR and Q3 + 1.5×IQR
Schema	Added / removed / retyped columns compared with the baseline
Drift	Population Stability Index (PSI): < 0.1 stable, 0.1-0.25 warning, > 0.25 fail
Freshness	Age of the newest timestamp vs the allowed limit

Quality score = 100 − 10 × (FAIL checks) − 3 × (WARN checks)

🛠️ Tech Stack

Python · Pandas · NumPy · SQLite · Streamlit · Plotly · Git/GitHub · Streamlit Community Cloud

👥 Team & Roles
Member	Role	Responsibilities	Files
Member 1 - Name	Data & Security Engineer	File ingestion (CSV/Excel/JSON), SQLite database design (runs, issues, baseline, users), account system with password hashing, built-in demo data	monitor/ingest.py, monitor/storage.py, monitor/auth.py, monitor/sample.py
Member 2 - Name	Monitoring & Alerts Engineer	Data-quality checks and thresholds, drift (PSI) logic, quality scoring, alerting (log + email), scheduled runs, unit tests	monitor/checks.py, monitor/alerts.py, monitor_cli.py, tests/
Member 3 - Name	UI, Integration & Documentation Lead	Streamlit dashboard, login / sign-up page, themes and charts, integrating all modules, deployment, README and demo	app.py, monitor/themes.py, README.md

All members worked with Git branches and pull requests, and tested the full flow together before the demo.

🚀 Run Locally
bash
git clone https://github.com/sharvi-saraswat/data-monitoring-pro.git
cd data-monitoring-pro
pip install -r requirements.txt
streamlit run app.py

Open http://localhost:8501, create an account (or use guest mode) and press ⚡ One-click demo.

Run a check without the UI (for scheduling):

bash
python monitor_cli.py data/sample_dirty.csv order_date

Run the tests: pip install pytest then pytest tests

Optional email alerts: set the environment variables SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ALERT_TO.

📁 Project Structure
├── app.py                 # dashboard + login UI
├── monitor/
│   ├── checks.py          # all data-quality checks
│   ├── alerts.py          # log / email alerts
│   ├── storage.py         # SQLite: runs, issues, baseline, users
│   ├── auth.py            # accounts + password hashing
│   ├── ingest.py          # CSV / Excel / JSON loaders
│   ├── sample.py          # built-in demo data
│   └── themes.py          # colour themes + CSS
├── monitor_cli.py         # headless runner for schedulers
├── generate_sample_data.py
├── tests/
├── data/                  # sample files, database, alert log
└── requirements.txt
⚠️ Notes & Limitations
On Streamlit Community Cloud the SQLite file resets when the app restarts, so accounts and history may be cleared. For permanent storage use an external database such as PostgreSQL.
The login system is meant for a project demo; production apps should use OAuth / SSO.
🔮 Future Improvements
Connect directly to MySQL / PostgreSQL tables and cloud storage
Slack / Telegram alerts
Separate baselines per dataset and drift trend charts over time
Role-based access and password reset by email
📄 License

Created for educational purposes.
