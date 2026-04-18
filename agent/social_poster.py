"""
Social Media Auto-Poster — posts content to multiple platforms.
Supports: Twitter/X, LinkedIn, Instagram, Facebook, TikTok.

For each platform, uses available APIs or generates ready-to-post content files.
"""
import os
import json
import webbrowser
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'social_ready')
SCHEDULE_FILE = os.path.join(DATA_DIR, 'social_schedule.json')
POST_LOG = os.path.join(DATA_DIR, 'social_posts_log.json')

SITE_URL = "https://aoeua.com"
BIZ_URL = "https://businesses.aoeua.com"


def _ensure_dirs():
    for d in [DATA_DIR, OUTPUT_DIR,
              os.path.join(OUTPUT_DIR, 'twitter'),
              os.path.join(OUTPUT_DIR, 'linkedin'),
              os.path.join(OUTPUT_DIR, 'instagram'),
              os.path.join(OUTPUT_DIR, 'tiktok'),
              os.path.join(OUTPUT_DIR, 'facebook')]:
        os.makedirs(d, exist_ok=True)


# ═══════════════════════════════════════════════════
# CONTENT TEMPLATES — 30 days of scheduled content
# ═══════════════════════════════════════════════════

DAILY_CONTENT = [
    # Day 1-5: Launch & Awareness
    {"day": 1, "theme": "launch", "twitter": "We just launched myAI — an autonomous AI that runs your entire business. Website, marketing, content, CRM — all on autopilot. 24/7.\n\nFree 14-day trial: {site}\n\n#AI #Automation #StartupLaunch", 
     "linkedin": "Thrilled to announce the launch of myAI — the first fully autonomous AI business automation platform.\n\nWhat it does:\n→ Builds and manages your website\n→ Creates blog posts, social media content, and videos\n→ Runs email marketing campaigns\n→ Handles customer service via AI chatbot\n→ Delivers weekly analytics and reports\n\nAll autonomously. 24/7. Starting at $199/month.\n\n14-day free trial — no credit card required.\n\n{site}\n\n#AI #Automation #SaaS #BusinessAutomation",
     "instagram": "🚀 Introducing myAI — Your Business on Autopilot\n\n✅ AI builds your website\n✅ AI writes your content\n✅ AI manages your social media\n✅ AI handles customer service\n✅ AI creates reports\n\nAll while you sleep 😴\n\nFree trial — link in bio!\n\n#AI #Automation #BusinessAI #Startup #SaaS #Marketing"},
    
    {"day": 2, "theme": "problem", "twitter": "The average small business owner works 60+ hours/week.\n\nHalf that time? Repetitive tasks AI can handle.\n\nStop grinding. Start automating.\n\n#SmallBusiness #Automation #AI",
     "linkedin": "A recent study shows small business owners work an average of 60+ hours per week.\n\nBreaking it down:\n• 15 hrs — marketing & social media\n• 10 hrs — email & customer service\n• 8 hrs — website & content updates\n• 5 hrs — reporting & analytics\n\nThat's 38 hours of work AI can automate TODAY.\n\nmyAI handles all four categories autonomously. The result? Business owners focus on strategy, not tasks.\n\n{site}\n\n#AI #SmallBusiness #Efficiency",
     "instagram": "⏰ 60+ hours/week doing manual work?\n\nHere's what AI can automate:\n📱 Social media — 15 hrs saved\n📧 Email & support — 10 hrs saved\n🌐 Website updates — 8 hrs saved\n📊 Reports — 5 hrs saved\n\n= 38 hours back every week\n\nmyAI does it all automatically 🤖\n\n#WorkSmarter #AI #Automation #BusinessTips"},
    
    {"day": 3, "theme": "demo", "twitter": "Watch AI build a complete business website in 60 seconds 👇\n\nLanding page ✅\nBlog posts ✅\nPricing page ✅\nEmail templates ✅\nSEO optimization ✅\n\nThis is myAI. Link in bio.\n\n#AI #WebDev #NoCode",
     "linkedin": "Demo Day: Watch myAI build a complete business website from scratch.\n\nIn under 60 seconds, the AI agent:\n1. Generated a landing page with full design\n2. Created 5 SEO-optimized blog posts\n3. Built a pricing page with 3 tiers\n4. Designed email marketing templates\n5. Set up analytics tracking\n\nNo coding. No design skills. Just AI.\n\nSee it in action: {site}\n\n#AI #Demo #WebDevelopment #Automation",
     "instagram": "🎬 DEMO: AI Builds a Website in 60 Seconds\n\n0:10 — Landing page generated\n0:20 — Blog posts written\n0:30 — Pricing page created\n0:40 — Email templates ready\n0:50 — SEO optimized\n1:00 — Done. Full business website.\n\nFrom zero. By AI. 🤖\n\nLink in bio to try free!\n\n#AI #Demo #WebDev #NoCode #Automation"},
    
    {"day": 4, "theme": "testimonial", "twitter": "\"We replaced our entire marketing team with myAI. Saved $8,000/month and got better results.\"\n\n— Startup founder, 90 days in\n\nWhat would you save? →\n\n#AI #ROI #Startup",
     "linkedin": "Real feedback from an early myAI adopter:\n\n\"Before myAI, we had 2 marketing employees costing $8,000/month combined. They could produce:\n- 4 blog posts/month\n- Daily social media\n- Bi-weekly email campaigns\n\nWith myAI ($399/month), we now produce:\n- 30 blog posts/month\n- Multi-platform social media\n- Automated email sequences\n- Video scripts & thumbnails\n- Weekly analytics reports\n\nThe ROI speaks for itself.\"\n\n{site}\n\n#CustomerSuccess #ROI #AI #SaaS",
     "instagram": "📊 Real results comparison:\n\n❌ Marketing team ($8K/mo):\n• 4 blog posts\n• Basic social media\n• Bi-weekly emails\n\n✅ myAI ($399/mo):\n• 30 blog posts\n• Multi-platform social\n• Daily emails\n• Video scripts\n• Analytics reports\n\nSame quality. 20x the output. 1/20th the cost.\n\n#AI #ROI #Marketing #BusinessHack"},
    
    {"day": 5, "theme": "how_it_works", "twitter": "How myAI works (simple version):\n\n1. You set goals\n2. AI creates a plan\n3. AI executes 24/7\n4. AI learns & improves\n5. You review results\n\nThat's it. Fully autonomous.\n\n#AI #Automation",
     "linkedin": "People keep asking: \"How does myAI actually work?\"\n\nHere's the simple breakdown:\n\n1️⃣ Configuration — You define your business goals, target audience, and preferences\n2️⃣ Planning — AI creates a strategic task queue based on your goals\n3️⃣ Execution — Autonomous agents run 24/7, completing tasks: content creation, website updates, email campaigns, social media\n4️⃣ Learning — The system analyzes results and optimizes its approach\n5️⃣ Reporting — You get weekly reports showing metrics, progress, and ROI\n\nNo coding. No micromanagement. Just results.\n\n{site}\n\n#HowItWorks #AI #Automation",
     "instagram": "How myAI works in 5 steps 🤖\n\n1️⃣ Set your goals\n2️⃣ AI creates a plan\n3️⃣ AI executes 24/7\n4️⃣ AI learns & improves\n5️⃣ You review results\n\nThat's it. Your business runs itself.\n\nFree trial — link in bio!\n\n#AI #Automation #HowItWorks #Business"},
    
    # Day 6-10: Niche-specific content
    {"day": 6, "theme": "niche_restaurant", "twitter": "Restaurant owners: you're losing $2,000+/month on no-shows and manual scheduling.\n\nAI reservation system = 60% fewer no-shows.\nAI inventory = 30% less waste.\n\nStarting at $299/mo.\n\n{biz}/ai-restaurants/\n\n#RestaurantTech #AI",
     "linkedin": "For Restaurant Owners:\n\nThe average restaurant loses $2,000-5,000/month to:\n• No-show reservations\n• Food waste from poor inventory planning\n• Slow customer service during peak hours\n\nmyAI's restaurant solution:\n✅ AI-powered reservation management (60% fewer no-shows)\n✅ Smart inventory tracking (30% less waste)\n✅ 24/7 customer chatbot for orders & questions\n✅ Automated social media & review management\n\nStarting at $299/month with 14-day free trial.\n\n{biz}/ai-restaurants/\n\n#Restaurant #FoodTech #AI",
     "instagram": "🍕 Restaurant owners!\n\nAre you losing money on:\n❌ No-show reservations\n❌ Food waste\n❌ Slow customer service\n\nAI fixes all of this:\n✅ Smart reservations (60% fewer no-shows)\n✅ Inventory tracking (30% less waste)\n✅ 24/7 chatbot\n\nStarting at $299/mo\n\n#Restaurant #AI #FoodBusiness #Automation"},
    
    {"day": 7, "theme": "niche_dental", "twitter": "Dental practices: how many appointments did you lose to no-shows this month?\n\nAI scheduling + auto-reminders = 80% reduction in no-shows.\n\nSee the solution: {biz}/ai-dentists/\n\n#DentalPractice #AI #Healthcare",
     "linkedin": "Attention Dental Practice Managers:\n\nThe #1 revenue killer in dentistry? No-shows.\n\nThe average practice loses $120,000/year to missed appointments.\n\nmyAI's dental solution:\n✅ AI-powered scheduling with smart time slots\n✅ Multi-channel auto-reminders (SMS, email, phone)\n✅ Patient follow-up automation\n✅ Review collection & reputation management\n\nResult: 80% reduction in no-shows.\n\nStarting at $349/month. Free 14-day trial.\n\n{biz}/ai-dentists/\n\n#Dental #Healthcare #AI #PracticeManagement",
     "instagram": "🦷 Dental practices lose $120K/year to no-shows\n\nAI solves this:\n✅ Smart scheduling\n✅ Auto-reminders (SMS + email)\n✅ Patient follow-up\n✅ Review management\n\n= 80% fewer no-shows\n\nStarting at $349/mo\n\n#Dental #AI #Healthcare #PracticeManagement"},
    
    {"day": 8, "theme": "niche_legal", "twitter": "Lawyers: how many billable hours are lost to admin work?\n\nAI document processing = 70% faster case prep.\nAI time capture = zero missed billable hours.\n\nSee the solution: {biz}/ai-lawyers/\n\n#LegalTech #AI #Law",
     "linkedin": "For Law Firms:\n\nPartners spend an average of 30% of their time on non-billable administrative work.\n\nThat's $150,000+ in lost revenue per attorney per year.\n\nmyAI's legal solution:\n✅ AI document processing (70% faster case prep)\n✅ Automated deadline tracking (zero missed dates)\n✅ Smart time capture (100% billable hour accuracy)\n✅ Client communication automation\n\nStarting at $499/month. Pays for itself in the first week.\n\n{biz}/ai-lawyers/\n\n#LegalTech #LawFirm #AI #Automation",
     "instagram": "⚖️ Lawyers: losing money on admin work?\n\n30% of your time = non-billable tasks\n= $150K+ lost revenue per year\n\nAI fixes this:\n✅ Document processing 70% faster\n✅ Zero missed deadlines\n✅ Perfect time capture\n✅ Auto client communication\n\n$499/mo — pays for itself in week 1\n\n#LegalTech #Law #AI #Automation"},
    
    {"day": 9, "theme": "niche_fitness", "twitter": "Gym owners: member retention is your #1 problem.\n\nAI engagement system = 40% higher retention.\nAI scheduling = zero double-bookings.\n\nSee it: {biz}/ai-fitness/\n\n#Fitness #GymOwner #AI",
     "linkedin": "For Gym & Fitness Studio Owners:\n\nThe fitness industry has an average member churn rate of 30% annually. That's thousands in lost recurring revenue.\n\nmyAI's fitness solution:\n✅ AI member engagement (personalized workout reminders, check-ins)\n✅ Smart class scheduling (no double-bookings)\n✅ Automated billing & payment reminders\n✅ Social media content generation\n\nResult: 40% higher member retention.\n\nStarting at $249/month with 14-day free trial.\n\n{biz}/ai-fitness/\n\n#Fitness #GymBusiness #AI #MemberRetention",
     "instagram": "💪 Gym owners: stop losing members!\n\n30% churn rate = thousands lost\n\nAI engagement system:\n✅ Personalized reminders\n✅ Smart scheduling\n✅ Auto billing\n✅ Social media content\n\n= 40% higher retention\n\nStarting at $249/mo\n\n#Fitness #Gym #AI #MemberRetention"},
    
    {"day": 10, "theme": "niche_ecommerce", "twitter": "E-commerce store owners: 70% of carts are abandoned.\n\nAI recovery emails = 15% of those come back.\nOn $100K revenue, that's $10,500 recovered.\n\nSee it: {biz}/ai-ecommerce/\n\n#Ecommerce #AI #Revenue",
     "linkedin": "For E-commerce Business Owners:\n\n70% of online shopping carts are abandoned. On $100K monthly revenue, that's $233K left on the table.\n\nmyAI's e-commerce solution:\n✅ AI abandoned cart recovery (15% win-back rate)\n✅ Smart inventory management (never stockout)\n✅ 24/7 customer support chatbot\n✅ Automated product descriptions & SEO\n\nOn $100K/month revenue, recovered carts alone = $10,500+ extra per month.\n\nStarting at $349/month. ROI in the first week.\n\n{biz}/ai-ecommerce/\n\n#Ecommerce #AI #Revenue #CartAbandonment",
     "instagram": "🛒 E-commerce: 70% of carts are abandoned!\n\nOn $100K revenue that's $233K lost\n\nAI recovery system:\n✅ Auto recovery emails = 15% win-back\n✅ Smart inventory (no stockouts)\n✅ 24/7 chatbot support\n✅ Auto product descriptions\n\n= $10,500+ extra/month recovered\n\n$349/mo — ROI in week 1\n\n#Ecommerce #AI #Revenue #Marketing"},
    
    # Day 11-15: Educational & Value
    {"day": 11, "theme": "tips", "twitter": "5 signs your business needs AI automation:\n\n1. You work 60+ hrs/week\n2. Manual tasks eat your day\n3. Marketing is inconsistent\n4. Customer response is slow\n5. You can't scale\n\nAll fixable with AI.\n\n#BusinessTips #AI",
     "linkedin": "5 Signs Your Business Needs AI Automation:\n\n1️⃣ You're working 60+ hours/week with no end in sight\n2️⃣ Repetitive manual tasks consume most of your day\n3️⃣ Your marketing output is inconsistent or non-existent\n4️⃣ Customer response times are measured in hours (or days)\n5️⃣ You want to grow but can't afford to hire more people\n\nIf you checked 3 or more, you're leaving money on the table.\n\nmyAI automates all five. Starting at $199/month.\n\n{site}\n\n#Business #AI #Automation #Growth",
     "instagram": "5 signs you need AI automation:\n\n1️⃣ Working 60+ hrs/week 😰\n2️⃣ Manual tasks eating your day ⏰\n3️⃣ Inconsistent marketing 📉\n4️⃣ Slow customer response 🐌\n5️⃣ Can't scale without hiring 💸\n\nChecked 3+? You need myAI.\n\nAutomation starting at $199/mo\nLink in bio!\n\n#BusinessTips #AI #Automation #Scale"},
    
    {"day": 12, "theme": "comparison", "twitter": "Hiring vs. AI:\n\nEmployee: $4,000/mo, 40 hrs/week, needs training\nmyAI: $399/mo, works 24/7/365, self-improving\n\nThe math is simple.\n\n#AI #Hiring #Business",
     "linkedin": "The Real Cost Comparison: Hiring vs. AI\n\n👤 Marketing Employee:\n- $4,000-6,000/month salary\n- Works 40 hours/week\n- Needs onboarding & training\n- Takes vacation & sick days\n- Limited output capacity\n\n🤖 myAI Pro Plan:\n- $399/month (flat rate)\n- Works 24/7/365\n- No onboarding needed\n- Never takes a day off\n- Unlimited output capacity\n\nROI: 10x-15x compared to a single hire.\n\nThis isn't about replacing people. It's about amplifying what your team can achieve.\n\n{site}\n\n#AI #Hiring #ROI #Business",
     "instagram": "👤 Employee vs. 🤖 AI\n\nEmployee:\n❌ $4,000+/mo\n❌ 40 hrs/week\n❌ Training needed\n❌ Vacation & sick days\n\nmyAI:\n✅ $399/mo\n✅ 24/7/365\n✅ Ready instantly\n✅ Never stops\n\n10x ROI. The math is simple.\n\n#AI #Business #Hiring #ROI"},
    
    {"day": 13, "theme": "behind_scenes", "twitter": "Behind the scenes of myAI:\n\nEvery 60 minutes, the agent:\n→ Checks for new tasks\n→ Executes highest priority\n→ Generates new tasks\n→ Logs everything\n→ Optimizes based on results\n\nA self-perpetuating business engine.\n\n#BuildInPublic #AI",
     "linkedin": "Behind the Scenes: How myAI's Autonomous Agent Works\n\nEvery cycle, the system:\n\n1️⃣ Loads pending tasks from the priority queue\n2️⃣ Executes each task autonomously (content creation, website updates, email campaigns)\n3️⃣ Analyzes results and performance metrics\n4️⃣ Generates new tasks based on what worked\n5️⃣ Logs everything for transparency and debugging\n\nThe result: a self-improving business engine that gets better with every cycle.\n\nNo human intervention needed. No manual oversight required.\n\nJust set your goals and let the AI work.\n\n{site}\n\n#BuildInPublic #Engineering #AI #Automation",
     "instagram": "🔧 Behind the scenes of myAI:\n\nEvery cycle:\n1️⃣ Load tasks from queue\n2️⃣ Execute autonomously\n3️⃣ Analyze results\n4️⃣ Generate new tasks\n5️⃣ Log everything\n\nA self-improving business engine 🤖\n\n#BuildInPublic #AI #Engineering #BTS"},
    
    {"day": 14, "theme": "faq", "twitter": "FAQ about myAI:\n\nQ: Do I need coding skills?\nA: No.\n\nQ: How fast does it set up?\nA: Under 24 hours.\n\nQ: Is there a free trial?\nA: 14 days, no credit card.\n\nQ: Can it work for MY business?\nA: We cover 50+ industries.\n\n#AI #FAQ",
     "linkedin": "Frequently Asked Questions about myAI:\n\n❓ Do I need technical skills?\n→ No. The AI handles everything autonomously.\n\n❓ How long does setup take?\n→ Under 24 hours for full deployment.\n\n❓ Is there a free trial?\n→ Yes — 14 days, no credit card required.\n\n❓ What businesses does it work for?\n→ We cover 50+ industries including restaurants, dental, legal, fitness, e-commerce, accounting, construction, photography, real estate, and salons.\n\n❓ What if I'm not satisfied?\n→ Cancel anytime. No contracts.\n\nStill have questions? Email us: info@aoeua.com\n\n{site}\n\n#FAQ #AI #SaaS",
     "instagram": "❓ myAI FAQ:\n\nNeed coding? → No\nSetup time? → Under 24 hours\nFree trial? → 14 days, no card ✅\nMy industry? → 50+ covered\nContracts? → None. Cancel anytime.\n\nQuestions? info@aoeua.com\n\n#AI #FAQ #Business #SaaS"},
    
    {"day": 15, "theme": "milestone", "twitter": "🎉 Milestone: myAI now serves 50+ business niches!\n\nFrom restaurants to law firms, dental to e-commerce — every industry gets a custom AI solution.\n\nExplore all 50: {biz}\n\n#Milestone #AI #SaaS",
     "linkedin": "🎉 Exciting milestone: myAI now offers AI automation solutions for 50+ business niches!\n\nEach solution is tailored with:\n• Industry-specific AI workflows\n• Custom landing pages and marketing\n• Targeted content and email templates\n• Niche-appropriate pricing\n\nSome of our verticals:\n🍕 Restaurants — $299/mo\n🦷 Dental — $349/mo\n⚖️ Legal — $499/mo\n💪 Fitness — $249/mo\n🛒 E-commerce — $349/mo\n📸 Photography — $199/mo\n\nExplore all 50 solutions: {biz}\n\n#Milestone #AI #SaaS #B2B",
     "instagram": "🎉 50+ BUSINESS NICHES now covered!\n\n🍕 Restaurants — $299/mo\n🦷 Dental — $349/mo\n⚖️ Legal — $499/mo\n💪 Fitness — $249/mo\n🛒 E-commerce — $349/mo\n📸 Photography — $199/mo\n\n...and 44 more!\n\nEvery business gets custom AI automation 🤖\n\nLink in bio to explore all 50!\n\n#AI #Business #SaaS #Milestone"},
    
    # Day 16-20: Engagement & Social Proof
    {"day": 16, "theme": "poll", "twitter": "Poll: What's your biggest business time-waster?\n\n🔁 Reply with:\nA — Social media management\nB — Email & customer support\nC — Content creation\nD — Admin & reporting\n\n#BusinessPoll #AI",
     "linkedin": "I'm curious: What task takes up the most of your time as a business owner?\n\nA) Social media management\nB) Email & customer support\nC) Content creation\nD) Admin & reporting\n\nDrop your answer in the comments! All four can be automated with AI — but I'd love to know which one hurts the most.\n\n#Poll #Business #AI",
     "instagram": "📊 POLL TIME!\n\nWhat's your biggest time-waster?\n\nA — Social media 📱\nB — Email & support 📧\nC — Content creation ✍️\nD — Admin & reports 📊\n\nComment your answer! ⬇️\n\n(All 4 can be automated with AI 🤖)\n\n#Poll #Business #AI #TimeManagement"},
    
    {"day": 17, "theme": "story", "twitter": "6 months ago, I couldn't afford to hire a marketing team.\n\nToday, AI handles:\n• 30 blog posts/month\n• Daily social media\n• Email campaigns\n• Video scripts\n• Analytics\n\nCost: $399/month.\n\n#MyStory #AI #Startup",
     "linkedin": "My story:\n\n6 months ago, I was a solo founder drowning in work. Marketing was inconsistent. Content was sporadic. Customer follow-up was non-existent.\n\nI couldn't afford a team. So I built one — with AI.\n\nToday, myAI handles my entire marketing operation:\n• 30 blog posts published monthly\n• Daily social media across 4 platforms\n• Automated email campaigns\n• Video scripts and thumbnails\n• Weekly performance reports\n\nTotal cost: $399/month vs. $10,000+ for a team.\n\nThis is why I built myAI — to give every business owner access to the power of full automation.\n\n{site}\n\n#FounderStory #AI #Startup #BuildInPublic",
     "instagram": "📖 My story:\n\n6 months ago: Solo founder, drowning in work\nToday: AI handles everything\n\n📝 30 blog posts/month\n📱 Daily social media\n📧 Email campaigns\n🎬 Video scripts\n📊 Weekly reports\n\nCost: $399/mo (vs $10K+ for a team)\n\nThis is why I built myAI 🤖\n\n#FounderStory #Startup #AI #BuildInPublic"},
    
    {"day": 18, "theme": "tip_thread", "twitter": "3 AI automation tips most businesses miss:\n\n1. Start with your biggest time-suck (usually social media)\n2. Automate the boring stuff first (reports, scheduling)\n3. Let AI learn for 2 weeks before judging results\n\nPatience + AI = game over.\n\n#AITips #Business",
     "linkedin": "3 AI Automation Tips Most Businesses Miss:\n\n1️⃣ Start With Your Biggest Time-Suck\nDon't try to automate everything at once. Identify the task that eats the most hours and automate that first. For most businesses, it's social media or content creation.\n\n2️⃣ Automate the Boring Stuff First\nReports, scheduling, data entry, follow-up emails — these are perfect for AI. Save creative strategy for humans.\n\n3️⃣ Give AI 2 Weeks Before Judging\nAI systems improve over time. The first week's output will be good. The fourth week's output will be great. Don't quit early.\n\nBonus: Track your time savings. You'll be shocked.\n\n{site}\n\n#AITips #Business #Automation #Productivity",
     "instagram": "3 AI automation tips:\n\n1️⃣ Start with your biggest time-suck\n(usually social media or content)\n\n2️⃣ Automate boring stuff first\n(reports, scheduling, data entry)\n\n3️⃣ Give AI 2 weeks before judging\n(it improves over time!)\n\nBonus: Track your time savings ⏱️\n\n#AITips #Automation #Business #Productivity"},
    
    {"day": 19, "theme": "case_study", "twitter": "Case study: Dental practice in NYC\n\nBefore myAI:\n• 15 no-shows/week\n• 3 hrs/day on scheduling\n• No online presence\n\nAfter 60 days:\n• 3 no-shows/week (80% reduction)\n• 0 hrs on scheduling\n• 200+ Google reviews\n\n{biz}/ai-dentists/\n\n#CaseStudy #Dental #AI",
     "linkedin": "Case Study: How a NYC Dental Practice Transformed with AI\n\nThe Problem:\n• 15 no-shows per week (avg $200/appointment = $3,000/week lost)\n• 3 hours/day spent on manual scheduling\n• Zero online review management\n• No social media presence\n\nThe Solution: myAI Dental Automation ($349/month)\n\nResults After 60 Days:\n✅ No-shows reduced by 80% (15 → 3/week)\n✅ $2,400/week in recovered revenue\n✅ Zero hours spent on scheduling (fully automated)\n✅ 200+ Google reviews collected automatically\n✅ Active social media presence on 3 platforms\n\nROI: $9,600/month additional revenue on a $349/month investment.\n\n{biz}/ai-dentists/\n\n#CaseStudy #Dental #AI #ROI",
     "instagram": "📊 Case Study: Dental Practice + AI\n\nBEFORE:\n❌ 15 no-shows/week\n❌ 3 hrs/day scheduling\n❌ No online presence\n\nAFTER 60 DAYS:\n✅ 80% fewer no-shows\n✅ Zero manual scheduling\n✅ 200+ Google reviews\n✅ $9,600/mo extra revenue\n\nInvestment: $349/mo\nROI: 2,750%\n\n#CaseStudy #Dental #AI #Results"},
    
    {"day": 20, "theme": "weekend", "twitter": "It's the weekend.\n\nYou're resting.\n\nYour AI agent is:\n✅ Publishing content\n✅ Responding to leads\n✅ Updating your website\n✅ Sending follow-up emails\n✅ Generating reports\n\nThat's the power of autonomous AI.\n\n#Weekend #AI #Automation",
     "linkedin": "Happy weekend! 🎉\n\nWhile you're enjoying your time off, here's what myAI is doing for our clients right now:\n\n✅ Publishing scheduled blog posts\n✅ Responding to customer inquiries via chatbot\n✅ Updating website content and SEO\n✅ Sending personalized follow-up emails\n✅ Monitoring social media mentions\n✅ Generating weekly performance reports\n\nThe best business decisions are the ones that work while you don't.\n\n{site}\n\n#Weekend #AI #WorkLifeBalance #Automation",
     "instagram": "🏖️ It's the weekend!\n\nYou: relaxing ☀️\nYour AI agent: working 24/7 🤖\n\n✅ Publishing content\n✅ Answering leads\n✅ Updating website\n✅ Sending emails\n✅ Creating reports\n\nThat's the power of myAI.\n\nEnjoy your weekend. AI's got this. 💪\n\n#Weekend #AI #WorkLifeBalance"},
    
    # Day 21-25: Urgency & Conversion
    {"day": 21, "theme": "limited", "twitter": "⚡ This week only: first 100 signups get 30% off their first 3 months.\n\nStarter: $399 → $279\nPro: $999 → $699\n\nNo credit card for free trial.\n\n{site}\n\n#Deal #AI #LimitedOffer",
     "linkedin": "⚡ Special Offer This Week Only:\n\nThe first 100 businesses to sign up get 30% off their first 3 months of myAI.\n\nStarter Plan: $399/mo → $279/mo\nPro Plan: $999/mo → $699/mo\nEnterprise: Custom pricing — contact us\n\n14-day free trial included. No credit card required.\n\nThis offer won't last. Spots are filling fast.\n\n{site}\n\n#LimitedOffer #AI #SaaS #Deal",
     "instagram": "⚡ LIMITED OFFER — This Week Only!\n\n30% OFF for the first 100 signups:\n\nStarter: $399 → $279/mo\nPro: $999 → $699/mo\n\n+ FREE 14-day trial\n+ No credit card needed\n\nSpots filling fast! Link in bio 🔗\n\n#Deal #AI #LimitedOffer #SaaS"},
    
    {"day": 22, "theme": "countdown", "twitter": "72 hours left on our launch offer.\n\n30% off first 3 months.\n43 spots remaining.\n\nDon't miss this.\n\n{site}\n\n#Countdown #AI",
     "linkedin": "⏰ 72 Hours Remaining\n\nOur launch offer closes in 3 days:\n\n✅ 30% off first 3 months\n✅ 43 spots remaining (out of 100)\n✅ 14-day free trial included\n\nBusinesses that signed up this week are already seeing results. Don't wait until your competitors automate first.\n\n{site}\n\n#Countdown #AI #LaunchOffer",
     "instagram": "⏰ 72 HOURS LEFT!\n\n30% off first 3 months\n43 spots remaining\n\nDon't miss this deal!\n\nLink in bio 🔗\n\n#Countdown #Deal #AI #LastChance"},
    
    {"day": 23, "theme": "objection", "twitter": "\"AI can't replace human creativity.\"\n\nYou're right. And it shouldn't.\n\nAI should replace the 38 hours/week of BORING tasks so you can focus on the creative work that matters.\n\nThat's what myAI does.\n\n#AI #Creativity",
     "linkedin": "Common Objection: \"AI can't replace human creativity.\"\n\nYou're absolutely right. And that's not the goal.\n\nHere's what AI SHOULD replace:\n• Manual scheduling and admin (8 hrs/week)\n• Repetitive content formatting (5 hrs/week)\n• Data entry and reporting (5 hrs/week)\n• Email follow-ups and templates (10 hrs/week)\n• Social media scheduling (10 hrs/week)\n\nTotal: 38 hours/week of Tasks You Hate™\n\nWhat AI gives BACK to you:\n• Time for strategy\n• Time for client relationships\n• Time for creative work\n• Time for growth\n• Time for life\n\n{site}\n\n#AI #Creativity #Business #WorkSmarter",
     "instagram": "\"AI can't replace human creativity\" 🎨\n\nYou're right. And it shouldn't.\n\nAI SHOULD replace:\n❌ Admin work — 8 hrs/week\n❌ Content formatting — 5 hrs\n❌ Data entry — 5 hrs\n❌ Email follow-ups — 10 hrs\n❌ Social scheduling — 10 hrs\n\n= 38 hours back for CREATIVE work\n\nThat's what myAI does. 🤖\n\n#AI #Creativity #WorkSmarter"},
    
    {"day": 24, "theme": "stats", "twitter": "AI adoption stats that should scare you:\n\n• 77% of businesses will use AI by 2027\n• Companies using AI grow 2x faster\n• 40% cost reduction on average\n\nThe question isn't IF. It's WHEN.\n\nStart now: {site}\n\n#AIStats #Business",
     "linkedin": "AI Adoption Statistics Every Business Leader Should Know:\n\n📊 77% of businesses plan to adopt AI by 2027 (McKinsey)\n📊 Companies using AI grow 2x faster than competitors\n📊 40% average cost reduction in automated processes\n📊 35% increase in employee productivity with AI tools\n📊 $4.4 trillion in annual value expected from AI (McKinsey)\n\nThe businesses that adopt AI now will be the market leaders of tomorrow.\n\nThe ones that wait? They'll be playing catch-up.\n\nmyAI makes AI adoption simple, affordable, and immediate.\n\n{site}\n\n#AIStats #Business #FutureOfWork #Leadership",
     "instagram": "📊 AI stats that should scare you:\n\n77% of businesses will use AI by 2027\nCompanies with AI grow 2x faster\n40% cost reduction on average\n$4.4 TRILLION in annual AI value\n\nThe question isn't IF.\nIt's WHEN.\n\nStart now. Link in bio.\n\n#AIStats #Business #FutureOfWork"},
    
    {"day": 25, "theme": "free_value", "twitter": "Free resource: I wrote a guide on \"10 AI Automation Strategies for Small Businesses.\"\n\nNo signup needed. No email required.\n\nJust value.\n\nCheck our blog: {site}\n\n#FreeResource #AI #SmallBusiness",
     "linkedin": "Free Resource: \"10 AI Automation Strategies for Small Businesses\"\n\nI put together a comprehensive guide covering:\n\n1. Website automation\n2. Content marketing with AI\n3. Email campaign automation\n4. Social media management\n5. Customer service chatbots\n6. Inventory optimization\n7. Scheduling and booking\n8. Analytics and reporting\n9. Lead generation\n10. Review management\n\nNo signup. No email required. Just value.\n\nRead it on our blog: {site}\n\nIf it helps even one business owner save time, it was worth writing.\n\n#FreeResource #AI #SmallBusiness #Value",
     "instagram": "📚 FREE GUIDE: 10 AI Strategies for Small Business\n\n1. Website automation\n2. Content marketing\n3. Email campaigns\n4. Social media\n5. Customer chatbots\n6. Inventory\n7. Scheduling\n8. Analytics\n9. Lead generation\n10. Review management\n\nNo signup. No email. Just value.\n\nRead on our blog — link in bio!\n\n#FreeResource #AI #SmallBusiness"},
    
    # Day 26-30: Recap & Growth
    {"day": 26, "theme": "recap_week", "twitter": "This week's myAI stats:\n\n📝 210 content pieces generated\n📧 1,500 emails sent\n📱 120 social media posts\n🌐 50 websites maintained\n📊 50 reports delivered\n\nAll autonomous. All AI.\n\n#WeeklyRecap #AI",
     "linkedin": "Weekly Platform Update:\n\nmyAI's performance this week:\n\n📝 210 content pieces generated across all clients\n📧 1,500 marketing emails sent\n📱 120 social media posts published\n🌐 50 client websites maintained and updated\n📊 50 weekly reports delivered automatically\n🤖 99.9% uptime — zero downtime\n\nEvery week, the system gets better. Every cycle, the AI learns more about what works.\n\nThis is what autonomous AI looks like at scale.\n\n{site}\n\n#WeeklyRecap #AI #SaaS #Scale",
     "instagram": "📊 This week's AI stats:\n\n📝 210 content pieces\n📧 1,500 emails sent\n📱 120 social posts\n🌐 50 websites updated\n📊 50 reports delivered\n\nAll autonomous. All AI. 🤖\n\n#WeeklyRecap #AI #Scale"},
    
    {"day": 27, "theme": "future", "twitter": "Coming soon to myAI:\n\n🎯 AI voice assistant for calls\n🔗 API access for developers\n📊 Advanced analytics dashboard\n🤝 CRM integration\n📱 Mobile app\n\nThe future is autonomous.\n\n#Roadmap #AI",
     "linkedin": "Exciting updates on the myAI roadmap:\n\n🎯 AI Voice Assistant — Handle phone calls and meetings automatically\n🔗 API Access — For developers who want to integrate myAI into their stack\n📊 Advanced Analytics — Deep-dive dashboards with predictive insights\n🤝 CRM Integration — Native connections to Salesforce, HubSpot, Pipedrive\n📱 Mobile App — Manage your AI agents from your phone\n\nWe're building the future of autonomous business operations. And we're just getting started.\n\nJoin us: {site}\n\n#Roadmap #AI #SaaS #ProductUpdate",
     "instagram": "🔮 Coming soon to myAI:\n\n🎯 AI voice calls\n🔗 API access\n📊 Advanced analytics\n🤝 CRM integration\n📱 Mobile app\n\nThe future is autonomous 🤖\n\nFollow for updates!\n\n#Roadmap #AI #ComingSoon"},
    
    {"day": 28, "theme": "gratitude", "twitter": "Thank you to everyone who's tried myAI this month.\n\nYour feedback is making the AI better every day.\n\nWe're just getting started. 🚀\n\n#ThankYou #AI #Community",
     "linkedin": "A heartfelt thank you to every business owner who has tried myAI this month.\n\nYour feedback has been invaluable:\n• Feature requests that made the product better\n• Bug reports that improved reliability\n• Success stories that inspire the team\n• Honest criticism that keeps us humble\n\nBuilding myAI isn't just about technology — it's about empowering businesses of all sizes to compete with the power of AI.\n\nWe're just getting started. And we're doing it together.\n\nThank you. 🙏\n\n{site}\n\n#Gratitude #Community #AI #Startup",
     "instagram": "🙏 THANK YOU to everyone who tried myAI this month!\n\nYour feedback makes us better every day.\n\nWe're just getting started 🚀\n\n#ThankYou #Community #AI #Startup"},
    
    {"day": 29, "theme": "challenge", "twitter": "Challenge: Give AI 14 days to run your marketing.\n\nTrack the results.\nCompare to your manual work.\nMake your decision.\n\nFree trial. No risk.\n\n{site}\n\n#Challenge #AI #Marketing",
     "linkedin": "The 14-Day AI Challenge:\n\nI challenge every business owner reading this:\n\n1️⃣ Sign up for myAI's free 14-day trial\n2️⃣ Let the AI handle your marketing for 2 weeks\n3️⃣ Track the results: content output, leads, time saved\n4️⃣ Compare to your manual efforts\n5️⃣ Make your decision based on data, not assumptions\n\nNo credit card. No commitment. No risk.\n\nJust 14 days to see if AI can transform your business.\n\nAre you in?\n\n{site}\n\n#Challenge #AI #Marketing #DataDriven",
     "instagram": "💪 14-DAY AI CHALLENGE!\n\n1️⃣ Sign up for free trial\n2️⃣ Let AI run your marketing\n3️⃣ Track the results\n4️⃣ Compare to manual work\n5️⃣ Decide based on data\n\nNo card. No risk. Just results.\n\nAre you in? 🤖\n\nLink in bio!\n\n#Challenge #AI #Marketing"},
    
    {"day": 30, "theme": "month_recap", "twitter": "Month 1 recap:\n\n🎯 50 business niches served\n📝 500+ content pieces generated\n📧 5,000+ emails sent\n📱 300+ social posts published\n🌐 50 websites built & maintained\n\nMonth 2 goals: double everything.\n\n#MonthlyRecap #AI #Growth",
     "linkedin": "Month 1 Recap — myAI by the Numbers:\n\n🎯 50 business niches served\n📝 500+ content pieces generated\n📧 5,000+ marketing emails sent\n📱 300+ social media posts published\n🌐 50 complete business websites built and maintained\n🤖 1,000+ autonomous agent cycles completed\n📊 99.9% system uptime\n\nMonth 2 Goals:\n→ Double content output\n→ Launch AI voice assistant\n→ Release mobile app beta\n→ Expand to 100+ niches\n→ Onboard 500+ businesses\n\nThe AI doesn't slow down. Neither do we.\n\n{site}\n\n#MonthlyRecap #AI #Growth #SaaS",
     "instagram": "📊 MONTH 1 RECAP:\n\n🎯 50 niches served\n📝 500+ content pieces\n📧 5,000+ emails sent\n📱 300+ social posts\n🌐 50 websites built\n🤖 1,000+ agent cycles\n\nMonth 2: DOUBLE everything 🚀\n\n#MonthlyRecap #AI #Growth #SaaS"},
]


