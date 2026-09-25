from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from src.data_processing import load_and_clean
from src.analytics import summary_kpis, location_summary, state_summary, city_summary

BASE = Path(__file__).resolve().parents[1]
DATA_FILE = BASE / "data" / "orders.csv"

app = FastAPI(title="GeoSales API", version="1.0.0")

def get_data():
    if not DATA_FILE.exists():
        raise HTTPException(404, "orders.csv not found. Run scripts/generate_data.py")
    return load_and_clean(str(DATA_FILE))

@app.get("/")
def root():
    return {"name": "GeoSales API", "status": "running"}

@app.get("/api/summary")
def summary():
    return summary_kpis(get_data())

@app.get("/api/states")
def states():
    return state_summary(get_data()).to_dict(orient="records")

@app.get("/api/cities/{city}")
def city(city: str):
    result = city_summary(get_data())
    result = result[result["city"].str.lower() == city.lower()]
    if result.empty:
        raise HTTPException(404, "City not found")
    return result.to_dict(orient="records")

@app.get("/api/pincode/{pincode}")
def pincode(pincode: str):
    result = location_summary(get_data())
    result = result[result["pin_code"].astype(str) == str(pincode)]
    if result.empty:
        raise HTTPException(404, "PIN code not found")
    return result.to_dict(orient="records")[0]

@app.get("/api/top-locations")
def top_locations(limit: int = Query(10, ge=1, le=100)):
    return location_summary(get_data()).head(limit).to_dict(orient="records")
