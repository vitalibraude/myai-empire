"""Create a Stripe product for the digital guide - £10 one-time purchase."""
import stripe
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "data", "payment_config.json")

with open(config_path) as f:
    config = json.load(f)

stripe.api_key = config["secret_key"]

# Create the product
product = stripe.Product.create(
    name="AI Business Automation Guide",
    description="The complete guide to automating your business with AI — 10 chapters, actionable steps, real tools.",
)

# Create the price (£10 one-time)
price = stripe.Price.create(
    product=product.id,
    unit_amount=1000,  # £10.00 in pence
    currency="gbp",
)

print(f"Product ID: {product.id}")
print(f"Price ID: {price.id}")
print(f"Price: £10.00 GBP (one-time)")

# Save to config
config["products"]["guide"] = {
    "name": "AI Business Automation Guide",
    "price_cents": 1000,
    "currency": "gbp",
    "type": "one_time",
    "stripe_price_id": price.id,
    "stripe_product_id": product.id,
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print("Saved to payment_config.json")
