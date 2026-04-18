"""
UK Manufacturer Finder v2 — Uses real manufacturer directories:
- Made in Britain member directory
- UK Manufacturer listings
- Kompass-style B2B directories
- Direct Google-indexed manufacturer sites
- Broader Trustpilot B2B categories that actually exist
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
                  " (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}

# Real Trustpilot categories that B2B/manufacturing companies appear under
TRUSTPILOT_B2B_CATEGORIES = [
    "industrial_services", "business_supplies",
    "construction_company", "heating_company",
    "electronics_and_technology", "energy_supplier",
    "clothing_store", "home_and_garden",
    "building_materials_store", "furniture_store",
    "food_products_supplier", "cosmetics_and_beauty_supply",
    "health_products", "agricultural_service",
    "chemical_supplier", "hardware_store",
    "printing_service", "packaging_service",
]

# Real manufacturer directory pages to scrape
DIRECTORY_URLS = [
    # Made in Britain style directories
    ("https://www.madeinbritain.org/members", "madeinbritain"),
    ("https://www.themanufacturer.com/uk-manufacturing-directory/", "themanufacturer"),
    ("https://www.ukmanufacturers.co.uk/", "ukmanufacturers"),
    ("https://www.bbcgoodfood.com/howto/guide/british-food-and-drink-producers", "foodproducers"),
]

# Search queries for finding manufacturer websites directly
SEARCH_QUERIES = [
    # Metal & Engineering
    "metal fabrication company UK contact",
    "CNC machining company UK email",
    "precision engineering UK manufacturer",
    "sheet metal UK manufacturer contact",
    "steel fabrication company UK",
    "welding company UK manufacturer",
    "casting foundry UK",
    "forging company UK",
    "spring manufacturer UK",
    "fastener manufacturer UK",
    "wire manufacturer UK",
    "tube manufacturer UK",
    "aluminium manufacturer UK",
    # Plastics & Polymers
    "injection moulding company UK",
    "plastic manufacturer UK contact",
    "rubber manufacturer UK",
    "extrusion company UK",
    "fiberglass manufacturer UK",
    # Food & Drink
    "food manufacturer UK contact",
    "bakery manufacturer UK",
    "drink manufacturer UK",
    "sauce manufacturer UK",
    "snack manufacturer UK",
    "dairy manufacturer UK",
    "meat processor UK",
    # Packaging
    "packaging manufacturer UK contact",
    "cardboard box manufacturer UK",
    "label manufacturer UK",
    "bottle manufacturer UK",
    "plastic packaging UK",
    # Textiles & Fashion
    "textile manufacturer UK",
    "clothing manufacturer UK contact",
    "fabric manufacturer UK",
    "uniform manufacturer UK",
    # Electronics
    "electronics manufacturer UK",
    "PCB manufacturer UK",
    "cable manufacturer UK",
    "LED manufacturer UK",
    "sensor manufacturer UK",
    # Building & Construction
    "building materials manufacturer UK",
    "brick manufacturer UK",
    "window manufacturer UK",
    "door manufacturer UK",
    "insulation manufacturer UK",
    "concrete manufacturer UK",
    "paint manufacturer UK",
    # Furniture & Wood
    "furniture manufacturer UK contact",
    "kitchen manufacturer UK",
    "timber merchant UK",
    "joinery manufacturer UK",
    # Chemicals & Pharma
    "chemical manufacturer UK",
    "pharmaceutical manufacturer UK",
    "cosmetics manufacturer UK",
    "cleaning products manufacturer UK",
    # Automotive & Aerospace
    "automotive parts manufacturer UK",
    "aerospace manufacturer UK",
    "auto component manufacturer UK",
    # General
    "manufacturer UK email contact",
    "UK factory company email",
    "British manufacturer contact details",
    "made in UK manufacturer",
]


def extract_emails_from_page(url, timeout=10):
    """Extract email addresses from a webpage."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return [], resp.url
        text = resp.text
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        blocked = ['example.com', 'sentry.io', 'wixpress.com', 'w3.org', 'schema.org',
                   'googleapis.com', 'google.com', 'facebook.com', 'twitter.com',
                   'gravatar.com', 'wordpress.org', 'jquery.com', 'cloudflare.com',
                   'bootstrap', 'fontawesome', 'jsdelivr', 'trustpilot.com',
                   'yell.com', 'bing.com', 'yahoo.com', 'hotmail.com', 'gmail.com',
                   'outlook.com', 'aol.com', 'icloud.com', 'protonmail.com']
        emails = [e.lower() for e in emails
                  if not any(b in e.lower() for b in blocked)
                  and not e.startswith('.')
                  and len(e) < 60]
        return list(set(emails)), resp.url
    except Exception:
        return [], url


