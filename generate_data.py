"""
Gera dataset fictício mas realista de e-commerce.
2 anos de dados diários, 120 produtos, 8 categorias.
Inclui sazonalidade, tendências, anomalias e variação de margem.
"""

import pandas as pd
import numpy as np
from datetime import date, timedelta
import json, os

np.random.seed(42)

# ── Configuração ──────────────────────────────────────
START_DATE = date(2023, 1, 1)
END_DATE   = date(2024, 12, 31)
dates      = [START_DATE + timedelta(days=i)
              for i in range((END_DATE - START_DATE).days + 1)]

CATEGORIES = {
    "Electronics":    {"products": 20, "avg_price": 189, "margin": 0.22, "volatility": 0.35},
    "Apparel":        {"products": 25, "avg_price": 67,  "margin": 0.48, "volatility": 0.25},
    "Home & Garden":  {"products": 18, "avg_price": 54,  "margin": 0.42, "volatility": 0.20},
    "Sports":         {"products": 15, "avg_price": 89,  "margin": 0.38, "volatility": 0.28},
    "Beauty":         {"products": 20, "avg_price": 45,  "margin": 0.55, "volatility": 0.18},
    "Books & Media":  {"products": 10, "avg_price": 24,  "margin": 0.32, "volatility": 0.15},
    "Food & Grocery": {"products": 8,  "avg_price": 32,  "margin": 0.28, "volatility": 0.22},
    "Toys & Games":   {"products": 4,  "avg_price": 48,  "margin": 0.40, "volatility": 0.45},
}

PRODUCT_NAMES = {
    "Electronics":   ["Wireless Earbuds Pro","Smart Watch X2","USB-C Hub 7-in-1","Bluetooth Speaker Mini","LED Desk Lamp","Webcam HD 1080p","Mechanical Keyboard","Gaming Mouse","Phone Stand Adjustable","Portable Charger 20k","Screen Protector Kit","Cable Organizer Set","WiFi Extender","Smart Plug 4-Pack","Dash Cam HD","Fitness Tracker Band","Tablet Stand","Laptop Cooling Pad","RGB LED Strip","Solar Power Bank"],
    "Apparel":       ["Classic Cotton Tee","Running Shorts Pro","Yoga Pants Women","Zip Hoodie Fleece","Compression Socks","Athletic Tank Top","Cycling Jersey","Trail Running Shoes","Waterproof Jacket","Casual Sneakers","Sports Bra High Impact","Swim Trunks Quick-Dry","Winter Gloves Touch","Baseball Cap UV","Thermal Base Layer","Workout Leggings","Crew Neck Sweatshirt","Ankle Socks 6-Pack","Rain Poncho Foldable","Sun Hat Wide Brim","Neck Gaiter Multi","Gym Bag Duffel","Resistance Bands Set","Cooling Towel Sport","Reflective Vest Run"],
    "Home & Garden": ["Bamboo Cutting Board","Stainless Measuring Cups","Cast Iron Skillet 10in","Herb Garden Kit","Compost Bin Counter","Water Filter Pitcher","Storage Ottoman","Shower Curtain Set","Blackout Curtains Pair","Non-Stick Pan Set","Vegetable Peeler Pro","Soap Dispenser Ceramic","Towel Set 6-Piece","Doormat Coir Natural","Plant Pots Set 3","Picture Hanging Kit","Drawer Organizer Set","Candle Set Soy"],
    "Sports":        ["Foam Roller Deep Tissue","Jump Rope Speed","Pull Up Bar Doorway","Ab Wheel Roller","Kettlebell 20lb","Yoga Mat Premium","Resistance Loop Bands","Push Up Bars Handles","Weight Plate 10lb","Balance Board Wobble","Agility Ladder 12ft","Dumbbell Set Adjustable","Boxing Gloves 12oz","Swim Goggles Anti-Fog"],
    "Beauty":        ["Vitamin C Serum 30ml","Retinol Night Cream","Hyaluronic Acid Toner","SPF 50 Sunscreen","Jade Face Roller","Charcoal Face Mask","Rose Hip Oil Pure","Collagen Eye Patches","Micellar Water 400ml","Tea Tree Cleanser","Peptide Eye Cream","Niacinamide Serum","Aloe Vera Gel","Exfoliating Scrub","Lip Balm Set 5","Makeup Remover Wipes","Sheet Mask 10-Pack","Brow Gel Clear","Setting Spray Matte","Gua Sha Stone"],
    "Books & Media": ["Data Science Handbook","Python for Beginners","Marketing Strategy 2024","Atomic Habits Journal","The E-Myth Revisited","Zero to One Paperback","Building a StoryBrand","Profit First Workbook","Never Split Difference","Good to Great Edition"],
    "Food & Grocery":["Whey Protein Chocolate","Collagen Peptides 500g","Matcha Powder Organic","MCT Oil 32oz","Electrolyte Powder Mix","Mushroom Coffee Blend","Protein Bars Box 12","Omega-3 Fish Oil 90ct"],
    "Toys & Games":  ["Strategy Board Game","STEM Robot Kit Kids","Puzzle 1000 Pieces","Card Game Family"],
}

