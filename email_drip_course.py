"""
Email Drip Course — 5-Day Free "Website Growth" Email Course
=============================================================
Lead magnet that captures emails and delivers value over 5 days.
Each email builds trust and sells the paid audit/consultation.

Day 1: Your Website Score + Quick Wins
Day 2: The SEO Checklist (Top 5 Fixes)
Day 3: How to Get More Google Reviews
Day 4: AI Tools That Save 10 Hours/Week
Day 5: The Full Growth Plan + Special Offer

Usage:
  python email_drip_course.py --send-day 1 --to "email@example.com" --name "John"
  python email_drip_course.py --send-all-due  (checks drip_subscribers.json, sends due emails)
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
SUBSCRIBERS_FILE = os.path.join(BASE_DIR, "data", "drip_subscribers.json")
CREDS_FILE = os.path.join(BASE_DIR, "credentials.json")


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


def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_subscribers(subs):
    os.makedirs(os.path.dirname(SUBSCRIBERS_FILE), exist_ok=True)
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(subs, f, indent=2, ensure_ascii=False)


def add_subscriber(email, name="there"):
    subs = load_subscribers()
    if any(s["email"].lower() == email.lower() for s in subs):
        print(f"  Already subscribed: {email}")
        return False
    subs.append({
        "email": email,
        "name": name,
        "subscribed": datetime.now().isoformat(),
        "last_day_sent": 0,
        "status": "active",
    })
    save_subscribers(subs)
    print(f"  Added subscriber: {email}")
    return True


DRIP_EMAILS = {
    1: {
        "subject": "Day 1: Your Website Growth Journey Starts Here",
        "body": lambda name: f"""
<div style="font-family:'Segoe UI',sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;border-radius:12px;overflow:hidden">
<div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:20px 30px;text-align:center">
<h1 style="font-size:20px;color:#fff;margin:0">Day 1 of 5: Quick Wins</h1>
<p style="color:rgba(255,255,255,0.8);margin:5px 0 0;font-size:13px">Your free website growth course</p>
</div>
<div style="padding:30px">
<p style="color:#ccc;font-size:15px">Hi {name},</p>
<p style="color:#aaa;line-height:1.7">Welcome to the 5-day Website Growth Course. Over the next 5 days, I'll show you exactly how to get more customers from your website — for free.</p>
<p style="color:#aaa;line-height:1.7">Let's start with <strong style="color:#00d4ff">3 quick wins</strong> you can implement today:</p>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:8px">Quick Win #1: Fix Your Title Tags</h3>
<p style="color:#aaa;font-size:13px;margin:0">Your title tag is what shows in Google search results. Change it from something generic like "Home" to something keyword-rich like "Emergency Plumber in London | 24/7 | Free Quotes".</p>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:8px">Quick Win #2: Add Your Phone Number to Every Page</h3>
<p style="color:#aaa;font-size:13px;margin:0">Make it clickable on mobile. Put it in the header AND footer. The easier you make it to contact you, the more calls you'll get.</p>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:8px">Quick Win #3: Compress Your Images</h3>
<p style="color:#aaa;font-size:13px;margin:0">Go to tinypng.com, upload your website images, download the compressed versions. This alone can make your site 2x faster.</p>
</div>

<p style="color:#aaa;line-height:1.7;margin-top:20px"><strong style="color:#fff">Your homework:</strong> Check your current website score with our <a href="https://aoeua.com/free-audit.html" style="color:#00d4ff">free audit tool</a>. It takes 30 seconds and shows you exactly what to fix.</p>

<p style="color:#aaa;line-height:1.7">Tomorrow, I'll share the SEO checklist that helped one business go from page 5 to page 1 on Google.</p>

<p style="color:#888;font-size:13px;margin-top:25px">— The myAI Team<br><a href="https://aoeua.com" style="color:#00d4ff">aoeua.com</a></p>
</div>
<div style="background:#111;padding:12px 30px;text-align:center;border-top:1px solid #222">
<span style="color:#555;font-size:11px">You're receiving this because you signed up for the free Website Growth Course. <a href="mailto:info@aoeua.com?subject=Unsubscribe" style="color:#666">Unsubscribe</a></span>
</div>
</div>"""
    },
    2: {
        "subject": "Day 2: The 5-Point SEO Checklist That Actually Works",
        "body": lambda name: f"""
