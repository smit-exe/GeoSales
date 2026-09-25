from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium

from src.data_processing import clean_orders, load_and_clean
from src.analytics import (
    summary_kpis, location_summary, state_summary, city_summary,
    monthly_summary, product_summary, low_penetration_locations
)

st.set_page_config(page_title="GeoSales", page_icon="📍", layout="wide")
st.title("📍 GeoSales")
st.caption("Location-Based Sales & Delivery Intelligence Platform")

DATA_FILE = Path(__file__).parent / "data" / "orders.csv"

with st.sidebar:
    st.header("Filters")
    uploaded = st.file_uploader("Upload orders CSV", type=["csv"])

if uploaded:
    try:
        df = clean_orders(pd.read_csv(uploaded))
    except Exception as exc:
        st.error(f"Could not process file: {exc}")
        st.stop()
elif DATA_FILE.exists():
    df = load_and_clean(str(DATA_FILE))
else:
    st.warning("Run `python scripts/generate_data.py` first.")
    st.stop()

with st.sidebar:
    states = ["All"] + sorted(df["state"].unique().tolist())
    selected_state = st.selectbox("State", states)

filtered = df if selected_state == "All" else df[df["state"] == selected_state]

with st.sidebar:
    cities = ["All"] + sorted(filtered["city"].unique().tolist())
    selected_city = st.selectbox("City", cities)

if selected_city != "All":
    filtered = filtered[filtered["city"] == selected_city]

k = summary_kpis(filtered)
cols = st.columns(6)
labels = [
    ("Orders", f"{k['orders']:,}"),
    ("Revenue", f"₹{k['revenue']:,.0f}"),
    ("Units", f"{k['units']:,}"),
    ("Cities", k["cities"]),
    ("PIN Codes", k["pin_codes"]),
    ("AOV", f"₹{k['aov']:,.0f}")
]
for col, (label, value) in zip(cols, labels):
    col.metric(label, value)

left, right = st.columns(2)

with left:
    st.subheader("Orders by State")
    s = state_summary(filtered)
    st.plotly_chart(px.bar(s, x="state", y="orders", text_auto=True),
                    use_container_width=True)

with right:
    st.subheader("Revenue by City")
    c = city_summary(filtered).head(15)
    st.plotly_chart(px.bar(c, x="city", y="revenue", text_auto=".2s"),
                    use_container_width=True)

st.subheader("Monthly Geographic Coverage")
m = monthly_summary(filtered)
st.plotly_chart(
    px.line(m, x="month", y="active_pin_codes", markers=True),
    use_container_width=True
)

st.subheader("Delivery Coverage Map")
map_df = filtered.dropna(subset=["latitude", "longitude"])

if not map_df.empty:
    fmap = folium.Map(
        location=[map_df["latitude"].mean(), map_df["longitude"].mean()],
        zoom_start=5
    )
    loc = (
        map_df.groupby(
            ["state", "city", "pin_code", "latitude", "longitude"],
            as_index=False
        )
        .agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"))
    )

    q33 = loc["orders"].quantile(0.33)
    q66 = loc["orders"].quantile(0.66)

    for _, row in loc.iterrows():
        demand = "High" if row["orders"] >= q66 else "Medium" if row["orders"] >= q33 else "Low"
        popup = (
            f"<b>PIN:</b> {row['pin_code']}<br>"
            f"<b>City:</b> {row['city']}<br>"
            f"<b>Orders:</b> {row['orders']:,}<br>"
            f"<b>Revenue:</b> ₹{row['revenue']:,.0f}<br>"
            f"<b>Demand:</b> {demand}"
        )
        folium.CircleMarker(
            [row["latitude"], row["longitude"]],
            radius=7,
            popup=folium.Popup(popup, max_width=280),
            fill=True
        ).add_to(fmap)

    st_folium(fmap, width=None, height=520)
else:
    st.info("Latitude and longitude are required for the map.")

st.subheader("Top Locations")
st.dataframe(location_summary(filtered).head(20), use_container_width=True)

st.subheader("Low-Penetration Locations")
threshold = st.slider("Maximum orders considered low penetration", 1, 100, 20)
st.dataframe(low_penetration_locations(filtered, threshold),
             use_container_width=True)

st.subheader("Product Performance")
p = product_summary(filtered)
st.plotly_chart(px.bar(p, x="product", y="revenue", text_auto=".2s"),
                use_container_width=True)
