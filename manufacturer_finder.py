"""
UK Manufacturer Finder — Scrapes Trustpilot, Yell.com, and web directories
for UK manufacturing businesses with email discovery.
"""
import json
import os
import re
import time
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "manufacturer_prospects.json")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# Manufacturing-specific Trustpilot categories
TRUSTPILOT_CATEGORIES = [
    "manufacturer", "factory", "industrial_supply",
    "metal_fabrication", "engineering_company", "packaging_company",
    "food_manufacturer", "chemical_company", "printing_company",
    "furniture_manufacturer", "textile_company", "electronics_manufacturer",
    "plastic_manufacturer", "paper_manufacturer", "glass_manufacturer",
    "steel_manufacturer", "pharmaceutical_company", "cosmetics_manufacturer",
    "building_materials", "concrete_company", "timber_merchant",
    "tool_manufacturer", "machine_manufacturer", "auto_parts",
    "cable_manufacturer", "paint_manufacturer", "adhesive_manufacturer",
    "rubber_manufacturer", "ceramic_manufacturer", "insulation_company",
    "sign_manufacturer", "label_manufacturer", "spring_manufacturer",
    "pump_manufacturer", "valve_manufacturer", "bearing_manufacturer",
    "fastener_manufacturer", "wire_manufacturer", "pipe_manufacturer",
    "sheet_metal", "cnc_machining", "laser_cutting",
    "injection_moulding", "extrusion", "fabrication",
    "welding_company", "foundry", "forge",
    "recycling_company", "waste_management",
]

# Yell.com manufacturing categories + UK cities
YELL_SEARCHES = [
    ("manufacturers", "london"), ("manufacturers", "manchester"),
    ("manufacturers", "birmingham"), ("manufacturers", "leeds"),
    ("manufacturers", "sheffield"), ("manufacturers", "bristol"),
    ("manufacturers", "liverpool"), ("manufacturers", "nottingham"),
    ("manufacturers", "leicester"), ("manufacturers", "coventry"),
    ("manufacturers", "newcastle"), ("manufacturers", "wolverhampton"),
    ("manufacturers", "glasgow"), ("manufacturers", "edinburgh"),
    ("manufacturers", "cardiff"), ("manufacturers", "belfast"),
    ("manufacturers", "derby"), ("manufacturers", "stoke-on-trent"),
    ("manufacturers", "sunderland"), ("manufacturers", "wakefield"),
    ("engineering-companies", "london"), ("engineering-companies", "manchester"),
    ("engineering-companies", "birmingham"), ("engineering-companies", "sheffield"),
    ("engineering-companies", "leeds"), ("engineering-companies", "bristol"),
    ("engineering-companies", "newcastle"), ("engineering-companies", "glasgow"),
    ("metal-fabrication", "london"), ("metal-fabrication", "birmingham"),
    ("metal-fabrication", "sheffield"), ("metal-fabrication", "manchester"),
    ("metal-fabrication", "leeds"), ("metal-fabrication", "wolverhampton"),
    ("food-manufacturers", "london"), ("food-manufacturers", "manchester"),
    ("food-manufacturers", "birmingham"), ("food-manufacturers", "leeds"),
    ("food-manufacturers", "bristol"), ("food-manufacturers", "leicester"),
    ("packaging-companies", "london"), ("packaging-companies", "manchester"),
    ("packaging-companies", "birmingham"), ("packaging-companies", "leeds"),
    ("printing-companies", "london"), ("printing-companies", "manchester"),
    ("printing-companies", "birmingham"), ("printing-companies", "bristol"),
    ("plastic-manufacturers", "london"), ("plastic-manufacturers", "birmingham"),
    ("plastic-manufacturers", "manchester"), ("plastic-manufacturers", "sheffield"),
    ("chemical-manufacturers", "london"), ("chemical-manufacturers", "manchester"),
    ("chemical-manufacturers", "middlesbrough"), ("chemical-manufacturers", "hull"),
    ("furniture-manufacturers", "london"), ("furniture-manufacturers", "nottingham"),
    ("furniture-manufacturers", "manchester"), ("furniture-manufacturers", "high-wycombe"),
    ("textile-manufacturers", "manchester"), ("textile-manufacturers", "leeds"),
    ("textile-manufacturers", "leicester"), ("textile-manufacturers", "bradford"),
    ("electronics-manufacturers", "london"), ("electronics-manufacturers", "cambridge"),
    ("electronics-manufacturers", "reading"), ("electronics-manufacturers", "bristol"),
    ("pharmaceutical-companies", "london"), ("pharmaceutical-companies", "cambridge"),
    ("pharmaceutical-companies", "manchester"), ("pharmaceutical-companies", "hertfordshire"),
    ("building-materials", "london"), ("building-materials", "birmingham"),
    ("building-materials", "manchester"), ("building-materials", "bristol"),
    ("cnc-machining", "sheffield"), ("cnc-machining", "birmingham"),
    ("cnc-machining", "manchester"), ("cnc-machining", "coventry"),
    ("injection-moulding", "birmingham"), ("injection-moulding", "manchester"),
    ("injection-moulding", "coventry"), ("injection-moulding", "telford"),
    ("welding", "sheffield"), ("welding", "birmingham"),
    ("welding", "manchester"), ("welding", "wolverhampton"),
    ("industrial-supplies", "london"), ("industrial-supplies", "manchester"),
    ("industrial-supplies", "birmingham"), ("industrial-supplies", "leeds"),
]