# ── Gerar catálogo de produtos ─────────────────────────
products = []
pid = 1
for cat, cfg in CATEGORIES.items():
    names = PRODUCT_NAMES[cat]
    for i in range(cfg["products"]):
        base_price  = cfg["avg_price"] * np.random.uniform(0.5, 1.8)
        cost_ratio  = 1 - cfg["margin"] * np.random.uniform(0.7, 1.3)
        cost_ratio  = max(0.2, min(0.85, cost_ratio))
        launch_date = START_DATE + timedelta(days=np.random.randint(0, 180))
        products.append({
            "product_id":   f"P{pid:04d}",
            "product_name": names[i % len(names)],
            "category":     cat,
            "base_price":   round(base_price, 2),
            "cost":         round(base_price * cost_ratio, 2),
            "launch_date":  launch_date.isoformat(),
            "is_active":    np.random.random() > 0.08,
            "rating":       round(np.random.uniform(3.2, 5.0), 1),
            "review_count": np.random.randint(5, 1200),
            "supplier":     np.random.choice(["SupplierA","SupplierB","SupplierC","SupplierD"]),
        })
        pid += 1

df_products = pd.DataFrame(products)

# ── Gerar vendas diárias ───────────────────────────────
records = []

def seasonal_multiplier(d):
    """Sazonalidade realista de e-commerce."""
    month = d.month
    dow   = d.weekday()
    # Black Friday / Cyber Monday boost
    if d.month == 11 and d.day >= 24 and d.day <= 30:
        return 3.8
    if d.month == 12 and d.day <= 10:
        return 2.2
    # Q4 geral
    if month == 12: return 1.8
    if month == 11: return 1.5
    if month == 10: return 1.1
    # Volta às aulas
    if month == 8:  return 1.3
    if month == 9:  return 1.2
    # Verão lento
    if month in [6, 7]: return 0.75
    # Fim de semana tem mais compras
    weekend = 1.25 if dow >= 5 else 1.0
    return np.random.uniform(0.85, 1.15) * weekend

def trend_multiplier(d):
    """Tendência de crescimento ao longo do tempo."""
    days_elapsed = (d - START_DATE).days
    total_days   = (END_DATE - START_DATE).days
    return 1.0 + 0.45 * (days_elapsed / total_days)

for prod in products:
    if not prod["is_active"]:
        continue
    launch = date.fromisoformat(prod["launch_date"])
    base_demand = np.random.randint(2, 25)  # unidades/dia base

    for d in dates:
        if d < launch:
            continue

        season  = seasonal_multiplier(d)
        trend   = trend_multiplier(d)
        noise   = np.random.lognormal(0, 0.4)

        # Anomalia plantada: alguns produtos têm queda súbita
        anomaly = 1.0
        if prod["product_id"] in ["P0003","P0017","P0041","P0078"]:
            if date(2024, 3, 1) <= d <= date(2024, 3, 31):
                anomaly = 0.15  # queda de 85% — competitor entrou no mercado

        # Anomalia positiva: campanha bem-sucedida
        if prod["product_id"] in ["P0008","P0022","P0055"]:
            if date(2024, 6, 1) <= d <= date(2024, 6, 15):
                anomaly = 2.8

        qty = max(0, int(base_demand * season * trend * noise * anomaly))
        if qty == 0 and np.random.random() > 0.3:
            continue  # produto não vendeu nesse dia

        # Desconto dinâmico
        discount_pct = 0.0
        if d.month == 11 and d.day >= 24:
            discount_pct = np.random.choice([0.20, 0.25, 0.30, 0.40])
        elif np.random.random() < 0.12:
            discount_pct = np.random.choice([0.05, 0.10, 0.15])

        price    = prod["base_price"] * (1 - discount_pct)
        revenue  = round(qty * price, 2)
        cost     = round(qty * prod["cost"], 2)
        margin   = round(revenue - cost, 2)

        channel  = np.random.choice(
            ["Organic Search","Paid Ads","Email","Social Media","Direct","Referral"],
            p=[0.32, 0.28, 0.15, 0.12, 0.08, 0.05]
        )
        country  = np.random.choice(
            ["United States","United Kingdom","Canada","Australia","Germany","France","Netherlands"],
            p=[0.52, 0.16, 0.10, 0.08, 0.06, 0.05, 0.03]
        )
        returned = 1 if (np.random.random() < 0.04 and qty > 0) else 0

        records.append({
            "date":         d.isoformat(),
            "product_id":   prod["product_id"],
            "category":     prod["category"],
            "units_sold":   qty,
            "unit_price":   round(price, 2),
            "discount_pct": round(discount_pct * 100, 1),
            "revenue":      revenue,
            "cogs":         cost,
            "gross_margin": margin,
            "channel":      channel,
            "country":      country,
            "returned":     returned,
        })

df_sales = pd.DataFrame(records)

# ── Salvar ─────────────────────────────────────────────
os.makedirs("/home/claude/ecommerce-dashboard/data", exist_ok=True)
df_products.to_csv("/home/claude/ecommerce-dashboard/data/products.csv", index=False)
df_sales.to_csv("/home/claude/ecommerce-dashboard/data/sales.csv", index=False)

print(f"Produtos: {len(df_products)}")
print(f"Registros de vendas: {len(df_sales):,}")
print(f"Período: {df_sales['date'].min()} → {df_sales['date'].max()}")
print(f"Receita total: US$ {df_sales['revenue'].sum():,.0f}")
print(f"Margem total: US$ {df_sales['gross_margin'].sum():,.0f}")
print(f"Categorias: {df_sales['category'].nunique()}")
print(f"Canais: {df_sales['channel'].unique().tolist()}")
print(f"Países: {df_sales['country'].nunique()}")
print("\nTop 5 categorias por receita:")
print(df_sales.groupby('category')['revenue'].sum().sort_values(ascending=False).head())
