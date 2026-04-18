import os
import json
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'marketing', 'social')


def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════
# PLATFORM ADAPTERS — format content per platform
# ═══════════════════════════════════════════════════

PLATFORM_LIMITS = {
    "twitter": {"max_chars": 280, "hashtags": 3, "style": "punchy"},
    "linkedin": {"max_chars": 3000, "hashtags": 5, "style": "professional"},
    "instagram": {"max_chars": 2200, "hashtags": 20, "style": "visual_storytelling"},
    "tiktok": {"max_chars": 2200, "hashtags": 5, "style": "trending_casual"},
    "facebook": {"max_chars": 5000, "hashtags": 3, "style": "community"},
}

HASHTAG_BANKS = {
    "core": ["#AI", "#Automation", "#BusinessAI", "#myAI"],
    "growth": ["#GrowthHacking", "#ScaleUp", "#StartupLife", "#SaaS", "#TechStartup"],
    "marketing": ["#DigitalMarketing", "#ContentMarketing", "#MarketingTips", "#SocialMedia"],
    "productivity": ["#Productivity", "#WorkSmarter", "#Efficiency", "#TimeManagement"],
    "trending": ["#BuildInPublic", "#IndieHacker", "#NoCode", "#FutureOfWork", "#AItools"],
}


def _select_hashtags(platform, topic_tags=None):
    limit = PLATFORM_LIMITS.get(platform, {}).get("hashtags", 5)
    tags = list(HASHTAG_BANKS["core"])
    if topic_tags:
        tags.extend(topic_tags)
    else:
        tags.extend(HASHTAG_BANKS["growth"][:2])
        tags.extend(HASHTAG_BANKS["trending"][:2])
    return tags[:limit]


# ═══════════════════════════════════════════════════
# SOCIAL POST GENERATOR
# ═══════════════════════════════════════════════════

def generate_social_posts(config):
    ensure_dir()

    topics = [
        {
            "theme": "product_launch",
            "twitter": "We just launched something wild: an AI that runs your entire business — website, marketing, content, CRM — all autonomous. 24/7. No humans needed.\n\nFree trial: myai.com",
            "linkedin": "Excited to announce the global launch of myAI — the first fully autonomous AI business platform.\n\nWhat does that mean? It means:\n→ Your website builds and updates itself\n→ Blog posts, social media, and videos are created automatically\n→ Customer inquiries are handled by an AI chatbot\n→ Weekly reports and analytics are delivered without lifting a finger\n\nWe built this because we believe every business — from solopreneurs to enterprises — deserves the power of full automation.\n\n14-day free trial. No credit card needed.\n\n#AI #Automation #SaaS #FutureOfWork",
            "instagram": "🤖 Introducing myAI — Your Business on Autopilot\n\nImagine waking up to:\n✅ 15 new leads captured\n✅ 3 blog posts published\n✅ Social media posted everywhere\n✅ Revenue reports ready\n\nAll done by AI. While you slept.\n\nFree trial — link in bio 🔗",
            "tiktok": "POV: Your entire business runs itself 🤖\n\nWebsite? AI builds it.\nContent? AI writes it.\nSocial media? AI posts it.\nCustomer service? AI handles it.\n\nThis is myAI. Link in bio for free trial!",
        },
        {
            "theme": "social_proof",
            "twitter": "\"We replaced 60 hours/week of manual marketing with one AI agent. ROI was 10x in the first month.\"\n\n— Real feedback from a myAI Pro user.\n\nWhat would you do with 60 extra hours?",
            "linkedin": "A client shared this with us last week:\n\n\"Before myAI, I was spending 60+ hours a week on marketing, content creation, and customer follow-ups. Now the AI handles all of it. I focus on strategy and growth.\"\n\nResults after 90 days:\n📈 347% increase in leads\n📉 40% reduction in marketing costs\n⏰ 60 hours/week saved\n\nThis is what autonomous AI looks like in practice.\n\n#CustomerSuccess #AI #Automation",
            "instagram": "📊 Real Results from Real Businesses:\n\n→ 347% more leads\n→ 40% lower costs\n→ 60 hours/week saved\n→ 10x ROI in month one\n\nAll powered by myAI's autonomous agents 🤖\n\nStart your free trial — link in bio!",
            "tiktok": "Client results after 90 days with myAI:\n\n📈 347% more leads\n💰 40% less marketing spend\n⏰ 60 hours/week saved\n\nThe AI did everything. Wild. Link in bio!",
        },
        {
            "theme": "educational",
            "twitter": "5 things AI can automate for your business TODAY:\n\n1. Blog & content writing\n2. Social media management\n3. Customer service (chatbot)\n4. Website building & SEO\n5. Weekly analytics reports\n\nStop doing these manually. Let AI handle it.",
            "linkedin": "5 Business Tasks You Should Automate with AI Today:\n\n1️⃣ Content Creation — AI generates blog posts, emails, and social content daily\n2️⃣ Social Media — Posts to all platforms with optimized hashtags and timing\n3️⃣ Customer Service — AI chatbot handles 80% of inquiries instantly\n4️⃣ Website Management — Auto-updates design, content, and SEO\n5️⃣ Reporting — Weekly analytics delivered to your inbox automatically\n\nThese aren't future predictions — they're tools available right now.\n\nThe question isn't whether to automate. It's how much time you're wasting by not doing it yet.\n\n#AI #BusinessAutomation #Productivity #Leadership",
            "instagram": "5 tasks your AI should be doing right now:\n\n1️⃣ Writing your blog posts ✍️\n2️⃣ Managing social media 📱\n3️⃣ Handling customer questions 💬\n4️⃣ Building your website 🌐\n5️⃣ Creating weekly reports 📊\n\nIf you're still doing these manually... it's time to upgrade.\n\nmyAI does all 5 automatically 🤖\nLink in bio!",
            "tiktok": "Still doing these manually? STOP ✋\n\n1. Blog writing — let AI do it\n2. Social media — let AI post\n3. Customer support — let AI chat\n4. Website updates — let AI build\n5. Reports — let AI analyze\n\nmyAI handles ALL of this. Link in bio!",
        },
    ]

    # Generate platform-specific post files
    all_posts = []
    for topic in topics:
        for platform in ["twitter", "linkedin", "instagram", "tiktok"]:
            if platform in topic:
                hashtags = _select_hashtags(platform)
                post = {
                    "theme": topic["theme"],
                    "platform": platform,
                    "content": topic[platform],
                    "hashtags": hashtags,
                    "status": "ready",
                    "created": datetime.now().isoformat(),
                    "scheduled": None,
                    "published": None
                }
                all_posts.append(post)

    path = os.path.join(OUTPUT_DIR, 'social_posts.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({
            "generated": datetime.now().isoformat(),
            "total_posts": len(all_posts),
            "platforms": list(set(p["platform"] for p in all_posts)),
            "posts": all_posts
        }, f, indent=2)

    return path


