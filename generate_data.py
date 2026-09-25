from pathlib import Path
import random
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

locations = [
    ("Maharashtra", "Mumbai", 400001, 19.0760, 72.8777),
    ("Maharashtra", "Mumbai", 400050, 19.0596, 72.8295),
    ("Maharashtra", "Thane", 400601, 19.2183, 72.9781),
    ("Maharashtra", "Pune", 411001, 18.5204, 73.8567),
    ("Maharashtra", "Nashik", 422001, 20.0059, 73.7797),
    ("Gujarat", "Ahmedabad", 380001, 23.0225, 72.5714),
    ("Gujarat", "Surat", 395003, 21.1702, 72.8311),
    ("Karnataka", "Bengaluru", 560001, 12.9716, 77.5946),
    ("Delhi", "New Delhi", 110001, 28.6139, 77.2090),
    ("Telangana", "Hyderabad", 500001, 17.3850, 78.4867),
]

products = ["Protein Bar", "Energy Drink", "Face Wash", "Shampoo", "Coffee", "Snacks"]
platforms = ["Zepto", "Blinkit", "Swiggy Instamart"]

rows = []
for i in range(1, 5001):
    state, city, pin, lat, lon = random.choice(locations)
    date = pd.Timestamp("2026-01-01") + pd.Timedelta(days=random.randint(0, 179))
    rows.append({
        "order_id": f"ORD{i:06d}",
        "order_date": date.date(),
        "product": random.choice(products),
        "state": state,
        "city": city,
        "pin_code": pin,
        "quantity": random.randint(1, 5),
        "price": random.choice([49, 79, 99, 129, 149, 199, 249, 299]),
        "platform": random.choice(platforms),
        "latitude": lat + np.random.normal(0, 0.01),
        "longitude": lon + np.random.normal(0, 0.01),
    })

out = Path(__file__).resolve().parents[1] / "data"
out.mkdir(exist_ok=True)
pd.DataFrame(rows).to_csv(out / "orders.csv", index=False)
print(f"Generated {len(rows)} synthetic orders at {out / 'orders.csv'}")
