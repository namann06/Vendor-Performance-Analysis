# Vendor Performance Analysis & Optimization Pipeline 

An end-to-end data engineering and analytics pipeline designed to evaluate vendor performance, optimize product pricing, and identify profitability opportunities. This project ingests transactional inventory, purchase, and sales logs (spanning over 12 million records), processes them in a local relational database, and exposes insights through statistical modeling and interactive dashboards.

---

## 🌟 Key Features

* **Scalable ETL Pipeline:** Custom Python scripts (`ingestion_db.py` and `get_vendor_summary.py`) with database connection pooling and optimized bulk transfers to process large transaction files.
* **Relational Data Modeling:** Consolidates raw tables (purchases, invoices, sales, inventory levels) into a structured SQLite data warehouse.
* **Automated Feature Engineering:** Programmatically computes business-critical KPIs including **Gross Profit**, **Profit Margin**, **Stock Turnover Ratio**, and **Sales-to-Purchase Ratio**.
* **Exploratory Data Analysis:** Comprehensive Jupyter Notebooks detailing statistical hypotheses, pricing elasticity, and vendor stratification.
* **Interactive Dashboard:** Interactive Power BI dashboard (`Vendor_Dashboard.pbix`) detailing executive KPIs, cost drivers, and vendor rank cards.

---

## 📁 Repository Structure

```text
vendor-performance-analysis/
├── .gitignore               # Excludes raw database/logs and temp files from Git
├── README.md                # Project documentation and guide
├── requirements.txt         # Project dependencies
├── inventory.db             # Local SQLite database (Generated locally, ignored by Git)
├── data/
│   ├── raw/                 # Contains 100-row sample CSVs for quick testing
│   │   ├── begin_inventory.csv
│   │   ├── end_inventory.csv
│   │   ├── purchase_prices.csv
│   │   ├── purchases.csv
│   │   ├── sales.csv
│   │   └── vendor_invoice.csv
│   └── processed/           # Processed summary data pushed to GitHub
│       ├── brand_performance.csv
│       ├── top_vendors.csv
│       └── vendor_sales_summary.csv
├── notebooks/
│   ├── EDA.ipynb            # Exploratory Data Analysis & Schema investigation
│   └── Vendor_Performance_Analysis.ipynb # Deep-dive vendor performance analysis
├── scripts/
│   ├── ingestion_db.py      # SQLite DB ingestion script
│   └── get_vendor_summary.py # SQL ETL process and metrics builder
├── dashboards/
│   └── Vendor_Dashboard.pbix # Interactive Power BI Dashboard
└── logs/
    ├── ingestion_db.log      # DB ingestion execution logs
    └── get_vendor_summary.log # ETL execution logs
```

---

## ⚙️ Quick Start

### 1. Installation & Environment Setup
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/your-username/vendor-performance-analysis.git
cd vendor-performance-analysis
pip install -r requirements.txt
```

### 2. Execute the Data Pipeline
Run the database ingestion script to load raw CSV data (uses sample datasets by default) into the SQLite database:
```bash
python scripts/ingestion_db.py
```

Generate the aggregated vendor sales summary table and export the processed datasets:
```bash
python scripts/get_vendor_summary.py
```

### 3. Notebook Exploration
Start Jupyter Notebook to inspect the data exploration and analysis files:
```bash
jupyter notebook
```
Navigate to the `notebooks/` folder to run:
* `EDA.ipynb` - Initial schema parsing and transaction counts.
* `Vendor_Performance_Analysis.ipynb` - Statistical testing (T-tests), pricing optimizations, and performance profiling.

### 4. Interactive Dashboard
Open `dashboards/Vendor_Dashboard.pbix` in Microsoft Power BI Desktop to explore interactive reports showcasing purchase vs. sales comparisons, freight ratios, and vendor scorecards.

---

## 📈 Business KPIs Computed

| Metric | Business Formula | Significance |
| :--- | :--- | :--- |
| **Gross Profit** | `TotalSalesDollars - TotalPurchaseDollars` | Determines net profitability of items sold from each vendor. |
| **Profit Margin** | `(GrossProfit / TotalSalesDollars) * 100` | Normalizes profitability across vendors of different sales volumes. |
| **Stock Turnover** | `TotalSalesQuantity / TotalPurchaseQuantity` | Tracks inventory efficiency and identifies slow-moving or overstocked items. |
| **Sales-to-Purchase Ratio** | `TotalSalesDollars / TotalPurchaseDollars` | Gauges return on capital invested in purchasing goods. |

---

## 🔍 Key Insights & Recommendations

* **High Margin Stratification:** Identified top vendors (e.g., *Diageo North America*, *Brown-Forman Corp*) driving the highest profit margins (25-28%), recommending strategic volume expansion with these suppliers.
* **Freight Cost Leakage:** Highlighted vendors where freight costs consumed more than 15% of gross profit, recommending freight cost consolidation or renegotiating delivery terms.
* **Inventory Turnover optimization:** Flagged slow-moving brands where stock turnover was below 0.5, representing locked-up working capital. Recommended promotional campaigns or vendor-managed inventory (VMI) agreements.

---

## 📦 Processing the Full Dataset (12M+ Rows)
To run the analysis on the complete dataset rather than the provided test samples:
1. Download the full dataset files from the source (e.g., Kaggle or your private server).
2. Place the full CSV files in the project root directory (to match gitignore settings) or override the sample CSV files in `data/raw/`.
3. Re-run `python scripts/ingestion_db.py` to rebuild the SQLite database.
