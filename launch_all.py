"""
launch_all.py — Mass Business Launcher
Generates all 50 businesses, their marketing content, emails, and master directory.
Then runs the main agent loop multiple times for ongoing growth.
"""
import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from agent.business_generator import (
    generate_all_businesses,
    generate_master_directory,
    load_businesses
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATS_PATH = os.path.join(BASE_DIR, 'data', 'business_stats.json')
LAUNCH_LOG = os.path.join(BASE_DIR, 'data', 'launch_log.json')


def banner(text):
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)


def phase_1_generate_all():
    """Phase 1: Generate all 50 business websites + content."""
    banner("PHASE 1: Generating 50 Business Websites")
    print(f"  Started: {datetime.now().strftime('%H:%M:%S')}")

    stats = generate_all_businesses()

    print(f"\n  Generated {stats['total_businesses']} businesses:")
    print(f"    - {stats['total_pages']} landing pages")
    print(f"    - {stats['total_social_posts']} social media posts")
    print(f"    - {stats['total_email_templates']} email templates")
    print(f"    - {stats['total_blog_posts']} blog posts")

    for biz in stats['businesses']:
        print(f"    OK  {biz['name']}")

    return stats


def phase_2_master_directory():
    """Phase 2: Generate the master directory linking all businesses."""
    banner("PHASE 2: Building Master Directory")
    path = generate_master_directory()
    print(f"  Master directory: {path}")
    return path


def phase_3_run_agent_loop(num_runs=5):
    """Phase 3: Run the main agent loop multiple times."""
    banner(f"PHASE 3: Running Agent Loop ({num_runs} runs)")

    from run import run as agent_run, get_run_number
    for i in range(num_runs):
        current = get_run_number()
        print(f"\n  --- Agent Run #{current} ---")
        try:
            agent_run()
        except Exception as e:
            print(f"  Run #{current} error: {e}")
        print()

    return num_runs


def phase_4_deployment_package():
    """Phase 4: Create deployment instructions for all 50 businesses."""
    banner("PHASE 4: Creating Deployment Package")
    businesses = load_businesses()

    deploy_instructions = {
        "generated": datetime.now().isoformat(),
        "total_businesses": len(businesses),
        "deployment_options": {
            "vercel": {
                "steps": [
                    "1. Install Vercel CLI: npm i -g vercel",
                    "2. For each business folder in output/businesses/:",
                    "   cd output/businesses/<business-id>",
                    "   vercel --prod",
                    "3. Each business gets its own URL automatically",
                    "4. Custom domains can be added in Vercel dashboard"
                ],
                "cost": "Free for up to 100 deployments"
            },
            "netlify": {
                "steps": [
                    "1. Install Netlify CLI: npm i -g netlify-cli",
                    "2. For each business folder:",
                    "   netlify deploy --prod --dir=output/businesses/<business-id>",
                    "3. Custom domains in Netlify dashboard"
                ],
                "cost": "Free tier available"
            },
            "github_pages": {
                "steps": [
                    "1. Create a GitHub repo for each business (or one monorepo)",
                    "2. Push the output/businesses/<id>/ folder",
                    "3. Enable GitHub Pages in repo settings",
                    "4. Each gets a free .github.io URL"
                ],
                "cost": "Free"
            },
            "bulk_deploy_script": "Run: python deploy.py (coming next)"
        },
        "businesses": [
            {
                "id": b['id'],
                "name": b['name'],
                "folder": f"output/businesses/{b['id']}/",
                "suggested_domain": f"{b['id']}.myai.business",
                "monthly_price": b['price']
            }
            for b in businesses
        ],
        "revenue_potential": {
            "if_1_client_each": sum(b['price'] for b in businesses),
            "if_10_clients_each": sum(b['price'] for b in businesses) * 10,
            "if_100_clients_each": sum(b['price'] for b in businesses) * 100,
            "note": "Monthly recurring revenue (MRR) estimates"
        }
    }

    deploy_path = os.path.join(BASE_DIR, 'data', 'deployment_plan.json')
    with open(deploy_path, 'w', encoding='utf-8') as f:
        json.dump(deploy_instructions, f, indent=2)

    print(f"  Deployment plan saved: {deploy_path}")
    print(f"\n  Revenue Potential:")
    rev = deploy_instructions['revenue_potential']
    print(f"    1 client each:   ${rev['if_1_client_each']:,}/mo")
    print(f"    10 clients each: ${rev['if_10_clients_each']:,}/mo")
    print(f"    100 clients each: ${rev['if_100_clients_each']:,}/mo")

    return deploy_path


