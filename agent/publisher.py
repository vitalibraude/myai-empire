import os
import json
from datetime import datetime

CONTENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'content')


def ensure_content_dir():
    os.makedirs(CONTENT_DIR, exist_ok=True)


def create_blog_post(title, content, tags=None):
    ensure_content_dir()
    post = {
        "id": _get_next_post_id(),
        "title": title,
        "content": content,
        "tags": tags or [],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "published": False,
        "platform": "blog"
    }
    posts = load_posts()
    posts.append(post)
    _save_posts(posts)
    return post


def load_posts():
    posts_file = os.path.join(CONTENT_DIR, 'posts.json')
    if not os.path.exists(posts_file):
        return []
    with open(posts_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_posts(posts):
    ensure_content_dir()
    posts_file = os.path.join(CONTENT_DIR, 'posts.json')
    with open(posts_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2)


def _get_next_post_id():
    posts = load_posts()
    if not posts:
        return 1
    return max(p["id"] for p in posts) + 1


def publish_post(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["published"] = True
            post["published_date"] = datetime.now().isoformat()
            break
    _save_posts(posts)


def get_unpublished_posts():
    return [p for p in load_posts() if not p.get("published")]


def get_published_posts():
    return [p for p in load_posts() if p.get("published")]


def generate_initial_posts():
    """Generate the first batch of blog posts about AI and automation."""
    posts_data = [
        {
            "title": "How AI Is Transforming Business Operations in 2026",
            "content": (
                "Artificial intelligence is no longer a buzzword — it's a daily business tool. "
                "Companies adopting AI report a 40% increase in productivity and 60% time savings. "
                "From automated customer service agents to real-time data analysis, AI enables "
                "small businesses to compete with enterprise-level organizations. The shift isn't "
                "coming — it's already here, and early adopters are reaping the rewards."
            ),
            "tags": ["AI", "business transformation", "automation", "productivity"]
        },
        {
            "title": "5 Ways to Automate Your Business — Starting Today",
            "content": (
                "1. **AI Customer Service Chatbot** — 24/7 support without hiring. "
                "2. **Marketing Automation** — Schedule social posts and send emails automatically. "
                "3. **Smart Inventory Management** — AI-powered reordering based on demand forecasts. "
                "4. **Automated Data Analysis** — Weekly reports generated without human intervention. "
                "5. **Invoicing & Payments** — Automatic generation, tracking, and follow-ups. "
                "Each of these can be set up in under a week with the right tools."
            ),
            "tags": ["automation", "tips", "efficiency", "small business"]
        },
        {
            "title": "The Complete Guide to Building an AI Agent for Your Business",
            "content": (
                "An AI agent is software that operates autonomously and executes tasks on behalf of "
                "a business owner. Step one: define clear goals — what should the agent do? "
                "Step two: choose the right tools — language models, APIs, and databases. "
                "Step three: build the logic — when the agent acts, how it makes decisions, "
                "and how it reports results. Step four: monitor performance and iterate. "
                "The key insight? Start small, measure everything, and scale what works."
            ),
            "tags": ["AI agents", "guide", "development", "strategy"]
        }
    ]

    created = []
    for data in posts_data:
        post = create_blog_post(data["title"], data["content"], data["tags"])
        publish_post(post["id"])
        created.append(post)
    return created


def generate_case_study_posts():
    """Generate blog posts about AI use cases in business."""
    posts_data = [
        {
            "title": "How an E-Commerce Company Grew Sales 85% with an AI Agent",
            "content": (
                "ShopSmart deployed an AI agent managing the entire sales funnel — "
                "from product recommendations to order tracking. The results were staggering: "
                "85% increase in sales, 60% reduction in customer response time, and 40% "
                "improvement in satisfaction scores. The agent learned from every interaction, "
                "discovering that customers buying Product A were highly likely to purchase "
                "Product C — an insight the marketing team hadn't found in months of manual analysis."
            ),
            "tags": ["case study", "e-commerce", "AI", "sales"]
        },
        {
            "title": "From Solopreneur to 7-Figure Business — Powered by Automation",
            "content": (
                "Marcus, an independent developer, built an automation system that runs his "
                "entire business: marketing, customer service, invoicing, and lead generation. "
                "Within a year, revenue grew from $30K/month to $200K — without hiring a single "
                "employee. The secret? An AI agent working 24/7, generating content, answering "
                "customers, and analyzing data. 'It felt like having a team of 10 people,' "
                "Marcus says, 'but in reality, it was just me and the agent.'"
            ),
            "tags": ["success story", "automation", "entrepreneurship", "solopreneur"]
        },
        {
            "title": "5 Common AI Implementation Mistakes — and How to Avoid Them",
            "content": (
                "1. **Starting too big** — Begin with one simple task, not a full revolution. "
                "2. **Unrealistic expectations** — AI doesn't replace humans; it augments them. "
                "3. **Ignoring data quality** — AI is only as good as the data it receives. "
                "4. **No tracking** — Without measurement, there's no improvement. Set KPIs from day one. "
                "5. **Fear of failure** — Every implementation requires trial and error. "
                "Failure is part of the process. The companies that win are the ones that iterate fast."
            ),
            "tags": ["tips", "mistakes", "implementation", "best practices"]
        }
    ]

    created = []
    for data in posts_data:
        post = create_blog_post(data["title"], data["content"], data["tags"])
        publish_post(post["id"])
        created.append(post)
    return created
