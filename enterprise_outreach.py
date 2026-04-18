"""
Enterprise Outreach — Send SAP/Priority/M365/Azure implementation proposals
to UK manufacturers found by manufacturer_finder.py.
"""
import json
import os
import sys
import time
import hashlib
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROSPECTS_FILE = os.path.join(BASE_DIR, "data", "manufacturer_prospects.json")
OUTREACH_LOG = os.path.join(BASE_DIR, "data", "enterprise_outreach_log.json")
CREDS_FILE = os.path.join(BASE_DIR, "credentials.json")

BATCH_SIZE = 50
DELAY_BETWEEN = 15  # seconds


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


def load_prospects():
    with open(PROSPECTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_outreach_log():
    if os.path.exists(OUTREACH_LOG):
        with open(OUTREACH_LOG, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_outreach_log(logs):
    os.makedirs(os.path.dirname(OUTREACH_LOG), exist_ok=True)
    with open(OUTREACH_LOG, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def build_enterprise_email(name, website, category="manufacturing"):
    """Build personalised enterprise implementation proposal email."""
    variant = int(hashlib.md5(website.encode()).hexdigest(), 16) % 3

    subjects = [
        f"{name} \u2014 still running production on spreadsheets?",
        f"How UK manufacturers like {name} are cutting costs 30% with ERP",
        f"{name}: free operations assessment \u2014 SAP, Priority & Microsoft 365",
    ]
    subject = subjects[variant]

    cat_display = category.replace("_", " ").replace("-", " ").title()

    body = f"""
<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;border-radius:12px;overflow:hidden">

<div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:20px 30px;text-align:center">
<h1 style="font-size:20px;font-weight:800;color:#fff;margin:0">Enterprise Solutions for UK Manufacturers</h1>
<p style="color:rgba(255,255,255,0.8);margin:5px 0 0;font-size:13px">SAP &middot; Priority ERP &middot; Microsoft 365 &middot; Azure &middot; Monday.com</p>
</div>

<div style="padding:30px">

<p style="font-size:15px;color:#ccc;margin-bottom:15px">Hi {name},</p>

<p style="color:#aaa;line-height:1.7;margin-bottom:15px;font-size:14px">
I noticed your {cat_display} business at <strong>{website}</strong> and wanted to reach out.
</p>

<p style="color:#aaa;line-height:1.7;margin-bottom:15px;font-size:14px">
We help UK manufacturers modernise their operations with enterprise software. If you're still relying on spreadsheets, disconnected systems, or outdated tools to manage production, inventory, or finance &mdash; we can help.
</p>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin-bottom:20px">
<h3 style="color:#00d4ff;margin-bottom:10px;font-size:14px">What We Implement</h3>
<table style="width:100%;font-size:13px;color:#ccc;border-collapse:collapse">
<tr><td style="padding:6px 0;border-bottom:1px solid #1a1a1a">&#127981; <strong>SAP Business One</strong></td><td style="padding:6px 0;border-bottom:1px solid #1a1a1a;color:#888">Full ERP &mdash; production, finance, inventory</td></tr>
<tr><td style="padding:6px 0;border-bottom:1px solid #1a1a1a">&#9889; <strong>Priority ERP</strong></td><td style="padding:6px 0;border-bottom:1px solid #1a1a1a;color:#888">Cloud-ready manufacturing ERP</td></tr>
<tr><td style="padding:6px 0;border-bottom:1px solid #1a1a1a">&#128203; <strong>Monday.com</strong></td><td style="padding:6px 0;border-bottom:1px solid #1a1a1a;color:#888">Project &amp; production tracking</td></tr>
<tr><td style="padding:6px 0;border-bottom:1px solid #1a1a1a">&#128193; <strong>SharePoint</strong></td><td style="padding:6px 0;border-bottom:1px solid #1a1a1a;color:#888">Document management &amp; intranet</td></tr>
<tr><td style="padding:6px 0;border-bottom:1px solid #1a1a1a">&#9729;&#65039; <strong>Microsoft 365</strong></td><td style="padding:6px 0;border-bottom:1px solid #1a1a1a;color:#888">Teams, Exchange, OneDrive</td></tr>
<tr><td style="padding:6px 0">&#128311; <strong>Azure</strong></td><td style="padding:6px 0;color:#888">Cloud infrastructure &amp; migration</td></tr>
</table>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin-bottom:20px">
<h3 style="color:#7b2ff7;margin-bottom:10px;font-size:14px">Why Manufacturers Choose Us</h3>
<ul style="list-style:none;padding:0;margin:0;font-size:13px">
<li style="color:#ccc;padding:4px 0">&#9989; UK-based team with manufacturing expertise</li>
<li style="color:#ccc;padding:4px 0">&#9989; Average 30% reduction in operational costs</li>
<li style="color:#ccc;padding:4px 0">&#9989; Implementation in 8-16 weeks (not months)</li>
<li style="color:#ccc;padding:4px 0">&#9989; Full training for your team included</li>
<li style="color:#ccc;padding:4px 0">&#9989; Data migration from any legacy system</li>
</ul>
</div>

<p style="color:#aaa;line-height:1.7;font-size:14px;margin-bottom:20px">
I'd love to offer you a <strong>free 30-minute operations assessment</strong> &mdash; no sales pitch, just an honest look at where technology could save you time and money.
</p>

<div style="text-align:center;margin:25px 0">
<a href="https://aoeua.com/enterprise-services.html" style="display:inline-block;padding:14px 36px;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:#fff;text-decoration:none;border-radius:50px;font-weight:700;font-size:15px">See Our Services &#8594;</a>
</div>

<div style="text-align:center;margin:10px 0">
<a href="https://aoeua.com/book-consultation.html" style="color:#00d4ff;font-size:13px;text-decoration:none">Book a free consultation call &#8594;</a>
</div>

<p style="color:#555;font-size:12px;line-height:1.6;margin-top:25px">
Simply reply to this email to get started, or visit our website for more details.
Not interested? Reply "stop" and we won't email again.
</p>

</div>

<div style="background:#111;padding:12px 30px;text-align:center;border-top:1px solid #222">
<span style="color:#555;font-size:11px">myAI | <a href="mailto:info@aoeua.com" style="color:#00d4ff;text-decoration:none">info@aoeua.com</a> | <a href="https://aoeua.com/enterprise-services.html" style="color:#00d4ff;text-decoration:none">aoeua.com</a></span>
</div>

</div>
"""
    return subject, body


def send_email(to_email, subject, html_body, creds):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"myAI Enterprise <{creds['email']}>"
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


def run(dry_run=False, batch=BATCH_SIZE):
    print("=" * 60)
    print("  ENTERPRISE OUTREACH \u2014 UK MANUFACTURERS")
    print(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"  Batch size: {batch}")
    print("=" * 60)

    prospects = load_prospects()
    creds = load_creds()
    logs = load_outreach_log()
    already_emailed = {log["to_email"].lower() for log in logs if "to_email" in log}

    eligible = [
        p for p in prospects
        if p.get("email")
        and p["email"].lower() not in already_emailed
    ]

    print(f"\n  Total manufacturer prospects: {len(prospects)}")
    print(f"  Already emailed: {len(already_emailed)}")
    print(f"  Eligible now: {len(eligible)}")
    print(f"  Will process: {min(len(eligible), batch)}")
    print()

    sent = 0
    failed = 0

    for prospect in eligible[:batch]:
        name = prospect.get("name", "there")
        email = prospect["email"]
        website = prospect.get("website", "your website")
        category = prospect.get("category", "manufacturing")
        idx = sent + failed + 1

        print(f"[{idx}/{min(len(eligible), batch)}] {name} \u2014 {email}")

        subject, html_body = build_enterprise_email(name, website, category)

        if dry_run:
            print(f"  \U0001f4e7 [DRY RUN] Would send: \"{subject}\"")
            logs.append({
                "to_email": email, "to_name": name, "website": website,
                "category": category, "status": "dry_run", "subject": subject,
                "timestamp": datetime.now().isoformat(), "campaign": "enterprise_v1",
            })
            sent += 1
        else:
            try:
                send_email(email, subject, html_body, creds)
                print(f"  \u2705 Sent to {email}")
                logs.append({
                    "to_email": email, "to_name": name, "website": website,
                    "category": category, "status": "sent", "subject": subject,
                    "timestamp": datetime.now().isoformat(), "campaign": "enterprise_v1",
                })
                sent += 1
                if sent < batch:
                    time.sleep(DELAY_BETWEEN)
            except Exception as e:
                print(f"  \u274c Failed: {e}")
                logs.append({
                    "to_email": email, "to_name": name, "website": website,
                    "category": category, "status": "failed", "error": str(e),
                    "timestamp": datetime.now().isoformat(), "campaign": "enterprise_v1",
                })
                failed += 1

        save_outreach_log(logs)

    print(f"\n{'=' * 60}")
    print(f"  RESULTS: Sent {sent}, Failed {failed}")
    print(f"  Log: {OUTREACH_LOG}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    b = BATCH_SIZE
    for arg in sys.argv:
        if arg.startswith("--batch"):
            try:
                b = int(sys.argv[sys.argv.index(arg) + 1])
            except (ValueError, IndexError):
                pass
    run(dry_run=dry, batch=b)
