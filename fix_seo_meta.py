"""
Batch SEO fixer: adds missing meta tags, OG tags, canonical URLs,
favicon, and JSON-LD structured data to all HTML pages.
"""
import os
import re

DOMAIN = "https://aoeua.com"
SITE_NAME = "myAI"
SITE_DESC = "AI-powered business automation platform — autonomous AI that runs your business."
FAVICON_SVG = "/favicon.svg"
OG_IMAGE = f"{DOMAIN}/favicon.svg"

# Page-specific metadata
PAGE_META = {
    "index.html": {
        "description": "A fully autonomous AI-powered platform that builds, markets, and scales digital businesses — without human intervention.",
        "og_type": "website",
        "jsonld_type": None  # already has it
    },
    "about.html": {
        "description": "Learn about myAI — the autonomous AI platform helping businesses automate marketing, sales, and operations.",
        "og_type": "website",
    },
    "ai-tools.html": {
        "description": "300+ curated AI tools for marketing, sales, content, design, automation and more. Updated weekly. Free access.",
        "og_type": "website",
    },
    "services.html": {
        "description": "Professional AI-powered business services — website audits, SEO optimization, landing pages, and full automation packages.",
        "og_type": "website",
    },
    "pricing.html": {
        "description": "Simple, transparent pricing for AI business automation. Plans from $399/month. Enterprise solutions available.",
        "og_type": "website",
    },
    "prompts.html": {
        "description": "500+ ready-to-use AI prompts for marketing, sales, SEO, content, email, social media and more. Copy, paste, profit.",
        "og_type": "product",
    },
    "investors.html": {
        "description": "Invest in myAI — the autonomous business platform scaling AI automation across 50+ industries.",
        "og_type": "website",
    },
    "enterprise-services.html": {
        "description": "Expert implementation of SAP Business One, Priority ERP, Monday.com, SharePoint, Microsoft 365 and Azure for UK manufacturers.",
        "og_type": "website",
        "jsonld_type": None  # already has FAQ
    },
    "dashboard.html": {
        "description": "myAI Empire Dashboard — manage your AI-powered business automation in one place.",
        "og_type": "website",
        "noindex": True
    },
    "guide.html": {
        "description": "AI Business Automation Guide — 10 chapters, real tools, step-by-step instructions to automate your business.",
        "og_type": "product",
    },
    "book-consultation.html": {
        "description": "Book a 1-on-1 AI automation consultation. We analyse your business and build a custom automation plan to save 20+ hours/week.",
        "og_type": "website",
    },
    "checkout.html": {
        "description": "Secure checkout — myAI business automation services.",
        "og_type": "website",
        "noindex": True
    },
    "checkout-success.html": {
        "description": "Thank you for your purchase — welcome to myAI.",
        "og_type": "website",
        "noindex": True
    },
    "free-audit.html": {
        "description": "Get a free, instant AI-powered website audit. Check your SEO score, speed, security and mobile readiness in 30 seconds.",
        "og_type": "website",
    },
    "free-course.html": {
        "description": "Free 5-day website growth course. Get more customers from your website with actionable daily tips. No spam.",
        "og_type": "website",
    },
    "prompt-pack.html": {
        "description": "Your AI Business Prompts download — 500+ prompts ready to use.",
        "og_type": "website",
        "noindex": True
    },
    "roi-calculator.html": {
        "description": "Free ROI calculator. Find out how much revenue you're losing from website issues and how much a professional audit could save.",
        "og_type": "website",
    },
    "results.html": {
        "description": "Real results from real businesses. See how UK small businesses improved their websites and got more customers with myAI.",
        "og_type": "website",
    },
    "order.html": {
        "description": "AI website services — SEO fix from $49, speed optimization from $99, custom landing pages from $149. Results guaranteed.",
        "og_type": "website",
    },
    "order-audit.html": {
        "description": "Professional 20-page SEO audit report with actionable fixes, competitor analysis, and priority roadmap. Delivered in 24 hours.",
        "og_type": "product",
    },
    "thank-you.html": {
        "description": "Thank you — your request has been received. We'll be in touch shortly.",
        "og_type": "website",
        "noindex": True
    },
    "website-audit.html": {
        "description": "Free instant website audit — find out why your website isn't ranking on Google. Takes 30 seconds, no signup required.",
        "og_type": "website",
    },
    "blog.html": {
        "description": "myAI blog — AI automation tips, SEO strategies, and business growth insights for small business owners.",
        "og_type": "website",
    },
    "guide-access.html": {
        "description": "AI Business Automation Guide — full access for customers.",
        "og_type": "website",
        "noindex": True
    },
    "accessibility.html": {
        "description": "myAI accessibility statement — our commitment to making AI automation accessible to everyone.",
        "og_type": "website",
    },
}


def get_title(html):
    """Extract existing title from HTML."""
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    return m.group(1).strip() if m else SITE_NAME


def has_tag(html, tag_pattern):
    """Check if HTML already has a specific meta tag."""
    return bool(re.search(tag_pattern, html, re.IGNORECASE))


