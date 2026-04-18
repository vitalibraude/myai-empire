"""Create Stripe products and update payment config."""
import stripe
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load keys from config
config_path = os.path.join(BASE_DIR, "data", "payment_config.json")
with open(config_path) as f:
    config = json.load(f)

stripe.api_key = config["secret_key"]

products_to_create = [
    {"key": "starter", "name": "myAI Starter", "price": 39900, "desc": "AI-powered business automation - Starter plan"},
    {"key": "pro", "name": "myAI Pro", "price": 99900, "desc": "AI-powered business automation - Pro plan (Most Popular)"},
    {"key": "enterprise", "name": "myAI Enterprise", "price": 249900, "desc": "AI-powered business automation - Enterprise plan"},
]

print("Creating Stripe products...")
for p in products_to_create:
    product = stripe.Product.create(name=p["name"], description=p["desc"])
    price = stripe.Price.create(
        product=product.id,
        unit_amount=p["price"],
        currency="usd",
        recurring={"interval": "month"},
    )
    config["products"][p["key"]]["stripe_price_id"] = price.id
    config["products"][p["key"]]["stripe_product_id"] = product.id
    print(f"  OK {p['name']}: price_id={price.id}")

# Save updated config
with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print(f"\nConfig saved to {config_path}")
print("Done! All 3 products created in Stripe.")
