"""
Client Onboarding Automation
============================
When a new client pays (via Stripe webhook), this system:
1. Sends a professional welcome email with next steps
2. Creates a client record in data/clients.json
3. Schedules the first deliverable
4. Sends an onboarding questionnaire

Run as part of the webhook handler or standalone.
"""
import json
import os
import smtplib
import ssl
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENTS_FILE = os.path.join(BASE_DIR, "data", "clients.json")
CREDS_FILE = os.path.join(BASE_DIR, "credentials.json")

PRODUCTS = {
    "guide": {"name": "AI Business Guide", "price": "£10", "delivery": "instant"},
    "audit_report": {"name": "Professional Website Audit", "price": "£49", "delivery": "24 hours"},
    "consultation": {"name": "Strategy Consultation", "price": "£99", "delivery": "book within 48h"},
    "prompt_pack": {"name": "500+ AI Business Prompts", "price": "£7", "delivery": "instant"},
    "starter": {"name": "Starter Plan", "price": "£29/mo", "delivery": "setup within 24h"},
    "pro": {"name": "Pro Plan", "price": "£79/mo", "delivery": "setup within 24h"},
    "enterprise": {"name": "Enterprise Plan", "price": "£199/mo", "delivery": "setup within 48h"},
}


def load_creds():
    with open(CREDS_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    email_cfg = raw.get("email", raw)
    return {
        "email": email_cfg.get("from_email", email_cfg.get("username", "")),
        "password": email_cfg.get("password", ""),
        "smtp_host": email_cfg.get("smtp_host", "smtp.gmail.com"),
        "smtp_port": int(email_cfg.get("smtp_port", 587)),
    }


def load_clients():
    if os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_clients(clients):
    os.makedirs(os.path.dirname(CLIENTS_FILE), exist_ok=True)
    with open(CLIENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(clients, f, indent=2, ensure_ascii=False)


def send_email(to_email, subject, html_body, creds):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"myAI <{creds['email']}>"
    msg["To"] = to_email
    msg["Reply-To"] = creds["email"]
    msg.attach(MIMEText(html_body, "html"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP(creds["smtp_host"], creds["smtp_port"], timeout=15) as server:
        server.ehlo()
        server.starttls(context=ctx)
        server.ehlo()
        server.login(creds["email"], creds["password"])
        server.sendmail(creds["email"], to_email, msg.as_string())
    return True


def build_welcome_email(client_name, product_key, client_email):
    """Build the welcome/onboarding email based on product purchased."""
    product = PRODUCTS.get(product_key, {"name": product_key, "price": "N/A", "delivery": "TBD"})

    if product_key in ("guide", "prompt_pack"):
        # Instant delivery products
        download_link = f"https://aoeua.com/{'guide-access' if product_key == 'guide' else 'prompt-pack'}.html"
        extra_section = f"""
        <div style="text-align:center;margin:24px 0">
        <a href="{download_link}" style="display:inline-block;padding:14px 36px;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:#fff;text-decoration:none;border-radius:50px;font-weight:700;font-size:16px">Access Your {product['name']} →</a>
        </div>
        """
    elif product_key == "audit_report":
        extra_section = """
        <div style="background:#111;border:1px solid #222;border-radius:12px;padding:20px;margin:20px 0">
        <h3 style="color:#00d4ff;margin-bottom:10px">📋 What Happens Next</h3>
        <ol style="color:#ccc;padding-left:20px;line-height:2">
        <li>We run a comprehensive AI audit of your website (takes ~2 hours)</li>
        <li>Our team reviews the automated findings and adds expert insights</li>
        <li>You receive your full report within 24 hours via email</li>
        <li>Free 15-minute call to walk through the results (optional)</li>
        </ol>
        </div>
        <p style="color:#aaa;font-size:14px">Please reply to this email with your website URL if you haven't already provided it.</p>
        """
    elif product_key == "consultation":
        extra_section = """
        <div style="background:#111;border:1px solid #222;border-radius:12px;padding:20px;margin:20px 0">
        <h3 style="color:#00d4ff;margin-bottom:10px">📋 Before Our Call</h3>
        <p style="color:#ccc;line-height:1.7">To make the most of your consultation, please reply with:</p>
        <ol style="color:#ccc;padding-left:20px;line-height:2">
        <li>Your website URL</li>
        <li>Your main business goal right now</li>
        <li>Your #1 challenge or frustration</li>
        <li>2-3 preferred time slots (UK time zone)</li>
        </ol>
        </div>
        <p style="color:#aaa;font-size:14px">We'll confirm your consultation time within 24 hours.</p>
        """
    else:
        # Subscription plans
        extra_section = """
        <div style="background:#111;border:1px solid #222;border-radius:12px;padding:20px;margin:20px 0">
        <h3 style="color:#00d4ff;margin-bottom:10px">📋 Onboarding Questionnaire</h3>
        <p style="color:#ccc;line-height:1.7">Please reply with answers to these questions so we can get started:</p>
        <ol style="color:#ccc;padding-left:20px;line-height:2">
        <li>Your website URL</li>
        <li>What does your business do? (1-2 sentences)</li>
        <li>Who is your target customer?</li>
        <li>What are your top 3 business goals for the next 90 days?</li>
        <li>Are there any competitors you admire?</li>
        <li>What's your current monthly marketing budget?</li>
        </ol>
        </div>
        <p style="color:#aaa;font-size:14px">Once we receive your answers, we'll begin setup within 24 hours.</p>
        """

    subject = f"Welcome to myAI — Your {product['name']} is Ready! 🚀"

    body = f"""
<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;border-radius:12px;overflow:hidden">

<div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:24px 30px;text-align:center">
<h1 style="font-size:24px;font-weight:800;color:#fff;margin:0">Welcome to myAI! 🎉</h1>
<p style="color:rgba(255,255,255,0.8);margin:5px 0 0;font-size:14px">Thank you for your purchase</p>
</div>

<div style="padding:30px">

<p style="font-size:16px;color:#ccc;margin-bottom:8px">Hi {client_name},</p>

<p style="color:#aaa;line-height:1.7;margin-bottom:20px">
Thank you for trusting myAI with your business growth. You've made a great decision — here's what to expect next.
</p>

<div style="background:#111;border:1px solid #222;border-radius:12px;padding:20px;margin:20px 0;text-align:center">
<p style="color:#888;font-size:13px;margin-bottom:8px">YOUR PURCHASE</p>
<h2 style="color:#fff;font-size:20px;margin-bottom:4px">{product['name']}</h2>
<p style="color:#00d4ff;font-size:18px;font-weight:700">{product['price']}</p>
<p style="color:#888;font-size:12px;margin-top:8px">Delivery: {product['delivery']}</p>
</div>

{extra_section}

<div style="background:#0d1117;border:1px solid #1a1a2e;border-radius:12px;padding:20px;margin:24px 0">
<h3 style="color:#7b2ff7;margin-bottom:10px;font-size:14px">💡 QUICK LINKS</h3>
<p style="margin:8px 0"><a href="https://aoeua.com/free-audit.html" style="color:#00d4ff;text-decoration:none">→ Free Website Audit Tool</a></p>
<p style="margin:8px 0"><a href="https://aoeua.com/ai-tools.html" style="color:#00d4ff;text-decoration:none">→ 300+ AI Tools Directory</a></p>
<p style="margin:8px 0"><a href="mailto:info@aoeua.com" style="color:#00d4ff;text-decoration:none">→ Email Support: info@aoeua.com</a></p>
</div>

<p style="color:#888;line-height:1.7;font-size:14px">
If you have any questions, just reply to this email. I personally read every message.
</p>

<p style="color:#ccc;margin-top:20px">
Best regards,<br>
<strong>The myAI Team</strong>
</p>

</div>

<div style="background:#111;padding:12px 30px;text-align:center;border-top:1px solid #222">
<span style="color:#555;font-size:11px">myAI | <a href="mailto:info@aoeua.com" style="color:#00d4ff;text-decoration:none">info@aoeua.com</a> | <a href="https://aoeua.com" style="color:#00d4ff;text-decoration:none">aoeua.com</a></span>
</div>

</div>
"""
    return subject, body


def onboard_client(client_email, client_name, product_key, stripe_session_id=None):
    """Full onboarding flow for a new client."""
    print(f"  🚀 Onboarding: {client_name} ({client_email}) — {product_key}")

    # 1. Create client record
    clients = load_clients()
    client_record = {
        "email": client_email,
        "name": client_name,
        "product": product_key,
        "status": "active",
        "onboarded_at": datetime.now().isoformat(),
        "stripe_session": stripe_session_id,
        "notes": [],
    }
    clients.append(client_record)
    save_clients(clients)
    print(f"  ✅ Client record created")

    # 2. Send welcome email
    creds = load_creds()
    subject, body = build_welcome_email(client_name, product_key, client_email)
    try:
        send_email(client_email, subject, body, creds)
        print(f"  ✅ Welcome email sent to {client_email}")
    except Exception as e:
        print(f"  ❌ Email failed: {e}")

    # 3. Notify ourselves
    try:
        product = PRODUCTS.get(product_key, {"name": product_key, "price": "?"})
        notify_subject = f"💰 NEW SALE: {product['name']} — {product['price']}"
        notify_body = f"""
        <h2>New Client!</h2>
        <p><strong>Name:</strong> {client_name}</p>
        <p><strong>Email:</strong> {client_email}</p>
        <p><strong>Product:</strong> {product['name']} ({product['price']})</p>
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <p><strong>Stripe Session:</strong> {stripe_session_id or 'N/A'}</p>
        """
        send_email(creds["email"], notify_subject, notify_body, creds)
        print(f"  ✅ Self-notification sent")
    except Exception as e:
        print(f"  ⚠️ Self-notification failed: {e}")

    return client_record


if __name__ == "__main__":
    # Test with a sample
    import sys
    if len(sys.argv) >= 4:
        onboard_client(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python client_onboarding.py <email> <name> <product_key>")
        print("Products:", list(PRODUCTS.keys()))
