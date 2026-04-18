"""
deploy.py — One-Click Deployment for All 50 Businesses
Deploys all generated sites to Vercel, Netlify, or GitHub Pages.
Also generates a package.json and netlify config for each site.
"""
import os
import sys
import json
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from agent.business_generator import load_businesses

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIZ_OUTPUT = os.path.join(BASE_DIR, 'output', 'businesses')
DEPLOY_LOG = os.path.join(BASE_DIR, 'data', 'deploy_log.json')


def prepare_site(biz_dir, biz):
    """Prepare a site for deployment with necessary config files."""

    # Create a minimal package.json for static site hosting
    pkg = {
        "name": biz['id'],
        "version": "1.0.0",
        "description": f"{biz['name']} — {biz['tagline']}",
        "scripts": {
            "start": "npx serve .",
            "build": "echo 'Static site — no build needed'"
        }
    }
    with open(os.path.join(biz_dir, 'package.json'), 'w') as f:
        json.dump(pkg, f, indent=2)

    # Create netlify.toml
    netlify = f"""[build]
  publish = "."
  command = "echo 'Static site ready'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Content-Security-Policy = "default-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'"
"""
    with open(os.path.join(biz_dir, 'netlify.toml'), 'w') as f:
        f.write(netlify)

    # Create vercel.json
    vercel = {
        "version": 2,
        "builds": [{"src": "**/*", "use": "@vercel/static"}],
        "routes": [{"handle": "filesystem"}, {"src": "/(.*)", "dest": "/index.html"}]
    }
    with open(os.path.join(biz_dir, 'vercel.json'), 'w') as f:
        json.dump(vercel, f, indent=2)

    return True


def deploy_to_vercel(biz_dir, biz):
    """Deploy a single site to Vercel."""
    try:
        result = subprocess.run(
            ['vercel', '--prod', '--yes', '--name', biz['id']],
            cwd=biz_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            url = result.stdout.strip().split('\n')[-1]
            return {"status": "deployed", "url": url}
        else:
            return {"status": "error", "error": result.stderr.strip()}
    except FileNotFoundError:
        return {"status": "skipped", "error": "Vercel CLI not installed. Run: npm i -g vercel"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def deploy_to_netlify(biz_dir, biz):
    """Deploy a single site to Netlify."""
    try:
        result = subprocess.run(
            ['netlify', 'deploy', '--prod', f'--dir={biz_dir}', f'--site={biz["id"]}'],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return {"status": "deployed", "output": result.stdout.strip()[-200:]}
        else:
            return {"status": "error", "error": result.stderr.strip()}
    except FileNotFoundError:
        return {"status": "skipped", "error": "Netlify CLI not installed. Run: npm i -g netlify-cli"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def prepare_all():
    """Prepare all 50 sites for deployment (no external tools needed)."""
    print("=" * 60)
    print("  PREPARING ALL 50 SITES FOR DEPLOYMENT")
    print("=" * 60)

    businesses = load_businesses()
    prepared = 0

    for biz in businesses:
        biz_dir = os.path.join(BIZ_OUTPUT, biz['id'])
        if os.path.exists(biz_dir):
            prepare_site(biz_dir, biz)
            prepared += 1
            print(f"  OK  {biz['name']} — package.json, netlify.toml, vercel.json")

    print(f"\n  {prepared} sites prepared for deployment.")
    print(f"\n  NEXT STEPS:")
    print(f"  Option A — Vercel (recommended):")
    print(f"    1. npm i -g vercel")
    print(f"    2. vercel login")
    print(f"    3. python deploy.py --vercel")
    print(f"  Option B — Netlify:")
    print(f"    1. npm i -g netlify-cli")
    print(f"    2. netlify login")
    print(f"    3. python deploy.py --netlify")
    print(f"  Option C — Manual:")
    print(f"    Drag each folder to https://app.netlify.com/drop")
    print(f"    (Free, no CLI needed!)")

    return prepared


def deploy_all(platform='vercel'):
    """Deploy all 50 sites to the chosen platform."""
    print("=" * 60)
    print(f"  DEPLOYING ALL 50 SITES TO {platform.upper()}")
    print("=" * 60)

    businesses = load_businesses()
    results = []

    for biz in businesses:
        biz_dir = os.path.join(BIZ_OUTPUT, biz['id'])
        if not os.path.exists(biz_dir):
            print(f"  SKIP  {biz['name']} — not generated yet")
            continue

        print(f"  Deploying {biz['name']}...", end=" ")
        prepare_site(biz_dir, biz)

        if platform == 'vercel':
            result = deploy_to_vercel(biz_dir, biz)
        elif platform == 'netlify':
            result = deploy_to_netlify(biz_dir, biz)
        else:
            result = {"status": "skipped", "error": f"Unknown platform: {platform}"}

        results.append({"business": biz['id'], "name": biz['name'], **result})

        if result['status'] == 'deployed':
            print(f"OK — {result.get('url', 'deployed')}")
        elif result['status'] == 'skipped':
            print(f"SKIPPED — {result.get('error', '')}")
            break  # If CLI not installed, stop trying
        else:
            print(f"ERROR — {result.get('error', '')}")

    # Save deploy log
    log = {
        "platform": platform,
        "timestamp": datetime.now().isoformat(),
        "total": len(results),
        "deployed": sum(1 for r in results if r['status'] == 'deployed'),
        "results": results
    }
    os.makedirs(os.path.dirname(DEPLOY_LOG), exist_ok=True)
    with open(DEPLOY_LOG, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2)

    deployed = sum(1 for r in results if r['status'] == 'deployed')
    print(f"\n  Deployed: {deployed}/{len(results)} sites")
    return log


if __name__ == '__main__':
    if '--vercel' in sys.argv:
        deploy_all('vercel')
    elif '--netlify' in sys.argv:
        deploy_all('netlify')
    else:
        prepare_all()
