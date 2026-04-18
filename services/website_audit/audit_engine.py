"""
AI Website Audit Engine — analyzes any URL and generates a professional PDF report.
This is a REAL service that delivers value customers pay for.
"""
import json
import os
import re
import ssl
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from html.parser import HTMLParser


class HTMLAnalyzer(HTMLParser):
    """Parse HTML and extract SEO/structure data."""
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_desc = ""
        self.h1s = []
        self.h2s = []
        self.h3s = []
        self.images = []
        self.links = []
        self.scripts = []
        self.stylesheets = []
        self.has_viewport = False
        self.has_charset = False
        self.has_og_tags = False
        self.has_twitter_tags = False
        self.has_favicon = False
        self.has_canonical = False
        self.canonical_url = ""
        self.has_structured_data = False
        self.text_content = []
        self._current_tag = ""
        self._in_title = False
        self._in_script = False
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._current_tag = tag

        if tag == "title":
            self._in_title = True
        elif tag == "script":
            self._in_script = True
            src = attrs_dict.get("src", "")
            if src:
                self.scripts.append(src)
            stype = attrs_dict.get("type", "")
            if "json" in stype.lower() and "ld" in stype.lower():
                self.has_structured_data = True
        elif tag == "style":
            self._in_style = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.meta_desc = content
            if name == "viewport":
                self.has_viewport = True
            if attrs_dict.get("charset"):
                self.has_charset = True
            if "http-equiv" in attrs_dict and attrs_dict["http-equiv"].lower() == "content-type":
                self.has_charset = True
            if prop.startswith("og:"):
                self.has_og_tags = True
            if name.startswith("twitter:") or prop.startswith("twitter:"):
                self.has_twitter_tags = True
        elif tag == "link":
            rel = attrs_dict.get("rel", "").lower()
            href = attrs_dict.get("href", "")
            if "icon" in rel or "shortcut" in rel:
                self.has_favicon = True
            if rel == "canonical":
                self.has_canonical = True
                self.canonical_url = href
            if rel == "stylesheet":
                self.stylesheets.append(href)
        elif tag == "h1":
            self.h1s.append("")
        elif tag == "h2":
            self.h2s.append("")
        elif tag == "h3":
            self.h3s.append("")
        elif tag == "img":
            alt = attrs_dict.get("alt", "")
            src = attrs_dict.get("src", "")
            self.images.append({"src": src, "alt": alt})
        elif tag == "a":
            href = attrs_dict.get("href", "")
            self.links.append(href)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self._current_tag == "h1" and self.h1s:
            self.h1s[-1] += data.strip()
        elif self._current_tag == "h2" and self.h2s:
            self.h2s[-1] += data.strip()
        elif self._current_tag == "h3" and self.h3s:
            self.h3s[-1] += data.strip()
        elif not self._in_script and not self._in_style:
            text = data.strip()
            if text:
                self.text_content.append(text)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            self._in_script = False
        elif tag == "style":
            self._in_style = False
        self._current_tag = ""


