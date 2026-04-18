"""
Mass Prospect Finder — uses WORKING sources to find UK manufacturers with real emails.
Sources:
  1. Thomson Local (25 listings/page, multiple categories + cities)
  2. Made in Britain directory (21 sectors, paginated)
  3. Contact page scraping for real emails
  4. Email verification (DNS + SMTP)
"""
import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_FILE = os.path.join(DATA_DIR, 'verified_prospects.json')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.9',
}

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

CONTACT_PATHS = [
    '/contact', '/contact-us', '/contactus', '/contact.html',
    '/about/contact', '/get-in-touch', '/enquiries',
    '/about', '/about-us', '/',
]

SKIP_PATTERNS = [
    'noreply@', 'no-reply@', 'mailer-daemon@', 'postmaster@',
    'webmaster@', 'test@', 'demo@', 'sentry@', 'wix@',
    '@sentry.io', '@wixpress.com', '@wordpress.com',
    '@example.com', '@test.com', '@squarespace.com', '@shopify.com',
    'email@email', 'your@email', 'name@company', 'info@example',
    '.png', '.jpg', '.gif', '.svg', '.webp', '.css', '.js',
]


def is_real_email(email):
    email_lower = email.lower().strip()
    for pat in SKIP_PATTERNS:
        if pat in email_lower:
            return False
    domain = email_lower.split('@')[1]
    if '.' not in domain or len(domain) < 4:
        return False
    return True


def scrape_emails_from_url(url, timeout=8):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return set()
        emails = set(EMAIL_RE.findall(resp.text))
        soup = BeautifulSoup(resp.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('mailto:'):
                em = href.replace('mailto:', '').split('?')[0].strip()
                if '@' in em:
                    emails.add(em)
        return {e.lower().strip() for e in emails if is_real_email(e)}
    except Exception:
        return set()


def find_emails_for_website(website):
    if not website:
        return []
    if not website.startswith('http'):
        website = 'https://' + website
    from urllib.parse import urlparse
    parsed = urlparse(website)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    domain = parsed.netloc.replace('www.', '')

    all_emails = set()
    for path in CONTACT_PATHS:
        url = base_url + path
        emails = scrape_emails_from_url(url)
        all_emails.update(emails)
        if all_emails:
            break
        time.sleep(0.3)

    same_domain = [e for e in all_emails if domain in e.split('@')[1]]
    return same_domain if same_domain else list(all_emails)


# ═══════════════════════════════════════════
# THOMSON LOCAL
# ═══════════════════════════════════════════

THOMSON_CATEGORIES = [
    'manufacturer', 'factory', 'engineering', 'packaging',
    'printing', 'logistics', 'warehouse', 'construction',
    'metalwork', 'fabrication', 'plastics', 'chemicals',
    'electronics', 'textiles', 'furniture+manufacturer',
    'food+manufacturer', 'industrial+supplies',
    'machine+tools', 'steel', 'electrical+contractor',
    'timber', 'glass+manufacturer', 'paper', 'rubber',
    'concrete', 'aerospace', 'pharmaceutical',
]

THOMSON_CITIES = [
    'london', 'manchester', 'birmingham', 'leeds', 'glasgow',
    'sheffield', 'liverpool', 'bristol', 'edinburgh', 'cardiff',
    'nottingham', 'newcastle', 'leicester', 'coventry', 'derby',
    'southampton', 'reading', 'wolverhampton', 'sunderland',
    'stoke-on-trent', 'aberdeen', 'dundee', 'belfast', 'cambridge',
    'oxford', 'brighton', 'plymouth', 'milton-keynes', 'swindon',
    'luton', 'bolton', 'blackburn', 'stockport', 'middlesbrough',
    'huddersfield', 'halifax', 'wigan', 'rotherham', 'doncaster',
    'wakefield', 'barnsley', 'grimsby', 'scunthorpe', 'ipswich',
    'norwich', 'peterborough', 'gloucester', 'cheltenham', 'exeter',
]


def scrape_thomson(category, city, max_pages=3):
    prospects = []
    for page in range(1, max_pages + 1):
        url = f"https://www.thomsonlocal.com/search/{category}/{city}/page{page}" if page > 1 else \
              f"https://www.thomsonlocal.com/search/{category}/{city}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text, 'html.parser')

            listings = soup.find_all('div', class_='listingDetailsCont')
            if not listings:
                break

            for listing in listings:
                name_tag = listing.find(['h2', 'h3'])
                name = name_tag.get_text(strip=True) if name_tag else None
                if not name:
                    continue

                website = None
                parent = listing.parent or listing
                for a in parent.find_all('a', href=True):
                    txt = a.get_text(strip=True).lower()
                    if txt == 'website':
                        website = a['href']
                        break

                prospects.append({
                    'name': name,
                    'website': website,
                    'source': 'thomson_local',
                    'category': category,
                    'location': city,
                })

            time.sleep(0.5)
        except Exception as e:
            break

    return prospects


# ═══════════════════════════════════════════
# MADE IN BRITAIN
# ═══════════════════════════════════════════

MADE_IN_BRITAIN_SECTORS = [
    'agriculture', 'building-construction', 'carpentryjoinery',
    'chemicals', 'clothing-apparel', 'creative-industries', 'defence',
    'electronics', 'energy', 'engineering', 'environment',
    'fire-safety', 'food-drink', 'garden-landscaping',
    'health-beauty', 'home-living', 'packaging',
    'printing-publishing', 'security', 'software', 'sports-leisure',
]


def scrape_made_in_britain(sector, max_pages=10):
    prospects = []
    for page in range(1, max_pages + 1):
        url = f"https://www.madeinbritain.org/members/sector/{sector}?page={page}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text, 'html.parser')

            cards = soup.find_all('div', class_=lambda c: c and 'card' in c.lower())
            found_any = False
            for card in cards:
                name_tag = card.find(['h2', 'h3', 'h4'])
                if not name_tag:
                    continue
                name = name_tag.get_text(strip=True)
                if not name or name in ('Categories', 'Licence the official Made in Britain trademark'):
                    continue

                link = card.find('a', href=True)
                detail_url = link['href'] if link else None
                if detail_url and not detail_url.startswith('http'):
                    detail_url = 'https://www.madeinbritain.org' + detail_url

                prospects.append({
                    'name': name,
                    'detail_url': detail_url,
                    'source': 'made_in_britain',
                    'category': sector,
                })
                found_any = True

            if not found_any:
                break
            time.sleep(0.5)
        except Exception:
            break

    return prospects


def get_website_from_mib_detail(detail_url):
    try:
        r = requests.get(detail_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            txt = a.get_text(strip=True).lower()
            href = a['href']
            if ('website' in txt or 'visit' in txt) and href.startswith('http'):
                if 'madeinbritain.org' not in href:
                    return href
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http') and 'madeinbritain.org' not in href and \
               'facebook' not in href and 'twitter' not in href and \
               'linkedin' not in href and 'instagram' not in href:
                return href
        return None
    except Exception:
        return None


def enrich_with_emails(prospects, max_workers=8):
    enriched = []
    total = len(prospects)
    print(f"[ENRICH] Scraping contact pages of {total} businesses for real emails...")

    def _process(p):
        website = p.get('website', '')
        if not website and p.get('detail_url'):
            website = get_website_from_mib_detail(p['detail_url'])
            p['website'] = website
        if not website:
            return None
        emails = find_emails_for_website(website)
        if emails:
            p['email'] = emails[0]
            p['email_source'] = 'website_scrape'
            return p
        return None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_process, p): p for p in prospects}
        done = 0
        for future in as_completed(futures):
            done += 1
            result = future.result()
            if result:
                enriched.append(result)
            if done % 25 == 0 or done == total:
                print(f"  [{done}/{total}] Found emails: {len(enriched)}")

    rate = len(enriched) * 100 / max(total, 1)
    print(f"[ENRICH] Found real emails for {len(enriched)}/{total} ({rate:.1f}%)")
    return enriched


