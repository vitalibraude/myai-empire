"""
Payment Server — Handles Stripe Checkout Sessions and Webhooks.
Run: python server.py
Serves on http://localhost:4242
"""
import os
import json
import stripe
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load payment config
with open(os.path.join(BASE_DIR, "data", "payment_config.json")) as f:
    pay_config = json.load(f)

stripe.api_key = pay_config["secret_key"]

# Determine the live site URL (used for success/cancel redirects)
SITE_URL = os.environ.get("SITE_URL", "http://localhost:4242")


class PaymentHandler(SimpleHTTPRequestHandler):
    """Serves static files + handles Stripe API endpoints."""

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/checkout-success":
            self._serve_file("output/website/checkout-success.html")
        elif parsed.path == "/api/config":
            self._json_response({
                "publishableKey": pay_config["publishable_key"],
                "prices": {
                    "starter": pay_config["products"]["starter"]["stripe_price_id"],
                    "pro": pay_config["products"]["pro"]["stripe_price_id"],
                    "enterprise": pay_config["products"]["enterprise"]["stripe_price_id"],
                }
            })
        else:
            # Serve static files from output/website/
            if parsed.path == "/":
                self.path = "/index.html"
            self.directory = os.path.join(BASE_DIR, "output", "website")
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len else b""

        if parsed.path == "/api/create-checkout-session":
            self._handle_create_session(body)
        elif parsed.path == "/api/webhook":
            self._handle_webhook(body)
        else:
            self.send_error(404)

    def _handle_create_session(self, body):
        try:
            data = json.loads(body)
            plan = data.get("plan", "pro")
            email = data.get("email", "")

            price_id = pay_config["products"].get(plan, {}).get("stripe_price_id")
            if not price_id:
                self._json_response({"error": f"Unknown plan: {plan}"}, 400)
                return

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="subscription",
                line_items=[{"price": price_id, "quantity": 1}],
                subscription_data={"trial_period_days": 14},
                customer_email=email if email else None,
                success_url=SITE_URL + "/checkout-success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=SITE_URL + "/checkout.html",
            )

            # Log the session
            self._log_event("checkout_session_created", {
                "session_id": session.id,
                "plan": plan,
                "email": email,
            })

            self._json_response({"sessionId": session.id, "url": session.url})

        except Exception as e:
            self._json_response({"error": str(e)}, 500)

    def _handle_webhook(self, body):
        sig = self.headers.get("Stripe-Signature", "")
        webhook_secret = pay_config.get("webhook_secret", "")

        try:
            if webhook_secret and not webhook_secret.startswith("whsec_REPLACE"):
                event = stripe.Webhook.construct_event(body, sig, webhook_secret)
            else:
                event = json.loads(body)

            event_type = event.get("type", "")
            print(f"[WEBHOOK] {event_type}")

            if event_type == "checkout.session.completed":
                session = event["data"]["object"]
                self._log_event("payment_received", {
                    "customer_email": session.get("customer_email"),
                    "amount_total": session.get("amount_total"),
                    "currency": session.get("currency"),
                    "subscription_id": session.get("subscription"),
                    "status": "active",
                })
                self._update_revenue(session)

            elif event_type == "invoice.paid":
                invoice = event["data"]["object"]
                self._log_event("invoice_paid", {
                    "customer_email": invoice.get("customer_email"),
                    "amount_paid": invoice.get("amount_paid"),
                    "subscription_id": invoice.get("subscription"),
                })

            self._json_response({"received": True})

        except Exception as e:
            print(f"[WEBHOOK ERROR] {e}")
            self._json_response({"error": str(e)}, 400)

    def _update_revenue(self, session):
        """Update revenue report when a payment comes in."""
        rev_path = os.path.join(BASE_DIR, "data", "revenue_report.json")
        try:
            with open(rev_path) as f:
                rev = json.load(f)
        except Exception:
            rev = {"overview": {"lifetime_revenue": 0, "monthly_recurring_revenue": 0,
                                "active_subscriptions": 0, "total_transactions": 0},
                   "transactions": []}

        amount = (session.get("amount_total") or 0) / 100
        rev["overview"]["total_transactions"] += 1
        rev["overview"]["active_subscriptions"] += 1
        rev["overview"]["lifetime_revenue"] += amount
        rev["overview"]["monthly_recurring_revenue"] += amount
        rev["generated_at"] = datetime.now().isoformat()

        if "transactions" not in rev:
            rev["transactions"] = []
        rev["transactions"].append({
            "date": datetime.now().isoformat(),
            "email": session.get("customer_email"),
            "amount": amount,
            "type": "subscription",
            "status": "active",
        })

        with open(rev_path, "w") as f:
            json.dump(rev, f, indent=2)

    def _log_event(self, event_type, data):
        log_path = os.path.join(BASE_DIR, "data", "payment_events.json")
        events = []
        if os.path.exists(log_path):
            with open(log_path) as f:
                events = json.load(f)
        events.append({
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
        })
        with open(log_path, "w") as f:
            json.dump(events, f, indent=2)

    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _serve_file(self, rel_path):
        fpath = os.path.join(BASE_DIR, rel_path)
        if os.path.exists(fpath):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open(fpath, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def log_message(self, fmt, *args):
        print(f"[SERVER] {args[0]}")


def main():
    port = int(os.environ.get("PORT", 4242))
    server = HTTPServer(("0.0.0.0", port), PaymentHandler)
    print("=" * 50)
    print(f"  myAI Payment Server running on port {port}")
    print(f"  http://localhost:{port}")
    print(f"  Stripe mode: {pay_config['mode']}")
    print("=" * 50)
    server.serve_forever()


if __name__ == "__main__":
    main()
