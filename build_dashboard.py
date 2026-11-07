#!/usr/bin/env python3
"""
Amazon India Sales Dashboard - build script
Sapphire IQ internship project

Reads  : data/Amazon_Sales_Data_India.xlsx
Writes : Amazon_India_Dashboard.html  (one self-contained file; double-click to open, no server needed)

Usage  : python build_dashboard.py [path/to/excel.xlsx]
Needs  : Python 3.9+, pandas, openpyxl
"""
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "data" / "Amazon_Sales_Data_India.xlsx"
OUT = HERE / "Amazon_India_Dashboard.html"
ARTIFACT_OUT = HERE / "build" / "dashboard_fragment.html"

REQUIRED = ["Order_ID", "Order_Date", "Category", "Product", "Quantity", "Unit_Price_INR", "Discount_Pct",
            "Total_Sales_INR", "Profit_INR", "Payment_Method", "Fulfillment", "Order_Status", "Ship_State"]


def load(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        sys.exit(f"Missing columns in Excel file: {missing}")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="raise")
    # Data-quality report (printed so it can be shown in the demo)
    print(f"Rows: {len(df):,} | Missing values: {int(df.isna().sum().sum())} | Duplicate Order IDs: {int(df.Order_ID.duplicated().sum())}")
    expected = (df.Quantity * df.Unit_Price_INR * (1 - df.Discount_Pct)).round(2)
    print(f"Rows where Total_Sales != Qty x Price x (1 - Discount): {int(((expected - df.Total_Sales_INR).abs() > 0.02).sum())}")
    return df


def encode(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["ym"] = df.Order_Date.dt.strftime("%Y-%m")
    months = sorted(df.ym.unique())
    # make sure every month between first and last exists (so the trend axis has no gaps)
    months = [p.strftime("%Y-%m") for p in pd.period_range(months[0], months[-1], freq="M")]
    cats = sorted(df.Category.unique())
    pays = sorted(df.Payment_Method.unique())
    fuls = sorted(df.Fulfillment.unique())
    states = sorted(df.Ship_State.unique())
    statuses = [s for s in ["Delivered", "Shipped", "Returned", "Cancelled"] if s in set(df.Order_Status)]
    statuses += sorted(set(df.Order_Status) - set(statuses))
    prods = (df[["Product", "Category"]].drop_duplicates().sort_values(["Category", "Product"]).values.tolist())
    prod_list = [[p, cats.index(c)] for p, c in prods]
    pidx = {p: i for i, (p, _) in enumerate(prod_list)}
    rows = [[months.index(r.ym), cats.index(r.Category), pidx[r.Product], int(r.Quantity), round(float(r.Total_Sales_INR), 2),
             round(float(r.Profit_INR), 2), pays.index(r.Payment_Method), fuls.index(r.Fulfillment),
             statuses.index(r.Order_Status), states.index(r.Ship_State)] for r in df.itertuples()]
    fmt = lambda d: d.strftime("%d %b %Y").lstrip("0")
    return {"months": months, "cats": cats, "products": prod_list, "pays": pays, "fuls": fuls, "states": states,
            "statuses": statuses, "rows": rows,
            "meta": {"first": fmt(df.Order_Date.min()), "last": fmt(df.Order_Date.max()), "source": SRC.name}}


def main():
    df = load(SRC)
    data = encode(df)
    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    tpl = tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
    head, body = tpl.split("<!--BODY-->")
    standalone = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                  '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                  f"{head}</head>\n<body>{body}</body>\n</html>\n")
    OUT.write_text(standalone, encoding="utf-8")
    ARTIFACT_OUT.parent.mkdir(exist_ok=True)
    ARTIFACT_OUT.write_text(head + body, encoding="utf-8")
    print(f"Built {OUT.name} ({OUT.stat().st_size/1024:.0f} KB). Open it in Chrome, Edge or Firefox.")


if __name__ == "__main__":
    main()
