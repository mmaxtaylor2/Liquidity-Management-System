# Liquidity Management System

A treasury operations tool that combines daily cash positioning, a 13-week cash forecast, revolver draw/repay automation, and scenario stress testing. This simulates core workflows performed by corporate treasury analysts managing short-term liquidity and funding needs.

---

## Key Features
- Daily bank balance ingestion and cash position overview
- 13-week rolling liquidity forecast with inflow/outflow schedules
- Stress-test scenarios (base, -5% inflows, -10% inflows, +15% outflows)
- Revolver draw/repayment logic to protect minimum liquidity thresholds
- Covenant and minimum cash monitoring with risk signals
- Liquidity status tiers: Stable, Warning, Critical
- Bank balance distribution view
- Exportable forecast report (CSV)

---

## Treasury Skills Demonstrated
| Area | Demonstrated |
|------|---------------|
| Cash Ops | Daily cash positioning & account visibility |
| Forecasting | Rolling 13-week liquidity coverage modeling |
| Credit Facility | Revolver mechanics, liquidity floor protection |
| Stress Testing | Sensitivity to cash shocks and funding needs |
| Reporting | Dashboard + CSV output for management use |

---

## Directory Structure
liquidity-management-system
│
├── data
│ ├── bank_balances.csv
│ └── forecast_inputs.csv
│
├── models
│ ├── forecast_engine.py # 13-week model
│ ├── draw_logic.py # Revolver rules
│ └── alerts.py # Threshold triggers
│
└── ui
├── cli_dashboard.py # Command-line version
└── streamlit_dashboard.py # Main app

---

## Installation

```bash
git clone https://github.com/mmaxtaylor2/Liquidity-Management-System.git
cd Liquidity-Management-System/liquidity-management-system
pip install -r requirements.txt

## Running the Application

streamlit run ui/streamlit_dashboard.py

If multiple Streamlit windows are open and you need to reset:

pkill -f streamlit
streamlit run ui/streamlit_dashboard.py

## Requirements

(Already included in requirements.txt)
pandas==2.1.1
streamlit==1.29.0
numpy==1.26.2
python-dateutil==2.8.2

## Next Step Expansion Ideas

Multi-currency/FX toggle for global entities
Short-term investment ladder (MMF/T-Bills/CP)
Dynamic interest expense on revolver balance
Automated cash sweep logic

## Purpose of the Project

This project is designed to demonstrate readiness for:

Treasury Analyst
Corporate Finance Analyst
Cash Management / FP&A
Short-term Funding / Liquidity Ops

The goal is to replicate real deliverables used by treasury teams.
