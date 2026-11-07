# Amazon India Sales Dashboard
Sapphire IQ AI/ML Internship, Project 1

An interactive management dashboard built from `Amazon_Sales_Data_India.xlsx` (10,000 orders, 1 Jan 2024 to 30 Aug 2026). It is written for a non-technical reader and follows the four sections of the project brief.

## Folder contents
| File | Purpose |
|---|---|
| `data/Amazon_Sales_Data_India.xlsx` | Source data (unchanged) |
| `build_dashboard.py` | Reads the Excel file, checks data quality, builds the dashboard |
| `template.html` | Dashboard design, charts and filter logic (HTML, CSS, JavaScript) |
| `Amazon_India_Dashboard.html` | **The finished dashboard.** One file, works offline |

## How to run (step by step)
**Just view it:** double-click `Amazon_India_Dashboard.html`. It opens in Chrome, Edge or Firefox. No server or internet needed (the font falls back to the system font offline).

**Rebuild from Excel (to show the Python step or after changing data):**
1. Install Python 3.9 or newer from python.org.
2. Open a terminal in the project folder.
3. Install the libraries: `pip install pandas openpyxl`
4. Run: `python build_dashboard.py`
5. The terminal prints a data-quality check, then `Built Amazon_India_Dashboard.html`. Open that file.

To use another Excel file with the same columns: `python build_dashboard.py path/to/file.xlsx`

## What the dashboard contains
1. **Overall performance:** Total Sales, Total Profit, Orders, Units Sold, Average Order Value, Profit Margin %; monthly trend (Sales and Profit, Orders, Units, Margin) with hover values and a Chart/Table switch.
2. **Category and product:** sales, profit and units by category; Top 10 products by sales; five lowest-margin products.
3. **Order status and revenue loss:** Delivered, Shipped, Returned, Cancelled counts; Return Rate; Cancellation Rate; Revenue Lost; status donut; returns and cancellations by category.
4. **Payment, fulfilment, geography:** sales and profit by payment method and by fulfilment method; state tile map (switch between Sales, Profit, Orders); ranked states; sortable state table.

**Interactivity:** filters for period (All, 2024, 2025, 2026 or any month range), category, order status, payment, fulfilment and state. Every number and chart updates together. You can also click any bar, donut slice or map tile to filter. Removable filter chips show what is active. Light and dark themes. Each section ends with an insight sentence that is recalculated for the current filters.

## Metric definitions
- Total Sales = sum of `Total_Sales_INR` (all orders, any status)
- Total Profit = sum of `Profit_INR`
- Orders = count of `Order_ID`; Units = sum of `Quantity`
- Average Order Value = Total Sales / Orders
- Profit Margin = Total Profit / Total Sales
- Return Rate = Returned orders / all orders; Cancellation Rate = Cancelled orders / all orders
- Revenue Lost = sales value of Returned + Cancelled orders

**Important data note:** in the source file, Returned and Cancelled orders keep their sales value but have zero profit. They are counted in Total Sales and reported separately as Revenue Lost.

## Data checks performed
10,000 rows, 13 columns, no missing values, no duplicate Order IDs, all dates valid, and `Total_Sales = Quantity x Unit Price x (1 - Discount)` holds on every row. No rows were removed or edited.

## Headline figures (all data)
Sales ₹15,57,89,894 (₹15.58 Cr) · Profit ₹3,31,67,008 (₹3.32 Cr) · Orders 10,000 · Units 24,926 · AOV ₹15,579 · Margin 21.3% · Return rate 4.9% · Cancellation rate 5.0% · Revenue lost ₹1.56 Cr (10.0% of sales).

## Suggested demo script (3 minutes)
1. Show the KPI row and say the margin is 21.3%.
2. Trend: hover over a month; switch to Orders and to Table.
3. Categories: Electronics & Mobiles is 79% of sales. Click it to filter the whole page.
4. Status: 10% of sales value is lost to returns and cancellations. Click Cancelled.
5. Geography: Maharashtra, Karnataka, Delhi are the top three states. Click Reset filters.
