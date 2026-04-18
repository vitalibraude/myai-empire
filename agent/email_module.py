import os
import json
from datetime import datetime

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'emails')
EMAILS_LOG = os.path.join(os.path.dirname(__file__), '..', 'data', 'emails_log.json')


def ensure_dirs():
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(EMAILS_LOG), exist_ok=True)


def create_email_template(template_name, subject, body_html):
    ensure_dirs()
    template = {
        "name": template_name,
        "subject": subject,
        "body": body_html,
        "created": datetime.now().isoformat()
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
</head>
<body style="margin:0; padding:0; background:#0a0a0a; font-family:'Segoe UI',Tahoma,sans-serif;">
    <div style="max-width:600px; margin:0 auto; background:#111; border-radius:12px; overflow:hidden; margin-top:20px; margin-bottom:20px;">
        <div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7); padding:2rem; text-align:center;">
            <h1 style="color:white; margin:0; font-size:1.8rem;">&#x1F916; myAI</h1>
        </div>
        <div style="padding:2rem; color:#e0e0e0; line-height:1.8;">
            {body_html}
        </div>
        <div style="padding:1.5rem 2rem; background:#0d0d0d; text-align:center; color:#555; font-size:0.85rem;">
            <p>Sent automatically by myAI</p>
            <p>To unsubscribe — <a href="#" style="color:#00d4ff;">click here</a></p>
        </div>
    </div>
</body>
</html>"""

    path = os.path.join(TEMPLATES_DIR, f'{template_name}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    templates = load_templates()
    templates.append(template)
    save_templates(templates)
    return path


def load_templates():
    meta_file = os.path.join(TEMPLATES_DIR, 'templates.json')
    if not os.path.exists(meta_file):
        return []
    with open(meta_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_templates(templates):
    ensure_dirs()
    meta_file = os.path.join(TEMPLATES_DIR, 'templates.json')
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(templates, f, indent=2)


def log_email(to, template_name, subject):
    ensure_dirs()
    logs = []
    if os.path.exists(EMAILS_LOG):
        with open(EMAILS_LOG, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    logs.append({
        "to": to,
        "template": template_name,
        "subject": subject,
        "sent_at": datetime.now().isoformat(),
        "status": "simulated"
    })
    with open(EMAILS_LOG, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2)


def generate_default_templates():
    ensure_dirs()
    templates_created = []

    path = create_email_template(
        "welcome",
        "Welcome to myAI! 🚀",
        """
        <h2 style="color:#00d4ff; margin-top:0;">Welcome aboard!</h2>
        <p>Thanks for joining myAI. We're thrilled to have you.</p>
        <p>Here's what you can do right now:</p>
        <ul style="color:#a0a0a0;">
            <li>&#x1F916; Set up your first AI agent</li>
            <li>&#x1F310; View the website built for you</li>
            <li>&#x1F4CA; Track your automated reports</li>
            <li>&#x1F3AC; Explore video marketing tools</li>
        </ul>
        <p>Your 14-day free trial is active. No credit card needed.</p>
        <p style="text-align:center; margin-top:2rem;">
            <a href="#" style="background:linear-gradient(90deg,#00d4ff,#7b2ff7); color:white; padding:0.8rem 2rem; border-radius:50px; text-decoration:none; font-weight:600;">
                Get Started Now
            </a>
        </p>
        """
    )
    templates_created.append(path)

    path = create_email_template(
        "weekly_report",
        "Your Weekly myAI Report 📊",
        """
        <h2 style="color:#00d4ff; margin-top:0;">Weekly Summary</h2>
        <p>Here's what your AI accomplished this week:</p>
        <div style="background:#1a1a1a; padding:1.5rem; border-radius:8px; margin:1rem 0;">
            <p>&#x1F4C8; <strong style="color:#00d4ff;">Tasks Completed:</strong> {{tasks_completed}}</p>
            <p>&#x1F465; <strong style="color:#00d4ff;">New Leads:</strong> {{new_leads}}</p>
            <p>&#x1F4DD; <strong style="color:#00d4ff;">Content Published:</strong> {{content_published}}</p>
            <p>&#x1F310; <strong style="color:#00d4ff;">Website Visitors:</strong> {{site_visits}}</p>
            <p>&#x1F3AC; <strong style="color:#00d4ff;">Videos Scripted:</strong> {{videos_scripted}}</p>
            <p>&#x1F4F1; <strong style="color:#00d4ff;">Social Posts:</strong> {{social_posts}}</p>
        </div>
        <p style="color:#888;">Full report available in your admin dashboard.</p>
        """
    )
    templates_created.append(path)

    path = create_email_template(
        "new_lead",
        "New Lead Captured! 🎯",
        """
        <h2 style="color:#00d4ff; margin-top:0;">New Lead!</h2>
        <p>A new inquiry was received through your website:</p>
        <div style="background:#1a1a1a; padding:1.5rem; border-radius:8px; margin:1rem 0;">
            <p>&#x1F464; <strong>Name:</strong> {{lead_name}}</p>
            <p>&#x1F4E7; <strong>Email:</strong> {{lead_email}}</p>
            <p>&#x1F4F1; <strong>Phone:</strong> {{lead_phone}}</p>
            <p>&#x1F3AF; <strong>Interest:</strong> {{lead_interest}}</p>
            <p>&#x1F4AC; <strong>Message:</strong> {{lead_message}}</p>
        </div>
        <p style="text-align:center; margin-top:2rem;">
            <a href="#" style="background:linear-gradient(90deg,#00d4ff,#7b2ff7); color:white; padding:0.8rem 2rem; border-radius:50px; text-decoration:none; font-weight:600;">
                View in CRM
            </a>
        </p>
        """
    )
    templates_created.append(path)

    return templates_created
