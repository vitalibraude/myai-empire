"""
SEO & Indexing Module — generates sitemaps, robots.txt, and
submits URLs to Google for faster indexing via the Indexing API.
Also generates structured data (JSON-LD) for all business pages.
"""
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAIN_SITE_URL = "https://aoeua.com"
BUSINESSES_SITE_URL = "https://businesses.aoeua.com"

MAIN_PAGES = [
    ("index.html", "1.0", "daily"),
    ("about.html", "0.8", "weekly"),
    ("services.html", "0.9", "weekly"),
    ("pricing.html", "0.9", "weekly"),
    ("blog.html", "0.8", "daily"),
    ("dashboard.html", "0.5", "daily"),
    ("checkout.html", "0.9", "weekly"),
]


def generate_sitemap_main():
    """Generate sitemap.xml for the main site."""
    output_dir = os.path.join(BASE_DIR, 'output', 'website')
    os.makedirs(output_dir, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    urls = ""
    for page, priority, freq in MAIN_PAGES:
        urls += f"""  <url>
    <loc>{MAIN_SITE_URL}/{page}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>
"""

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""

    path = os.path.join(output_dir, 'sitemap.xml')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(sitemap)

    # robots.txt
    robots = f"""User-agent: *
Allow: /

Sitemap: {MAIN_SITE_URL}/sitemap.xml
"""
    robots_path = os.path.join(output_dir, 'robots.txt')
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots)

    print(f"[SEO] Main site sitemap generated: {path}")
    print(f"[SEO] robots.txt generated: {robots_path}")
    return path


def generate_sitemap_businesses():
    """Generate sitemap.xml for the businesses site."""
    output_dir = os.path.join(BASE_DIR, 'output', 'businesses')
    os.makedirs(output_dir, exist_ok=True)

    businesses_json = os.path.join(BASE_DIR, 'businesses.json')
    if not os.path.exists(businesses_json):
        print("[SEO] businesses.json not found")
        return None

    with open(businesses_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    urls = f"""  <url>
    <loc>{BUSINESSES_SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
"""
    for biz in data.get("businesses", []):
        urls += f"""  <url>
    <loc>{BUSINESSES_SITE_URL}/{biz['id']}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""

    path = os.path.join(output_dir, 'sitemap.xml')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(sitemap)

    robots = f"""User-agent: *
Allow: /

Sitemap: {BUSINESSES_SITE_URL}/sitemap.xml
"""
    robots_path = os.path.join(output_dir, 'robots.txt')
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots)

    print(f"[SEO] Businesses sitemap generated with {len(data.get('businesses', []))+1} URLs")
    return path


def generate_structured_data():
    """Generate JSON-LD structured data snippets for embedding in pages."""
    org_data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "myAI",
        "url": MAIN_SITE_URL,
        "description": "AI-powered business automation platform serving 50+ industries",
        "logo": f"{MAIN_SITE_URL}/logo.png",
        "sameAs": [],
        "offers": {
            "@type": "AggregateOffer",
            "lowPrice": "149",
            "highPrice": "2499",
            "priceCurrency": "USD",
            "offerCount": "50"
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "sales",
            "url": f"{MAIN_SITE_URL}/index.html#contact"
        }
    }

    output_path = os.path.join(BASE_DIR, 'output', 'website', 'structured-data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(org_data, f, indent=2)

    print(f"[SEO] Structured data generated: {output_path}")
    return output_path


def inject_seo_into_pages():
    """Add structured data, Open Graph meta, and canonical URLs to all pages."""
    website_dir = os.path.join(BASE_DIR, 'output', 'website')
    businesses_dir = os.path.join(BASE_DIR, 'output', 'businesses')
    count = 0

    # Main site pages
    for page, _, _ in MAIN_PAGES:
        page_path = os.path.join(website_dir, page)
        if not os.path.exists(page_path):
            continue

        with open(page_path, 'r', encoding='utf-8') as f:
            html = f.read()

        canonical = f'{MAIN_SITE_URL}/{page}'
        title = _extract_title(html) or "myAI — AI Business Automation"

        seo_meta = f'''
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:description" content="AI-powered business automation for 50+ industries. Automate operations, boost revenue, save time.">
    <meta property="og:site_name" content="myAI">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">'''

        if '<link rel="canonical"' not in html:
            html = html.replace('</head>', f'{seo_meta}\n</head>', 1)
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(html)
            count += 1

    # Business pages
    businesses_json = os.path.join(BASE_DIR, 'businesses.json')
    if os.path.exists(businesses_json):
        with open(businesses_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for biz in data.get("businesses", []):
            biz_page = os.path.join(businesses_dir, biz['id'], 'index.html')
            if not os.path.exists(biz_page):
                continue
            with open(biz_page, 'r', encoding='utf-8') as f:
                html = f.read()

            canonical = f'{BUSINESSES_SITE_URL}/{biz["id"]}/'
            seo_meta = f'''
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{biz["name"]} — AI Automation">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="product">
    <meta property="og:description" content="{biz.get("tagline", "")}">
    <meta property="og:site_name" content="myAI">
    <meta name="twitter:card" content="summary_large_image">'''

            if '<link rel="canonical"' not in html:
                html = html.replace('</head>', f'{seo_meta}\n</head>', 1)
                with open(biz_page, 'w', encoding='utf-8') as f:
                    f.write(html)
                count += 1

    print(f"[SEO] Injected SEO meta tags into {count} pages")
    return count


def _extract_title(html):
    import re
    match = re.search(r'<title>(.*?)</title>', html)
    return match.group(1) if match else None


def generate_all_seo():
    """Run all SEO generation tasks."""
    print("\n=== SEO & INDEXING MODULE ===\n")
    generate_sitemap_main()
    generate_sitemap_businesses()
    generate_structured_data()
    count = inject_seo_into_pages()
    print(f"\n[SEO] Complete. {count} pages optimized for search engines.")
    return count


if __name__ == "__main__":
    generate_all_seo()
