import pandas as pd  # pyright: ignore[reportMissingModuleSource]

REQUIRED_COLUMNS = [
    "order_id", "order_date", "product", "state", "city",
    "pin_code", "quantity", "price", "platform"
]

def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["pin_code"] = pd.to_numeric(df["pin_code"], errors="coerce").astype("Int64")

    for col in ["state", "city", "product", "platform"]:
        df[col] = df[col].astype("string").str.strip()

    df = df.drop_duplicates(subset=["order_id"])
    df = df.dropna(subset=["order_id", "order_date", "state", "city", "pin_code"])
    df = df[(df["quantity"] > 0) & (df["price"] >= 0)]

    df["revenue"] = df["quantity"] * df["price"]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df.reset_index(drop=True)

def load_and_clean(path: str) -> pd.DataFrame:
    return clean_orders(pd.read_csv(path))