def build_meta_block(filename, html):
    """Build missing meta tags to inject into <head>."""
    meta = PAGE_META.get(filename, {
        "description": SITE_DESC,
        "og_type": "website",
    })
    
    title = get_title(html)
    desc = meta.get("description", SITE_DESC)
    canonical = f"{DOMAIN}/{filename}"
    noindex = meta.get("noindex", False)
    og_type = meta.get("og_type", "website")
    
    tags = []
    
    # Favicon
    if not has_tag(html, r'rel="icon".*?favicon\.svg') and 'favicon.svg' not in html:
        tags.append(f'    <link rel="icon" type="image/svg+xml" href="{FAVICON_SVG}">')
    
    # Meta description
    if not has_tag(html, r'name="description"'):
        tags.append(f'    <meta name="description" content="{desc}">')
    
    # Canonical
    if not has_tag(html, r'rel="canonical"'):
        tags.append(f'    <link rel="canonical" href="{canonical}">')
    
    # Noindex
    if noindex and not has_tag(html, r'name="robots"'):
        tags.append('    <meta name="robots" content="noindex, nofollow">')
    
    # Open Graph
    if not has_tag(html, r'property="og:title"'):
        tags.append(f'    <meta property="og:title" content="{title}">')
    if not has_tag(html, r'property="og:description"'):
        tags.append(f'    <meta property="og:description" content="{desc}">')
    if not has_tag(html, r'property="og:url"'):
        tags.append(f'    <meta property="og:url" content="{canonical}">')
    if not has_tag(html, r'property="og:type"'):
        tags.append(f'    <meta property="og:type" content="{og_type}">')
    if not has_tag(html, r'property="og:site_name"'):
        tags.append(f'    <meta property="og:site_name" content="{SITE_NAME}">')
    if not has_tag(html, r'property="og:image"'):
        tags.append(f'    <meta property="og:image" content="{OG_IMAGE}">')
    
    # Twitter Card
    if not has_tag(html, r'name="twitter:card"'):
        tags.append('    <meta name="twitter:card" content="summary_large_image">')
    if not has_tag(html, r'name="twitter:title"'):
        tags.append(f'    <meta name="twitter:title" content="{title}">')
    if not has_tag(html, r'name="twitter:description"'):
        tags.append(f'    <meta name="twitter:description" content="{desc}">')
    if not has_tag(html, r'name="twitter:image"'):
        tags.append(f'    <meta name="twitter:image" content="{OG_IMAGE}">')
    
    # Theme color
    if not has_tag(html, r'name="theme-color"'):
        tags.append('    <meta name="theme-color" content="#0a0a0a">')
    
    return "\n".join(tags)


def build_jsonld(filename, html):
    """Build JSON-LD structured data for pages that don't have it."""
    meta = PAGE_META.get(filename, {})
    
    # Skip if already has JSON-LD or explicitly marked
    if 'application/ld+json' in html:
        return ""
    if meta.get("jsonld_type") is None and filename in PAGE_META and "jsonld_type" in meta:
        return ""
    if meta.get("noindex"):
        return ""
    
    title = get_title(html)
    desc = meta.get("description", SITE_DESC)
    canonical = f"{DOMAIN}/{filename}"
    
    jsonld = f'''    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "{title}",
      "description": "{desc}",
      "url": "{canonical}",
      "isPartOf": {{
        "@type": "WebSite",
        "name": "{SITE_NAME}",
        "url": "{DOMAIN}"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "{SITE_NAME}",
        "url": "{DOMAIN}",
        "logo": {{
          "@type": "ImageObject",
          "url": "{DOMAIN}/favicon.svg"
        }}
      }}
    }}
    </script>'''
    
    return jsonld


def fix_broken_favicon(html):
    """Fix empty favicon href references."""
    # Fix empty favicon href
    html = re.sub(
        r'<link\s+rel="icon"\s+id="dynFavicon"\s+type="image/png"\s+href="">',
        f'<link rel="icon" type="image/svg+xml" href="{FAVICON_SVG}">',
        html
    )
    return html


def process_file(filepath, filename):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # Fix broken favicons first
    html = fix_broken_favicon(html)
    
    # Build meta tags
    meta_block = build_meta_block(filename, html)
    jsonld_block = build_jsonld(filename, html)
    
    injection = ""
    if meta_block:
        injection += meta_block + "\n"
    if jsonld_block:
        injection += jsonld_block + "\n"
    
    if injection:
        # Inject right before </head>
        html = html.replace("</head>", injection + "</head>", 1)
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    
    # Process root HTML files
    count = 0
    for filename in sorted(os.listdir(root)):
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            if process_file(filepath, filename):
                print(f"  [FIXED] {filename}")
                count += 1
            else:
                print(f"  [OK]    {filename}")
    
    # Process blog HTML files
    blog_dir = os.path.join(root, "blog")
    if os.path.exists(blog_dir):
        for filename in sorted(os.listdir(blog_dir)):
            if filename.endswith('.html') and filename != 'index.html':
                filepath = os.path.join(blog_dir, filename)
                if process_file(filepath, f"blog/{filename}"):
                    print(f"  [FIXED] blog/{filename}")
                    count += 1
                else:
                    print(f"  [OK]    blog/{filename}")
    
    print(f"\nDone! Fixed {count} files.")


if __name__ == "__main__":
    main()
