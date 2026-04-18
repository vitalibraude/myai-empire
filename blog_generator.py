"""
SEO Blog Content Generator
===========================
Generates SEO-optimized blog posts targeting local business keywords.
Each post is designed to rank for "[service] + [location]" searches
and drives traffic to the free audit tool and paid services.

Generates static HTML blog posts ready for GitHub Pages deployment.
"""
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "output", "website", "blog")


def generate_blog_post(title, keyword, content_sections, meta_desc, slug):
    """Generate a complete SEO-optimized blog post as HTML."""

    sections_html = ""
    for section in content_sections:
        sections_html += f"""
        <h2>{section['heading']}</h2>
        {''.join(f'<p>{p}</p>' for p in section['paragraphs'])}
        """

    # FAQ schema
    faq_items = content_sections[-1].get("faq", []) if content_sections else []
    faq_schema = ""
    faq_html = ""
    if faq_items:
        faq_html = '<h2>Frequently Asked Questions</h2>'
        faq_entries = []
        for faq in faq_items:
            faq_html += f"""
            <div class="faq-item">
            <h3>{faq['q']}</h3>
            <p>{faq['a']}</p>
            </div>
            """
            faq_entries.append(f'{{"@type":"Question","name":"{faq["q"]}","acceptedAnswer":{{"@type":"Answer","text":"{faq["a"]}"}}}}')

        faq_schema = f"""
        <script type="application/ld+json">
        {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(faq_entries)}]}}
        </script>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | myAI Blog</title>
<meta name="description" content="{meta_desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<link rel="canonical" href="https://aoeua.com/blog/{slug}.html">
{faq_schema}
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',-apple-system,sans-serif;background:#0a0a0a;color:#e0e0e0;line-height:1.8}}
.nav{{display:flex;justify-content:space-between;align-items:center;padding:1rem 3rem;background:rgba(10,10,10,.95);border-bottom:1px solid #1a1a1a;position:fixed;top:0;left:0;right:0;z-index:100}}
.nav-brand{{font-size:1.5rem;font-weight:800;background:linear-gradient(90deg,#00d4ff,#7b2ff7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none}}
.nav-links{{display:flex;gap:2rem}}
.nav-links a{{color:#a0a0a0;text-decoration:none}}
article{{max-width:780px;margin:6rem auto 2rem;padding:2rem}}
article h1{{font-size:2.5rem;font-weight:800;margin-bottom:.5rem;line-height:1.2}}
.meta{{color:#888;font-size:.9rem;margin-bottom:2rem;padding-bottom:1rem;border-bottom:1px solid #222}}
article h2{{color:#00d4ff;font-size:1.5rem;margin:2.5rem 0 1rem;padding-bottom:.5rem;border-bottom:1px solid #1a1a1a}}
article h3{{color:#7b2ff7;margin:1.5rem 0 .5rem}}
article p{{color:#ccc;margin-bottom:1rem}}
article ul,article ol{{padding-left:2rem;margin-bottom:1rem;color:#ccc}}
article li{{margin-bottom:.5rem}}
.cta-box{{background:linear-gradient(135deg,#0d1117,#1a1a2e);border:1px solid #222;border-radius:16px;padding:2rem;text-align:center;margin:3rem 0}}
.cta-box h3{{color:#00d4ff;margin-bottom:.5rem;font-size:1.3rem}}
.cta-box p{{color:#888;margin-bottom:1.5rem}}
.cta-btn{{display:inline-block;padding:1rem 2.5rem;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:#fff;text-decoration:none;border-radius:50px;font-weight:700}}
.faq-item{{background:#111;border:1px solid #222;border-radius:12px;padding:1.2rem;margin-bottom:1rem}}
.faq-item h3{{color:#00d4ff;font-size:1rem;margin-bottom:.5rem}}
.faq-item p{{color:#aaa;margin:0}}
.related{{margin:3rem 0;padding:2rem;background:#111;border-radius:16px;border:1px solid #222}}
.related h3{{margin-bottom:1rem}}
.related a{{display:block;color:#00d4ff;text-decoration:none;padding:.5rem 0;border-bottom:1px solid #1a1a1a}}
footer{{text-align:center;padding:2rem;border-top:1px solid #1a1a1a;color:#555;font-size:.85rem;margin-top:2rem}}
footer a{{color:#00d4ff;text-decoration:none}}
</style>
</head>
<body>

<nav class="nav">
<a href="/" class="nav-brand">myAI</a>
<div class="nav-links">
<a href="/free-audit.html">Free Audit</a>
<a href="/prompts.html">Prompts</a>
<a href="/ai-tools.html">AI Tools</a>
<a href="/blog/">Blog</a>
</div>
</nav>

<article>
<h1>{title}</h1>
<div class="meta">Published {datetime.now().strftime('%B %d, %Y')} · by myAI · 8 min read</div>

{sections_html}

{faq_html}

<div class="cta-box">
<h3>Get Your Free Website Audit</h3>
<p>Find out your website's score in 30 seconds. AI-powered, instant results.</p>
<a href="/free-audit.html" class="cta-btn">Audit My Website — Free</a>
</div>

</article>

<footer>
<p>© 2025 <a href="https://aoeua.com">myAI</a> · <a href="mailto:info@aoeua.com">info@aoeua.com</a></p>
</footer>

</body>
</html>"""

    return html