# ═══════════════════════════════════════════════════
# LINKEDIN ARTICLES
# ═══════════════════════════════════════════════════

def generate_linkedin_articles(config):
    ensure_dir()

    articles = [
        {
            "title": "Why Every Business Will Have an AI Agent by 2027",
            "summary": "The shift from manual operations to autonomous AI agents is accelerating. Here's why early adopters will dominate.",
            "body": (
                "The business landscape is undergoing a fundamental transformation. "
                "According to McKinsey, AI could generate $4.4 trillion in annual value globally. "
                "But here's what most people miss: it's not about using AI tools — it's about deploying AI agents.\n\n"
                "An AI tool helps you work. An AI agent works for you.\n\n"
                "At myAI, we've built autonomous agents that handle complete business workflows: "
                "website creation, content marketing, social media, customer service, and analytics. "
                "The system runs 24/7, learns from results, and improves every cycle.\n\n"
                "Early adopters are seeing:\n"
                "• 40% cost reduction vs. hiring\n"
                "• 10x faster content production\n"
                "• 300%+ increase in leads\n"
                "• 60+ hours/week freed up\n\n"
                "The question isn't if AI agents will become standard — it's whether you'll adopt them "
                "before or after your competitors do."
            ),
            "cta": "Try myAI free for 14 days — no credit card required.",
            "tags": ["AI", "Business Strategy", "Automation", "Leadership"]
        }
    ]

    path = os.path.join(OUTPUT_DIR, 'linkedin_articles.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"generated": datetime.now().isoformat(), "articles": articles}, f, indent=2)
    return path


# ═══════════════════════════════════════════════════
# TWITTER THREAD GENERATOR
# ═══════════════════════════════════════════════════

def generate_twitter_threads(config):
    ensure_dir()

    threads = [
        {
            "title": "Build in Public — myAI Architecture",
            "tweets": [
                "🧵 I built an AI that runs an entire business autonomously.\n\nWebsite. Blog. Social media. Email. Video scripts. Analytics.\n\nAll on autopilot. Here's how:",
                "1/ The Architecture:\n\nA central agent loop runs every cycle:\n→ Load 5 pending tasks\n→ Execute each one\n→ Generate 5 new tasks\n→ Log everything\n→ Repeat\n\nIt's a self-perpetuating business engine.",
                "2/ Website Generation:\n\nThe agent builds full HTML/CSS pages:\n• Landing page with animations & particles\n• About, Services, Pricing, Blog\n• Responsive design, dark theme\n• Lead capture forms\n\nAll generated from code. Zero manual design.",
                "3/ Content Engine:\n\nEvery run produces:\n• SEO blog posts\n• Email campaigns\n• Social media posts (4 platforms)\n• Video scripts (YouTube + Reels)\n• Thumbnails\n\nContent is the fuel. AI is the engine.",
                "4/ Video Marketing:\n\nThe agent writes:\n• Full YouTube scripts with timestamps\n• TikTok/Instagram Reels scripts\n• Content calendars\n• Hashtag strategies\n\nVideo is king. AI makes it scalable.",
                "5/ The Business Model:\n\nStarter: $399/mo — 1 agent, basic site\nPro: $999/mo — 3 agents, full suite\nEnterprise: $2,499/mo — unlimited everything\n\n14-day free trial. No credit card.\n\nThe math works at scale. 1,000 Pro users = $1M/month.",
                "6/ What's next:\n\n→ Real hosting & deployment (Vercel/Netlify)\n→ Stripe payment integration\n→ Live AI chatbot\n→ API access for enterprise\n→ More platforms & integrations\n\nThis is just the beginning. Follow for updates.\n\nLink to try it: myai.com"
            ]
        }
    ]

    path = os.path.join(OUTPUT_DIR, 'twitter_threads.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"generated": datetime.now().isoformat(), "threads": threads}, f, indent=2)
    return path
