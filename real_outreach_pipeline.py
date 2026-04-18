"""
Real Outreach Pipeline — the complete revenue-generating flow:
1. Load real prospects (from find_real_prospects.py)
2. Run website audit on each
3. Send personalized email with free audit report
4. Track everything

This is the script that actually makes money.
"""
import json
import os
import sys
import time
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from services.website_audit.audit_engine import run_audit, generate_html_report

PROSPECTS_FILE = os.path.join(BASE_DIR, "data", "real_prospects.json")
OUTREACH_LOG = os.path.join(BASE_DIR, "data", "outreach_log.json")
CREDS_FILE = os.path.join(BASE_DIR, "credentials.json")


def load_creds():
    with open(CREDS_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    email_cfg = raw.get("email", raw)
    return {
        "email": email_cfg.get("from_email", email_cfg.get("username", email_cfg.get("email", ""))),
        "password": email_cfg.get("password", ""),
        "smtp_host": email_cfg.get("smtp_host", "smtp.gmail.com"),
        "smtp_port": int(email_cfg.get("smtp_port", 587)),
    }


def load_prospects():
    with open(PROSPECTS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    # Flatten if dict
    if isinstance(data, dict):
        flat = []
        for niche, items in data.items():
            for item in items:
                item["niche"] = niche
                flat.append(item)
        return flat
    return data


def load_outreach_log():
    if os.path.exists(OUTREACH_LOG):
        with open(OUTREACH_LOG, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_outreach_log(logs):
    os.makedirs(os.path.dirname(OUTREACH_LOG), exist_ok=True)
    with open(OUTREACH_LOG, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def build_email(name, website, audit):
    """Build personalized HTML email with audit results."""
    score = audit.get("overall_score", 0)
    grade = audit.get("grade", "?")
    issues = audit.get("seo", {}).get("issues", [])
    warnings = audit.get("seo", {}).get("warnings", [])
    good = audit.get("seo", {}).get("good", [])
    load_time = audit.get("performance", {}).get("load_time", 0)

    color = "#00cc66" if score >= 80 else "#ffa500" if score >= 60 else "#ff4444"

    issues_html = ""
    for i in issues[:5]:
        issues_html += f'<li style="color:#ff6b6b;padding:6px 0;border-bottom:1px solid #1a1a1a">❌ {i}</li>'
    for w in warnings[:3]:
        issues_html += f'<li style="color:#ffa500;padding:6px 0;border-bottom:1px solid #1a1a1a">⚠️ {w}</li>'

    good_html = ""
    for g in good[:3]:
        good_html += f'<li style="color:#00cc66;padding:4px 0">✅ {g}</li>'

    # Personalize subject line based on score
    if score >= 80:
        subject = f"Your site scored {score}/100 — but here's how to get to 95+"
    elif score >= 60:
        subject = f"Your website scored {score}/100 — quick fixes could boost your rankings"
    else:
        subject = f"Your website scored {score}/100 — these issues are costing you customers"

    body = f"""
<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;border-radius:12px;overflow:hidden">

<div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:20px 30px;text-align:center">
<h1 style="font-size:22px;font-weight:800;color:#fff;margin:0">Your Free Website Audit</h1>
<p style="color:rgba(255,255,255,0.8);margin:5px 0 0;font-size:14px">AI-powered analysis of {website}</p>
</div>

<div style="padding:30px">

<p style="font-size:15px;color:#ccc;margin-bottom:15px">Hi {name},</p>

<p style="color:#aaa;line-height:1.7;margin-bottom:20px;font-size:14px">
I came across your business and ran a quick AI audit on your website. Here are the results — completely free, no strings attached.
</p>

<div style="text-align:center;margin:25px 0">
<div style="display:inline-block;width:110px;height:110px;border-radius:50%;border:5px solid {color};text-align:center;line-height:110px">
<span style="font-size:38px;font-weight:800;color:{color}">{score}</span>
</div>
<div style="color:#888;margin-top:8px;font-size:13px">Grade: <strong>{grade}</strong> | Load time: {load_time:.1f}s</div>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin-bottom:20px">
<h3 style="color:#ff6b6b;margin-bottom:8px;font-size:13px;text-transform:uppercase;letter-spacing:1px">Issues Found</h3>
<ul style="list-style:none;padding:0;margin:0;font-size:13px">
{issues_html}
</ul>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin-bottom:20px">
<h3 style="color:#00cc66;margin-bottom:8px;font-size:13px;text-transform:uppercase;letter-spacing:1px">What's Working</h3>
<ul style="list-style:none;padding:0;margin:0;font-size:13px">
{good_html}
</ul>
</div>

<p style="color:#aaa;line-height:1.7;font-size:14px;margin-bottom:20px">
These issues may be hurting your Google rankings and costing you potential customers. Most can be fixed quickly.
</p>

<div style="text-align:center;margin:25px 0">
<a href="https://aoeua.com/order.html" style="display:inline-block;padding:14px 36px;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:#fff;text-decoration:none;border-radius:50px;font-weight:700;font-size:15px">Fix My Website — From £49</a>
</div>

<p style="color:#555;font-size:12px;line-height:1.6;margin-top:25px">
This audit was generated by myAI. No signup needed, your data is not stored.
Reply to this email for a detailed report or to ask questions.
Not interested? Reply "stop" and we won't email again.
</p>

</div>

<div style="background:#111;padding:12px 30px;text-align:center;border-top:1px solid #222">
<span style="color:#555;font-size:11px">myAI | <a href="mailto:info@aoeua.com" style="color:#00d4ff;text-decoration:none">info@aoeua.com</a> | <a href="https://aoeua.com" style="color:#00d4ff;text-decoration:none">aoeua.com</a></span>
</div>

</div>
"""
    return subject, body


def send_email(to_email, subject, html_body, creds):
    """Send a single email via SMTP."""
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


def run_pipeline(dry_run=False, max_emails=10):
    """Run the full pipeline: audit → email → track."""
    print("=" * 60)
    print("  REAL OUTREACH PIPELINE")
    print(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"  Max emails: {max_emails}")
    print("=" * 60)

    # Load data
    prospects = load_prospects()
    creds = load_creds()
    logs = load_outreach_log()
    already_emailed = {log["to_email"] for log in logs if "to_email" in log}

    # Filter: only prospects with email + website, not yet emailed
    eligible = [
        p for p in prospects
        if p.get("email") and p.get("website") and p["email"] not in already_emailed
    ]

    print(f"\n  Total prospects: {len(prospects)}")
    print(f"  Already emailed: {len(already_emailed)}")
    print(f"  Eligible now: {len(eligible)}")
    print(f"  Will process: {min(len(eligible), max_emails)}")
    print()

    sent = 0
    failed = 0

    for prospect in eligible[:max_emails]:
        name = prospect.get("name", "Manager")
        email = prospect["email"]
        website = prospect["website"]
        niche = prospect.get("niche", "general")

        print(f"[{sent+failed+1}/{min(len(eligible), max_emails)}] {name} — {website}")

        # Step 1: Audit
        try:
            audit = run_audit(website)
            if "error" in audit and "overall_score" not in audit:
                print(f"  ❌ Audit failed: {audit.get('error')}")
                logs.append({
                    "to_email": email,
                    "to_name": name,
                    "website": website,
                    "niche": niche,
                    "status": "audit_failed",
                    "error": audit.get("error"),
                    "timestamp": datetime.now().isoformat(),
                })
                failed += 1
                continue

            score = audit.get("overall_score", 0)
            grade = audit.get("grade", "?")
            print(f"  📊 Score: {score}/100 (Grade: {grade})")

            # Save audit report
            safe_name = website.replace("https://", "").replace("http://", "").replace("/", "_").rstrip("_")
            report_path = os.path.join(BASE_DIR, "output", "audits", f"audit_{safe_name}.html")
            generate_html_report(audit, report_path)

        except Exception as e:
            print(f"  ❌ Audit error: {e}")
            failed += 1
            continue

        # Step 2: Build email
        subject, html_body = build_email(name, website, audit)

        # Step 3: Send (or dry run)
        if dry_run:
            print(f"  📧 [DRY RUN] Would send to {email}: \"{subject}\"")
            logs.append({
                "to_email": email,
                "to_name": name,
                "website": website,
                "niche": niche,
                "score": score,
                "grade": grade,
                "status": "dry_run",
                "subject": subject,
                "timestamp": datetime.now().isoformat(),
            })
            sent += 1
        else:
            try:
                send_email(email, subject, html_body, creds)
                print(f"  ✅ Sent to {email}")
                logs.append({
                    "to_email": email,
                    "to_name": name,
                    "website": website,
                    "niche": niche,
                    "score": score,
                    "grade": grade,
                    "status": "sent",
                    "subject": subject,
                    "timestamp": datetime.now().isoformat(),
                })
                sent += 1
                time.sleep(3)  # Rate limit: 1 email per 3 seconds
            except Exception as e:
                print(f"  ❌ Send failed: {e}")
                logs.append({
                    "to_email": email,
                    "to_name": name,
                    "website": website,
                    "niche": niche,
                    "score": score,
                    "grade": grade,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                })
                failed += 1

        save_outreach_log(logs)

    print(f"\n{'=' * 60}")
    print(f"  RESULTS: {sent} sent, {failed} failed")
    print(f"  Log saved to: {OUTREACH_LOG}")
    print(f"{'=' * 60}")

    return sent, failed


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Real outreach pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually send emails")
    parser.add_argument("--max", type=int, default=10, help="Max emails to send")
    args = parser.parse_args()

    run_pipeline(dry_run=args.dry_run, max_emails=args.max)