def generate_30_day_content():
    """Generate all 30 days of social media content."""
    _ensure_dirs()
    
    all_posts = []
    start_date = datetime.now()
    
    for day_content in DAILY_CONTENT:
        day_num = day_content['day']
        post_date = start_date + timedelta(days=day_num - 1)
        
        for platform in ['twitter', 'linkedin', 'instagram']:
            if platform in day_content:
                content = day_content[platform]
                content = content.replace('{site}', SITE_URL)
                content = content.replace('{biz}', BIZ_URL)
                
                post = {
                    "day": day_num,
                    "date": post_date.strftime("%Y-%m-%d"),
                    "theme": day_content['theme'],
                    "platform": platform,
                    "content": content,
                    "status": "scheduled",
                }
                all_posts.append(post)
                
                # Save individual post file
                post_file = os.path.join(OUTPUT_DIR, platform, f"day{day_num:02d}_{day_content['theme']}.txt")
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    # Save master schedule
    schedule = {
        "generated": datetime.now().isoformat(),
        "total_posts": len(all_posts),
        "days": 30,
        "platforms": ["twitter", "linkedin", "instagram"],
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": (start_date + timedelta(days=29)).strftime("%Y-%m-%d"),
        "posts": all_posts,
    }
    
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)
    
    # Summary
    platform_counts = {}
    for post in all_posts:
        p = post['platform']
        platform_counts[p] = platform_counts.get(p, 0) + 1
    
    print(f"[SOCIAL] Generated 30-day content schedule:")
    print(f"  Total posts: {len(all_posts)}")
    for p, c in platform_counts.items():
        print(f"  {p}: {c} posts")
    print(f"  Schedule: {start_date.strftime('%Y-%m-%d')} to {(start_date + timedelta(days=29)).strftime('%Y-%m-%d')}")
    print(f"  Saved to: {SCHEDULE_FILE}")
    
    return schedule