def extract_company_info_from_page(url, timeout=10):
    """Extract company name, email, phone from a website."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Get title as company name
        title = ""
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True).split("|")[0].split("-")[0].strip()
        
        # Get emails
        text = resp.text
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        blocked = ['example.com', 'sentry.io', 'wixpress.com', 'w3.org', 'schema.org',
                   'googleapis.com', 'google.com', 'facebook.com', 'twitter.com',
                   'gravatar.com', 'wordpress.org', 'jquery.com', 'cloudflare.com',
                   'bootstrap', 'fontawesome', 'jsdelivr', 'noreply', 'no-reply']
        emails = [e.lower() for e in emails
                  if not any(b in e.lower() for b in blocked)
                  and not e.startswith('.') and len(e) < 60]
        emails = list(set(emails))
        
        # Get phone numbers (UK format)
        phones = re.findall(r'(?:0|\+44)\s*(?:\d[\d\s]{8,12}\d)', text)
        phones = [re.sub(r'\s+', ' ', p.strip()) for p in phones]
        
        if title or emails:
            return {
                "name": title[:100] if title else "",
                "email": emails[0] if emails else "",
                "phone": phones[0] if phones else "",
                "all_emails": emails[:3],
            }
        return None
    except Exception:
        return None


def scrape_trustpilot_b2b(category, max_pages=3):
    """Scrape Trustpilot under broader B2B categories."""
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


def scrape_directory_page(url, source_name):
    """Scrape a manufacturer directory page for business links."""
    prospects = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return prospects
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Find external links (to manufacturer websites)
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            text = link.get_text(strip=True)
            # Filter for external manufacturer links
            if (href.startswith("http") and
                source_name not in href and
                "google" not in href and
                "facebook" not in href and
                "twitter" not in href and
                "linkedin" not in href and
                "youtube" not in href and
                len(text) > 2 and len(text) < 100):
                
                domain = href.replace("https://", "").replace("http://", "").split("/")[0]
                if "." in domain and len(domain) > 4:
                    prospects.append({
                        "name": text,
                        "website": f"https://{domain}",
                        "source": source_name,
                        "category": "directory_listing",
                        "niche": "manufacturing",
                    })
        time.sleep(2)
    except Exception:
        pass
    return prospects


def find_manufacturers_via_search(queries, max_results_per_query=20):
    """
    Use DuckDuckGo HTML search to find manufacturer websites.
    More reliable than Google for scraping.
    """
    prospects = []
    for i, query in enumerate(queries):
        print(f"  [{i+1}/{len(queries)}] Searching: {query}")
        try:
            search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            resp = requests.get(search_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }, timeout=15)
            if resp.status_code != 200:
                time.sleep(2)
                continue
            
            soup = BeautifulSoup(resp.text, "html.parser")
            results = soup.select('.result__a') or soup.select('a.result-link')
            
            for result in results[:max_results_per_query]:
                href = result.get("href", "")
                text = result.get_text(strip=True)
                
                # Extract actual URL from DuckDuckGo redirect
                if "uddg=" in href:
                    import urllib.parse
                    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                    if "uddg" in parsed:
                        href = parsed["uddg"][0]
                
                if not href.startswith("http"):
                    continue
                    
                domain = href.replace("https://", "").replace("http://", "").split("/")[0]
                
                # Skip non-manufacturer sites
                skip_domains = ['wikipedia', 'youtube', 'facebook', 'twitter', 'linkedin',
                               'amazon', 'ebay', 'reddit', 'gov.uk', 'bbc.co.uk',
                               'yell.com', 'trustpilot', 'yelp', 'gumtree',
                               'indeed.com', 'glassdoor', 'duckduckgo', 'google']
                if any(s in domain.lower() for s in skip_domains):
                    continue
                
                if "." in domain and len(domain) > 4:
                    prospects.append({
                        "name": text[:100],
                        "website": f"https://{domain}",
                        "source": "search",
                        "category": query.split(" ")[0],
                        "niche": "manufacturing",
                    })
            
            found = len([r for r in results[:max_results_per_query]])
            print(f"    Found: {found} results")
            time.sleep(2)  # Rate limiting
        except Exception as e:
            print(f"    Error: {e}")
            time.sleep(3)
    
    return prospects


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


def enrich_with_email(prospects, max_enrich=500):
    """Visit prospect websites to find email addresses and better names."""
    enriched = 0
    found_emails = 0
    for p in prospects:
        if enriched >= max_enrich:
            break
        if not p.get("website"):
            continue
        if p.get("email"):
            found_emails += 1
            enriched += 1
            continue
        
        enriched += 1
        base_url = p["website"]
        
        # Check main page + contact page
        for suffix in ["", "/contact", "/contact-us", "/about", "/about-us", "/contact.html"]:
            try_url = base_url.rstrip("/") + suffix
            emails, final_url = extract_emails_from_page(try_url)
            if emails:
                p["email"] = emails[0]
                found_emails += 1
                break
            time.sleep(0.5)
        
        # Try to get better name from title
        if not p.get("name") or len(p["name"]) < 3:
            info = extract_company_info_from_page(base_url)
            if info and info.get("name"):
                p["name"] = info["name"]
            if info and info.get("phone") and not p.get("phone"):
                p["phone"] = info["phone"]
        
        if enriched % 20 == 0:
            print(f"  \U0001f4e7 Enriched {enriched}/{max_enrich} \u2014 Found {found_emails} emails so far")
    
    return found_emails


def load_existing():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_prospects(prospects):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(prospects, f, indent=2, ensure_ascii=False)


def run():
    print("=" * 60)
    print("  UK MANUFACTURER FINDER v2")
    print(f"  Search queries: {len(SEARCH_QUERIES)}")
    print(f"  B2B Trustpilot categories: {len(TRUSTPILOT_B2B_CATEGORIES)}")
    print(f"  Directories: {len(DIRECTORY_URLS)}")
    print("=" * 60)

    existing = load_existing()
    existing_domains = {
        p.get("website", "").replace("https://", "").replace("http://", "").split("/")[0].lower()
        for p in existing
    }
    print(f"\n  Existing prospects: {len(existing)}")

    all_new = []

    # Phase 1: DuckDuckGo Search (most effective for B2B)
    print(f"\n{'=' * 60}")
    print("  PHASE 1: Search Engine Discovery")
    print(f"{'=' * 60}")
    search_results = find_manufacturers_via_search(SEARCH_QUERIES)
    new_from_search = [
        p for p in search_results
        if p.get("website", "").replace("https://", "").replace("http://", "").split("/")[0].lower()
        not in existing_domains
    ]
    for p in new_from_search:
        domain = p["website"].replace("https://", "").replace("http://", "").split("/")[0].lower()
        existing_domains.add(domain)
    all_new.extend(new_from_search)
    print(f"\n  Search results: {len(search_results)} total, {len(new_from_search)} new")

    # Phase 2: Trustpilot B2B categories
    print(f"\n{'=' * 60}")
    print("  PHASE 2: Trustpilot B2B Categories")
    print(f"{'=' * 60}")
    for i, cat in enumerate(TRUSTPILOT_B2B_CATEGORIES, 1):
        print(f"  [{i}/{len(TRUSTPILOT_B2B_CATEGORIES)}] Scraping: {cat}")
        found = scrape_trustpilot_b2b(cat)
        new = [p for p in found
               if p.get("website", "").replace("https://", "").replace("http://", "").split("/")[0].lower()
               not in existing_domains]
        for p in new:
            domain = p["website"].replace("https://", "").replace("http://", "").split("/")[0].lower()
            existing_domains.add(domain)
        all_new.extend(new)
        print(f"    Found: {len(found)} total, {len(new)} new")

    # Phase 3: Directory scraping
    print(f"\n{'=' * 60}")
    print("  PHASE 3: Manufacturer Directories")
    print(f"{'=' * 60}")
    for url, source in DIRECTORY_URLS:
        print(f"  Scraping: {source} ({url})")
        found = scrape_directory_page(url, source)
        new = [p for p in found
               if p.get("website", "").replace("https://", "").replace("http://", "").split("/")[0].lower()
               not in existing_domains]
        for p in new:
            domain = p["website"].replace("https://", "").replace("http://", "").split("/")[0].lower()
            existing_domains.add(domain)
        all_new.extend(new)
        print(f"    Found: {len(found)} total, {len(new)} new")

    # Deduplicate
    all_new = deduplicate(all_new)
    print(f"\n  Total unique new prospects: {len(all_new)}")

    # Phase 4: Email enrichment
    print(f"\n{'=' * 60}")
    print("  PHASE 4: Email Discovery")
    print(f"{'=' * 60}")
    with_website = [p for p in all_new if p.get("website")]
    emails_found = enrich_with_email(with_website, max_enrich=500)

    # Merge
    all_prospects = existing + all_new
    all_prospects = deduplicate(all_prospects)
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
