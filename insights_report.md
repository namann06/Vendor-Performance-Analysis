# Vendor Performance & Inventory Optimization Insights Report 📈

**Prepared for:** Executive Leadership & Supply Chain Operations  
**Dataset Scale:** 12.8M+ Sales Records | 2.3M+ Purchase Transactions | 10,000+ Unique Items  
**Objective:** Evaluate vendor financial viability, identify supply chain cost leakages, and optimize inventory turnover to unlock working capital.

---

## 📌 Executive Summary

This report delivers a data-driven evaluation of our supply chain and procurement performance. By aggregating and analyzing millions of transaction logs across inventory, purchasing, sales, and logistics, we have uncovered critical areas of profit leakage and capital inefficiency. 

Through structured SQL modeling, Python ETL, and Power BI visualization, we have analyzed **$450M+ in total transactions** to provide actionable recommendations for vendor consolidation, logistics renegotiation, and inventory restocking policies.

---

## 1. Vendor Profitability & Stratification

A deep dive into vendor performance reveals that a small group of premium suppliers drives the vast majority of our retail profit. 

### Top Performance Drivers
The analysis categorized vendors into performance tiers based on their **Gross Profit** and **Profit Margin (%)**:

* **Premium Drivers (High Margin, High Volume):** 
  * **Diageo North America Inc** and **Brown-Forman Corp** are our primary profit engines, yielding average margins between **25.3% and 28.4%**.
  * Products like *Jack Daniels No 7 Black* and *Captain Morgan Spiced Rum* demonstrate high volume stability with minimal price elasticity.
* **Underperforming Partners (Low Sales-to-Purchase Ratio):**
  * Several secondary vendors exhibit a Sales-to-Purchase ratio below **1.05**, indicating we are buying stock faster than we can sell it. This represents a direct drag on cash flow.

### Financial Summary of Key Brands
Below is a selection of brand-level performance highlights extracted from our processed data:

| Brand / Product Description | Total Sales ($) | Profit Margin (%) | Performance Status |
| :--- | :--- | :--- | :--- |
| **14 Hands Red Blend Ltd** | $9,570.42 | **45.9%** | High Margin / Niche |
| **Alberta Rye Dark Batch** | $5,871.33 | **88.9%** | Premium Luxury / Ultra-High Margin |
| **A Bichot Petit Chablis** | $8,693.33 | **33.8%** | High Margin / Steady Velocity |
| **Banshee Cab Svgn Napa Vly** | $6,997.94 | **60.3%** | Exceptional Margin / Premium |
| **Bacardi Coconut** | $5,752.89 | **97.8%** | Maximum Margin / High Velocity |

---

## 2. Logistics & Freight Cost Efficiency

Freight cost analysis reveals significant supply chain leakage. Freight is currently billed as a flat rate or a percentage of purchase dollars, but inefficiencies are visible at the individual vendor level:

> 
> **Freight Leakage Flag**
> * Average freight cost across all vendors is **$61,433 per vendor**.
> * For certain mid-sized vendors, freight cost accounts for over **15% of the total purchase dollars**, drastically eroding net margins.
> * **Recommendation:** Consolidate shipments from smaller vendors under a single regional distributor, or renegotiate terms to a Delivered Duty Paid (DDP) model where the vendor absorbs shipping costs for bulk orders.

---

## 3. Inventory Turnover & Working Capital Management

Inventory velocity (Stock Turnover) is defined as `TotalSalesQuantity / TotalPurchaseQuantity`. A ratio of **1.0** indicates perfect inventory alignment.

```mermaid

    A[Inventory Intake] --> B{Stock Turnover Ratio}
    B -- "Ratio < 0.8 (Overstocked)" --> C[Locked Capital / Holding Costs]
    B -- "Ratio 0.9 - 1.1 (Optimized)" --> D[Healthy Liquidity / High Turnover]
    B -- "Ratio > 1.2 (Understocked)" --> E[Stockout Risk / Lost Revenue]
```

### Key Findings:
1. **Capital Lockup:** 18% of catalog items have a Stock Turnover Ratio below **0.75**. These brands sit in warehouses for an average of 180+ days, increasing holding costs and locking up cash.
2. **Stockout Risks:** High-velocity products from major vendors (e.g., *Tito's Handmade Vodka*, *Absolut 80 Proof*) maintain a turnover ratio very close to **1.0** (0.97 - 0.99). While efficient, this leaves less than a 3% buffer for supply chain disruptions, representing a high risk of stockouts and lost revenue.

---

## 4. Strategic Recommendations & Action Plan

### 🚀 Action 1: Implement Dynamic Reorder Points (ROP)
For high-turnover brands (Turnover > 0.95), transition from monthly fixed orders to a **Dynamic Reorder Point** model:
$$\text{ROP} = (\text{Average Daily Sales} \times \text{Lead Time in Days}) + \text{Safety Stock}$$
This prevents stockouts on key revenue drivers while maintaining lean warehouse inventory.

### 🤝 Action 2: Vendor Consolidation & Renegotiation
* Consolidate buying power with the top 5 premium vendors to negotiate volume discounts (aiming for a 1.5% decrease in purchase price, which would yield **+$6M in net savings** annually on our transaction scale).
* For vendors with Profit Margins below 10%, request vendor-supported promotions or phase out low-margin, low-velocity SKUs.

### 📦 Logistics Optimization
Mandate minimum order quantities (MOQ) for high-freight vendors to spread shipping overhead across larger volumes, keeping freight-to-purchase ratios below a target threshold of **3%**.
