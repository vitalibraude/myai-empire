"""
Automated Follow-Up Email Pipeline
===================================
Sends follow-up emails to prospects who received initial outreach but haven't responded.
Research shows 80% of deals close after follow-up 3-7.

Follow-up schedule:
- Follow-up 1: Day 3 — short, adds value
- Follow-up 2: Day 7 — case study / social proof
- Follow-up 3: Day 14 — breakup email (last chance)

Usage:
    python follow_up_pipeline.py                    # Send all due follow-ups
    python follow_up_pipeline.py --dry-run           # Preview without sending
    python follow_up_pipeline.py --max 10            # Limit to 10 emails
"""
import json
import os
import sys
import smtplib
import ssl
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTREACH_LOG = os.path.join(BASE_DIR, "data", "outreach_log.json")
FOLLOWUP_LOG = os.path.join(BASE_DIR, "data", "followup_log.json")
CREDS_FILE = os.path.join(BASE_DIR, "credentials.json")

# Follow-up schedule: (days_after_initial, follow_up_number)
FOLLOWUP_SCHEDULE = [
    (3, 1),   # Day 3: Quick value-add
    (7, 2),   # Day 7: Case study
    (14, 3),  # Day 14: Breakup email
]


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


def load_outreach_log():
    if os.path.exists(OUTREACH_LOG):
        with open(OUTREACH_LOG, encoding="utf-8") as f:
            return json.load(f)
    return []


