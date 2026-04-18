"""
Revenue Tracker — tracks all revenue streams, monitors income
from leads, and generates financial reports.
"""
import os
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REVENUE_PATH = os.path.join(DATA_DIR, 'revenue.json')


def _load_revenue():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(REVENUE_PATH):
        with open(REVENUE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "transactions": [],
        "monthly_totals": {},
        "lifetime_revenue": 0,
        "active_subscriptions": 0,
        "mrr": 0,  # Monthly Recurring Revenue
    }


def _save_revenue(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(REVENUE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def record_transaction(lead_id, amount, plan, business_niche="general"):
    """Record a revenue transaction from a converted lead."""
    data = _load_revenue()

    tx = {
        "id": f"tx_{len(data['transactions'])+1:05d}",
        "lead_id": lead_id,
        "amount": amount,
        "plan": plan,
        "business_niche": business_niche,
        "date": datetime.now().isoformat(),
        "month": datetime.now().strftime("%Y-%m"),
        "type": "subscription",
    }
    data["transactions"].append(tx)

    # Update monthly totals
    month = tx["month"]
    data["monthly_totals"][month] = data["monthly_totals"].get(month, 0) + amount

    # Update lifetime
    data["lifetime_revenue"] += amount
    data["active_subscriptions"] += 1
    data["mrr"] = data["active_subscriptions"] * (amount if amount < 1000 else amount / 12)

    _save_revenue(data)
    print(f"[REVENUE] Transaction recorded: ${amount} from {plan} plan ({business_niche})")
    return tx


def get_revenue_summary():
    """Get a comprehensive revenue summary."""
    data = _load_revenue()

    return {
        "lifetime_revenue": data["lifetime_revenue"],
        "mrr": data["mrr"],
        "active_subscriptions": data["active_subscriptions"],
        "total_transactions": len(data["transactions"]),
        "monthly_totals": data["monthly_totals"],
        "recent_transactions": data["transactions"][-10:],
    }


def generate_revenue_report():
    """Generate a comprehensive financial report."""
    data = _load_revenue()
    summary = get_revenue_summary()

    report = {
        "generated_at": datetime.now().isoformat(),
        "overview": {
            "lifetime_revenue": f"${data['lifetime_revenue']:,.2f}",
            "monthly_recurring_revenue": f"${data['mrr']:,.2f}",
            "active_subscriptions": data["active_subscriptions"],
            "total_transactions": len(data["transactions"]),
        },
        "projections": {
            "next_month": f"${data['mrr']:,.2f}",
            "annual_run_rate": f"${data['mrr'] * 12:,.2f}",
        },
        "monthly_breakdown": data["monthly_totals"],
        "portfolio": {
            "total_businesses": 50,
            "live_sites": 2,
            "urls": {
                "main": "https://aoeua.com/",
                "businesses": "https://businesses.aoeua.com/",
            }
        }
    }

    report_path = os.path.join(DATA_DIR, 'revenue_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*50}")
    print(f"  REVENUE REPORT")
    print(f"{'='*50}")
    print(f"  Lifetime Revenue: {report['overview']['lifetime_revenue']}")
    print(f"  MRR: {report['overview']['monthly_recurring_revenue']}")
    print(f"  Active Subs: {report['overview']['active_subscriptions']}")
    print(f"  Annual Run Rate: {report['projections']['annual_run_rate']}")
    print(f"{'='*50}")

    return report_path


if __name__ == "__main__":
    generate_revenue_report()
