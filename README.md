# GeoSales — Location-Based Sales & Delivery Intelligence Platform

Portfolio project for analyzing order/delivery datasets by State, City and PIN Code.

## Features
- Pandas data cleaning and validation
- SQL-ready database schema
- Location-wise sales and delivery analytics
- Streamlit + Plotly dashboard
- Folium geographical map
- FastAPI REST endpoints
- Synthetic demo dataset generator
- Geographic coverage and low-penetration analysis

## Run

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python scripts/generate_data.py
streamlit run app.py
```

API:

```bash
uvicorn api.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

## Structure

```text
GeoSales/
├── app.py
├── requirements.txt
├── README.md
├── data/orders.csv
├── src/data_processing.py
├── src/analytics.py
├── api/main.py
├── database/schema.sql
└── scripts/generate_data.py
```

The included dataset is synthetic demo data. Do not describe it as real company data.