def main():
    print("=" * 60)
    print("  MASS PROSPECT FINDER — UK Manufacturers")
    print("=" * 60)

    all_prospects = []
    seen_names = set()

    def _add(prospects):
        added = 0
        for p in prospects:
            key = p['name'].lower().strip()
            if key not in seen_names and len(key) > 2:
                seen_names.add(key)
                all_prospects.append(p)
                added += 1
        return added

    # Phase 1: Thomson Local
    print("\n[PHASE 1] Scraping Thomson Local...")
    total_thomson = 0
    for cat in THOMSON_CATEGORIES:
        cat_count = 0
        for city in THOMSON_CITIES:
            results = scrape_thomson(cat, city, max_pages=2)
            added = _add(results)
            cat_count += added
            total_thomson += added
        if cat_count > 0:
            print(f"  [THOMSON] {cat}: +{cat_count} (total: {total_thomson})")
        time.sleep(0.3)

    print(f"  [THOMSON] Total unique: {total_thomson}")

    # Phase 2: Made in Britain
    print("\n[PHASE 2] Scraping Made in Britain...")
    total_mib = 0
    for sector in MADE_IN_BRITAIN_SECTORS:
        results = scrape_made_in_britain(sector, max_pages=20)
        added = _add(results)
        total_mib += added
        if added > 0:
            print(f"  [MIB] {sector}: +{added} (total: {total_mib})")
        time.sleep(0.3)

    print(f"  [MIB] Total unique: {total_mib}")
    print(f"\n[TOTAL] {len(all_prospects)} unique businesses found")

    # Phase 3: Get emails
    print("\n[PHASE 3] Scraping websites for real email addresses...")
    with_emails = enrich_with_emails(all_prospects, max_workers=8)

    # Phase 4: Verify
    print("\n[PHASE 4] Verifying emails...")
    try:
        from email_verifier import verify_prospect_list, save_verified, save_invalid
        verified, invalid, risky = verify_prospect_list(with_emails, max_workers=5)
        save_verified(verified, risky)
        save_invalid(invalid)
        final_count = len(verified) + len(risky)
    except Exception as e:
        print(f"  [WARN] Verifier error: {e} — saving all scraped emails")
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(with_emails, f, indent=2, ensure_ascii=False)
        final_count = len(with_emails)

    print("\n" + "=" * 60)
    print(f"  DONE — {final_count} VERIFIED prospects ready for outreach")
    print("=" * 60)


if __name__ == '__main__':
    main()