def extract_emails_from_page(url, timeout=10):
    """Extract email addresses from a webpage."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return []
        text = resp.text
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        blocked = ['example.com', 'sentry.io', 'wixpress.com', 'w3.org', 'schema.org',
                   'googleapis.com', 'google.com', 'facebook.com', 'twitter.com',
                   'gravatar.com', 'wordpress.org', 'jquery.com', 'cloudflare.com',
                   'bootstrap', 'fontawesome', 'jsdelivr', 'trustpilot.com']
        emails = [e.lower() for e in emails
                  if not any(b in e.lower() for b in blocked)
                  and not e.startswith('.')
                  and len(e) < 60]
        return list(set(emails))
    except Exception:
        return []


def scrape_trustpilot_category(category, max_pages=3):
    """Scrape a Trustpilot UK business category."""
    prospects = []
    for page in range(1, max_pages + 1):
        url = f"https://uk.trustpilot.com/categories/{category}?page={page}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                break
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select('div[class*="businessUnit"]') or soup.select('a[href*="/review/"]')
            if not cards:
                break
            for card in cards:
                link = card.get("href", "") or ""
                if not link:
                    a_tag = card.select_one('a[href*="/review/"]')
                    if a_tag:
                        link = a_tag.get("href", "")
                name_el = card.select_one('p, span, div[class*="name"], h2, h3')
                name = name_el.get_text(strip=True) if name_el else ""
                if link and "/review/" in link:
                    domain = link.split("/review/")[-1].split("?")[0].strip("/")
                    if domain and "." in domain:
                        prospects.append({
                            "name": name or domain.split(".")[0].title(),
                            "website": f"https://{domain}",
                            "source": "trustpilot",
                            "category": category,
                            "niche": "manufacturing",
                        })
            time.sleep(1.5)
        except Exception:
            break
    return prospects


def scrape_yell_search(category, city):
    """Scrape Yell.com for manufacturers in a UK city."""
    prospects = []
    url = f"https://www.yell.com/ucs/UcsSearchAction.do?keywords={category}&location={city}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return prospects
        soup = BeautifulSoup(resp.text, "html.parser")
        listings = soup.select('.businessCapsule') or soup.select('article')
        for listing in listings[:20]:
            name_el = listing.select_one('h2, .businessCapsule--name, [class*="name"]')
            name = name_el.get_text(strip=True) if name_el else ""
            website_el = listing.select_one('a[href*="http"][class*="website"], a[rel="nofollow"]')
            website = ""
            if website_el:
                website = website_el.get("href", "")
                if "yell.com" in website:
                    website = ""
            phone_el = listing.select_one('[class*="phone"], [class*="tel"]')
            phone = phone_el.get_text(strip=True) if phone_el else ""
            if name:
                prospects.append({
                    "name": name,
                    "website": website,
                    "phone": phone,
                    "source": "yell",
                    "category": f"{category} in {city}",
                    "niche": "manufacturing",
                })
        time.sleep(1.5)
    except Exception:
        pass
    return prospects


def enrich_with_email(prospects, max_enrich=800):
    """Visit prospect websites to find email addresses."""
    enriched = 0
    found_emails = 0
    for p in prospects:
        if enriched >= max_enrich:
            break
        if not p.get("website"):
            continue
        if p.get("email"):
            continue
        enriched += 1
        base_url = p["website"]
        emails = []
        for suffix in ["", "/contact", "/contact-us", "/about", "/about-us"]:
            try_url = base_url.rstrip("/") + suffix
            found = extract_emails_from_page(try_url)
            emails.extend(found)
            if emails:
                break
            time.sleep(0.5)
        if emails:
            p["email"] = emails[0]
            found_emails += 1
        if enriched % 20 == 0:
            print(f"  \U0001f4e7 Enriched {enriched}/{max_enrich} — Found {found_emails} emails so far")
    return found_emails


def deduplicate(prospects):
    """Remove duplicates based on website domain."""
    seen = set()
    unique = []
    for p in prospects:
        domain = p.get("website", "").replace("https://", "").replace("http://", "").split("/")[0].lower()
        if domain and domain not in seen:
            seen.add(domain)
            unique.append(p)
        elif not domain and p.get("name"):
            key = p["name"].lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(p)
    return unique


def load_existing():
    """Load existing manufacturer prospects."""
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_prospects(prospects):
    """Save prospects to file."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(prospects, f, indent=2, ensure_ascii=False)


