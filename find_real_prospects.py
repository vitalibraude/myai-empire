"""
Real Prospect Finder v2 — uses Trustpilot (works!) to find REAL UK businesses,
then visits their websites to extract contact emails.

Usage:
    python find_real_prospects.py                  # Default: 5 niches, 10 per niche
    python find_real_prospects.py --niches 3 --max 5   # Quick run: 3 niches, 5 each
"""
import json
import os
import re
import time
import warnings
import argparse
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "real_prospects.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}

# Trustpilot category URLs for UK businesses
TRUSTPILOT_CATEGORIES = {
    "restaurants": "https://uk.trustpilot.com/categories/restaurant",
    "dental": "https://uk.trustpilot.com/categories/dentist",
    "salons": "https://uk.trustpilot.com/categories/hair_salon",
    "plumbers": "https://uk.trustpilot.com/categories/plumber",
    "electricians": "https://uk.trustpilot.com/categories/electrician",
    "accountants": "https://uk.trustpilot.com/categories/accounting_firm",
    "lawyers": "https://uk.trustpilot.com/categories/law_firm",
    "construction": "https://uk.trustpilot.com/categories/contractor",
    "photographers": "https://uk.trustpilot.com/categories/photographer",
    "ecommerce": "https://uk.trustpilot.com/categories/electronics_technology",
}


def scrape_trustpilot_category(url, niche, max_businesses=15):
    """Scrape Trustpilot category page for businesses."""
    businesses = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"  HTTP {r.status_code}")
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        profile_links = soup.find_all("a", href=re.compile(r"/review/"))

        seen = set()
        for link in profile_links:
            if len(businesses) >= max_businesses:
                break
            href = link.get("href", "")
            name_raw = link.get_text(strip=True)
            if not name_raw or len(name_raw) < 3 or name_raw in seen:
                continue
            skip = ["review", "write", "read", "see all", "more", "page", "next", "filter", "sort"]
            if any(w in name_raw.lower() for w in skip) and len(name_raw) < 25:
                continue
            seen.add(name_raw)

            # Clean name
            name = re.split(r'www\.|https?://|\d+\.\d+|\d+,?\d*\s*review', name_raw)[0].strip()
            if not name:
                name = name_raw[:40]

            # Extract domain
            domain_match = re.search(r'([\w\-]+\.(?:co\.uk|com|org\.uk|uk|net|org))', name_raw)
            website = f"https://www.{domain_match.group(1)}" if domain_match else ""

            profile_url = href if href.startswith("http") else f"https://uk.trustpilot.com{href}"

            businesses.append({
                "name": name,
                "website": website,
                "trustpilot_url": profile_url,
                "niche": niche,
            })

    except Exception as e:
        print(f"  Error: {e}")

    return businesses


def get_website_from_profile(profile_url):
    """Get business website from Trustpilot profile."""
    try:
        r = requests.get(profile_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return ""
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True).lower()
            href = a["href"]
            if ("website" in text or "visit" in text) and href.startswith("http") and "trustpilot" not in href:
                return href

        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    url = data.get("url", "")
                    if url and "trustpilot" not in url:
                        return url
            except:
                pass

    except Exception:
        pass
    return ""


def extract_email_from_website(url):
    """Visit a business website and find email addresses."""
    if not url or not url.startswith("http"):
        return ""

    emails_found = set()
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    domain = parsed.netloc.replace("www.", "")

    pages = [url]
    for suffix in ["/contact", "/contact-us", "/about", "/about-us", "/contact.html", "/get-in-touch"]:
        pages.append(base + suffix)

    for page_url in pages[:4]:
        try:
            r = requests.get(page_url, headers=HEADERS, timeout=8,
                           allow_redirects=True, verify=False)
            if r.status_code == 200:
                found = re.findall(
                    r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
                    r.text
                )
                for email in found:
                    email = email.lower().strip()
                    skip = ["example.com", "domain.com", "email.com", "yoursite",
                            "sentry.io", "wixpress", "googleapis", "schema.org",
                            "w3.org", "wordpress.org", "gravatar", "jquery",
                            ".png", ".jpg", ".gif", ".svg", ".css", ".js",
                            "noreply", "no-reply", "donotreply", "@2x", "@3x"]
                    if not any(s in email for s in skip):
                        emails_found.add(email)
        except Exception:
            continue
        time.sleep(0.3)

    if not emails_found:
        return ""

    for prefix in ["info@", "hello@", "contact@", "enquir", "admin@", "office@", "mail@", "team@"]:
        for e in emails_found:
            if e.startswith(prefix):
                return e

    for e in emails_found:
        if domain in e:
            return e

    return list(emails_found)[0]


def find_real_prospects(num_niches=5, max_per_niche=10):
    """Main: find real UK businesses with emails."""
    print("=" * 60)
    print("  REAL PROSPECT FINDER v2")
    print("  Source: Trustpilot UK + website email extraction")
    print("=" * 60)

    all_prospects = {}
    total_with_email = 0
    niches_to_use = dict(list(TRUSTPILOT_CATEGORIES.items())[:num_niches])

    for niche, url in niches_to_use.items():
        print(f"\n{'~'*50}")
        print(f"[{niche.upper()}] Scraping Trustpilot...")

        businesses = scrape_trustpilot_category(url, niche, max_businesses=max_per_niche * 2)
        print(f"  Found {len(businesses)} businesses on Trustpilot")

        for b in businesses:
            if not b.get("website") and b.get("trustpilot_url"):
                b["website"] = get_website_from_profile(b["trustpilot_url"])
                time.sleep(0.5)

        with_website = [b for b in businesses if b.get("website")]
        print(f"  {len(with_website)} have websites")

        print(f"  Extracting emails from websites...")
        for b in with_website[:max_per_niche]:
            email = extract_email_from_website(b["website"])
            b["email"] = email
            status = f"> {email}" if email else "  no email found"
            print(f"    {b['name'][:30]:30s} | {status}")
            time.sleep(0.3)

        with_email = [b for b in with_website if b.get("email")]
        all_prospects[niche] = with_email
        total_with_email += len(with_email)

        print(f"  [{niche.upper()}] {len(with_email)} prospects ready")
        time.sleep(1)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_prospects, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"  DONE: {total_with_email} real prospects with websites + emails")
    print(f"  Saved to: {OUTPUT_FILE}")
    print(f"{'=' * 60}")

    return all_prospects


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--niches", type=int, default=5, help="Number of niches")
    parser.add_argument("--max", type=int, default=10, help="Max per niche")
    args = parser.parse_args()

    find_real_prospects(num_niches=args.niches, max_per_niche=args.max)