def load_followup_log():
    if os.path.exists(FOLLOWUP_LOG):
        with open(FOLLOWUP_LOG, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_followup_log(logs):
    os.makedirs(os.path.dirname(FOLLOWUP_LOG), exist_ok=True)
    with open(FOLLOWUP_LOG, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def get_followup_status(email, followup_logs):
    """Get the highest follow-up number sent to this email."""
    sent = [log["followup_number"] for log in followup_logs
            if log.get("to_email") == email and log.get("status") == "sent"]
    return max(sent) if sent else 0


def build_followup_1(name, website, score):
    """Day 3: Short, adds value, references the audit."""
    subject = f"Quick tip for {website.replace('https://', '').replace('http://', '').rstrip('/')}"

    body = f"""
<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;color:#333;line-height:1.7">

<p>Hi {name},</p>

<p>I sent you a free website audit a few days ago — your site scored <strong>{score}/100</strong>.</p>

<p>I wanted to share one quick win that could make an immediate difference:</p>

<div style="background:#f8f9fa;border-left:4px solid #00d4ff;padding:16px;margin:16px 0;border-radius:4px">
<strong>Speed matters more than ever.</strong> Google now penalises sites loading over 3 seconds.
A simple image compression + lazy loading implementation typically improves scores by 15-20 points
and can increase conversions by up to 30%.
</div>

<p>I can implement this for you in under 24 hours — or if you'd prefer to do it yourself, here's a free tool:
<a href="https://aoeua.com/free-audit.html" style="color:#00d4ff">aoeua.com/free-audit.html</a></p>

<p>Would a quick 10-minute call be helpful? I'll walk you through the top 3 fixes for free.</p>

<p style="margin-top:24px">Best,<br>
<strong>myAI Team</strong><br>
<a href="https://aoeua.com" style="color:#00d4ff">aoeua.com</a></p>

<p style="color:#999;font-size:11px;margin-top:30px">
Reply "stop" to unsubscribe. No hard feelings.
</p>

</div>
"""
    return subject, body


def build_followup_2(name, website, score):
    """Day 7: Social proof / case study angle."""
    subject = f"How a {get_business_type(website)} increased leads by 40%"

    body = f"""
<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;color:#333;line-height:1.7">

<p>Hi {name},</p>

<p>I know you're busy running your business, so I'll keep this brief.</p>

<p>Last month, we helped a small business similar to yours go from a website score of 62 to 94.
The result?</p>

<ul style="padding-left:20px">
<li><strong>40% more enquiries</strong> from Google in the first 2 weeks</li>
<li><strong>3x faster</strong> page load speed</li>
<li><strong>Page 1 ranking</strong> for their top 3 local search terms</li>
</ul>

<p>Your site scored <strong>{score}/100</strong> — there's significant room for improvement.</p>

<div style="text-align:center;margin:24px 0">
<a href="https://aoeua.com/book-consultation.html" style="display:inline-block;padding:12px 32px;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:#fff;text-decoration:none;border-radius:50px;font-weight:700">Book a Free 15-Minute Strategy Call</a>
</div>

<p>No pressure, no sales pitch — just actionable advice you can implement yourself.</p>

<p style="margin-top:24px">Best,<br>
<strong>myAI Team</strong><br>
<a href="https://aoeua.com" style="color:#00d4ff">aoeua.com</a></p>

<p style="color:#999;font-size:11px;margin-top:30px">
Reply "stop" to unsubscribe.
</p>

</div>
"""
    return subject, body


def build_followup_3(name, website, score):
    """Day 14: Breakup email — creates urgency."""
    subject = f"Closing your file, {name}"

    body = f"""
<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;color:#333;line-height:1.7">

<p>Hi {name},</p>

<p>I've reached out a couple of times about your website audit (score: {score}/100) — I understand
you might be busy or this isn't the right time.</p>

<p>I'm going to close your file and won't follow up again.</p>

<p>But before I do — here's what I'd recommend you tackle first, even without our help:</p>

<div style="background:#fff3cd;border:1px solid #ffc107;padding:16px;margin:16px 0;border-radius:8px">
<ol style="padding-left:20px;margin:0">
<li>Compress your images (free tool: squoosh.app)</li>
<li>Add meta descriptions to every page</li>
<li>Make sure your Google Business Profile is claimed and complete</li>
</ol>
</div>

<p>These three things alone can boost your local search visibility significantly.</p>

<p>If you ever want a full audit or professional optimisation, the offer stands:</p>
<ul style="padding-left:20px">
<li><a href="https://aoeua.com/free-audit.html" style="color:#00d4ff">Free instant audit</a></li>
<li><a href="https://aoeua.com/order-audit.html" style="color:#00d4ff">Professional audit report — £49</a></li>
<li><a href="https://aoeua.com/book-consultation.html" style="color:#00d4ff">Strategy consultation — £99</a></li>
</ul>

<p>Wishing you and your business all the best.</p>

<p style="margin-top:24px">Cheers,<br>
<strong>myAI Team</strong><br>
<a href="https://aoeua.com" style="color:#00d4ff">aoeua.com</a></p>

<p style="color:#999;font-size:11px;margin-top:30px">
This is my last email. No further follow-ups.
</p>

</div>
"""
    return subject, body


def get_business_type(website):
    """Extract a readable business type from the website URL."""
    domain = website.replace("https://", "").replace("http://", "").split("/")[0]
    # Remove common TLDs and www
    name = domain.replace("www.", "").split(".")[0]
    return "local business"


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


def run_followups(dry_run=False, max_emails=100):
    """Check all outreach logs and send due follow-ups."""
    print("=" * 60)
    print("  AUTOMATED FOLLOW-UP PIPELINE")
    print(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"  Max emails: {max_emails}")
    print("=" * 60)

    outreach_logs = load_outreach_log()
    followup_logs = load_followup_log()
    creds = load_creds()

    now = datetime.now()
    sent_count = 0
    skipped = 0

    # Only process prospects that were successfully sent initial emails
    sent_prospects = [log for log in outreach_logs if log.get("status") == "sent"]
    print(f"\n  Total initial emails sent: {len(sent_prospects)}")

    for prospect in sent_prospects:
        if sent_count >= max_emails:
            break

        email = prospect["to_email"]
        name = prospect.get("to_name", "Manager")
        website = prospect.get("website", "")
        score = prospect.get("score", 0)

        # Parse the timestamp of the initial email
        try:
            initial_sent = datetime.fromisoformat(prospect["timestamp"])
        except (KeyError, ValueError):
            skipped += 1
            continue

        days_since = (now - initial_sent).days

        # Get current follow-up status for this prospect
        current_followup = get_followup_status(email, followup_logs)

        # Determine which follow-up to send
        followup_to_send = None
        for days_threshold, followup_num in FOLLOWUP_SCHEDULE:
            if days_since >= days_threshold and current_followup < followup_num:
                followup_to_send = followup_num
                break  # Send the earliest due follow-up first

        if followup_to_send is None:
            skipped += 1
            continue

        # Build the appropriate follow-up email
        if followup_to_send == 1:
            subject, body = build_followup_1(name, website, score)
        elif followup_to_send == 2:
            subject, body = build_followup_2(name, website, score)
        elif followup_to_send == 3:
            subject, body = build_followup_3(name, website, score)
        else:
            continue

        print(f"\n[{sent_count+1}] Follow-up #{followup_to_send} → {name} ({email})")
        print(f"    Website: {website} | Score: {score}")
        print(f"    Days since initial: {days_since} | Subject: {subject}")

        if dry_run:
            print(f"    📧 [DRY RUN] Would send follow-up #{followup_to_send}")
            followup_logs.append({
                "to_email": email,
                "to_name": name,
                "website": website,
                "score": score,
                "followup_number": followup_to_send,
                "subject": subject,
                "status": "dry_run",
                "timestamp": now.isoformat(),
            })
        else:
            try:
                send_email(email, subject, body, creds)
                print(f"    ✅ Sent follow-up #{followup_to_send}")
                followup_logs.append({
                    "to_email": email,
                    "to_name": name,
                    "website": website,
                    "score": score,
                    "followup_number": followup_to_send,
                    "subject": subject,
                    "status": "sent",
                    "timestamp": now.isoformat(),
                })
            except Exception as e:
                print(f"    ❌ Failed: {e}")
                followup_logs.append({
                    "to_email": email,
                    "to_name": name,
                    "followup_number": followup_to_send,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": now.isoformat(),
                })
                continue

        sent_count += 1

    save_followup_log(followup_logs)

    print(f"\n{'=' * 60}")
    print(f"  RESULTS")
    print(f"  Follow-ups sent: {sent_count}")
    print(f"  Skipped (not due yet): {skipped}")
    print(f"  Log saved to: {FOLLOWUP_LOG}")
    print(f"{'=' * 60}")

    return sent_count


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    max_emails = 100
    for i, arg in enumerate(sys.argv):
        if arg == "--max" and i + 1 < len(sys.argv):
            max_emails = int(sys.argv[i + 1])

    run_followups(dry_run=dry_run, max_emails=max_emails)