def run():
    print("=" * 60)
    print("  UK MANUFACTURER FINDER")
    print(f"  Trustpilot categories: {len(TRUSTPILOT_CATEGORIES)}")
    print(f"  Yell searches: {len(YELL_SEARCHES)}")
    print("=" * 60)

    existing = load_existing()
    existing_domains = {
        p.get("website", "").replace("https://", "").replace("http://", "").split("/")[0].lower()
        for p in existing
    }
    print(f"\n  Existing manufacturer prospects: {len(existing)}")

    all_new = []

    # Phase 1: Trustpilot
    print(f"\n{'=' * 60}")
    print("  PHASE 1: Trustpilot UK Manufacturing Categories")
    print(f"{'=' * 60}")
    for i, cat in enumerate(TRUSTPILOT_CATEGORIES, 1):
        print(f"  [{i}/{len(TRUSTPILOT_CATEGORIES)}] Scraping: {cat}")
        found = scrape_trustpilot_category(cat)
        new = [p for p in found
               if p.get("website", "").replace("https://", "").replace("http://", "").split("/")[0].lower()
               not in existing_domains]
        for p in new:
            domain = p["website"].replace("https://", "").replace("http://", "").split("/")[0].lower()
            existing_domains.add(domain)
        all_new.extend(new)
        print(f"    Found: {len(found)} total, {len(new)} new")

    # Phase 2: Yell.com
    print(f"\n{'=' * 60}")
    print("  PHASE 2: Yell.com UK Manufacturing Directory")
    print(f"{'=' * 60}")
    for i, (cat, city) in enumerate(YELL_SEARCHES, 1):
        print(f"  [{i}/{len(YELL_SEARCHES)}] Scraping: {cat} in {city}")
        found = scrape_yell_search(cat, city)
        new = []
        for p in found:
            domain = p.get("website", "").replace("https://", "").replace("http://", "").split("/")[0].lower()
            name_key = p.get("name", "").lower().strip()
            if domain and domain not in existing_domains:
                existing_domains.add(domain)
                new.append(p)
            elif not domain and name_key and name_key not in existing_domains:
                existing_domains.add(name_key)
                new.append(p)
        all_new.extend(new)
        print(f"    Found: {len(found)} total, {len(new)} new")

    # Deduplicate
    all_new = deduplicate(all_new)
    print(f"\n  Total raw manufacturer prospects (before email enrichment): {len(all_new)}")

    # Phase 3: Email enrichment
    print(f"\n{'=' * 60}")
    print("  PHASE 3: Email Discovery")
    print(f"{'=' * 60}")
    with_website = [p for p in all_new if p.get("website")]
    emails_found = enrich_with_email(with_website, max_enrich=800)

    # Merge with existing
    all_prospects = existing + all_new
    all_prospects = deduplicate(all_prospects)

    # Save
    save_prospects(all_prospects)

    # Summary
    with_email = [p for p in all_prospects if p.get("email")]
    print(f"\n{'=' * 60}")
    print("  RESULTS")
    print(f"{'=' * 60}")
    print(f"  Total manufacturer prospects: {len(all_prospects)}")
    print(f"  With email: {len(with_email)}")
    print(f"  With website: {len([p for p in all_prospects if p.get('website')])}")
    print(f"  New this run: {len(all_new)}")
    print(f"  Emails found this run: {emails_found}")
    print(f"\n  Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
