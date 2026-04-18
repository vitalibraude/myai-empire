"""
Autonomous Pipeline — the MAIN automation script that runs everything:
1. Checks for new leads (from Netlify Forms)
2. Runs SEO optimization
3. Deploys updates to both sites
4. Generates revenue reports
5. Logs everything

This is what makes the system actually work autonomously.
Run it periodically or set it as a scheduled task.
"""
import os
import sys
import json
import time
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.lead_monitor import check_new_leads, get_lead_summary
from agent.seo_indexing import generate_all_seo
from agent.revenue_tracker import generate_revenue_report, get_revenue_summary

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(DATA_DIR, 'pipeline_logs')
NETLIFY_CONFIG = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'netlify', 'Config', 'config.json')


def _get_netlify_token():
    if not os.path.exists(NETLIFY_CONFIG):
        return None
    with open(NETLIFY_CONFIG, 'r') as f:
        cfg = json.load(f)
    uid = cfg.get('userId')
    if not uid:
        return None
    return cfg.get('users', {}).get(uid, {}).get('auth', {}).get('token')


def _log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"  [{timestamp}] {msg}")


def _deploy_site(site_name, site_id, deploy_dir):
    """Deploy a site to Netlify using the API for file upload."""
    token = _get_netlify_token()
    if not token:
        _log(f"  No Netlify token — skipping {site_name} deploy")
        return False

    try:
        result = subprocess.run(
            ["netlify", "deploy", "--prod", f"--dir={deploy_dir}", f"--site={site_id}"],
            capture_output=True, text=True, timeout=120,
            cwd=BASE_DIR
        )
        if result.returncode == 0:
            _log(f"  {site_name} deployed successfully")
            return True
        else:
            error = result.stderr.strip()
            if "429" in error or "Too Many" in error or "Forbidden" in error:
                _log(f"  {site_name}: Rate limited — will retry later")
            else:
                _log(f"  {site_name}: Deploy failed — {error[:100]}")
            return False
    except subprocess.TimeoutExpired:
        _log(f"  {site_name}: Deploy timed out")
        return False
    except FileNotFoundError:
        _log(f"  Netlify CLI not found — using API fallback")
        return _deploy_via_api(site_id, deploy_dir, token)


def _deploy_via_api(site_id, deploy_dir, token):
    """Fallback: trigger a deploy via Netlify REST API."""
    import urllib.request
    import urllib.error
    try:
        url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
        req = urllib.request.Request(
            url,
            data=b'{"title":"autonomous pipeline deploy"}',
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            _log(f"  Deploy triggered: {result.get('id', 'unknown')}")
            return True
    except urllib.error.HTTPError as e:
        _log(f"  API deploy failed: {e.code}")
        return False


def run_pipeline():
    """Execute the full autonomous pipeline."""
    os.makedirs(LOGS_DIR, exist_ok=True)

    run_time = datetime.now()
    run_id = run_time.strftime("%Y%m%d_%H%M%S")

    print(f"\n{'='*60}")
    print(f"  AUTONOMOUS PIPELINE — Run {run_id}")
    print(f"  {run_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    results = {
        "run_id": run_id,
        "timestamp": run_time.isoformat(),
        "steps": {},
        "success": True,
    }

    # ─── STEP 1: Check for new leads ──────────────
    print("  STEP 1: Checking for new leads...")
    try:
        new_leads = check_new_leads()
        summary = get_lead_summary()
        results["steps"]["leads"] = {
            "new_leads": len(new_leads),
            "total_leads": summary["total"],
            "status": "success"
        }
        _log(f"Leads: {len(new_leads)} new, {summary['total']} total")
    except Exception as e:
        results["steps"]["leads"] = {"status": "error", "error": str(e)}
        _log(f"Lead check failed: {e}")

    # ─── STEP 2: SEO Optimization ──────────────────
    print("\n  STEP 2: Running SEO optimization...")
    try:
        seo_count = generate_all_seo()
        results["steps"]["seo"] = {"pages_optimized": seo_count, "status": "success"}
        _log(f"SEO: {seo_count} pages optimized")
    except Exception as e:
        results["steps"]["seo"] = {"status": "error", "error": str(e)}
        _log(f"SEO failed: {e}")

    # ─── STEP 3: Deploy sites ─────────────────────
    print("\n  STEP 3: Deploying sites to Netlify...")
    main_deployed = _deploy_site(
        "myai-empire",
        "dd23c22c-225e-410e-affd-038b237bcc9c",
        os.path.join(BASE_DIR, "output", "website")
    )
    biz_deployed = _deploy_site(
        "myai-businesses",
        "391d0663-7bea-41d3-981c-6cb22ee58995",
        os.path.join(BASE_DIR, "output", "businesses")
    )
    results["steps"]["deploy"] = {
        "main_site": "deployed" if main_deployed else "skipped",
        "businesses_site": "deployed" if biz_deployed else "skipped",
        "status": "success" if (main_deployed or biz_deployed) else "rate_limited"
    }

    # ─── STEP 4: Revenue Report ───────────────────
    print("\n  STEP 4: Generating revenue report...")
    try:
        generate_revenue_report()
        rev = get_revenue_summary()
        results["steps"]["revenue"] = {
            "lifetime": rev["lifetime_revenue"],
            "mrr": rev["mrr"],
            "active_subs": rev["active_subscriptions"],
            "status": "success"
        }
    except Exception as e:
        results["steps"]["revenue"] = {"status": "error", "error": str(e)}
        _log(f"Revenue report failed: {e}")

    # ─── STEP 5: Save pipeline log ────────────────
    log_path = os.path.join(LOGS_DIR, f"pipeline_{run_id}.json")
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # ─── Summary ──────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"  Leads: {results['steps'].get('leads', {}).get('new_leads', '?')} new / {results['steps'].get('leads', {}).get('total_leads', '?')} total")
    print(f"  SEO: {results['steps'].get('seo', {}).get('pages_optimized', '?')} pages")
    print(f"  Deploy: main={results['steps'].get('deploy', {}).get('main_site', '?')}, businesses={results['steps'].get('deploy', {}).get('businesses_site', '?')}")
    print(f"  Revenue: ${results['steps'].get('revenue', {}).get('lifetime', 0):,.2f} lifetime")
    print(f"\n  Live sites:")
    print(f"    https://aoeua.com/")
    print(f"    https://businesses.aoeua.com/")
    print(f"{'='*60}\n")

    return results


if __name__ == "__main__":
    run_pipeline()
