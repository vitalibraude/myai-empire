"""
Lead Monitor — connects to Netlify Forms API to pull real leads
from all 50 business sites + main site, tracks them, and feeds
them into the outreach pipeline.
"""
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LEADS_PATH = os.path.join(DATA_DIR, 'leads.json')
NETLIFY_CONFIG = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'netlify', 'Config', 'config.json')

# Both live Netlify sites
SITES = {
    "myai-empire": "dd23c22c-225e-410e-affd-038b237bcc9c",
    "myai-businesses": "391d0663-7bea-41d3-981c-6cb22ee58995",
}


def _get_netlify_token():
    """Read the Netlify auth token from CLI config."""
    if not os.path.exists(NETLIFY_CONFIG):
        return None
    with open(NETLIFY_CONFIG, 'r') as f:
        cfg = json.load(f)
    user_id = cfg.get('userId')
    if not user_id:
        return None
    user_data = cfg.get('users', {}).get(user_id, {})
    return user_data.get('auth', {}).get('token')


def _load_leads():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(LEADS_PATH):
        with open(LEADS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"leads": [], "last_check": None, "stats": {"total": 0, "new": 0, "contacted": 0, "converted": 0}}


def _save_leads(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LEADS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def fetch_leads_from_netlify():
    """Pull all form submissions from both Netlify sites via API."""
    token = _get_netlify_token()
    if not token:
        print("[LEAD MONITOR] No Netlify token found. Leads will be captured when forms are submitted.")
        return []

    try:
        import urllib.request
        import urllib.error

        all_submissions = []
        for site_name, site_id in SITES.items():
            url = f"https://api.netlify.com/api/v1/sites/{site_id}/submissions?per_page=100"
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
            try:
                with urllib.request.urlopen(req) as resp:
                    submissions = json.loads(resp.read().decode())
                    for sub in submissions:
                        all_submissions.append({
                            "id": sub.get("id"),
                            "site": site_name,
                            "form": sub.get("form_name", "unknown"),
                            "name": sub.get("name") or sub.get("data", {}).get("name", ""),
                            "email": sub.get("email") or sub.get("data", {}).get("email", ""),
                            "phone": sub.get("data", {}).get("phone", ""),
                            "company": sub.get("company") or sub.get("data", {}).get("company", ""),
                            "message": sub.get("data", {}).get("message", ""),
                            "plan": sub.get("data", {}).get("plan", ""),
                            "submitted_at": sub.get("created_at", ""),
                            "source_url": sub.get("site_url", ""),
                        })
                    print(f"[LEAD MONITOR] {site_name}: {len(submissions)} submissions found")
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f"[LEAD MONITOR] {site_name}: No forms found yet (waiting for first submission)")
                else:
                    print(f"[LEAD MONITOR] {site_name}: API error {e.code}")

        return all_submissions

    except Exception as e:
        print(f"[LEAD MONITOR] Error fetching leads: {e}")
        return []


def check_new_leads():
    """Check for new leads and update the leads database."""
    data = _load_leads()
    existing_ids = {lead.get("id") for lead in data["leads"]}

    submissions = fetch_leads_from_netlify()
    new_leads = []

    for sub in submissions:
        if sub["id"] not in existing_ids:
            sub["status"] = "new"
            sub["contacted"] = False
            sub["notes"] = ""
            data["leads"].append(sub)
            new_leads.append(sub)

    data["last_check"] = datetime.now().isoformat()
    data["stats"]["total"] = len(data["leads"])
    data["stats"]["new"] = len([l for l in data["leads"] if l.get("status") == "new"])
    data["stats"]["contacted"] = len([l for l in data["leads"] if l.get("contacted")])
    data["stats"]["converted"] = len([l for l in data["leads"] if l.get("status") == "converted"])

    _save_leads(data)

    if new_leads:
        print(f"\n{'='*50}")
        print(f"  NEW LEADS FOUND: {len(new_leads)}")
        print(f"{'='*50}")
        for lead in new_leads:
            print(f"  Name: {lead['name']}")
            print(f"  Email: {lead['email']}")
            print(f"  From: {lead['site']} / {lead['form']}")
            print(f"  Plan: {lead.get('plan', 'N/A')}")
            print(f"  ---")
    else:
        print(f"[LEAD MONITOR] No new leads. Total tracked: {data['stats']['total']}")

    return new_leads


def get_lead_summary():
    """Return a summary of all leads for display."""
    data = _load_leads()
    return {
        "total": data["stats"]["total"],
        "new": data["stats"]["new"],
        "contacted": data["stats"]["contacted"],
        "converted": data["stats"]["converted"],
        "last_check": data.get("last_check"),
        "leads": data["leads"][-20:]  # Last 20 leads
    }


def mark_lead_contacted(lead_id):
    data = _load_leads()
    for lead in data["leads"]:
        if lead.get("id") == lead_id:
            lead["contacted"] = True
            lead["status"] = "contacted"
            lead["contacted_at"] = datetime.now().isoformat()
            break
    data["stats"]["contacted"] = len([l for l in data["leads"] if l.get("contacted")])
    data["stats"]["new"] = len([l for l in data["leads"] if l.get("status") == "new"])
    _save_leads(data)


def mark_lead_converted(lead_id, revenue=0):
    data = _load_leads()
    for lead in data["leads"]:
        if lead.get("id") == lead_id:
            lead["status"] = "converted"
            lead["converted_at"] = datetime.now().isoformat()
            lead["revenue"] = revenue
            break
    data["stats"]["converted"] = len([l for l in data["leads"] if l.get("status") == "converted"])
    _save_leads(data)


if __name__ == "__main__":
    print("Checking for leads across all Netlify sites...")
    new = check_new_leads()
    summary = get_lead_summary()
    print(f"\nLead Summary:")
    print(f"  Total: {summary['total']}")
    print(f"  New: {summary['new']}")
    print(f"  Contacted: {summary['contacted']}")
    print(f"  Converted: {summary['converted']}")
