"""
Cold Outreach System — finds businesses and sends them personalized
sales emails offering our AI automation services.
"""
import os
import json
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROSPECTS_PATH = os.path.join(DATA_DIR, 'prospects.json')
OUTREACH_LOG = os.path.join(DATA_DIR, 'outreach_log.json')

SITE_URL = "https://businesses.aoeua.com"

# ─── Prospect database by niche ──────────────────
# These are generic role-based emails that work for outreach
NICHE_PROSPECTS = {
    "restaurants": {
        "roles": ["owner", "manager", "operations"],
        "pain": "Manual reservations, inventory waste, and slow customer service are killing your margins",
        "solution": "AI-powered reservation system, smart inventory tracking, and 24/7 chatbot",
        "page": f"{SITE_URL}/ai-restaurants/",
        "price": "$299/month"
    },
    "real-estate": {
        "roles": ["agent", "broker", "office manager"],
        "pain": "Spending hours on lead qualification and manual listing management",
        "solution": "AI lead scoring, automated listing updates, and smart property matching",
        "page": f"{SITE_URL}/ai-realestate/",
        "price": "$399/month"
    },
    "dental": {
        "roles": ["practice manager", "dentist", "office coordinator"],
        "pain": "No-shows, manual scheduling, and patient follow-up eating into your practice time",
        "solution": "AI appointment management, automated reminders, and patient engagement",
        "page": f"{SITE_URL}/ai-dentists/",
        "price": "$349/month"
    },
    "fitness": {
        "roles": ["gym owner", "studio manager", "fitness director"],
        "pain": "Member retention dropping, class scheduling chaos, and manual billing",
        "solution": "AI member engagement, smart scheduling, and automated billing",
        "page": f"{SITE_URL}/ai-fitness/",
        "price": "$249/month"
    },
    "legal": {
        "roles": ["attorney", "paralegal", "office manager"],
        "pain": "Drowning in paperwork, missed deadlines, and unbilled hours",
        "solution": "AI document processing, deadline tracking, and time capture",
        "page": f"{SITE_URL}/ai-lawyers/",
        "price": "$499/month"
    },
    "salon": {
        "roles": ["owner", "manager", "stylist"],
        "pain": "Last-minute cancellations, booking confusion, and no repeat customer system",
        "solution": "AI booking, automated reminders, and loyalty program automation",
        "page": f"{SITE_URL}/ai-salons/",
        "price": "$199/month"
    },
    "accounting": {
        "roles": ["CPA", "bookkeeper", "accountant"],
        "pain": "Tax season overwhelm, manual data entry, and client communication gaps",
        "solution": "AI data extraction, automated reports, and client portal",
        "page": f"{SITE_URL}/ai-accountants/",
        "price": "$399/month"
    },
    "ecommerce": {
        "roles": ["store owner", "marketing manager", "operations"],
        "pain": "Cart abandonment, inventory stockouts, and manual customer support",
        "solution": "AI abandoned cart recovery, smart inventory, and chatbot support",
        "page": f"{SITE_URL}/ai-ecommerce/",
        "price": "$349/month"
    },
    "construction": {
        "roles": ["contractor", "project manager", "estimator"],
        "pain": "Project delays, budget overruns, and scattered communication",
        "solution": "AI project tracking, cost estimation, and team coordination",
        "page": f"{SITE_URL}/ai-construction/",
        "price": "$449/month"
    },
    "photography": {
        "roles": ["photographer", "studio owner", "creative director"],
        "pain": "Booking admin, endless editing queues, and chasing payments",
        "solution": "AI booking, workflow automation, and invoice management",
        "page": f"{SITE_URL}/ai-photographers/",
        "price": "$199/month"
    },
}


def _generate_email_subject(niche_data):
    """Generate compelling email subject lines."""
    subjects = [
        "Quick question about your {niche} business",
        "Cut your admin time by 70% — here's how",
        "Is {pain_short} costing you money?",
        "AI is changing {niche} businesses — are you ready?",
        "[Free Demo] See how AI can automate your {niche}",
        "Other {niche} businesses are saving 20+ hours/week",
    ]
    niche = list(NICHE_PROSPECTS.keys())[0]  # default
    return random.choice(subjects).format(
        niche=niche,
        pain_short="manual work"
    )


