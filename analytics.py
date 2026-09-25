import pandas as pd

def summary_kpis(df: pd.DataFrame) -> dict:
    orders = df["order_id"].nunique()
    return {
        "orders": int(orders),
        "revenue": float(df["revenue"].sum()),
        "units": int(df["quantity"].sum()),
        "cities": int(df["city"].nunique()),
        "states": int(df["state"].nunique()),
        "pin_codes": int(df["pin_code"].nunique()),
        "aov": float(df["revenue"].sum() / max(orders, 1)),
    }

def location_summary(df):
    return (df.groupby(["state", "city", "pin_code"], as_index=False)
            .agg(orders=("order_id", "nunique"),
                 units=("quantity", "sum"),
                 revenue=("revenue", "sum"))
            .sort_values("orders", ascending=False))

def state_summary(df):
    return (df.groupby("state", as_index=False)
            .agg(orders=("order_id", "nunique"),
                 revenue=("revenue", "sum"),
                 units=("quantity", "sum"),
                 cities=("city", "nunique"),
                 pin_codes=("pin_code", "nunique"))
            .sort_values("orders", ascending=False))

def city_summary(df):
    return (df.groupby(["state", "city"], as_index=False)
            .agg(orders=("order_id", "nunique"),
                 revenue=("revenue", "sum"),
                 units=("quantity", "sum"),
                 pin_codes=("pin_code", "nunique"))
            .sort_values("orders", ascending=False))

def monthly_summary(df):
    return (df.groupby("month", as_index=False)
            .agg(orders=("order_id", "nunique"),
                 revenue=("revenue", "sum"),
                 active_pin_codes=("pin_code", "nunique"))
            .sort_values("month"))

def product_summary(df):
    return (df.groupby("product", as_index=False)
            .agg(orders=("order_id", "nunique"),
                 units=("quantity", "sum"),
                 revenue=("revenue", "sum"))
            .sort_values("revenue", ascending=False))

def low_penetration_locations(df, threshold=20):
    loc = location_summary(df)
    return loc[loc["orders"] <= threshold].sort_values("orders")
