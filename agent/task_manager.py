import json
import os
import re
from datetime import datetime

TASKS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'tasks.json')
README_PATH = os.path.join(os.path.dirname(__file__), '..', 'README.md')


def _ensure_data_dir():
    os.makedirs(os.path.dirname(TASKS_PATH), exist_ok=True)


def load_tasks():
    _ensure_data_dir()
    if not os.path.exists(TASKS_PATH):
        save_tasks([])
        return []
    with open(TASKS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_tasks(tasks):
    _ensure_data_dir()
    with open(TASKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)


def add_task(title, priority="medium", category="general"):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "status": "pending",
        "priority": priority,
        "category": category,
        "created": datetime.now().isoformat(),
        "completed": None
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed"
            task["completed"] = datetime.now().isoformat()
            break
    save_tasks(tasks)


def get_pending_tasks(limit=5):
    tasks = load_tasks()
    pending = [t for t in tasks if t["status"] == "pending"]
    return pending[:limit]


def generate_next_tasks(completed_tasks, run_number):
    """Generate 5 new tasks based on the current run number."""
    task_templates = {
        1: [
            ("Build landing page with hero, services, testimonials, and contact form", "high", "website"),
            ("Create initial blog content — 3 posts on AI and automation", "high", "content"),
            ("Set up logging system with detailed run reports", "medium", "system"),
            ("Build market analysis module — competitor & trend research", "medium", "research"),
            ("Create basic CRM system with JSON storage", "medium", "system"),
        ],
        2: [
            ("Enhance landing page — add animations, particles, and responsive nav", "high", "website"),
            ("Build About page and Services page for the website", "high", "website"),
            ("Write 3 case study blog posts — real AI business results", "medium", "content"),
            ("Build pricing page with 3 tiers (Starter/Pro/Enterprise)", "medium", "business"),
            ("Generate email templates (welcome, weekly report, new lead)", "medium", "system"),
        ],
        3: [
            ("Generate YouTube video scripts (3 educational videos)", "high", "marketing"),
            ("Generate short-form Reels/TikTok scripts (5 scripts)", "high", "marketing"),
            ("Create 4-week content calendar for all platforms", "medium", "marketing"),
            ("Generate social media posts for Twitter, LinkedIn, Instagram, TikTok", "medium", "marketing"),
            ("Generate thumbnails for all YouTube video scripts", "medium", "marketing"),
        ],
        4: [
            ("Generate LinkedIn articles and Twitter threads", "high", "marketing"),
            ("Build admin dashboard page with business statistics", "high", "system"),
            ("Add SEO optimization to all website pages", "medium", "website"),
            ("Create API specification for business services", "medium", "system"),
            ("Generate automated weekly performance report module", "medium", "system"),
        ],
        5: [
            ("Build Stripe checkout page with payment flow for all plans", "high", "payments"),
            ("Generate investor pitch page with opportunity and roadmap", "high", "investors"),
            ("Generate structured pitch deck data for investor presentations", "medium", "investors"),
            ("Create payment configuration with Stripe integration setup", "medium", "payments"),
            ("Update all website pages with checkout and investor links", "medium", "website"),
        ],
        6: [
            ("Generate 3 new blog posts about payment automation and investor relations", "high", "content"),
            ("Create investor outreach email templates", "high", "investors"),
            ("Generate social media announcement posts for funding round", "medium", "marketing"),
            ("Build financial projections dashboard page", "medium", "business"),
            ("Generate press release content for product launch", "medium", "marketing"),
        ],
    }

    if run_number in task_templates:
        tasks = task_templates[run_number]
    elif run_number == 7:
        tasks = [
            ("Generate all 50 business niche websites with landing pages", "high", "empire"),
            ("Build master directory page linking all 50 businesses", "high", "empire"),
            ("Generate niche social media marketing content for all businesses", "high", "marketing"),
            ("Generate niche email templates for all businesses", "medium", "marketing"),
            ("Update all website SEO and cross-link businesses", "medium", "website"),
        ]
    elif run_number == 8:
        tasks = [
            ("Generate new blog content — posts for run #8", "high", "content"),
            ("Create LinkedIn articles showcasing the 50-business empire", "high", "marketing"),
            ("Generate Twitter threads about each business niche", "medium", "marketing"),
            ("Create YouTube video scripts for business empire launch", "medium", "marketing"),
            ("Generate Reels/TikTok scripts for niche business promotions", "medium", "marketing"),
        ]
    elif run_number == 9:
        tasks = [
            ("Generate social media posts for all niche businesses", "high", "marketing"),
            ("Create content calendar for multi-business marketing", "high", "marketing"),
            ("Build enhanced pricing page with all 50 business options", "medium", "website"),
            ("Generate investor pitch update with 50-business portfolio", "high", "investors"),
            ("Create email templates for investor outreach", "medium", "investors"),
        ]
    elif run_number == 10:
        tasks = [
            ("Generate case study blog posts for top-performing niches", "high", "content"),
            ("Create YouTube scripts for 5 niche-specific demo videos", "high", "marketing"),
            ("Generate thumbnail designs for niche demo videos", "medium", "marketing"),
            ("Build automated performance report for all 50 businesses", "medium", "system"),
            ("Generate press release for 50-business AI platform launch", "medium", "marketing"),
        ]
    elif run_number == 11:
        tasks = [
            ("Enhance landing page with animated business counter", "high", "website"),
            ("Generate social media posts for week 2 campaign", "high", "marketing"),
            ("Create email sequence for lead nurturing", "medium", "marketing"),
            ("Generate Reels/TikTok batch 2 — success story scripts", "medium", "marketing"),
            ("Build comprehensive market report update", "medium", "research"),
        ]
    else:
        tasks = [
            (f"Optimize and improve the system — run #{run_number}", "high", "system"),
            (f"Generate new content — posts #{run_number * 3 - 2} to #{run_number * 3}", "high", "content"),
            (f"Analyze performance and improve conversions — round #{run_number}", "medium", "business"),
            (f"Update website with new features — round #{run_number}", "medium", "website"),
            (f"Review and enrich client database — round #{run_number}", "medium", "business"),
        ]

    new_tasks = []
    for title, priority, category in tasks:
        new_tasks.append(add_task(title, priority, category))
    return new_tasks


def update_readme_tasks(run_number, next_tasks):
    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    task_table = f"\n## Next Run Tasks (#{run_number})\n\n"
    task_table += "| # | Task | Status | Priority |\n"
    task_table += "|---|------|--------|----------|\n"
    for i, task in enumerate(next_tasks, 1):
        status = "Pending" if task["status"] == "pending" else "Completed"
        task_table += f"| {i} | {task['title']} | {status} | {task['priority']} |\n"

    pattern = r'\n## Next Run Tasks.*?(?=\n---|\n## [^N]|\Z)'
    content = re.sub(pattern, task_table, content, flags=re.DOTALL)

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)


def append_run_to_readme(run_number, completed_summary, next_tasks):
    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    run_entry = f"\n### Run #{run_number} — ({now})\n"
    for item in completed_summary:
        run_entry += f"- {item}\n"
    run_entry += "\n"

    history_marker = "## Run History\n"
    insertion_point = content.find(history_marker)
    if insertion_point != -1:
        insertion_point += len(history_marker)
        content = content[:insertion_point] + run_entry + content[insertion_point:]

    content = re.sub(
        r'\*\*Last Run:\*\* .*',
        f'**Last Run:** {now}',
        content
    )
    content = re.sub(
        r'\*\*Total Runs:\*\* \d+',
        f'**Total Runs:** {run_number}',
        content
    )

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    update_readme_tasks(run_number + 1, next_tasks)