def generate_outreach_email(niche_key, recipient_name="there"):
    """Generate a personalized cold outreach email for a specific niche."""
    niche = NICHE_PROSPECTS.get(niche_key, NICHE_PROSPECTS["restaurants"])

    subjects = [
        f"Quick question about your {niche_key} business",
        f"Is your {niche_key} business losing money to manual work?",
        f"How {niche_key} businesses are saving 20+ hours/week with AI",
        f"[Free Demo] AI automation for your {niche_key}",
    ]

    subject = random.choice(subjects)

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; font-family:'Segoe UI',Arial,sans-serif; background:#f9f9f9;">
<div style="max-width:600px; margin:20px auto; background:white; border-radius:8px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,0.1);">
    
    <div style="background:linear-gradient(135deg,#00d4ff,#7b2ff7); padding:20px 30px;">
        <h1 style="color:white; margin:0; font-size:1.4rem;">myAI</h1>
    </div>
    
    <div style="padding:30px; line-height:1.8; color:#333;">
        <p>Hi {recipient_name},</p>
        
        <p>{niche['pain']}.</p>
        
        <p>We built an AI solution specifically for {niche_key} businesses:</p>
        <p><strong>{niche['solution']}</strong></p>
        
        <ul style="color:#555;">
            <li>Set up in under 24 hours</li>
            <li>No technical knowledge required</li>
            <li>14-day free trial — no credit card</li>
            <li>Starting at just {niche['price']}</li>
        </ul>
        
        <p style="text-align:center; margin:25px 0;">
            <a href="{niche['page']}" style="background:linear-gradient(90deg,#00d4ff,#7b2ff7); color:white; padding:12px 30px; border-radius:50px; text-decoration:none; font-weight:600; font-size:1.05rem;">
                See It In Action →
            </a>
        </p>
        
        <p>Would you be open to a quick 10-minute demo this week?</p>
        
        <p>Best,<br>
        <strong>James</strong><br>
        <span style="color:#888;">myAI — AI Business Automation</span><br>
        <a href="https://aoeua.com/" style="color:#00d4ff;">aoeua.com</a>
        </p>
    </div>
    
    <div style="padding:15px 30px; background:#f5f5f5; text-align:center; font-size:0.8rem; color:#999;">
        <p>You received this because we think AI can help your business.</p>
        <p><a href="#" style="color:#00d4ff;">Unsubscribe</a></p>
    </div>
</div>
</body>
</html>"""

    return subject, html


def generate_all_outreach_templates():
    """Generate outreach email templates for all niches."""
    output_dir = os.path.join(BASE_DIR, 'output', 'outreach')
    os.makedirs(output_dir, exist_ok=True)

    templates = []
    for niche_key in NICHE_PROSPECTS:
        subject, html = generate_outreach_email(niche_key)
        
        # Save HTML template
        path = os.path.join(output_dir, f'outreach_{niche_key}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        templates.append({
            "niche": niche_key,
            "subject": subject,
            "template_path": path,
            "page_url": NICHE_PROSPECTS[niche_key]["page"],
            "price": NICHE_PROSPECTS[niche_key]["price"],
        })

    # Save template index
    index_path = os.path.join(output_dir, 'templates_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(templates, f, indent=2)

    print(f"[OUTREACH] Generated {len(templates)} email templates in output/outreach/")
    return templates


def send_outreach_campaign(niche_key, recipients):
    """
    Send outreach emails to a list of prospects for a specific niche.
    recipients: list of {"email": "...", "name": "..."} dicts
    """
    from agent.email_sender import send_email
    import time

    niche = NICHE_PROSPECTS.get(niche_key)
    if not niche:
        print(f"[OUTREACH] Unknown niche: {niche_key}")
        return {"sent": 0, "failed": 0}

    sent = 0
    failed = 0
    logs = _load_outreach_log()

    for r in recipients:
        email = r.get("email")
        name = r.get("name", "there")

        # Skip already contacted
        if email in [l.get("email") for l in logs]:
            print(f"[OUTREACH] Skipping {email} — already contacted")
            continue

        subject, html = generate_outreach_email(niche_key, recipient_name=name)
        ok = send_email(email, subject, html, to_name=name)

        log_entry = {
            "email": email,
            "name": name,
            "niche": niche_key,
            "subject": subject,
            "sent_at": datetime.now().isoformat(),
            "status": "sent" if ok else "failed"
        }
        logs.append(log_entry)

        if ok:
            sent += 1
        else:
            failed += 1

        time.sleep(3)  # Rate limit: 3 sec between emails

    _save_outreach_log(logs)
    print(f"[OUTREACH] Campaign {niche_key}: {sent} sent, {failed} failed")
    return {"sent": sent, "failed": failed}


def _load_outreach_log():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(OUTREACH_LOG):
        with open(OUTREACH_LOG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def _save_outreach_log(logs):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTREACH_LOG, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def get_outreach_stats():
    logs = _load_outreach_log()
    return {
        "total_sent": len([l for l in logs if l["status"] == "sent"]),
        "total_failed": len([l for l in logs if l["status"] == "failed"]),
        "niches_contacted": list(set(l.get("niche", "") for l in logs)),
        "last_sent": logs[-1]["sent_at"] if logs else None,
    }


if __name__ == "__main__":
    print("Generating outreach templates...")
    templates = generate_all_outreach_templates()
    for t in templates:
        print(f"  {t['niche']}: {t['subject']} ({t['price']})")
