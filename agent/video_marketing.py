import os
import json
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'marketing')


def ensure_dirs():
    for sub in ['scripts', 'thumbnails', 'social', 'reels', 'calendar']:
        os.makedirs(os.path.join(OUTPUT_DIR, sub), exist_ok=True)


# ═══════════════════════════════════════════════════
# VIDEO SCRIPTS
# ═══════════════════════════════════════════════════

def generate_video_scripts(config):
    ensure_dirs()

    scripts = [
        {
            "id": "yt_001",
            "platform": "youtube",
            "title": "How AI Agents Can Run Your Entire Business in 2025",
            "duration": "8 min",
            "hook": "What if I told you there's an AI that can build your website, write your content, manage your social media, and grow your revenue — all while you sleep?",
            "outline": [
                {"time": "0:00-0:30", "section": "HOOK", "content": "Open with shocking stat: 87% of businesses still do marketing manually. Show the problem — late nights, repetitive tasks, missed opportunities."},
                {"time": "0:30-2:00", "section": "THE PROBLEM", "content": "Walk through a typical business owner's day: emails, social media, website updates, customer service. It's a 60-hour workweek just to keep up."},
                {"time": "2:00-4:00", "section": "THE SOLUTION", "content": "Introduce myAI: an autonomous system that handles all of this. Show the agent loop — execute tasks, learn, improve, repeat 24/7."},
                {"time": "4:00-6:00", "section": "DEMO", "content": "Screen recording: run the agent, watch it generate a landing page, write blog posts, create social content, and send email campaigns."},
                {"time": "6:00-7:30", "section": "RESULTS", "content": "Case study: from 0 to 500 leads/month. 10x faster content production. 40% cost reduction vs. hiring."},
                {"time": "7:30-8:00", "section": "CTA", "content": "Start your free 14-day trial at myai.com. Link in description. Like, subscribe, turn on notifications."}
            ],
            "tags": ["AI automation", "business AI", "autonomous agents", "marketing automation", "startup tools"],
            "thumbnail_text": "AI RUNS MY BUSINESS"
        },
        {
            "id": "yt_002",
            "platform": "youtube",
            "title": "I Let AI Handle My Marketing for 30 Days — Here's What Happened",
            "duration": "10 min",
            "hook": "I handed my entire marketing operation to an AI agent for 30 days. The results were absolutely insane.",
            "outline": [
                {"time": "0:00-0:30", "section": "HOOK", "content": "Teaser of results — show the dashboard with metrics popping up. 'I couldn't believe it either.'"},
                {"time": "0:30-2:30", "section": "THE SETUP", "content": "Day 1: Configure the AI agent. Set business goals, target audience, and content preferences. One command starts everything."},
                {"time": "2:30-5:00", "section": "WEEK BY WEEK", "content": "Week 1: Website built, 5 blog posts published. Week 2: Social media pipeline flowing, video scripts created. Week 3: Email campaigns active, leads coming in. Week 4: System self-optimized based on performance data."},
                {"time": "5:00-7:00", "section": "THE NUMBERS", "content": "Traffic: 0 → 12,000 visitors. Leads: 0 → 347. Content pieces: 67 published automatically. Time spent by me: approximately 2 hours total."},
                {"time": "7:00-9:00", "section": "DEEP DIVE", "content": "How the AI decides what to do next. The task queue system. How it self-corrects and improves with each run cycle."},
                {"time": "9:00-10:00", "section": "CTA", "content": "Your business deserves this. Free trial, no credit card. Link below."}
            ],
            "tags": ["AI experiment", "marketing AI", "30 day challenge", "autonomous business", "AI results"],
            "thumbnail_text": "30 DAYS OF AI"
        },
        {
            "id": "yt_003",
            "platform": "youtube",
            "title": "5 Tasks You Should NEVER Do Manually Again (AI Does Them Better)",
            "duration": "7 min",
            "hook": "You're wasting 20+ hours a week on tasks that AI can do in minutes. Here are the top 5.",
            "outline": [
                {"time": "0:00-0:30", "section": "HOOK", "content": "Quick montage of boring manual tasks. 'Stop. Just stop. There's a better way.'"},
                {"time": "0:30-2:00", "section": "1. CONTENT WRITING", "content": "Blog posts, product descriptions, email campaigns. AI writes them faster AND optimized for SEO."},
                {"time": "2:00-3:00", "section": "2. SOCIAL MEDIA", "content": "Creating posts, scheduling, optimizing hashtags. AI handles all platforms simultaneously."},
                {"time": "3:00-4:00", "section": "3. WEBSITE UPDATES", "content": "Design changes, new pages, content refreshes. AI rebuilds and optimizes continuously."},
                {"time": "4:00-5:30", "section": "4. CUSTOMER SERVICE", "content": "FAQ responses, meeting booking, lead qualification. AI chatbot handles 80% of inquiries."},
                {"time": "5:30-6:30", "section": "5. REPORTING", "content": "Weekly reports, market analysis, competitor tracking. AI generates them automatically."},
                {"time": "6:30-7:00", "section": "CTA", "content": "Start automating today. Link in description for your free trial."}
            ],
            "tags": ["productivity", "automation", "AI tools", "business tips", "time saving"],
            "thumbnail_text": "STOP DOING THIS!"
        }
    ]

    path = os.path.join(OUTPUT_DIR, 'scripts', 'video_scripts.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"generated": datetime.now().isoformat(), "scripts": scripts}, f, indent=2)
    return path


# ═══════════════════════════════════════════════════
# REELS / SHORT-FORM CONTENT
# ═══════════════════════════════════════════════════

def generate_reels_scripts(config):
    ensure_dirs()

    reels = [
        {
            "id": "reel_001",
            "platforms": ["tiktok", "instagram_reels", "youtube_shorts"],
            "title": "POV: Your business runs itself",
            "duration": "30 sec",
            "script": "POV: You wake up and check your phone...\n[Show notification: '15 new leads captured']\n[Show notification: '3 blog posts published']\n[Show notification: 'Social media posted to 4 platforms']\n[Show notification: 'Revenue up 23% this week']\n...and your AI agent did it all while you slept.\n[Text overlay: 'myAI — Your business on autopilot']",
            "hashtags": ["#AIbusiness", "#automation", "#entrepreneurlife", "#passiveincome", "#techstartup", "#aitools", "#businessautomation"],
            "music_suggestion": "Trending upbeat lo-fi or tech beat",
            "style": "screen_recording_with_overlays"
        },
        {
            "id": "reel_002",
            "platforms": ["tiktok", "instagram_reels", "youtube_shorts"],
            "title": "Things AI agents can do that most people don't know",
            "duration": "45 sec",
            "script": "Things AI agents can do that most people don't know:\n1. Build your entire website from scratch [show website generating]\n2. Write and publish blog posts daily [show blog posts]\n3. Create marketing videos and thumbnails [show assets]\n4. Manage all your social media [show dashboard]\n5. Handle customer service 24/7 [show chatbot]\n6. Generate revenue reports weekly [show charts]\n...and it costs less than one employee.\n[Text: 'Link in bio for free trial']",
            "hashtags": ["#AI", "#didyouknow", "#businesstips", "#automation", "#techtools", "#marketing", "#growth"],
            "music_suggestion": "Dramatic reveal / list trend audio",
            "style": "text_overlay_with_broll"
        },
        {
            "id": "reel_003",
            "platforms": ["tiktok", "instagram_reels", "youtube_shorts"],
            "title": "My morning routine as an AI-powered business owner",
            "duration": "25 sec",
            "script": "My morning routine as a business owner:\n6:00 AM — Wake up naturally (no alarm) ☕\n6:15 AM — Check AI dashboard — everything's running\n6:20 AM — Review overnight metrics — 12 new leads\n6:25 AM — Approve AI-generated content for the day\n6:30 AM — Done. Time for yoga.\nThe AI handles the rest.\n[Text: '@myai — automation that actually works']",
            "hashtags": ["#morningroutine", "#CEO", "#AIautomation", "#lifestyle", "#techengineer", "#buildInPublic", "#startup"],
            "music_suggestion": "Chill morning vibe / aesthetic routine audio",
            "style": "lifestyle_vlog"
        },
        {
            "id": "reel_004",
            "platforms": ["tiktok", "instagram_reels"],
            "title": "Hiring an employee vs. using AI 🤖",
            "duration": "20 sec",
            "script": "Hiring an employee:\n❌ $4,000/month salary\n❌ 40 hours/week max\n❌ Sick days, vacations\n❌ Training needed\n\nUsing myAI:\n✅ $399/month\n✅ Works 24/7/365\n✅ Never calls in sick\n✅ Self-learning\n\nThe choice is obvious.\n[Text: 'Start free trial — link in bio']",
            "hashtags": ["#AIvsHuman", "#businesshack", "#startup", "#entrepreneurship", "#costcutting", "#hiring", "#AItools"],
            "music_suggestion": "Comparison trend audio",
            "style": "split_screen_comparison"
        },
        {
            "id": "reel_005",
            "platforms": ["tiktok", "instagram_reels", "youtube_shorts"],
            "title": "Watch AI build a website in 60 seconds",
            "duration": "60 sec",
            "script": "[Screen recording with timer overlay]\n0:00 — Run the command: python run.py\n0:10 — Agent starts executing tasks from queue\n0:20 — Landing page generated with full design\n0:30 — Blog posts created and published\n0:40 — Pricing page with 3 tiers\n0:50 — Email templates generated\n0:55 — 5 new tasks queued for next run\n1:00 — Done. Full business website. From zero.\n[Text: 'This is myAI. Link in bio.']",
            "hashtags": ["#speedrun", "#webdev", "#AI", "#coding", "#automation", "#nocode", "#buildinpublic"],
            "music_suggestion": "Fast-paced electronic / racing countdown",
            "style": "screen_recording_timelapse"
        }
    ]

    path = os.path.join(OUTPUT_DIR, 'reels', 'reels_scripts.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"generated": datetime.now().isoformat(), "scripts": reels}, f, indent=2)
    return path


# ═══════════════════════════════════════════════════
# THUMBNAIL GENERATOR (HTML-based)
# ═══════════════════════════════════════════════════

def generate_thumbnail(script_id, title_text, subtitle=""):
    ensure_dirs()

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
    * {{ margin:0; padding:0; }}
    body {{
        width:1280px; height:720px; overflow:hidden;
        background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);
        display:flex; justify-content:center; align-items:center;
        font-family:'Segoe UI',Arial,sans-serif; position:relative;
    }}
    .bg-glow {{
        position:absolute; width:400px; height:400px; border-radius:50%;
        background:radial-gradient(circle,rgba(123,47,247,.3),transparent);
        top:-100px; right:-100px;
    }}
    .bg-glow2 {{
        position:absolute; width:300px; height:300px; border-radius:50%;
        background:radial-gradient(circle,rgba(0,212,255,.2),transparent);
        bottom:-50px; left:-50px;
    }}
    .content {{
        text-align:center; z-index:1; padding:2rem;
    }}
    h1 {{
        font-size:4.5rem; font-weight:900;
        background:linear-gradient(90deg,#00d4ff,#7b2ff7,#ff6b6b);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        line-height:1.1; margin-bottom:1rem; max-width:1000px;
    }}
    .subtitle {{ font-size:2rem; color:#a0a0a0; }}
    .brand {{
        position:absolute; bottom:30px; right:40px;
        font-size:2rem; font-weight:800;
        background:linear-gradient(90deg,#00d4ff,#7b2ff7);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    }}
    .emoji {{ font-size:5rem; margin-bottom:1rem; }}
</style></head>
<body>
    <div class="bg-glow"></div>
    <div class="bg-glow2"></div>
    <div class="content">
        <div class="emoji">&#x1F916;</div>
        <h1>{title_text}</h1>
        <div class="subtitle">{subtitle}</div>
    </div>
    <div class="brand">myAI</div>
</body></html>"""

    path = os.path.join(OUTPUT_DIR, 'thumbnails', f'{script_id}_thumb.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


def generate_all_thumbnails(config):
    ensure_dirs()
    scripts_path = os.path.join(OUTPUT_DIR, 'scripts', 'video_scripts.json')
    if not os.path.exists(scripts_path):
        generate_video_scripts(config)

    with open(scripts_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    paths = []
    for script in data.get("scripts", []):
        p = generate_thumbnail(
            script["id"],
            script.get("thumbnail_text", script["title"]),
            script.get("duration", "")
        )
        paths.append(p)
    return paths


# ═══════════════════════════════════════════════════
# CONTENT CALENDAR
# ═══════════════════════════════════════════════════

def generate_content_calendar(config):
    ensure_dirs()

    today = datetime.now()
    schedule = config.get("marketing", {}).get("posting_schedule", {})

    calendar_entries = []
    for week in range(4):
        week_start = today + timedelta(weeks=week)

        # YouTube — weekly
        yt_day = week_start + timedelta(days=(1 - week_start.weekday()) % 7)  # Tuesday
        calendar_entries.append({
            "date": yt_day.strftime("%Y-%m-%d"),
            "platform": "youtube",
            "type": "long_form_video",
            "title": f"Week {week+1} YouTube Video",
            "description": f"Educational video covering AI automation topic #{week+1}",
            "status": "scripted" if week == 0 else "planned",
            "time": schedule.get("youtube", "Tuesday 10:00 UTC")
        })

        # TikTok — 3x/week
        for day_offset in [0, 2, 4]:
            tt_day = week_start + timedelta(days=day_offset)
            calendar_entries.append({
                "date": tt_day.strftime("%Y-%m-%d"),
                "platform": "tiktok",
                "type": "short_form_reel",
                "title": f"TikTok Reel — W{week+1}D{day_offset//2+1}",
                "description": "Short-form vertical content (15-60s)",
                "status": "planned",
                "time": schedule.get("tiktok", "Daily 18:00 UTC")
            })

        # Instagram — 3x/week
        for day_offset in [1, 3, 5]:
            ig_day = week_start + timedelta(days=day_offset)
            calendar_entries.append({
                "date": ig_day.strftime("%Y-%m-%d"),
                "platform": "instagram",
                "type": "reel",
                "title": f"Instagram Reel — W{week+1}D{day_offset//2+1}",
                "description": "Reel optimized for Explore page",
                "status": "planned",
                "time": schedule.get("instagram", "Daily 17:00 UTC")
            })

        # LinkedIn — 2x/week
        for day_offset in [1, 3]:
            li_day = week_start + timedelta(days=day_offset)
            calendar_entries.append({
                "date": li_day.strftime("%Y-%m-%d"),
                "platform": "linkedin",
                "type": "thought_leadership_post",
                "title": f"LinkedIn Post — W{week+1}",
                "description": "Professional AI industry insights",
                "status": "planned",
                "time": schedule.get("linkedin", "Tue/Thu 14:00 UTC")
            })

        # Twitter/X — daily
        for day_offset in range(7):
            tw_day = week_start + timedelta(days=day_offset)
            calendar_entries.append({
                "date": tw_day.strftime("%Y-%m-%d"),
                "platform": "twitter",
                "type": "tweet_thread",
                "title": f"Twitter Thread — W{week+1}D{day_offset+1}",
                "description": "Short insights, tips, or build-in-public updates",
                "status": "planned",
                "time": schedule.get("twitter", "Daily 15:00 UTC")
            })

        # Blog — 2x/week
        for day_offset in [0, 3]:
            bl_day = week_start + timedelta(days=day_offset)
            calendar_entries.append({
                "date": bl_day.strftime("%Y-%m-%d"),
                "platform": "blog",
                "type": "article",
                "title": f"Blog Post — W{week+1}",
                "description": "Long-form SEO-optimized article",
                "status": "planned",
                "time": "Mon/Thu 12:00 UTC"
            })

    path = os.path.join(OUTPUT_DIR, 'calendar', 'content_calendar.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({
            "generated": datetime.now().isoformat(),
            "period": f"{today.strftime('%Y-%m-%d')} to {(today + timedelta(weeks=4)).strftime('%Y-%m-%d')}",
            "total_pieces": len(calendar_entries),
            "breakdown": {
                "youtube": sum(1 for e in calendar_entries if e["platform"] == "youtube"),
                "tiktok": sum(1 for e in calendar_entries if e["platform"] == "tiktok"),
                "instagram": sum(1 for e in calendar_entries if e["platform"] == "instagram"),
                "linkedin": sum(1 for e in calendar_entries if e["platform"] == "linkedin"),
                "twitter": sum(1 for e in calendar_entries if e["platform"] == "twitter"),
                "blog": sum(1 for e in calendar_entries if e["platform"] == "blog")
            },
            "entries": calendar_entries
        }, f, indent=2)
    return path