<div style="font-family:'Segoe UI',sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;border-radius:12px;overflow:hidden">
<div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:20px 30px;text-align:center">
<h1 style="font-size:20px;color:#fff;margin:0">Day 2 of 5: SEO Checklist</h1>
<p style="color:rgba(255,255,255,0.8);margin:5px 0 0;font-size:13px">Your free website growth course</p>
</div>
<div style="padding:30px">
<p style="color:#ccc;font-size:15px">Hi {name},</p>
<p style="color:#aaa;line-height:1.7">Yesterday was about quick wins. Today, let's talk about the SEO fundamentals that actually move the needle.</p>
<p style="color:#aaa;line-height:1.7">Forget the complicated stuff. These 5 things account for <strong style="color:#00d4ff">80% of local SEO results</strong>:</p>

<div style="background:#111;border-left:4px solid #00d4ff;padding:12px 16px;margin:10px 0;color:#ccc;font-size:14px">
<strong>1.</strong> Claim your Google Business Profile (free, takes 10 min)<br>
<strong>2.</strong> Get 10 Google reviews from happy customers<br>
<strong>3.</strong> Add your city name to title tags and headings<br>
<strong>4.</strong> Create a page for each service you offer<br>
<strong>5.</strong> List your business on 5 online directories (Yell, Thomson, etc.)
</div>

<p style="color:#aaa;line-height:1.7;margin-top:15px">That's it. Seriously. Do these 5 things and you'll outrank 90% of local competitors who haven't bothered.</p>

<p style="color:#aaa;line-height:1.7"><strong style="color:#fff">Real result:</strong> A Bristol dentist went from invisible to position #3 for "dentist Bristol" by doing exactly these 5 things. It took 6 weeks.</p>

<p style="color:#aaa;line-height:1.7"><strong style="color:#fff">Your homework:</strong> If you haven't claimed your Google Business Profile, do it today at <a href="https://business.google.com" style="color:#00d4ff">business.google.com</a>.</p>

<p style="color:#aaa;line-height:1.7">Tomorrow: How to get Google reviews (without being awkward about it).</p>

<p style="color:#888;font-size:13px;margin-top:25px">— The myAI Team<br><a href="https://aoeua.com" style="color:#00d4ff">aoeua.com</a></p>
</div>
<div style="background:#111;padding:12px 30px;text-align:center;border-top:1px solid #222">
<span style="color:#555;font-size:11px"><a href="mailto:info@aoeua.com?subject=Unsubscribe" style="color:#666">Unsubscribe</a></span>
</div>
</div>"""
    },
    3: {
        "subject": "Day 3: How to Get Google Reviews (The Non-Awkward Way)",
        "body": lambda name: f"""
<div style="font-family:'Segoe UI',sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;border-radius:12px;overflow:hidden">
<div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:20px 30px;text-align:center">
<h1 style="font-size:20px;color:#fff;margin:0">Day 3 of 5: Google Reviews</h1>
<p style="color:rgba(255,255,255,0.8);margin:5px 0 0;font-size:13px">Your free website growth course</p>
</div>
<div style="padding:30px">
<p style="color:#ccc;font-size:15px">Hi {name},</p>
<p style="color:#aaa;line-height:1.7">Reviews are the #1 trust signal for local businesses. Here's the truth: <strong style="color:#00d4ff">88% of people trust online reviews as much as personal recommendations</strong>.</p>
<p style="color:#aaa;line-height:1.7">But asking for reviews feels awkward, right? Here are 3 ways that work without the cringe:</p>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:8px">Method 1: The Right-After-Service Text</h3>
<p style="color:#aaa;font-size:13px;margin:0">"Hi [Name], really glad we could help with [service]. If you have 30 seconds, a Google review would mean the world to us: [your review link]"</p>
<p style="color:#666;font-size:12px;margin-top:5px">Send within 1 hour of completing the service. Response rate: 30-40%.</p>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:8px">Method 2: The QR Code Card</h3>
<p style="color:#aaa;font-size:13px;margin:0">Print business cards with a QR code linking to your Google review page. Hand them out after every job. "If you were happy with the service, we'd love a quick review."</p>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:8px">Method 3: The Follow-Up Email</h3>
<p style="color:#aaa;font-size:13px;margin:0">3 days after the service, send a follow-up email asking about their experience. Include the review link at the bottom. People who've had time to enjoy the results are more likely to write detailed reviews.</p>
</div>

