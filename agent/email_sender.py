"""
Real Email Sender — sends actual emails via SMTP using credentials.json.
Supports HTML templates, bulk sending, and delivery tracking.
"""
import os
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_PATH = os.path.join(BASE_DIR, 'credentials.json')
DATA_DIR = os.path.join(BASE_DIR, 'data')
SENT_LOG = os.path.join(DATA_DIR, 'emails_sent.json')


def _load_creds():
    with open(CREDS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)['email']


def _load_sent_log():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(SENT_LOG):
        with open(SENT_LOG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def _save_sent_log(logs):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SENT_LOG, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def test_connection():
    """Test SMTP connection. Returns True if successful."""
    creds = _load_creds()
    print(f"[EMAIL] Testing SMTP connection to {creds['smtp_host']}:{creds['smtp_port']}...")
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(creds['smtp_host'], creds['smtp_port'], timeout=15) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(creds['username'], creds['password'])
            print(f"[EMAIL] Connection successful! Logged in as {creds['username']}")
            return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"[EMAIL] Authentication FAILED: {e}")
        print("[EMAIL] If using Gmail, you need an App Password:")
        print("        1. Go to https://myaccount.google.com/security")
        print("        2. Enable 2-Step Verification")
        print("        3. Create App Password for 'Mail'")
        return False
    except Exception as e:
        print(f"[EMAIL] Connection error: {e}")
        return False


def send_email(to_email, subject, html_body, to_name=""):
    """Send a single email. Returns True if sent successfully."""
    creds = _load_creds()
    
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{creds['from_name']} <{creds['from_email']}>"
    msg['To'] = f"{to_name} <{to_email}>" if to_name else to_email
    msg['Subject'] = subject
    msg['Reply-To'] = creds['from_email']

    # Plain text fallback
    plain = subject
    msg.attach(MIMEText(plain, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(creds['smtp_host'], creds['smtp_port'], timeout=15) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(creds['username'], creds['password'])
            server.sendmail(creds['from_email'], to_email, msg.as_string())

        # Log success
        logs = _load_sent_log()
        logs.append({
            "to": to_email,
            "to_name": to_name,
            "subject": subject,
            "sent_at": datetime.now().isoformat(),
            "status": "sent"
        })
        _save_sent_log(logs)
        print(f"[EMAIL] Sent to {to_email}: {subject}")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f"[EMAIL] Auth failed — check credentials or use App Password")
        return False
    except Exception as e:
        logs = _load_sent_log()
        logs.append({
            "to": to_email,
            "subject": subject,
            "sent_at": datetime.now().isoformat(),
            "status": "failed",
            "error": str(e)
        })
        _save_sent_log(logs)
        print(f"[EMAIL] Failed to send to {to_email}: {e}")
        return False


def send_bulk(recipients, subject, html_body, delay_seconds=2):
    """
    Send emails to a list of recipients.
    recipients: list of {"email": "...", "name": "..."} dicts
    """
    import time
    sent = 0
    failed = 0

    print(f"[EMAIL] Starting bulk send: {len(recipients)} recipients")
    for r in recipients:
        email = r.get("email", r) if isinstance(r, dict) else r
        name = r.get("name", "") if isinstance(r, dict) else ""

        ok = send_email(email, subject, html_body, to_name=name)
        if ok:
            sent += 1
        else:
            failed += 1

        if delay_seconds > 0:
            time.sleep(delay_seconds)

    print(f"[EMAIL] Bulk send complete: {sent} sent, {failed} failed")
    return {"sent": sent, "failed": failed}


def get_send_stats():
    """Get email sending statistics."""
    logs = _load_sent_log()
    sent = len([l for l in logs if l.get("status") == "sent"])
    failed = len([l for l in logs if l.get("status") == "failed"])
    return {
        "total_sent": sent,
        "total_failed": failed,
        "total_attempts": len(logs),
        "last_sent": logs[-1]["sent_at"] if logs else None,
    }


if __name__ == "__main__":
    test_connection()