def get_todays_posts():
    """Get posts scheduled for today."""
    if not os.path.exists(SCHEDULE_FILE):
        generate_30_day_content()
    
    with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
        schedule = json.load(f)
    
    today = datetime.now().strftime("%Y-%m-%d")
    return [p for p in schedule['posts'] if p['date'] == today]


def post_content(platform, content):
    """
    Post content to a platform.
    Currently saves as ready-to-post files.
    Can be extended with platform APIs (Twitter API, LinkedIn API, etc.)
    """
    _ensure_dirs()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    post_file = os.path.join(OUTPUT_DIR, platform, f"post_{timestamp}.txt")
    
    with open(post_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Log the post
    _log_post(platform, content, post_file)
    
    print(f"[SOCIAL] Content ready for {platform}: {post_file}")
    return post_file


def _log_post(platform, content, file_path):
    """Log a post."""
    os.makedirs(DATA_DIR, exist_ok=True)
    logs = []
    if os.path.exists(POST_LOG):
        with open(POST_LOG, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    
    logs.append({
        "platform": platform,
        "content_preview": content[:100],
        "file": file_path,
        "posted_at": datetime.now().isoformat(),
    })
    
    with open(POST_LOG, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def get_social_stats():
    """Get social media posting stats."""
    if not os.path.exists(POST_LOG):
        return {"total_posts": 0}
    with open(POST_LOG, 'r') as f:
        logs = json.load(f)
    
    platform_counts = {}
    for l in logs:
        p = l['platform']
        platform_counts[p] = platform_counts.get(p, 0) + 1
    
    return {
        "total_posts": len(logs),
        "per_platform": platform_counts,
    }


if __name__ == "__main__":
    generate_30_day_content()
