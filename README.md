# 📊 Global Exchanges Market Performance Enterprise Workspace

A production-grade Streamlit terminal engineered to map daily market trends across global stock exchanges and benchmark indices—spanning **India (BSE & NSE)**, **USA (NYSE & NASDAQ)**, **China (SSE & SZSE)**, **Hong Kong (HKEX)**, **Singapore (SGX)**, **Japan (TSE)**, **UK (LSE)**, and **Germany (XETRA)**. This application follows a strict **Verification-First structural framework**, ensuring you can inspect and filter the base multi-exchange index registry on your desktop screen before compiling filtered ReportLab accounting ledgers and initiating downstream email operations via secure SMTP.

## About
Production-grade **Autonomous Financial Data Agent Workspace** built with **Streamlit** for **Global Stock Exchanges & Benchmark Indices** with automated reporting, filtered PDF export, and multi-exchange `yfinance` data ingestion capabilities.

### ⭐ Show Your Support

If you like the UI design, system architecture, or multi-exchange financial data engineering behind **Global Exchanges Market Performance Enterprise Workspace**, please consider giving this repository a **Star ⭐** on GitHub! It helps showcase this work and motivates future builds.

<img src="assets/desktop.png" width="100%" alt="Desktop Preview">

---

## 📂 System Architecture Repository Tree

```text
global-exchanges-tracker/
├── .github/
│   └── workflows/
│       └── sync_exchanges.yml          # Automated GitHub Actions cron runner
├── .streamlit/
│   └── secrets.toml                    # Encrypted enterprise SMTP credentials & target email storage
├── assets/
│   └── desktop.png                     # README desktop preview screenshot
├── data/
│   └── global_exchanges_master.csv     # Single master ledger: Country, Exchange, Index, Ticker & live prices
├── src/
│   ├── __init__.py                     # Explicit package boundary initialization
│   ├── data_engine.py                  # Multi-exchange yfinance ingestion & delta calculation engine
│   ├── email_service.py                # Secure SMTP distribution layer targeting port 587
│   └── pdf_generator.py                # Production ReportLab engine drafting filtered landscape PDFs
├── .gitignore                          # Excludes cache, temporary PDFs, and secrets
├── LICENSE                             # MIT License
├── README.md                           # System operational manual with structural Mermaid diagrams
├── app.py                              # Streamlit interface executing port 8501 runtimes
├── cron_job.py                         # Headless CLI runner for automated ingestion & email dispatch
├── generate_local_csv.py               # Baseline multi-exchange master CSV generator
└── requirements.txt                    # Python dependencies list
```

---

## 🛠️ Architecture & Core Components

```mermaid
flowchart TD
    %% Base Infrastructure Load
    A[app.py Platform Boot] e1@-->|Step 1: On-Init Standby| B(src/data_engine.py: fetch_master_list)
    B e2@-->|Pathway 1: Relative Disk| C{data/global_exchanges_master.csv}
    B e3@-->|Pathway 2: Auto-Bootstrap| D[generate_local_csv.py]
    
    %% Desktop Interface Rendering
    C e4@-->|Populate Data Frame| E[📋 Master Ledger Workspace]
    D e5@-->|Populate Data Frame| E
    E e6@-->|4-Tier Registry Filters| F[User Verification & Filter Phase]
    
    %% Live Processing Ingestion Execution
    F e7@-->|Step 2: Trigger Action| G[🚀 Execute Live Ingestion Button]
    G e8@-->|Multi-Exchange Batch + Fallback| H(yfinance Multi-Market Engine)
    H e9@-->|Download Date Horizon Windows| I[Calculate Closes, Price Diff & % Diff]
    
    %% Downstream Document Output
    I e10@-->|Step 3: Render Metrics| J[Update Grid + Cross-Sectional Charts]
    I e11@-->|Compile Filtered Ledger| K(src/pdf_generator.py)
    K e12@-->|Build 5-Column Landscape PDF| L[Filtered_Exchanges_Report.pdf]
    
    %% Secure Transmission Route
    J e13@-->|Step 4: Download or Dispatch| M[📥 Download / 📤 Dispatch PDF]
    L e14@-->|Step 4: Download or Dispatch| M
    M e15@-->|Extract Context via TOML Secrets| N{st.secrets gmail}
    N e16@-->|Route Secure TLS Packet| O(src/email_service.py)
    O e17@-->|Target Server: smtp.gmail.com| P["********@gmail.com"]

    %% Running Flow Animation Definitions
    e1@{ animate: true }
    e2@{ animate: true }
    e3@{ animate: true }
    e4@{ animate: true }
    e5@{ animate: true }
    e6@{ animate: true }
    e7@{ animate: true }
    e8@{ animate: true }
    e9@{ animate: true }
    e10@{ animate: true }
    e11@{ animate: true }
    e12@{ animate: true }
    e13@{ animate: true }
    e14@{ animate: true }
    e15@{ animate: true }
    e16@{ animate: true }
    e17@{ animate: true }

    %% Class Styling for Clean UI Nodes
    style E fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px;
    style F fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    style L fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    style P fill:#ffebee,stroke:#c62828,stroke-width:2px;
```

---

## 🚀 Local Network Initialization

To spin up the server environment locally on port **`8501`**, execute the following sequence inside your project repository terminal:

### Boot Up the Streamlit Core Server
Run the platform using the explicit network flag to map the interface directly to port `8501`:

```bash
streamlit run app.py --server.port 8501 --server.address localhost
```

Once executed, open your desktop browser and navigate to the live deployment link:
🔗 **`http://localhost:8501`**

---

## ⚡ Operational Guidelines

1. **Phase 1 (Verification Standby):** On application boot, the global exchange registry (`Country`, `Exchange`, `Index / Benchmark Name`, `yfinance Ticker`) instantly loads onto the interactive desktop table grid. Use the cascading filters to narrow down specific countries, exchanges, or benchmark indices before running calculations.
2. **Phase 2 (Live Sync):** Select your **Start Date** and **End Date** horizon in the sidebar and click **🚀 Execute Live Ingestion**. The system ingests cross-timezone pricing via `yfinance`, computes **Previous Close**, **Last Closing Price**, **Price Difference**, and **% Difference**, paints color-coded trends (`🟢 Up` / `🔴 Down`), and renders cross-sectional performance charts.
3. **Phase 3 (Filtered Document Download & Delivery):** Click **📥 Download Filtered PDF** to save a clean 5-column landscape PDF report of your active selection locally, or click **📤 Dispatch Filtered PDF via Email** to route the report via `EnterpriseEmailService` using your hidden `secrets.toml` credentials without exposing confidential fields on-screen.

---

## ⚠️ Financial & Operational Disclaimer

For educational and research purposes only; not financial advice. Market data via `yfinance` may be delayed across international exchanges. Users must manage their own local credentials and comply with platform terms.

---

## ⭐ Support & Contribution

If you clone, test, or build upon this repository, please consider giving it a **Star (⭐)** on GitHub—it helps others discover the project and supports continued development.

* **Found a bug or have an idea?** Open an [Issue](https://github.com).
* **Want to improve the code?** Feel free to **Fork** this repository and submit a Pull Request.

* **Lead Architect & Developer:** [Srinivasta](https://github.com/SRINIVASTA)

### 🌐 Let’s Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srinivas-t-a-557637119/)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/srinivasta)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tasrinivass@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SRINIVASTA)
[![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=website&logoColor=white)](https://srinivasta.github.io)