def fetch_url(url, timeout=15):
    """Fetch URL with timing info."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        "User-Agent": "myAI-WebAudit/1.0 (https://aoeua.com)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    req = urllib.request.Request(url, headers=headers)

    start = datetime.now()
    try:
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        load_time = (datetime.now() - start).total_seconds()
        html = resp.read().decode("utf-8", errors="replace")
        status = resp.status
        final_url = resp.url
        content_type = resp.headers.get("Content-Type", "")
        server = resp.headers.get("Server", "Unknown")
        has_gzip = "gzip" in resp.headers.get("Content-Encoding", "")
        has_hsts = bool(resp.headers.get("Strict-Transport-Security"))
        has_xframe = bool(resp.headers.get("X-Frame-Options"))
        has_xcontent = bool(resp.headers.get("X-Content-Type-Options"))
        return {
            "html": html,
            "status": status,
            "load_time": load_time,
            "final_url": final_url,
            "content_type": content_type,
            "server": server,
            "has_gzip": has_gzip,
            "has_https": final_url.startswith("https"),
            "has_hsts": has_hsts,
            "has_xframe": has_xframe,
            "has_xcontent": has_xcontent,
            "size_kb": len(html) / 1024,
        }
    except urllib.error.HTTPError as e:
        load_time = (datetime.now() - start).total_seconds()
        return {"error": f"HTTP {e.code}", "status": e.code, "load_time": load_time}
    except Exception as e:
        load_time = (datetime.now() - start).total_seconds()
        return {"error": str(e), "status": 0, "load_time": load_time}


def analyze_seo(analyzer, fetch_data, url):
    """Generate SEO score and recommendations."""
    issues = []
    warnings = []
    good = []
    score = 100

    # Title
    title = analyzer.title.strip()
    if not title:
        issues.append("Missing <title> tag — critical for SEO")
        score -= 15
    elif len(title) < 30:
        warnings.append(f"Title too short ({len(title)} chars). Aim for 50-60 chars")
        score -= 5
    elif len(title) > 60:
        warnings.append(f"Title too long ({len(title)} chars). Keep under 60 chars")
        score -= 3
    else:
        good.append(f"Title length is optimal ({len(title)} chars)")

    # Meta description
    if not analyzer.meta_desc:
        issues.append("Missing meta description — hurts click-through rate")
        score -= 10
    elif len(analyzer.meta_desc) < 120:
        warnings.append(f"Meta description too short ({len(analyzer.meta_desc)} chars). Aim for 150-160")
        score -= 3
    elif len(analyzer.meta_desc) > 160:
        warnings.append(f"Meta description too long ({len(analyzer.meta_desc)} chars). Keep under 160")
        score -= 2
    else:
        good.append(f"Meta description length is good ({len(analyzer.meta_desc)} chars)")

    # H1
    if not analyzer.h1s:
        issues.append("No H1 heading found — every page needs one")
        score -= 10
    elif len(analyzer.h1s) > 1:
        warnings.append(f"Multiple H1 tags ({len(analyzer.h1s)}). Best practice: one H1 per page")
        score -= 3
    else:
        good.append("Single H1 tag present")

    # Headings hierarchy
    if analyzer.h2s:
        good.append(f"Uses H2 subheadings ({len(analyzer.h2s)} found)")
    else:
        warnings.append("No H2 headings — add subheadings for better structure")
        score -= 3

    # Images
    imgs_no_alt = [i for i in analyzer.images if not i["alt"]]
    if imgs_no_alt:
        issues.append(f"{len(imgs_no_alt)} of {len(analyzer.images)} images missing alt text")
        score -= min(10, len(imgs_no_alt) * 2)
    elif analyzer.images:
        good.append(f"All {len(analyzer.images)} images have alt text")

    # Mobile
    if analyzer.has_viewport:
        good.append("Viewport meta tag present (mobile-friendly)")
    else:
        issues.append("Missing viewport meta — site won't render properly on mobile")
        score -= 10

    # HTTPS
    if fetch_data.get("has_https"):
        good.append("HTTPS enabled")
    else:
        issues.append("Not using HTTPS — Google penalizes non-secure sites")
        score -= 15

    # Speed
    load_time = fetch_data.get("load_time", 0)
    if load_time < 1.5:
        good.append(f"Fast load time ({load_time:.1f}s)")
    elif load_time < 3:
        warnings.append(f"Moderate load time ({load_time:.1f}s). Aim for under 1.5s")
        score -= 5
    else:
        issues.append(f"Slow load time ({load_time:.1f}s). This hurts rankings and conversions")
        score -= 10

    # Page size
    size_kb = fetch_data.get("size_kb", 0)
    if size_kb > 500:
        warnings.append(f"Large page size ({size_kb:.0f}KB). Consider optimizing")
        score -= 5

    # Social
    if analyzer.has_og_tags:
        good.append("Open Graph tags present (good for social sharing)")
    else:
        warnings.append("Missing Open Graph tags — social shares won't look good")
        score -= 3

    if analyzer.has_twitter_tags:
        good.append("Twitter Card tags present")

    # Technical
    if analyzer.has_canonical:
        good.append("Canonical URL set")
    else:
        warnings.append("No canonical URL — may cause duplicate content issues")
        score -= 3

    if analyzer.has_favicon:
        good.append("Favicon found")
    else:
        warnings.append("No favicon — looks unprofessional in browser tabs")
        score -= 2

    if analyzer.has_structured_data:
        good.append("Structured data (JSON-LD) found")
    else:
        warnings.append("No structured data — add Schema.org markup for rich snippets")
        score -= 3

    # Security headers
    if fetch_data.get("has_hsts"):
        good.append("HSTS header present")
    if fetch_data.get("has_xframe"):
        good.append("X-Frame-Options header present")
    if fetch_data.get("has_xcontent"):
        good.append("X-Content-Type-Options header present")

    security_missing = []
    if not fetch_data.get("has_hsts"):
        security_missing.append("HSTS")
    if not fetch_data.get("has_xframe"):
        security_missing.append("X-Frame-Options")
    if not fetch_data.get("has_xcontent"):
        security_missing.append("X-Content-Type-Options")
    if security_missing:
        warnings.append(f"Missing security headers: {', '.join(security_missing)}")
        score -= 2

    # Content analysis
    word_count = sum(len(t.split()) for t in analyzer.text_content)
    if word_count < 300:
        warnings.append(f"Thin content ({word_count} words). Aim for 800+ words for SEO")
        score -= 5
    elif word_count > 800:
        good.append(f"Good content length ({word_count} words)")

    # Links
    internal = [l for l in analyzer.links if not l.startswith("http") or urllib.parse.urlparse(url).netloc in l]
    external = [l for l in analyzer.links if l.startswith("http") and urllib.parse.urlparse(url).netloc not in l]
    good.append(f"Links: {len(internal)} internal, {len(external)} external")

    score = max(0, min(100, score))

    return {
        "score": score,
        "grade": "A+" if score >= 95 else "A" if score >= 90 else "B+" if score >= 85 else "B" if score >= 80 else "C+" if score >= 75 else "C" if score >= 70 else "D" if score >= 60 else "F",
        "issues": issues,
        "warnings": warnings,
        "good": good,
        "stats": {
            "title": title,
            "title_length": len(title),
            "meta_desc_length": len(analyzer.meta_desc),
            "h1_count": len(analyzer.h1s),
            "h2_count": len(analyzer.h2s),
            "h3_count": len(analyzer.h3s),
            "image_count": len(analyzer.images),
            "images_without_alt": len(imgs_no_alt),
            "word_count": word_count,
            "internal_links": len(internal),
            "external_links": len(external),
            "scripts_count": len(analyzer.scripts),
            "stylesheets_count": len(analyzer.stylesheets),
            "load_time_sec": round(load_time, 2),
            "page_size_kb": round(size_kb, 1),
        }
    }


def run_audit(url):
    """Run complete website audit on given URL."""
    if not url.startswith("http"):
        url = "https://" + url

    print(f"[AUDIT] Fetching {url}...")
    fetch_data = fetch_url(url)
    if "error" in fetch_data and "html" not in fetch_data:
        return {"error": fetch_data["error"], "url": url}

    print("[AUDIT] Analyzing HTML structure...")
    analyzer = HTMLAnalyzer()
    try:
        analyzer.feed(fetch_data["html"])
    except Exception:
        pass

    print("[AUDIT] Running SEO analysis...")
    seo = analyze_seo(analyzer, fetch_data, url)

    report = {
        "url": url,
        "audit_date": datetime.now().isoformat(),
        "overall_score": seo["score"],
        "grade": seo["grade"],
        "seo": seo,
        "performance": {
            "load_time": fetch_data.get("load_time", 0),
            "page_size_kb": fetch_data.get("size_kb", 0),
            "server": fetch_data.get("server", "Unknown"),
            "has_gzip": fetch_data.get("has_gzip", False),
        },
        "security": {
            "https": fetch_data.get("has_https", False),
            "hsts": fetch_data.get("has_hsts", False),
            "xframe": fetch_data.get("has_xframe", False),
            "xcontent_type": fetch_data.get("has_xcontent", False),
        },
        "mobile": {
            "has_viewport": analyzer.has_viewport,
        },
        "social": {
            "og_tags": analyzer.has_og_tags,
            "twitter_tags": analyzer.has_twitter_tags,
        },
    }

    print(f"[AUDIT] Score: {seo['score']}/100 (Grade: {seo['grade']})")
    print(f"[AUDIT] Issues: {len(seo['issues'])}, Warnings: {len(seo['warnings'])}, Good: {len(seo['good'])}")
    return report


def generate_html_report(report, output_path=None):
    """Generate a beautiful HTML audit report."""
    if "error" in report:
        return f"<h1>Audit Failed</h1><p>Error: {report['error']}</p>"

    seo = report["seo"]
    score = report["overall_score"]
    grade = report["grade"]

    color = "#00d4ff" if score >= 80 else "#ffa500" if score >= 60 else "#ff4444"

    issues_html = "".join(f'<li class="issue">{i}</li>' for i in seo["issues"])
    warnings_html = "".join(f'<li class="warning">{w}</li>' for w in seo["warnings"])
    good_html = "".join(f'<li class="good">{g}</li>' for g in seo["good"])

    stats = seo["stats"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Website Audit Report — {report['url']}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Segoe UI',sans-serif; background:#0a0a0a; color:#e0e0e0; padding:2rem; }}
.report {{ max-width:900px; margin:0 auto; }}
.header {{ text-align:center; margin-bottom:3rem; padding:3rem; background:#111; border-radius:20px; border:1px solid #222; }}
.brand {{ font-size:1.2rem; color:#00d4ff; margin-bottom:1rem; }}
.url {{ color:#888; font-size:1rem; word-break:break-all; }}
.score-circle {{ width:160px; height:160px; border-radius:50%; border:6px solid {color};
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  margin:2rem auto; }}
.score-num {{ font-size:3rem; font-weight:800; color:{color}; }}
.score-grade {{ font-size:1.2rem; color:#888; }}
.date {{ color:#555; font-size:0.9rem; margin-top:1rem; }}
.section {{ background:#111; border:1px solid #222; border-radius:16px; padding:2rem; margin-bottom:1.5rem; }}
.section h2 {{ font-size:1.4rem; margin-bottom:1rem; color:#00d4ff; }}
ul {{ list-style:none; }}
li {{ padding:0.6rem 0; border-bottom:1px solid #1a1a1a; padding-left:1.5rem; position:relative; }}
li:last-child {{ border:none; }}
li::before {{ position:absolute; left:0; }}
.issue::before {{ content:"\\2716"; color:#ff4444; }}
.warning::before {{ content:"\\26A0"; color:#ffa500; }}
.good::before {{ content:"\\2714"; color:#00cc66; }}
.stats-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:1rem; }}
.stat {{ background:#0a0a0a; padding:1rem; border-radius:10px; text-align:center; }}
.stat-value {{ font-size:1.8rem; font-weight:700; color:#00d4ff; }}
.stat-label {{ font-size:0.85rem; color:#888; margin-top:0.3rem; }}
.cta {{ text-align:center; margin-top:3rem; padding:3rem; background:linear-gradient(135deg,#111,#1a1a2e);
  border-radius:20px; border:1px solid #222; }}
.cta h2 {{ color:#00d4ff; margin-bottom:1rem; }}
.cta p {{ color:#888; margin-bottom:2rem; }}
.cta a {{ display:inline-block; padding:1rem 3rem; background:linear-gradient(90deg,#00d4ff,#7b2ff7);
  color:#fff; text-decoration:none; border-radius:50px; font-weight:600; font-size:1.1rem; }}
.footer {{ text-align:center; margin-top:2rem; color:#444; font-size:0.85rem; }}
</style>
</head>
<body>
<div class="report">
<div class="header">
  <div class="brand">myAI Website Audit Report</div>
  <div class="score-circle">
    <div class="score-num">{score}</div>
    <div class="score-grade">Grade: {grade}</div>
  </div>
  <div class="url">{report['url']}</div>
  <div class="date">Generated: {report['audit_date'][:10]}</div>
</div>

<div class="section">
<h2>Key Statistics</h2>
<div class="stats-grid">
  <div class="stat"><div class="stat-value">{stats['load_time_sec']}s</div><div class="stat-label">Load Time</div></div>
  <div class="stat"><div class="stat-value">{stats['page_size_kb']}KB</div><div class="stat-label">Page Size</div></div>
  <div class="stat"><div class="stat-value">{stats['word_count']}</div><div class="stat-label">Word Count</div></div>
  <div class="stat"><div class="stat-value">{stats['image_count']}</div><div class="stat-label">Images</div></div>
  <div class="stat"><div class="stat-value">{stats['internal_links']}</div><div class="stat-label">Internal Links</div></div>
  <div class="stat"><div class="stat-value">{stats['external_links']}</div><div class="stat-label">External Links</div></div>
</div>
</div>

{"<div class='section'><h2>Critical Issues (" + str(len(seo['issues'])) + ")</h2><ul>" + issues_html + "</ul></div>" if seo['issues'] else ""}

{"<div class='section'><h2>Warnings (" + str(len(seo['warnings'])) + ")</h2><ul>" + warnings_html + "</ul></div>" if seo['warnings'] else ""}

<div class="section"><h2>What's Working Well ({len(seo['good'])})</h2><ul>{good_html}</ul></div>

<div class="cta">
  <h2>Want Us to Fix These Issues?</h2>
  <p>Our AI-powered service can automatically fix SEO issues, optimize performance, and improve your website's ranking.</p>
  <a href="https://aoeua.com/services.html">Get Professional Fix - Starting at $49</a>
</div>

<div class="footer">
  Powered by myAI | info@aoeua.com | <a href="https://aoeua.com/" style="color:#444;">aoeua.com</a>
</div>
</div>
</body>
</html>"""

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[AUDIT] Report saved to: {output_path}")

    return html


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://aoeua.com/"
    report = run_audit(url)
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output = os.path.join(base, "output", "audits", f"audit_{urllib.parse.urlparse(url).netloc}.html")
    generate_html_report(report, output)
    json_out = os.path.join(base, "output", "audits", f"audit_{urllib.parse.urlparse(url).netloc}.json")
    os.makedirs(os.path.dirname(json_out), exist_ok=True)
    with open(json_out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[AUDIT] JSON saved to: {json_out}")
