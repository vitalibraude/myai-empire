import stripe
import json
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

# Product 1: Done-for-you SEO Audit Report (£49)
audit_product = stripe.Product.create(
    name="Professional SEO Audit Report",
    description="Comprehensive 20-page SEO audit with actionable fixes, competitor analysis, and priority roadmap. Delivered within 24 hours.",
)
audit_price = stripe.Price.create(
    product=audit_product.id,
    unit_amount=4900,
    currency="gbp",
    metadata={"type": "one_time"}
)
print(f"Audit Report: product={audit_product.id}, price={audit_price.id}")

# Product 2: AI Consultation Call (£99)
consult_product = stripe.Product.create(
    name="AI Automation Consultation",
    description="60-minute 1-on-1 consultation call. We analyse your business, identify automation opportunities, and create a custom implementation plan.",
)
consult_price = stripe.Price.create(
    product=consult_product.id,
    unit_amount=9900,
    currency="gbp",
    metadata={"type": "one_time"}
)
print(f"Consultation: product={consult_product.id}, price={consult_price.id}")

# Update payment_config.json
with open("data/payment_config.json", "r") as f:
    config = json.load(f)

config["products"]["audit_report"] = {
    "name": "Professional SEO Audit Report",
    "price_cents": 4900,
    "currency": "gbp",
    "type": "one_time",
    "stripe_price_id": audit_price.id,
    "stripe_product_id": audit_product.id
}
config["products"]["consultation"] = {
    "name": "AI Automation Consultation",
    "price_cents": 9900,
    "currency": "gbp",
    "type": "one_time",
    "stripe_price_id": consult_price.id,
    "stripe_product_id": consult_product.id
}

with open("data/payment_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("payment_config.json updated")
print(f"\nAudit Report: £49 — {audit_price.id}")
print(f"Consultation: £99 — {consult_price.id}")
