import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUSINESSES_PATH = os.path.join(BASE_DIR, 'businesses.json')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'businesses')
STATS_PATH = os.path.join(BASE_DIR, 'data', 'business_stats.json')


def load_businesses():
    with open(BUSINESSES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)['businesses']


def _css():
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; background: #0a0a0a; color: #e0e0e0; line-height: 1.7; }
        nav { position: fixed; top: 0; left: 0; right: 0; display: flex; justify-content: space-between; align-items: center; padding: 1rem 3rem; background: rgba(10,10,10,0.95); backdrop-filter: blur(12px); border-bottom: 1px solid #1a1a1a; z-index: 1000; }
        .brand { font-size: 1.5rem; font-weight: 800; background: linear-gradient(90deg,#00d4ff,#7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        nav a { color: #a0a0a0; text-decoration: none; margin-left: 2rem; }
        nav a:hover { color: #00d4ff; }
        .cta-btn { display: inline-block; padding: 0.8rem 2.5rem; border-radius: 50px; background: linear-gradient(90deg,#00d4ff,#7b2ff7); color: white; text-decoration: none; font-weight: 600; transition: transform 0.3s, box-shadow 0.3s; border: none; cursor: pointer; font-size: 1rem; }
        .cta-btn:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,212,255,0.3); }
        .cta-outline { display: inline-block; padding: 0.8rem 2.5rem; border-radius: 50px; border: 2px solid #333; background: transparent; color: #a0a0a0; text-decoration: none; transition: all 0.3s; }
        .cta-outline:hover { border-color: #00d4ff; color: #00d4ff; }
        .hero { min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 6rem 2rem 4rem; position: relative; overflow: hidden; }
        .hero::before { content: ''; position: absolute; top: 50%; left: 50%; width: 600px; height: 600px; background: radial-gradient(circle, rgba(0,212,255,0.08), transparent 70%); transform: translate(-50%,-50%); pointer-events: none; }
        .hero h1 { font-size: 3.5rem; font-weight: 800; line-height: 1.1; margin-bottom: 1.5rem; }
        .hero h1 span { background: linear-gradient(90deg,#00d4ff,#7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 1.3rem; color: #a0a0a0; max-width: 600px; margin-bottom: 2rem; }
        .buttons { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; }
        section { padding: 5rem 2rem; max-width: 1100px; margin: 0 auto; }
        .section-title { text-align: center; font-size: 2.5rem; margin-bottom: 0.5rem; color: #00d4ff; }
        .section-sub { text-align: center; color: #777; margin-bottom: 3rem; }
        .grid3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
        .card { background: #111; border: 1px solid #1a1a1a; border-radius: 16px; padding: 2rem; transition: transform 0.3s, border-color 0.3s; }
        .card:hover { transform: translateY(-5px); border-color: #00d4ff; }
        .card h3 { font-size: 1.3rem; margin-bottom: 0.5rem; }
        .card p { color: #888; font-size: 0.95rem; }
        .card .icon { font-size: 2.5rem; margin-bottom: 1rem; }
        .pricing-card { background: #111; border: 1px solid #1a1a1a; border-radius: 16px; padding: 2.5rem; text-align: center; }
        .pricing-card.featured { border-color: #00d4ff; position: relative; }
        .pricing-card.featured::before { content: 'MOST POPULAR'; position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: linear-gradient(90deg,#00d4ff,#7b2ff7); padding: 0.3rem 1.5rem; border-radius: 50px; font-size: 0.75rem; font-weight: 700; color: white; }
        .price { font-size: 3rem; font-weight: 800; margin: 1rem 0; }
        .price span { font-size: 1rem; color: #777; font-weight: 400; }
        .features { list-style: none; margin: 1.5rem 0; text-align: left; }
        .features li { padding: 0.5rem 0; border-bottom: 1px solid #1a1a1a; color: #aaa; }
        .features li::before { content: '\\2713 '; color: #00d4ff; font-weight: 700; }
        .testimonial { background: #111; border: 1px solid #1a1a1a; border-radius: 16px; padding: 2rem; }
        .testimonial .stars { color: #ffd700; margin-bottom: 1rem; }
        .testimonial .author { color: #00d4ff; font-weight: 600; margin-top: 1rem; }
        #contact { background: #111; border-radius: 16px; padding: 3rem; max-width: 600px; margin: 4rem auto; }
        #contact input, #contact textarea { width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #333; border-radius: 8px; background: #0a0a0a; color: #e0e0e0; font-size: 1rem; }
        #contact textarea { min-height: 120px; resize: vertical; }
        footer { text-align: center; padding: 3rem 2rem; color: #555; border-top: 1px solid #1a1a1a; }
        footer a { color: #00d4ff; text-decoration: none; }
        .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; text-align: center; padding: 3rem 0; }
        .stats .num { font-size: 2.5rem; font-weight: 800; background: linear-gradient(90deg,#00d4ff,#7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stats .label { color: #777; font-size: 0.9rem; }
        @media (max-width: 768px) { .hero h1 { font-size: 2.2rem; } .stats { grid-template-columns: repeat(2, 1fr); } nav { padding: 1rem 1.5rem; } }
    """


def _features_for_niche(biz):
    niche = biz['niche'].lower()
    base = [
        "AI-powered customer management",
        "Automated scheduling & booking",
        "Smart invoicing & payments",
        "Real-time analytics dashboard",
        "Automated email & SMS marketing",
        "24/7 AI chatbot for customers",
    ]
    if 'restaurant' in niche:
        return ["AI menu optimization", "Automated table reservations", "Smart inventory tracking", "Online ordering system", "Customer loyalty automation", "Kitchen workflow AI"]
    elif 'real estate' in niche:
        return ["AI property matching", "Automated listing management", "Smart lead scoring", "Virtual tour scheduling", "Contract automation", "Market analysis AI"]
    elif 'e-commerce' in niche or 'ecommerce' in niche:
        return ["AI product recommendations", "Automated inventory management", "Dynamic pricing engine", "Cart abandonment recovery", "Multi-channel selling AI", "Smart fulfillment routing"]
    elif 'fitness' in niche or 'gym' in niche:
        return ["AI workout plans", "Automated class scheduling", "Member retention AI", "Progress tracking automation", "Nutrition plan generator", "Billing automation"]
    elif 'dental' in niche:
        return ["AI appointment scheduling", "Automated patient reminders", "Insurance verification AI", "Treatment plan optimization", "Patient portal automation", "Recall system AI"]
    elif 'legal' in niche or 'law' in niche:
        return ["AI document review", "Automated case management", "Smart billing & time tracking", "Client intake automation", "Legal research AI", "Deadline tracking system"]
    elif 'accounting' in niche:
        return ["AI bookkeeping automation", "Tax preparation assistant", "Automated reconciliation", "Financial reporting AI", "Client portal automation", "Compliance monitoring"]
    elif 'insurance' in niche:
        return ["AI policy matching", "Automated claims processing", "Lead scoring AI", "Renewal automation", "Risk assessment AI", "Client communication automation"]
    elif 'staffing' in niche or 'recruitment' in niche:
        return ["AI resume screening", "Automated interview scheduling", "Candidate matching AI", "Onboarding automation", "Timesheet management", "Client portal AI"]
    elif 'travel' in niche:
        return ["AI trip planning", "Automated booking management", "Dynamic pricing alerts", "Customer preference AI", "Itinerary automation", "Review management AI"]
    elif 'construction' in niche:
        return ["AI project scheduling", "Automated cost estimation", "Safety compliance AI", "Subcontractor management", "Progress tracking automation", "Material ordering AI"]
    elif 'trucking' in niche or 'fleet' in niche:
        return ["AI route optimization", "Automated fleet tracking", "Fuel management AI", "Driver scheduling automation", "Compliance monitoring", "Load matching AI"]
    elif 'auto' in niche and 'dealer' in niche:
        return ["AI lead scoring", "Automated inventory pricing", "Customer follow-up AI", "Test drive scheduling", "Trade-in valuation AI", "Marketing automation"]
    else:
        return base


def _testimonials_for_niche(biz):
    audience = biz['audience']
    return [
        {"text": f"This AI completely transformed how I run my business. I save 20+ hours every week.", "author": f"Sarah M., {audience}", "stars": 5},
        {"text": f"The automation is incredible. My revenue increased 40% in the first 3 months.", "author": f"Mike R., {audience}", "stars": 5},
        {"text": f"I was skeptical at first, but now I can't imagine running my business without it.", "author": f"Jennifer L., {audience}", "stars": 5},
    ]


def _blog_posts_for_niche(biz):
    name = biz['name']
    niche = biz['niche']
    audience = biz['audience']
    return [
        {
            "title": f"How AI is Revolutionizing {niche}",
            "excerpt": f"Discover how artificial intelligence is transforming the way {audience.lower()} operate their businesses, from customer management to automated marketing.",
            "date": "2025-01-15",
            "read_time": "5 min"
        },
        {
            "title": f"5 Ways {name} Saves You 20 Hours Per Week",
            "excerpt": f"Time is money. Learn about the five key automation features that let {audience.lower()} focus on what matters most — growing their business.",
            "date": "2025-01-22",
            "read_time": "4 min"
        },
        {
            "title": f"Case Study: How One Business Grew Revenue 40% with AI",
            "excerpt": f"A real success story from one of our clients who used {name} to dramatically increase efficiency and profitability.",
            "date": "2025-01-29",
            "read_time": "6 min"
        },
    ]


def generate_business_site(biz):
    """Generate a complete landing page for one business niche."""
    biz_dir = os.path.join(OUTPUT_DIR, biz['id'])
    os.makedirs(biz_dir, exist_ok=True)

    features = _features_for_niche(biz)
    testimonials = _testimonials_for_niche(biz)
    blog_posts = _blog_posts_for_niche(biz)

    price = biz['price']
    pro_price = int(price * 2.2)
    ent_price = int(price * 4.5)

    features_html = ""
    icons = ["&#x1F4CA;", "&#x1F916;", "&#x26A1;", "&#x1F4B0;", "&#x1F4E7;", "&#x1F50D;"]
    for i, feat in enumerate(features):
        features_html += f"""
            <div class="card">
                <div class="icon">{icons[i % len(icons)]}</div>
                <h3>{feat}</h3>
                <p>Powered by advanced AI to automate and optimize every aspect of your {biz['niche'].lower()}.</p>
            </div>"""

    testimonials_html = ""
    for t in testimonials:
        stars = "&#x2B50;" * t['stars']
        testimonials_html += f"""
            <div class="testimonial">
                <div class="stars">{stars}</div>
                <p>"{t['text']}"</p>
                <div class="author">— {t['author']}</div>
            </div>"""

    blog_html = ""
    for post in blog_posts:
        blog_html += f"""
            <div class="card">
                <p style="color:#00d4ff;font-size:0.85rem;">{post['date']} &middot; {post['read_time']} read</p>
                <h3>{post['title']}</h3>
                <p>{post['excerpt']}</p>
            </div>"""

    starter_features = "\n".join(f"<li>{f}</li>" for f in features[:3])
    pro_features = "\n".join(f"<li>{f}</li>" for f in features[:5])
    ent_features = "\n".join(f"<li>{f}</li>" for f in features)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{biz['name']} — {biz['tagline']}</title>
    <meta name="description" content="{biz['name']}: {biz['tagline']}. AI-powered {biz['niche'].lower()} for {biz['audience'].lower()}. Starting at ${price}/mo.">
    <meta name="keywords" content="{biz['niche']}, AI, automation, {biz['audience']}, {biz['name']}">
    <meta property="og:title" content="{biz['name']} — {biz['tagline']}">
    <meta property="og:description" content="AI-powered {biz['niche'].lower()} starting at ${price}/mo.">
    <meta property="og:type" content="website">
    <style>{_css()}</style>
</head>
<body>
    <nav>
        <div class="brand">&#x1F916; {biz['name']}</div>
        <div>
            <a href="#features">Features</a>
            <a href="#pricing">Pricing</a>
            <a href="#testimonials">Reviews</a>
            <a href="#blog">Blog</a>
            <a href="#contact">Contact</a>
        </div>
    </nav>

    <div class="hero">
        <h1>{biz['tagline'].split(' ')[0]} <span>{' '.join(biz['tagline'].split(' ')[1:])}</span></h1>
        <p>{biz['name']} uses advanced AI to automate every aspect of your {biz['niche'].lower()} — so you can focus on what matters most.</p>
        <div class="buttons">
            <a href="#pricing" class="cta-btn">Start Free Trial</a>
            <a href="#features" class="cta-outline">See Features</a>
        </div>
    </div>

    <section>
        <div class="stats">
            <div><div class="num">500+</div><div class="label">Active Businesses</div></div>
            <div><div class="num">20hrs</div><div class="label">Saved Per Week</div></div>
            <div><div class="num">40%</div><div class="label">Revenue Increase</div></div>
            <div><div class="num">99.9%</div><div class="label">Uptime</div></div>
        </div>
    </section>

    <section id="features">
        <h2 class="section-title">Powerful Features</h2>
        <p class="section-sub">Everything {biz['audience'].lower()} need to run smarter</p>
        <div class="grid3">{features_html}
        </div>
    </section>

    <section id="pricing">
        <h2 class="section-title">Simple Pricing</h2>
        <p class="section-sub">Start free. Scale when you're ready.</p>
        <div class="grid3">
            <div class="pricing-card">
                <h3>Starter</h3>
                <div class="price">${price}<span>/mo</span></div>
                <ul class="features">{starter_features}</ul>
                <a href="#contact" class="cta-btn" style="width:100%;text-align:center;">Start Free Trial</a>
            </div>
            <div class="pricing-card featured">
                <h3>Professional</h3>
                <div class="price">${pro_price}<span>/mo</span></div>
                <ul class="features">{pro_features}</ul>
                <a href="#contact" class="cta-btn" style="width:100%;text-align:center;">Start Free Trial</a>
            </div>
            <div class="pricing-card">
                <h3>Enterprise</h3>
                <div class="price">${ent_price}<span>/mo</span></div>
                <ul class="features">{ent_features}</ul>
                <a href="#contact" class="cta-btn" style="width:100%;text-align:center;">Contact Sales</a>
            </div>
        </div>
    </section>

    <section id="testimonials">
        <h2 class="section-title">Trusted by {biz['audience']}</h2>
        <p class="section-sub">Join hundreds of businesses already using AI</p>
        <div class="grid3">{testimonials_html}
        </div>
    </section>

    <section id="blog">
        <h2 class="section-title">Latest Insights</h2>
        <p class="section-sub">Learn how AI is transforming {biz['niche'].lower()}</p>
        <div class="grid3">{blog_html}
        </div>
    </section>

    <section id="contact">
        <h2 class="section-title">Get Started Today</h2>
        <p class="section-sub">14-day free trial. No credit card required.</p>
        <div style="max-width:600px;margin:2rem auto;">
            <form name="contact-{biz['id']}" method="POST" data-netlify="true" action="/thank-you.html">
                <input type="hidden" name="form-name" value="contact-{biz['id']}">
                <input type="hidden" name="business-niche" value="{biz['name']}">
                <input type="text" name="name" placeholder="Your Name" required>
                <input type="email" name="email" placeholder="Your Email" required>
                <input type="tel" name="phone" placeholder="Your Phone Number">
                <input type="text" name="company" placeholder="Your Business Name">
                <select name="plan" style="width:100%;padding:0.8rem;margin-bottom:1rem;border:1px solid #333;border-radius:8px;background:#0a0a0a;color:#e0e0e0;font-size:1rem;">
                    <option value="">Select a Plan</option>
                    <option value="starter-${price}">Starter — ${price}/mo</option>
                    <option value="pro-${pro_price}">Professional — ${pro_price}/mo</option>
                    <option value="enterprise-${ent_price}">Enterprise — ${ent_price}/mo</option>
                </select>
                <textarea name="message" placeholder="Tell us about your {biz['niche'].lower()} needs..."></textarea>
                <button type="submit" class="cta-btn" style="width:100%;text-align:center;font-size:1.1rem;padding:1rem;">Get My Free Trial</button>
            </form>
        </div>
    </section>

    <footer>
        <p>&copy; 2025 {biz['name']} — Powered by <a href="../index.html">myAI</a> | <a href="mailto:hello@myai.business">hello@myai.business</a></p>
    </footer>

    <script>
        document.querySelectorAll('a[href^="#"]').forEach(a => {{
            a.addEventListener('click', e => {{
                e.preventDefault();
                const el = document.querySelector(a.getAttribute('href'));
                if(el) el.scrollIntoView({{behavior:'smooth'}});
            }});
        }});
    </script>
</body>
</html>"""

    index_path = os.path.join(biz_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Save niche-specific content data
    content_data = {
        "business": biz,
        "features": features,
        "testimonials": testimonials,
        "blog_posts": blog_posts,
        "pricing": {
            "starter": price,
            "professional": pro_price,
            "enterprise": ent_price
        },
        "generated": datetime.now().isoformat()
    }
    data_path = os.path.join(biz_dir, 'data.json')
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(content_data, f, indent=2)

    return index_path


def generate_social_content(biz):
    """Generate social media marketing content for a business niche."""
    biz_dir = os.path.join(OUTPUT_DIR, biz['id'])
    os.makedirs(biz_dir, exist_ok=True)

    name = biz['name']
    tagline = biz['tagline']
    audience = biz['audience']
    niche = biz['niche']
    price = biz['price']

    posts = {
        "twitter": [
            f"Tired of spending 20+ hours on admin? {name} automates your entire {niche.lower()} with AI. Start free today. #AI #Automation #{biz['id'].replace('-','')}",
            f"\"I saved $3,000/month and 25 hours/week.\" — Real feedback from {audience.lower()} using {name}. Try it free.",
            f"Your competitors are already using AI. Don't get left behind. {name} starting at ${price}/mo. #SmallBusiness #AI",
            f"THREAD: 5 ways {name} is changing {niche.lower()} forever (and saving {audience.lower()} thousands)...",
            f"What if your business ran itself while you slept? That's not a dream — that's {name}. Start your free trial.",
        ],
        "linkedin": [
            f"I'm excited to share how AI is transforming {niche.lower()}.\n\n{audience} are saving 20+ hours per week with {name} — our AI-powered automation platform.\n\nKey results we're seeing:\n- 40% revenue increase\n- 60% faster customer response\n- 90% less paperwork\n\nThe future of {niche.lower()} is automated. Is your business ready?\n\n#AI #Automation #{niche.replace(' ','')} #Business",
            f"Case Study: How one business used {name} to transform their operations.\n\nBefore {name}:\n- 30hrs/week on admin\n- Missed leads\n- Manual scheduling\n\nAfter {name}:\n- 10hrs/week on admin\n- 100% lead capture\n- Fully automated scheduling\n\nResult: 40% revenue growth in 90 days.\n\nWant the same? Link in comments.",
        ],
        "instagram": [
            f"Stop working IN your business. Start working ON it. {name} automates everything. Link in bio.",
            f"{tagline} — AI-powered automation for {audience.lower()}. Free trial available now.",
            f"Real results. Real {audience.lower()}. Real AI. Try {name} free for 14 days.",
        ],
        "reels_scripts": [
            {
                "title": f"Day in the Life with {name}",
                "hook": f"Watch how this AI runs an entire {niche.lower()} business",
                "script": f"Before {name}: Drowning in emails, scheduling chaos, missed leads.\nAfter {name}: AI handles everything. Bookings automated. Leads captured. Revenue up 40%.\nThe future is here. Link in bio.",
                "duration": "15-30 seconds"
            },
            {
                "title": f"3 Reasons {audience} Need AI",
                "hook": "POV: You just discovered AI can run your business",
                "script": f"Reason 1: Save 20+ hours per week on admin.\nReason 2: Never miss a lead or customer again.\nReason 3: Increase revenue by 40% on autopilot.\nTry {name} free. Link in bio.",
                "duration": "15-30 seconds"
            },
        ]
    }

    social_path = os.path.join(biz_dir, 'social_content.json')
    with open(social_path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2)
    return social_path


def generate_email_templates(biz):
    """Generate email marketing templates for a business niche."""
    biz_dir = os.path.join(OUTPUT_DIR, biz['id'])
    os.makedirs(biz_dir, exist_ok=True)

    name = biz['name']
    audience = biz['audience']
    niche = biz['niche']
    price = biz['price']

    welcome_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0a0a0a;font-family:Arial,sans-serif;">
<div style="max-width:600px;margin:0 auto;background:#111;border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:2rem;text-align:center;">
        <h1 style="color:white;margin:0;font-size:1.8rem;">Welcome to {name}!</h1>
    </div>
    <div style="padding:2rem;color:#e0e0e0;">
        <p>Hi there,</p>
        <p>Thank you for starting your free trial! You've just taken the first step toward transforming your {niche.lower()} with AI.</p>
        <p>Here's what happens next:</p>
        <ul style="color:#aaa;">
            <li>Your AI assistant is setting up your dashboard right now</li>
            <li>Your first automated workflow will be ready in 5 minutes</li>
            <li>Check your dashboard to customize your preferences</li>
        </ul>
        <div style="text-align:center;margin:2rem 0;">
            <a href="#" style="display:inline-block;padding:1rem 3rem;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:white;text-decoration:none;border-radius:50px;font-weight:600;">Go to My Dashboard</a>
        </div>
        <p>Questions? Just reply to this email.</p>
        <p>— The {name} Team</p>
    </div>
</div>
</body></html>"""

    followup_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0a0a0a;font-family:Arial,sans-serif;">
<div style="max-width:600px;margin:0 auto;background:#111;border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(90deg,#00d4ff,#7b2ff7);padding:2rem;text-align:center;">
        <h1 style="color:white;margin:0;font-size:1.8rem;">{name} — Your Week in Review</h1>
    </div>
    <div style="padding:2rem;color:#e0e0e0;">
        <p>Here's what your AI accomplished this week:</p>
        <div style="background:#0a0a0a;border-radius:12px;padding:1.5rem;margin:1rem 0;">
            <p style="color:#00d4ff;font-size:1.5rem;font-weight:800;margin:0;">12 hours saved</p>
            <p style="color:#777;margin:0;">That's 12 hours you got back this week</p>
        </div>
        <div style="background:#0a0a0a;border-radius:12px;padding:1.5rem;margin:1rem 0;">
            <p style="color:#7b2ff7;font-size:1.5rem;font-weight:800;margin:0;">47 tasks automated</p>
            <p style="color:#777;margin:0;">From scheduling to customer follow-ups</p>
        </div>
        <div style="text-align:center;margin:2rem 0;">
            <a href="#" style="display:inline-block;padding:1rem 3rem;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:white;text-decoration:none;border-radius:50px;font-weight:600;">View Full Report</a>
        </div>
    </div>
</div>
</body></html>"""

    templates = {
        "welcome": welcome_html,
        "weekly_report": followup_html,
        "generated": datetime.now().isoformat()
    }

    emails_dir = os.path.join(biz_dir, 'emails')
    os.makedirs(emails_dir, exist_ok=True)

    with open(os.path.join(emails_dir, 'welcome.html'), 'w', encoding='utf-8') as f:
        f.write(welcome_html)
    with open(os.path.join(emails_dir, 'weekly_report.html'), 'w', encoding='utf-8') as f:
        f.write(followup_html)

    meta_path = os.path.join(emails_dir, 'templates.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump({"business": biz['id'], "templates": ["welcome", "weekly_report"], "generated": datetime.now().isoformat()}, f, indent=2)

    return emails_dir


def generate_all_businesses():
    """Generate websites, content, social, and emails for ALL 50 businesses."""
    businesses = load_businesses()
    results = []

    for biz in businesses:
        site_path = generate_business_site(biz)
        social_path = generate_social_content(biz)
        email_dir = generate_email_templates(biz)
        results.append({
            "id": biz['id'],
            "name": biz['name'],
            "site": site_path,
            "social": social_path,
            "emails": email_dir,
            "status": "generated"
        })

    # Save stats
    os.makedirs(os.path.dirname(STATS_PATH), exist_ok=True)
    stats = {
        "total_businesses": len(results),
        "generated_at": datetime.now().isoformat(),
        "total_pages": len(results),
        "total_social_posts": len(results) * 10,
        "total_email_templates": len(results) * 2,
        "total_blog_posts": len(results) * 3,
        "businesses": results
    }
    with open(STATS_PATH, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    return stats


def generate_master_directory():
    """Generate a master directory page linking to all 50 businesses."""
    businesses = load_businesses()

    cards = ""
    for biz in businesses:
        cards += f"""
            <a href="{biz['id']}/index.html" class="card" style="text-decoration:none;">
                <h3 style="color:#00d4ff;">{biz['name']}</h3>
                <p>{biz['tagline']}</p>
                <p style="color:#7b2ff7;font-weight:700;">Starting at ${biz['price']}/mo</p>
                <p style="font-size:0.85rem;">Target: {biz['audience']}</p>
            </a>"""

    total_revenue = sum(b['price'] for b in businesses)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>myAI — 50 AI-Powered Businesses</title>
    <meta name="description" content="myAI: 50 autonomous AI-powered business solutions across every industry. Find the perfect AI automation for your niche.">
    <style>{_css()}
        .grid3 {{ grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); }}
        .hero h1 {{ font-size: 3rem; }}
    </style>
</head>
<body>
    <nav>
        <div class="brand">&#x1F916; myAI Empire</div>
        <div>
            <a href="https://aoeua.com/">Home</a>
            <a href="#businesses">All Businesses</a>
            <a href="#contact">Contact</a>
        </div>
    </nav>

    <div class="hero">
        <h1>50 AI Businesses. <span>One Platform.</span></h1>
        <p>We've built AI-powered automation solutions for every industry. Each one is a complete business — ready to deploy, ready to earn.</p>
        <div class="buttons">
            <a href="#businesses" class="cta-btn">Explore All Businesses</a>
        </div>
    </div>

    <section>
        <div class="stats">
            <div><div class="num">50</div><div class="label">Active Businesses</div></div>
            <div><div class="num">${total_revenue:,}</div><div class="label">Potential MRR (1 client each)</div></div>
            <div><div class="num">150</div><div class="label">Blog Posts</div></div>
            <div><div class="num">500+</div><div class="label">Marketing Assets</div></div>
        </div>
    </section>

    <section id="businesses">
        <h2 class="section-title">All 50 Businesses</h2>
        <p class="section-sub">Click any card to view the full landing page</p>
        <div class="grid3">{cards}
        </div>
    </section>

    <footer>
        <p>&copy; 2025 myAI Empire — 50 Businesses, One AI Platform | <a href="mailto:hello@myai.business">hello@myai.business</a></p>
    </footer>
</body>
</html>"""

    dir_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(dir_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return dir_path