<p style="color:#aaa;line-height:1.7;margin-top:15px"><strong style="color:#fff">Pro tip:</strong> Respond to EVERY review — positive and negative. Businesses that respond to reviews get 35% more clicks.</p>

<p style="color:#aaa;line-height:1.7">Tomorrow: 5 AI tools that save you 10+ hours per week (most are free).</p>

<p style="color:#888;font-size:13px;margin-top:25px">— The myAI Team<br><a href="https://aoeua.com" style="color:#00d4ff">aoeua.com</a></p>
</div>
<div style="background:#111;padding:12px 30px;text-align:center;border-top:1px solid #222">
<span style="color:#555;font-size:11px"><a href="mailto:info@aoeua.com?subject=Unsubscribe" style="color:#666">Unsubscribe</a></span>
</div>
</div>"""
    },
    4: {
        "subject": "Day 4: 5 Free AI Tools That Save 10 Hours/Week",
        "body": lambda name: f"""
<div style="font-family:'Segoe UI',sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;border-radius:12px;overflow:hidden">
<div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:20px 30px;text-align:center">
<h1 style="font-size:20px;color:#fff;margin:0">Day 4 of 5: AI Tools</h1>
<p style="color:rgba(255,255,255,0.8);margin:5px 0 0;font-size:13px">Your free website growth course</p>
</div>
<div style="padding:30px">
<p style="color:#ccc;font-size:15px">Hi {name},</p>
<p style="color:#aaa;line-height:1.7">These 5 AI tools are free (or nearly free) and can save you 10+ hours per week. Most of my clients start using them within 24 hours of hearing about them.</p>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:4px">1. ChatGPT (Free)</h3>
<p style="color:#aaa;font-size:13px;margin:0"><strong>Use it for:</strong> Email replies, social media posts, blog articles, business letters, customer FAQ answers. Saves 3-5 hours/week.</p>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:4px">2. Canva AI (Free)</h3>
<p style="color:#aaa;font-size:13px;margin:0"><strong>Use it for:</strong> Social media graphics, flyers, business cards, presentations. Magic Design creates layouts from a simple description. Saves 2-3 hours/week.</p>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:4px">3. Grammarly (Free)</h3>
<p style="color:#aaa;font-size:13px;margin:0"><strong>Use it for:</strong> Professional emails, proposals, website copy. Catches errors and improves your tone. Install the browser extension.</p>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:4px">4. Tidio Chatbot (Free up to 50 chats/mo)</h3>
<p style="color:#aaa;font-size:13px;margin:0"><strong>Use it for:</strong> Answering customer questions on your website 24/7. Captures leads while you sleep. Saves 2-4 hours/week.</p>
</div>

<div style="background:#111;border:1px solid #222;border-radius:10px;padding:16px;margin:15px 0">
<h3 style="color:#00d4ff;font-size:14px;margin-bottom:4px">5. Buffer (Free for 3 channels)</h3>
<p style="color:#aaa;font-size:13px;margin:0"><strong>Use it for:</strong> Schedule a week's social media in 30 minutes. AI suggests the best times to post. Saves 2-3 hours/week.</p>
</div>

<p style="color:#aaa;line-height:1.7;margin-top:15px">Want more? We've curated <a href="https://aoeua.com/ai-tools.html" style="color:#00d4ff">300+ AI tools</a> searchable by category and price.</p>

<p style="color:#aaa;line-height:1.7">Tomorrow is the final day — I'll share the complete growth plan that ties everything together (plus a special offer).</p>

