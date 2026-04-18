"""
Outreach email to all prospects — SAP, Priority, Monday.com, M365, SharePoint & Automations.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent.email_sender import send_email

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
VERIFIED_FILE = os.path.join(DATA_DIR, 'verified_prospects.json')
PROSPECTS_FILE = os.path.join(DATA_DIR, 'real_prospects.json')
MANUFACTURER_FILE = os.path.join(DATA_DIR, 'manufacturer_prospects.json')


def build_html(name):
    return f"""
<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;border-radius:12px;overflow:hidden;border:1px solid #222;">
  <div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:2rem;text-align:center;">
    <h1 style="margin:0;color:#fff;font-size:1.8rem;">myAI — Business Automation</h1>
    <p style="color:rgba(255,255,255,.85);margin:.5rem 0 0;font-size:1rem;">SAP &bull; Priority &bull; Monday.com &bull; Microsoft 365 &bull; SharePoint</p>
  </div>
  <div style="padding:2rem;">
    <p style="font-size:1.05rem;color:#ccc;">Hi {name},</p>
    <p style="color:#aaa;line-height:1.7;">
      We help businesses like yours automate and streamline operations with expert integration services:
    </p>
    <table style="width:100%;border-collapse:collapse;margin:1.5rem 0;">
      <tr>
        <td style="padding:.8rem;background:#111;border:1px solid #222;border-radius:8px;text-align:center;width:33%;">
          <div style="font-size:1.8rem;">⚙️</div>
          <div style="color:#00d4ff;font-weight:600;margin-top:.3rem;">SAP</div>
          <div style="color:#888;font-size:.8rem;">ERP integration &amp; automation</div>
        </td>
        <td style="padding:.8rem;background:#111;border:1px solid #222;border-radius:8px;text-align:center;width:33%;">
          <div style="font-size:1.8rem;">📋</div>
          <div style="color:#00d4ff;font-weight:600;margin-top:.3rem;">Priority</div>
          <div style="color:#888;font-size:.8rem;">Full ERP customization</div>
        </td>
        <td style="padding:.8rem;background:#111;border:1px solid #222;border-radius:8px;text-align:center;width:33%;">
          <div style="font-size:1.8rem;">📅</div>
          <div style="color:#00d4ff;font-weight:600;margin-top:.3rem;">Monday.com</div>
          <div style="color:#888;font-size:.8rem;">Workflows &amp; automations</div>
        </td>
      </tr>
      <tr>
        <td style="padding:.8rem;background:#111;border:1px solid #222;border-radius:8px;text-align:center;" colspan="2">
          <div style="font-size:1.8rem;">☁️</div>
          <div style="color:#00d4ff;font-weight:600;margin-top:.3rem;">Microsoft 365 &amp; SharePoint</div>
          <div style="color:#888;font-size:.8rem;">Power Automate, Teams, Power Apps, document management</div>
        </td>
        <td style="padding:.8rem;background:#111;border:1px solid #222;border-radius:8px;text-align:center;">
          <div style="font-size:1.8rem;">⚡</div>
          <div style="color:#00d4ff;font-weight:600;margin-top:.3rem;">Automations</div>
          <div style="color:#888;font-size:.8rem;">Custom API &amp; RPA solutions</div>
        </td>
      </tr>
    </table>
    <p style="color:#aaa;line-height:1.7;">
      Whether you need to connect your existing systems, automate manual processes, or build custom dashboards &mdash;
      we deliver tailored solutions that save time and reduce costs.
    </p>
    <div style="text-align:center;margin:2rem 0;">
      <a href="https://aoeua.com/services.html"
         style="display:inline-block;padding:.9rem 2.5rem;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:#fff;text-decoration:none;border-radius:50px;font-weight:600;font-size:1rem;">
        See Our Services
      </a>
    </div>
    <p style="color:#888;font-size:.9rem;">
      Reply to this email or visit <a href="https://aoeua.com" style="color:#00d4ff;text-decoration:none;">aoeua.com</a> to learn more.
    </p>
  </div>
  <div style="background:#111;padding:1.2rem;text-align:center;color:#555;font-size:.8rem;border-top:1px solid #222;">
    myAI &mdash; Autonomous AI That Runs Your Business &bull;
    <a href="https://aoeua.com" style="color:#00d4ff;text-decoration:none;">aoeua.com</a>
  </div>
</div>
"""


def load_all_prospects():
    """Load ONLY verified prospects. Falls back to unverified if no verified file."""
    all_prospects = []
    seen_emails = set()

    # Prefer verified prospects file
    if os.path.exists(VERIFIED_FILE):
        print("[OUTREACH] Using VERIFIED prospects only")
        with open(VERIFIED_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for p in data:
            email = p.get('email', '').strip().lower()
            if email and email not in seen_emails:
                seen_emails.add(email)
                all_prospects.append({
                    'name': p.get('name', 'there'),
                    'email': email
                })
        return all_prospects

    # Fallback: unverified (but warn)
    print("[OUTREACH] WARNING: No verified prospects file found!")
    print("[OUTREACH] Run 'python email_verifier.py' first to verify emails")
    print("[OUTREACH] Using unverified list — expect bounces!")

    for filepath in [PROSPECTS_FILE, MANUFACTURER_FILE]:
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for p in data:
            email = p.get('email', '').strip().lower()
            if email and email not in seen_emails:
                seen_emails.add(email)
                all_prospects.append({
                    'name': p.get('name', 'there'),
                    'email': email
                })

    return all_prospects


def main():
    prospects = load_all_prospects()
    print(f"[OUTREACH] Total unique prospects with email: {len(prospects)}")

    if not prospects:
        print("[OUTREACH] No prospects found!")
        return

    subject = "Automate Your Business — SAP, Priority, Monday.com, M365 & SharePoint"

    import time
    sent = 0
    failed = 0

    for i, p in enumerate(prospects, 1):
        name = p['name'] if p['name'] and p['name'] != 'there' else 'there'
        html = build_html(name)
        ok = send_email(p['email'], subject, html, to_name=p['name'])
        if ok:
            sent += 1
        else:
            failed += 1
        print(f"  [{i}/{len(prospects)}] {'OK' if ok else 'FAIL'} -> {p['email']}")
        if i < len(prospects):
            time.sleep(3)  # rate limit

    print(f"\n[OUTREACH] Done! Sent: {sent}, Failed: {failed}")


if __name__ == '__main__':
    main()