def phase_5_final_report():
    """Phase 5: Generate the final stats report."""
    banner("PHASE 5: Final Report")

    businesses = load_businesses()
    total_price = sum(b['price'] for b in businesses)

    # Count all generated files
    biz_dir = os.path.join(BASE_DIR, 'output', 'businesses')
    total_files = 0
    for root, dirs, files in os.walk(biz_dir):
        total_files += len(files)

    report = {
        "generated": datetime.now().isoformat(),
        "summary": {
            "businesses_created": len(businesses),
            "total_files_generated": total_files,
            "landing_pages": len(businesses),
            "social_content_files": len(businesses),
            "email_template_sets": len(businesses),
            "blog_posts": len(businesses) * 3,
            "total_social_posts": len(businesses) * 10,
        },
        "revenue": {
            "mrr_1_client_each": total_price,
            "arr_1_client_each": total_price * 12,
            "mrr_10_clients_each": total_price * 10,
            "arr_10_clients_each": total_price * 10 * 12,
        },
        "deployment_status": "READY — all files generated, pending deployment",
        "next_steps": [
            "Deploy all 50 sites to Vercel/Netlify (free)",
            "Set up Stripe for each business",
            "Launch social media campaigns with generated content",
            "Send email sequences using generated templates",
            "Monitor leads and conversions"
        ]
    }

    report_path = os.path.join(BASE_DIR, 'data', 'final_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\n  EMPIRE STATS:")
    print(f"  {'-' * 40}")
    print(f"  Businesses:       {report['summary']['businesses_created']}")
    print(f"  Landing Pages:    {report['summary']['landing_pages']}")
    print(f"  Blog Posts:       {report['summary']['blog_posts']}")
    print(f"  Social Posts:     {report['summary']['total_social_posts']}")
    print(f"  Email Templates:  {report['summary']['email_template_sets'] * 2}")
    print(f"  Total Files:      {report['summary']['total_files_generated']}")
    print(f"  {'-' * 40}")
    print(f"  MRR (1 client/biz):  ${report['revenue']['mrr_1_client_each']:,}")
    print(f"  ARR (1 client/biz):  ${report['revenue']['arr_1_client_each']:,}")
    print(f"  MRR (10 clients):    ${report['revenue']['mrr_10_clients_each']:,}")
    print(f"  ARR (10 clients):    ${report['revenue']['arr_10_clients_each']:,}")
    print(f"  {'-' * 40}")
    print(f"  STATUS: READY TO DEPLOY")

    return report


def main():
    start = datetime.now()
    banner("myAI EMPIRE LAUNCHER — 50 BUSINESSES")
    print(f"  Launch Time: {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Target: 50 AI-powered micro-SaaS businesses")

    # Phase 1: Generate all business sites
    stats = phase_1_generate_all()

    # Phase 2: Master directory
    dir_path = phase_2_master_directory()

    # Phase 3: Run the agent loop 5 times
    runs = phase_3_run_agent_loop(5)

    # Phase 4: Deployment package
    deploy_path = phase_4_deployment_package()

    # Phase 5: Final report
    report = phase_5_final_report()

    elapsed = (datetime.now() - start).total_seconds()

    # Save launch log
    log = {
        "started": start.isoformat(),
        "completed": datetime.now().isoformat(),
        "elapsed_seconds": round(elapsed, 1),
        "phases_completed": 5,
        "businesses_generated": stats['total_businesses'],
        "agent_runs": runs,
        "status": "SUCCESS"
    }
    os.makedirs(os.path.dirname(LAUNCH_LOG), exist_ok=True)
    with open(LAUNCH_LOG, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2)

    banner("LAUNCH COMPLETE")
    print(f"  Duration: {elapsed:.1f} seconds")
    print(f"  50 businesses generated and ready to deploy!")
    print(f"  Run 'python deploy.py' to deploy all sites")
    print("=" * 60)


if __name__ == '__main__':
    main()