def create_blog_posts():
    """Generate a set of SEO blog posts targeting valuable keywords."""
    os.makedirs(BLOG_DIR, exist_ok=True)

    posts = [
        {
            "title": "10 SEO Mistakes Small Businesses Make (And How to Fix Them)",
            "keyword": "small business SEO mistakes",
            "meta_desc": "Discover the top 10 SEO mistakes costing small businesses customers. Free fixes you can implement today to boost your Google rankings.",
            "slug": "seo-mistakes-small-businesses",
            "sections": [
                {"heading": "Why SEO Matters for Small Businesses",
                 "paragraphs": [
                     "In 2025, 97% of consumers search online before visiting a local business. If your website isn't optimised for search engines, you're invisible to potential customers.",
                     "The good news? Most SEO mistakes are easy to fix. Here are the 10 most common ones we see when auditing small business websites."
                 ]},
                {"heading": "1. Missing or Duplicate Title Tags",
                 "paragraphs": [
                     "Your title tag is the single most important on-page SEO element. It's what shows up in Google search results as the blue clickable link.",
                     "We see countless small business websites with generic titles like 'Home' or duplicate titles across every page. Each page should have a unique, keyword-rich title under 60 characters."
                 ]},
                {"heading": "2. No Meta Descriptions",
                 "paragraphs": [
                     "Meta descriptions don't directly affect rankings, but they massively impact click-through rates. A compelling 155-character description can double your clicks from search results.",
                     "Write a unique meta description for every important page. Include your target keyword and a clear call-to-action."
                 ]},
                {"heading": "3. Slow Page Load Speed",
                 "paragraphs": [
                     "Google has confirmed that page speed is a ranking factor. Pages that take more than 3 seconds to load lose 53% of mobile visitors.",
                     "The most common causes? Uncompressed images, too many plugins, and no caching. A simple image compression can improve load times by 50% or more."
                 ]},
                {"heading": "4. Not Mobile-Friendly",
                 "paragraphs": [
                     "Over 60% of searches happen on mobile devices. Google uses mobile-first indexing, meaning it primarily uses the mobile version of your site for ranking.",
                     "If your site isn't responsive, you're hurting your rankings AND losing customers. Test your site with Google's Mobile-Friendly Test tool."
                 ]},
                {"heading": "5. No Google Business Profile",
                 "paragraphs": [
                     "If you're a local business without a Google Business Profile, you're missing out on the #1 source of local leads. GBP listings appear above organic results for local searches.",
                     "Claim your profile, add photos, keep your hours updated, and encourage reviews. Businesses with 10+ reviews get 3x more clicks."
                 ]},
                {"heading": "6. Ignoring Local Keywords",
                 "paragraphs": [
                     "Targeting 'plumber' is nearly impossible. Targeting 'emergency plumber in Bristol' is achievable and more valuable.",
                     "Add your city, neighbourhood, and service area to your page titles, headings, content, and meta descriptions. Local keywords are less competitive and convert better."
                 ]},
                {"heading": "7. No Internal Linking Strategy",
                 "paragraphs": [
                     "Internal links help Google understand your site structure and distribute authority between pages. Most small business websites have zero internal linking strategy.",
                     "Link from your blog posts to your service pages. Link from your homepage to your most important pages. Use descriptive anchor text, not 'click here'."
                 ]},
                {"heading": "8. Thin Content",
                 "paragraphs": [
                     "Pages with fewer than 300 words rarely rank. Google wants to see comprehensive, helpful content that answers the searcher's question.",
                     "Your service pages should have at least 500 words describing what you do, who you serve, and why you're the best choice. Include FAQs, testimonials, and case studies."
                 ]},
                {"heading": "9. No SSL Certificate (HTTPS)",
                 "paragraphs": [
                     "Google has flagged non-HTTPS sites as 'Not Secure' since 2018. If your URL starts with http:// instead of https://, visitors see a warning and many leave immediately.",
                     "Most hosting providers offer free SSL certificates. There's no excuse not to have one in 2025."
                 ]},
                {"heading": "10. Not Tracking Results",
                 "paragraphs": [
                     "You can't improve what you don't measure. Yet many small businesses don't have Google Analytics or Google Search Console set up.",
                     "These free tools tell you how people find your site, which pages perform best, and where you're losing visitors. Set them up today — it takes 10 minutes."
                 ],
                 "faq": [
                     {"q": "How long does SEO take to work?", "a": "Most businesses see initial improvements within 3-6 months. Competitive keywords may take 6-12 months. Local SEO improvements can show results within weeks."},
                     {"q": "How much does SEO cost for a small business?", "a": "DIY SEO is free but time-consuming. Professional SEO services typically range from £300-£2000 per month. A one-time audit and fix can cost £49-£500."},
                     {"q": "Can I do SEO myself?", "a": "Absolutely. Start with the basics: title tags, meta descriptions, page speed, and Google Business Profile. Use free tools like Google Search Console. For more advanced work, consider professional help."},
                     {"q": "What's the most important SEO factor?", "a": "For local businesses, Google Business Profile is the #1 factor for local pack rankings. For organic rankings, high-quality content and relevant backlinks are most important."},
                     {"q": "How do I check my website's SEO score?", "a": "Use our free AI-powered audit tool at aoeua.com/free-audit.html. It checks SEO, speed, mobile, security, and accessibility in 30 seconds."},
                 ]},
            ]
        },
        {
            "title": "How to Get More Customers from Google (Without Paying for Ads)",
            "keyword": "get more customers from Google",
            "meta_desc": "7 proven strategies to get more customers from Google search without spending on ads. Local SEO, content marketing & more.",
            "slug": "get-more-customers-google",
            "sections": [
                {"heading": "Why Google Is Your Best Salesperson",
                 "paragraphs": [
                     "Every day, millions of people search Google for local services. 'Dentist near me', 'best plumber in Manchester', 'emergency electrician London'. These aren't just searches — they're buying signals.",
                     "The businesses that appear at the top of these searches get the calls. The ones on page 2? They might as well not exist. Here's how to get to the top without spending a penny on ads."
                 ]},
                {"heading": "1. Claim and Optimise Your Google Business Profile",
                 "paragraphs": [
                     "This is the single highest-ROI activity for any local business. Your Google Business Profile (formerly Google My Business) appears in the map pack above organic results.",
                     "Complete every field: business name, address, phone, website, hours, categories, attributes. Add at least 10 photos. Write a compelling description with your key services and locations."
                 ]},
                {"heading": "2. Get More Google Reviews",
                 "paragraphs": [
                     "Businesses with more positive reviews rank higher and get more clicks. It's that simple. Aim for 10+ reviews to stand out, 50+ to dominate.",
                     "Ask every happy customer for a review. Send them a direct link to your Google review page. Time it right — ask right after you've delivered great service."
                 ]},
                {"heading": "3. Create Location-Specific Pages",
                 "paragraphs": [
                     "If you serve multiple areas, create a separate page for each one. 'Emergency Plumber in Bristol', 'Emergency Plumber in Bath', etc.",
                     "Each page should have unique content about that location. Mention local landmarks, common issues in that area, and your experience serving those customers."
                 ]},
                {"heading": "4. Start a Blog That Answers Customer Questions",
                 "paragraphs": [
                     "Every question your customers ask is a potential blog post. 'How much does a boiler replacement cost?', 'How often should I visit the dentist?', 'What to look for in a wedding photographer?'",
                     "These informational searches bring people to your site. Once there, they discover your services. Write one helpful blog post per week and you'll see traffic grow within 3 months."
                 ]},
                {"heading": "5. Fix Technical SEO Issues",
                 "paragraphs": [
                     "Slow load times, broken links, missing title tags, no SSL — these technical issues hold your site back. The good news? Most are easy to fix.",
                     "Run our free audit at aoeua.com/free-audit.html to find your specific issues. Fix the critical ones first and you'll see improvements within weeks."
                 ]},
                {"heading": "6. Build Local Backlinks",
                 "paragraphs": [
                     "Backlinks from other websites tell Google you're trustworthy. For local businesses, the best backlinks come from: local directories, trade associations, local news sites, and partner businesses.",
                     "Start by listing your business on Yell.com, Thomson Local, and industry-specific directories. Join your local Chamber of Commerce. Sponsor a local event."
                 ]},
                {"heading": "7. Track and Improve",
                 "paragraphs": [
                     "Set up Google Search Console (free) to see which keywords bring people to your site. Set up Google Analytics (free) to see how visitors behave once they arrive.",
                     "Review your data monthly. Double down on what's working. Fix what isn't. SEO is a marathon, not a sprint — but it compounds over time.",
                 ],
                 "faq": [
                     {"q": "How long until I see results from SEO?", "a": "Google Business Profile optimizations can show results within weeks. Blog content typically takes 3-6 months to rank. Technical fixes can improve rankings within days."},
                     {"q": "Is SEO better than Google Ads?", "a": "Both have their place. SEO is free and compounds over time but takes longer. Google Ads gives immediate results but stops when you stop paying. The best strategy uses both."},
                     {"q": "How many reviews do I need?", "a": "Aim for at least 10 reviews to appear credible. 30-50 reviews significantly improves your visibility. Consistency matters more than volume — aim for 2-3 new reviews per month."},
                 ]},
            ]
        },
        {
            "title": "Website Audit Checklist: 25 Things to Check Before Your Site Goes Live",
            "keyword": "website audit checklist",
            "meta_desc": "Complete 25-point website audit checklist covering SEO, speed, security, mobile & accessibility. Free downloadable checklist.",
            "slug": "website-audit-checklist",
            "sections": [
                {"heading": "Why Every Website Needs an Audit",
                 "paragraphs": [
                     "Your website is your 24/7 salesperson. If it's slow, broken, or invisible to search engines, you're leaving money on the table every single day.",
                     "This checklist covers everything we check in our professional audits. Use it yourself for free, or let us handle it for you."
                 ]},
                {"heading": "SEO Checks (1-8)",
                 "paragraphs": [
                     "1. ✅ Unique title tag on every page (under 60 characters, keyword included)",
                     "2. ✅ Meta description on every page (150-155 characters, compelling CTA)",
                     "3. ✅ H1 heading on every page (one per page, includes primary keyword)",
                     "4. ✅ Image alt text on all images (descriptive, includes keywords where natural)",
                     "5. ✅ XML sitemap created and submitted to Google Search Console",
                     "6. ✅ Robots.txt file is present and not blocking important pages",
                     "7. ✅ Internal links connect your most important pages",
                     "8. ✅ No broken links (404 errors) on the site",
                 ]},
                {"heading": "Speed Checks (9-14)",
                 "paragraphs": [
                     "9. ✅ Page load time under 3 seconds (test with PageSpeed Insights)",
                     "10. ✅ Images are compressed and served in modern formats (WebP)",
                     "11. ✅ Browser caching is enabled",
                     "12. ✅ CSS and JavaScript files are minified",
                     "13. ✅ Lazy loading is enabled for below-the-fold images",
                     "14. ✅ Core Web Vitals pass (LCP < 2.5s, FID < 100ms, CLS < 0.1)",
                 ]},
                {"heading": "Security Checks (15-18)",
                 "paragraphs": [
                     "15. ✅ SSL certificate installed (HTTPS, not HTTP)",
                     "16. ✅ HTTP redirects to HTTPS automatically",
                     "17. ✅ No mixed content warnings (HTTP resources on HTTPS pages)",
                     "18. ✅ Security headers present (X-Frame-Options, CSP, HSTS)",
                 ]},
                {"heading": "Mobile Checks (19-22)",
                 "paragraphs": [
                     "19. ✅ Responsive design works on all screen sizes",
                     "20. ✅ Text is readable without zooming (minimum 16px font)",
                     "21. ✅ Tap targets are large enough (minimum 48x48px)",
                     "22. ✅ No horizontal scrolling on mobile",
                 ]},
                {"heading": "Accessibility & UX Checks (23-25)",
                 "paragraphs": [
                     "23. ✅ Contact information is easy to find (header or footer)",
                     "24. ✅ Clear call-to-action on every page",
                     "25. ✅ Forms work correctly and have validation",
                 ],
                 "faq": [
                     {"q": "How often should I audit my website?", "a": "We recommend a full audit every 3-6 months, or after any major website changes. Use our free tool for quick checks anytime."},
                     {"q": "What's a good website audit score?", "a": "80+ is good, 90+ is excellent. Most small business websites score between 40-70. Even improving from 50 to 70 can significantly boost your traffic."},
                     {"q": "Can I fix these issues myself?", "a": "Many issues like meta descriptions and image compression can be fixed with basic skills. For technical issues like security headers and Core Web Vitals, you may want professional help."},
                 ]},
            ]
        },
    ]

    generated = []
    for post in posts:
        html = generate_blog_post(
            title=post["title"],
            keyword=post["keyword"],
            content_sections=post["sections"],
            meta_desc=post["meta_desc"],
            slug=post["slug"]
        )
        filepath = os.path.join(BLOG_DIR, f'{post["slug"]}.html')
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        generated.append(post["slug"])
        print(f"  ✅ Generated: blog/{post['slug']}.html")

    # Create blog index page
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog — Free SEO Tips & Business Growth Guides | myAI</title>
<meta name="description" content="Free SEO tips, website optimization guides, and business growth strategies for UK small businesses.">
<link rel="canonical" href="https://aoeua.com/blog/">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',sans-serif;background:#0a0a0a;color:#e0e0e0;min-height:100vh}
.nav{display:flex;justify-content:space-between;align-items:center;padding:1rem 3rem;background:rgba(10,10,10,.95);border-bottom:1px solid #1a1a1a;position:fixed;top:0;left:0;right:0;z-index:100}
.nav-brand{font-size:1.5rem;font-weight:800;background:linear-gradient(90deg,#00d4ff,#7b2ff7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none}
.nav-links{display:flex;gap:2rem}
.nav-links a{color:#a0a0a0;text-decoration:none}
.hero{text-align:center;padding:7rem 2rem 3rem;max-width:800px;margin:0 auto}
.hero h1{font-size:3rem;font-weight:800;margin-bottom:1rem}
.hero h1 span{background:linear-gradient(90deg,#00d4ff,#7b2ff7);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{color:#888;font-size:1.2rem}
.posts{max-width:800px;margin:2rem auto;padding:0 2rem}
.post-card{background:#111;border:1px solid #222;border-radius:16px;padding:2rem;margin-bottom:1.5rem;transition:transform .3s,border-color .3s}
.post-card:hover{transform:translateY(-3px);border-color:#00d4ff40}
.post-card h2{margin-bottom:.5rem}
.post-card h2 a{color:#fff;text-decoration:none}
.post-card h2 a:hover{color:#00d4ff}
.post-card .meta{color:#888;font-size:.85rem;margin-bottom:1rem}
.post-card p{color:#aaa;line-height:1.6}
.post-card .read-more{display:inline-block;margin-top:1rem;color:#00d4ff;text-decoration:none;font-weight:600}
footer{text-align:center;padding:2rem;border-top:1px solid #1a1a1a;color:#555;font-size:.85rem;margin-top:3rem}
footer a{color:#00d4ff;text-decoration:none}
</style>
</head>
<body>
<nav class="nav">
<a href="/" class="nav-brand">myAI</a>
<div class="nav-links">
<a href="/free-audit.html">Free Audit</a>
<a href="/prompts.html">Prompts</a>
<a href="/ai-tools.html">AI Tools</a>
<a href="/blog/">Blog</a>
</div>
</nav>

<section class="hero">
<h1>The myAI <span>Blog</span></h1>
<p>Free SEO tips, website optimization guides, and business growth strategies.</p>
</section>

<div class="posts">
"""

    for post in posts:
        index_html += f"""
<div class="post-card">
<h2><a href="/blog/{post['slug']}.html">{post['title']}</a></h2>
<div class="meta">{datetime.now().strftime('%B %d, %Y')} · 8 min read</div>
<p>{post['meta_desc']}</p>
<a href="/blog/{post['slug']}.html" class="read-more">Read more →</a>
</div>
"""

    index_html += """
</div>

<footer>
<p>© 2025 <a href="https://aoeua.com">myAI</a> · <a href="mailto:info@aoeua.com">info@aoeua.com</a></p>
</footer>
</body>
</html>"""

    index_path = os.path.join(BLOG_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  ✅ Generated: blog/index.html")

    return generated


if __name__ == "__main__":
    print("=" * 60)
    print("  SEO BLOG CONTENT GENERATOR")
    print("=" * 60)
    posts = create_blog_posts()
    print(f"\n  Generated {len(posts)} blog posts + index page")
    print("  Deploy to GitHub Pages to go live.")