<p style="color:#888;font-size:13px;margin-top:25px">— The myAI Team<br><a href="https://aoeua.com" style="color:#00d4ff">aoeua.com</a></p>
</div>
<div style="background:#111;padding:12px 30px;text-align:center;border-top:1px solid #222">
<span style="color:#555;font-size:11px"><a href="mailto:info@aoeua.com?subject=Unsubscribe" style="color:#666">Unsubscribe</a></span>
</div>
</div>"""
    },
    5: {
        "subject": "Day 5: Your Complete Website Growth Plan + Special Offer",
        "body": lambda name: f"""
<div style="font-family:'Segoe UI',sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;border-radius:12px;overflow:hidden">
<div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:20px 30px;text-align:center">
<h1 style="font-size:20px;color:#fff;margin:0">Day 5 of 5: The Full Plan</h1>
<p style="color:rgba(255,255,255,0.8);margin:5px 0 0;font-size:13px">Your free website growth course — Final day!</p>
</div>
<div style="padding:30px">
<p style="color:#ccc;font-size:15px">Hi {name},</p>
<p style="color:#aaa;line-height:1.7">This is it — the final day. Let me bring everything together into a complete growth plan you can follow.</p>

<h3 style="color:#00d4ff;margin:20px 0 10px;font-size:16px">Your 30-Day Website Growth Plan</h3>

<div style="background:#111;border-left:4px solid #00d4ff;padding:12px 16px;margin:10px 0;color:#ccc;font-size:14px">
<strong style="color:#00d4ff">Week 1: Foundation</strong><br>
&#9745; Run a free website audit<br>
&#9745; Fix title tags and meta descriptions<br>
&#9745; Compress all images<br>
&#9745; Claim Google Business Profile
</div>

<div style="background:#111;border-left:4px solid #7b2ff7;padding:12px 16px;margin:10px 0;color:#ccc;font-size:14px">
<strong style="color:#7b2ff7">Week 2: Trust</strong><br>
&#9745; Ask 10 customers for Google reviews<br>
&#9745; Add testimonials to your website<br>
&#9745; Install a chatbot for 24/7 lead capture<br>
&#9745; Make phone number clickable on every page
</div>

<div style="background:#111;border-left:4px solid #00cc66;padding:12px 16px;margin:10px 0;color:#ccc;font-size:14px">
<strong style="color:#00cc66">Week 3: Content</strong><br>
&#9745; Write 2 blog posts answering customer questions<br>
&#9745; Create a month of social media content with AI<br>
&#9745; Schedule posts with Buffer<br>
&#9745; Add FAQ section to main service pages
</div>

<div style="background:#111;border-left:4px solid #ffa500;padding:12px 16px;margin:10px 0;color:#ccc;font-size:14px">
<strong style="color:#ffa500">Week 4: Amplify</strong><br>
&#9745; List on 5 online directories<br>
&#9745; Set up Google Analytics and Search Console<br>
&#9745; Review data and adjust<br>
&#9745; Plan next month's content
</div>

<p style="color:#aaa;line-height:1.7;margin-top:20px">Follow this plan and you'll see measurable results within 30 days. Traffic will grow, phone will ring more, and your Google ranking will start climbing.</p>

<h3 style="color:#00d4ff;margin:25px 0 10px;font-size:16px">Want Us to Do It For You?</h3>
<p style="color:#aaa;line-height:1.7">If you'd rather focus on running your business while we handle the growth, here are two options:</p>

<div style="text-align:center;margin:20px 0">
<div style="display:inline-block;background:#111;border:2px solid #222;border-radius:16px;padding:20px 25px;margin:0 8px;vertical-align:top;width:220px">
<h3 style="color:#00d4ff;font-size:1.1rem;margin-bottom:5px">Full Audit Report</h3>
<p style="color:#888;font-size:2rem;font-weight:800;margin:10px 0">&#163;49</p>
<p style="color:#777;font-size:.85rem;margin-bottom:15px">Detailed analysis with specific fixes for your website</p>
<a href="https://aoeua.com/order-audit.html" style="display:block;padding:10px;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:#fff;text-decoration:none;border-radius:25px;font-weight:700;font-size:14px">Get Audit Report</a>
</div>

