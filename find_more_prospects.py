"""
Extended Prospect Finder — multiple sources and pagination.
Adds more Trustpilot categories + page 2, plus direct Google-indexed contact pages.
"""
import json
import os
import re
import time
import warnings
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "real_prospects.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}

# Expanded categories with page 2
TRUSTPILOT_URLS = {
    "pet_services": "https://uk.trustpilot.com/categories/pet_store",
    "florists": "https://uk.trustpilot.com/categories/florist",
    "cleaners": "https://uk.trustpilot.com/categories/cleaning_service",
    "moving": "https://uk.trustpilot.com/categories/moving_company",
    "tutoring": "https://uk.trustpilot.com/categories/tutoring_service",
    "car_repair": "https://uk.trustpilot.com/categories/auto_repair_shop",
    "physiotherapy": "https://uk.trustpilot.com/categories/physiotherapist",
    "vets": "https://uk.trustpilot.com/categories/veterinarian",
    "printing": "https://uk.trustpilot.com/categories/printing_service",
    "catering": "https://uk.trustpilot.com/categories/catering_service",
    "locksmiths": "https://uk.trustpilot.com/categories/locksmith",
    "wedding": "https://uk.trustpilot.com/categories/wedding_planner",
    "pest_control": "https://uk.trustpilot.com/categories/pest_control_service",
    "roofing": "https://uk.trustpilot.com/categories/roofing_service",
    "gardening": "https://uk.trustpilot.com/categories/gardener",
    "restaurants_p2": "https://uk.trustpilot.com/categories/restaurant?page=2",
    "dental_p2": "https://uk.trustpilot.com/categories/dentist?page=2",
    "salons_p2": "https://uk.trustpilot.com/categories/hair_salon?page=2",
    "plumbers_p2": "https://uk.trustpilot.com/categories/plumber?page=2",
    "accountants": "https://uk.trustpilot.com/categories/accounting_firm?page=2",
    "lawyers_p2": "https://uk.trustpilot.com/categories/law_firm?page=2",
}


def extract_email_from_website(url):
    """Visit a business website and find email addresses."""
    if not url or not url.startswith("http"):
        return ""

    emails_found = set()
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    domain = parsed.netloc.replace("www.", "")

    pages = [url]
    for suffix in ["/contact", "/contact-us", "/about", "/about-us", "/contact.html", "/get-in-touch", "/info"]:
        pages.append(base + suffix)

    for page_url in pages[:5]:
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

    return emails_found.pop()


def scrape_trustpilot(url, niche, max_biz=20):
    businesses = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"  HTTP {r.status_code} for {niche}")
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all("a", href=re.compile(r"/review/"))
        seen = set()
        for link in links:
            if len(businesses) >= max_biz:
                break
            href = link.get("href", "")
            name_raw = link.get_text(strip=True)
            if not name_raw or len(name_raw) < 3 or name_raw in seen:
                continue
            skip_words = ["review", "write", "read", "see all", "more", "page", "next", "filter", "sort"]
            if any(w in name_raw.lower() for w in skip_words) and len(name_raw) < 25:
                continue
            seen.add(name_raw)
            name = re.split(r'www\.|https?://|\d+\.\d+|\d+,?\d*\s*review', name_raw)[0].strip()
            name = re.sub(r'^Most relevant', '', name).strip()
            if not name:
                name = name_raw[:40]
            domain_match = re.search(r'([\w\-]+\.(?:co\.uk|com|org\.uk|uk|net|org))', name_raw)
            website = f"https://www.{domain_match.group(1)}" if domain_match else ""

            # Try to get website from profile if not found in text
            if not website:
                profile_url = href if href.startswith("http") else f"https://uk.trustpilot.com{href}"
                website = get_website_from_profile(profile_url)

            businesses.append({
                "name": name,
                "website": website,
                "niche": niche.replace("_p2", ""),
            })
    except Exception as e:
        print(f"  Error: {e}")
    return businesses


def get_website_from_profile(profile_url):
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
    except:
        pass
    return ""


def main():
    # Load existing prospects
    existing = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            existing = json.load(f)

    # Collect already-known emails to avoid duplicates
    known_emails = set()
    for niche_list in existing.values():
        for p in niche_list:
            if p.get("email"):
                known_emails.add(p["email"].lower())

    print("=" * 60)
    print("  EXTENDED PROSPECT FINDER")
    print(f"  Existing emails: {len(known_emails)}")
    print(f"  Categories to scan: {len(TRUSTPILOT_URLS)}")
    print("=" * 60)

    new_total = 0

    for niche, url in TRUSTPILOT_URLS.items():
        niche_key = niche.replace("_p2", "")
        print(f"\n[{niche.upper()}] Scraping...")
        businesses = scrape_trustpilot(url, niche, max_biz=20)
        print(f"  Found {len(businesses)} businesses")

        found_this = 0
        for biz in businesses:
            if not biz["website"]:
                continue
            email = extract_email_from_website(biz["website"])
            if email and email.lower() not in known_emails:
                biz["email"] = email
                known_emails.add(email.lower())

                if niche_key not in existing:
                    existing[niche_key] = []
                existing[niche_key].append(biz)
                found_this += 1
                new_total += 1
                print(f"    NEW: {biz['name']} | {email}")

        print(f"  [{niche.upper()}] {found_this} new prospects")
        time.sleep(1)

    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(existing, f, indent=2)

    total_all = sum(len(v) for v in existing.values())
    print(f"\n{'=' * 60}")
    print(f"  DONE: {new_total} new prospects found")
    print(f"  Total prospects: {total_all}")
    print(f"  Saved to: {OUTPUT_FILE}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