<div style="display:inline-block;background:#111;border:2px solid #00d4ff;border-radius:16px;padding:20px 25px;margin:0 8px;vertical-align:top;width:220px">
<h3 style="color:#00d4ff;font-size:1.1rem;margin-bottom:5px">1-on-1 Consultation</h3>
<p style="color:#888;font-size:2rem;font-weight:800;margin:10px 0">&#163;99</p>
<p style="color:#777;font-size:.85rem;margin-bottom:15px">30-min call + custom growth plan for your business</p>
<a href="https://aoeua.com/book-consultation.html" style="display:block;padding:10px;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:#fff;text-decoration:none;border-radius:25px;font-weight:700;font-size:14px">Book Consultation</a>
</div>
</div>

<p style="color:#aaa;line-height:1.7;margin-top:20px">Thank you for completing the course. Whether you DIY it or let us help, I'm rooting for your business to succeed.</p>

<p style="color:#aaa;line-height:1.7">Got questions? Just reply to this email — I read and respond to every one.</p>

<p style="color:#888;font-size:13px;margin-top:25px">— The myAI Team<br><a href="https://aoeua.com" style="color:#00d4ff">aoeua.com</a></p>
</div>
<div style="background:#111;padding:12px 30px;text-align:center;border-top:1px solid #222">
<span style="color:#555;font-size:11px"><a href="mailto:info@aoeua.com?subject=Unsubscribe" style="color:#666">Unsubscribe</a></span>
</div>
</div>"""
    },
}


def send_drip_email(to_email, name, day, creds):
    drip = DRIP_EMAILS[day]
    subject = drip["subject"]
    body = drip["body"](name)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"myAI <{creds['email']}>"
    msg["To"] = to_email
    msg["Reply-To"] = creds["email"]
    msg.attach(MIMEText(body, "html"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP(creds["smtp_host"], creds["smtp_port"], timeout=15) as server:
        server.ehlo()
        server.starttls(context=ctx)
        server.ehlo()
        server.login(creds["email"], creds["password"])
        server.sendmail(creds["email"], to_email, msg.as_string())
    return True


def send_all_due(dry_run=False):
    """Send all due drip emails to subscribers."""
    subs = load_subscribers()
    creds = load_creds()
    now = datetime.now()
    sent_count = 0

    print("=" * 60)
    print("  EMAIL DRIP COURSE — Sending Due Emails")
    print(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"  Subscribers: {len(subs)}")
    print("=" * 60)

    for sub in subs:
        if sub.get("status") != "active":
            continue

        subscribed = datetime.fromisoformat(sub["subscribed"])
        last_sent = sub.get("last_day_sent", 0)
        next_day = last_sent + 1

        if next_day > 5:
            continue  # Course completed

        # Calculate when the next email is due (1 email per day)
        due_date = subscribed + timedelta(days=next_day - 1)
        if now < due_date:
            continue  # Not yet due

        email = sub["email"]
        name = sub.get("name", "there")

        if dry_run:
            print(f"  [DRY RUN] Would send Day {next_day} to {email}")
        else:
            try:
                send_drip_email(email, name, next_day, creds)
                sub["last_day_sent"] = next_day
                if next_day == 5:
                    sub["status"] = "completed"
                print(f"  Sent Day {next_day} to {email}")
                sent_count += 1
            except Exception as e:
                print(f"  Failed Day {next_day} to {email}: {e}")

    save_subscribers(subs)
    print(f"\n  Total sent: {sent_count}")
    return sent_count


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--add", help="Add a subscriber email")
    parser.add_argument("--name", default="there", help="Subscriber name")
    parser.add_argument("--send-all-due", action="store_true", help="Send all due drip emails")
    parser.add_argument("--send-day", type=int, help="Send specific day to --to address")
    parser.add_argument("--to", help="Email address for --send-day")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.add:
        add_subscriber(args.add, args.name)
    elif args.send_all_due:
        send_all_due(dry_run=args.dry_run)
    elif args.send_day and args.to:
        creds = load_creds()
        if args.dry_run:
            print(f"[DRY RUN] Would send Day {args.send_day} to {args.to}")
        else:
            send_drip_email(args.to, args.name, args.send_day, creds)
            print(f"Sent Day {args.send_day} to {args.to}")
    else:
        parser.print_help()
