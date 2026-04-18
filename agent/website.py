import os
import json
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'website')


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════
# SHARED COMPONENTS
# ═══════════════════════════════════════════════════

SHARED_NAV = """
    <nav class="main-nav">
        <div class="nav-brand">&#x1F916; myAI</div>
        <div class="nav-links">
            <a href="index.html">Home</a>
            <a href="about.html">About</a>
            <a href="services.html">Services</a>
            <a href="pricing.html">Pricing</a>
            <a href="blog.html">Blog</a>
            <a href="https://businesses.aoeua.com/">50 Businesses</a>
            <a href="dashboard.html">Dashboard</a>
            <a href="index.html#contact">Contact</a>
        </div>
        <a href="index.html#contact" class="nav-cta">Get Started</a>
    </nav>
"""

SHARED_NAV_CSS = """
        .main-nav {
            position: fixed; top: 0; left: 0; right: 0;
            display: flex; justify-content: space-between; align-items: center;
            padding: 1rem 3rem;
            background: rgba(10,10,10,0.92);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid #1a1a1a;
            z-index: 1000;
        }
        .nav-brand {
            font-size: 1.5rem; font-weight: 800;
            background: linear-gradient(90deg,#00d4ff,#7b2ff7);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a {
            color: #a0a0a0; text-decoration: none; font-size: 0.95rem;
            transition: color 0.3s;
        }
        .nav-links a:hover { color: #00d4ff; }
        .nav-cta {
            padding: 0.5rem 1.5rem; border-radius: 50px; font-size: 0.9rem;
            background: linear-gradient(90deg,#00d4ff,#7b2ff7);
            color: white; text-decoration: none; font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .nav-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,212,255,0.3);
        }
"""

SHARED_FOOTER_CSS = """
        footer {
            text-align: center; padding: 3rem 2rem; color: #555; font-size: 0.9rem;
            border-top: 1px solid #1a1a1a; background: #0a0a0a;
        }
        footer a { color: #00d4ff; text-decoration: none; }
"""

BASE_CSS = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            background: #0a0a0a; color: #e0e0e0; line-height: 1.7;
        }
        .cta-button {
            display: inline-block; padding: 1rem 3rem; font-size: 1.15rem;
            border: none; border-radius: 50px;
            background: linear-gradient(90deg,#00d4ff,#7b2ff7);
            color: white; cursor: pointer; text-decoration: none; font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,212,255,0.3);
        }
        .cta-secondary {
            display: inline-block; padding: 1rem 3rem; font-size: 1.15rem;
            border: 2px solid #333; border-radius: 50px;
            background: transparent; color: #a0a0a0; cursor: pointer;
            text-decoration: none; transition: all 0.3s;
        }
        .cta-secondary:hover { border-color: #00d4ff; color: #00d4ff; }
        .section-title {
            text-align: center; font-size: 2.5rem; margin-bottom: 0.5rem; color: #00d4ff;
        }
        .section-subtitle {
            text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 3rem;
        }
        .animate-on-scroll {
            opacity: 0; transform: translateY(30px);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }
        .animate-on-scroll.visible { opacity: 1; transform: translateY(0); }
"""


def _footer(year):
    return f"""
    <footer>
        <div style="max-width:900px;margin:0 auto;">
            <p style="margin-bottom:1rem;">&#x1F916; <strong>myAI</strong> — Autonomous AI That Runs Your Business</p>
            <p>
                <a href="index.html">Home</a> &middot;
                <a href="about.html">About</a> &middot;
                <a href="services.html">Services</a> &middot;
                <a href="pricing.html">Pricing</a> &middot;
                <a href="blog.html">Blog</a> &middot;
                <a href="index.html#contact">Contact</a>
            </p>
            <p style="margin-top:1.5rem;">&copy; {year} myAI Inc. All rights reserved. Built autonomously by AI.</p>
        </div>
    </footer>
"""


SCROLL_JS = """
    <script>
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); });
        }, { threshold: 0.1 });
        document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
    </script>
"""


# ═══════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════

def generate_landing_page(config):
    ensure_output_dir()
    title = config.get("website", {}).get("title", "myAI")
    biz = config.get("business", {}).get("name", "myAI")
    tagline = config.get("business", {}).get("tagline", "")
    desc = config.get("business", {}).get("description", "")
    year = datetime.now().year

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
    <title>{title}</title>
    <style>
        {BASE_CSS}
        {SHARED_NAV_CSS}

        @keyframes pulse {{ 0%,100%{{transform:scale(1);opacity:.5}} 50%{{transform:scale(1.1);opacity:1}} }}
        @keyframes fadeInUp {{ from{{opacity:0;transform:translateY(40px)}} to{{opacity:1;transform:translateY(0)}} }}
        @keyframes float {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-12px)}} }}
        @keyframes glow {{ 0%,100%{{box-shadow:0 0 20px rgba(0,212,255,.1)}} 50%{{box-shadow:0 0 40px rgba(123,47,247,.3)}} }}

        #particles {{
            position:fixed; top:0; left:0; width:100%; height:100%;
            pointer-events:none; z-index:0;
        }}

        .hero {{
            min-height:100vh; display:flex; flex-direction:column;
            justify-content:center; align-items:center; text-align:center;
            padding:7rem 2rem 3rem;
            background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);
            position:relative; overflow:hidden;
        }}
        .hero::before {{
            content:''; position:absolute; top:-50%; left:-50%;
            width:200%; height:200%;
            background:radial-gradient(circle,rgba(0,212,255,.05) 0%,transparent 50%);
            animation:pulse 8s ease-in-out infinite;
        }}
        .hero h1 {{
            font-size:4.5rem; font-weight:900;
            background:linear-gradient(90deg,#00d4ff,#7b2ff7,#ff6b6b);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text; margin-bottom:.5rem;
            position:relative; z-index:1;
            animation:fadeInUp 1s ease-out;
        }}
        .hero .tagline {{
            font-size:1.6rem; color:#c0c0c0; max-width:700px;
            margin-bottom:.5rem; position:relative; z-index:1;
            animation:fadeInUp 1s ease-out .2s both;
        }}
        .hero .desc {{
            font-size:1.15rem; color:#888; max-width:600px;
            margin-bottom:2rem; position:relative; z-index:1;
            animation:fadeInUp 1s ease-out .4s both;
        }}
        .stats-bar {{
            display:flex; gap:4rem; margin:2rem 0;
            position:relative; z-index:1;
            animation:fadeInUp 1s ease-out .5s both;
        }}
        .stat-item {{ text-align:center; }}
        .stat-item .number {{ font-size:2.5rem; font-weight:800; color:#00d4ff; }}
        .stat-item .label {{ color:#666; font-size:.9rem; }}
        .cta-group {{
            display:flex; gap:1rem;
            position:relative; z-index:1;
            animation:fadeInUp 1s ease-out .7s both;
        }}

        .services {{ padding:6rem 2rem; max-width:1200px; margin:0 auto; }}
        .services-grid {{
            display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:2rem;
        }}
        .service-card {{
            background:#111; border:1px solid #222; border-radius:16px;
            padding:2.5rem; transition:transform .4s,border-color .4s,box-shadow .4s;
            position:relative; overflow:hidden;
        }}
        .service-card::before {{
            content:''; position:absolute; top:0; left:0;
            width:100%; height:3px;
            background:linear-gradient(90deg,#00d4ff,#7b2ff7);
            transform:scaleX(0); transition:transform .4s; transform-origin:right;
        }}
        .service-card:hover::before {{ transform:scaleX(1); transform-origin:left; }}
        .service-card:hover {{
            transform:translateY(-8px); border-color:#7b2ff7;
            box-shadow:0 20px 40px rgba(0,0,0,.3);
        }}
        .service-card .icon {{ font-size:3rem; margin-bottom:1rem; display:block; animation:float 4s ease-in-out infinite; }}
        .service-card h3 {{ font-size:1.4rem; margin-bottom:.8rem; color:#7b2ff7; }}
        .service-card p {{ color:#999; }}

        .testimonials {{ padding:6rem 2rem; background:#0d0d0d; }}
        .testimonials-grid {{
            max-width:1000px; margin:0 auto;
            display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:2rem;
        }}
        .testimonial-card {{
            background:#111; border:1px solid #1a1a1a; border-radius:16px; padding:2rem;
        }}
        .testimonial-card .stars {{ color:#ffd700; margin-bottom:1rem; font-size:1.2rem; }}
        .testimonial-card .text {{ color:#999; font-style:italic; margin-bottom:1rem; }}
        .testimonial-card .author {{ color:#00d4ff; font-weight:600; }}

        .contact {{ padding:6rem 2rem; text-align:center; background:#111; }}
        .contact-form {{
            max-width:550px; margin:2rem auto;
            display:flex; flex-direction:column; gap:1rem;
        }}
        .form-row {{ display:flex; gap:1rem; }}
        .form-row input {{ flex:1; }}
        .contact-form input, .contact-form textarea, .contact-form select {{
            padding:1rem 1.2rem; border:1px solid #333; border-radius:12px;
            background:#1a1a1a; color:#e0e0e0; font-size:1rem;
            transition:border-color .3s,box-shadow .3s; width:100%;
        }}
        .contact-form input:focus, .contact-form textarea:focus, .contact-form select:focus {{
            outline:none; border-color:#7b2ff7;
            box-shadow:0 0 15px rgba(123,47,247,.15);
        }}
        .contact-form textarea {{ min-height:150px; resize:vertical; }}
        .form-success {{
            display:none; padding:1.5rem;
            background:rgba(0,212,255,.1); border:1px solid #00d4ff;
            border-radius:12px; color:#00d4ff; font-size:1.1rem;
        }}

        {SHARED_FOOTER_CSS}

        @media(max-width:768px) {{
            .hero h1 {{ font-size:2.5rem; }}
            .hero .tagline {{ font-size:1.1rem; }}
            .stats-bar {{ flex-direction:column; gap:1rem; }}
            .cta-group {{ flex-direction:column; }}
            .nav-links,.nav-cta {{ display:none; }}
            .form-row {{ flex-direction:column; }}
        }}
    </style>
</head>
<body>
    <canvas id="particles"></canvas>
    {SHARED_NAV}

    <section class="hero">
        <h1>{biz}</h1>
        <p class="tagline">{tagline}</p>
        <p class="desc">{desc}</p>
        <div class="stats-bar">
            <div class="stat-item"><div class="number">24/7</div><div class="label">Uptime</div></div>
            <div class="stat-item"><div class="number">100%</div><div class="label">Autonomous</div></div>
            <div class="stat-item"><div class="number">10x</div><div class="label">Faster Growth</div></div>
        </div>
        <div class="cta-group">
            <a href="#contact" class="cta-button">Start Free Trial</a>
            <a href="services.html" class="cta-secondary">See How It Works</a>
        </div>
    </section>

    <section class="services">
        <h2 class="section-title animate-on-scroll">What We Automate</h2>
        <p class="section-subtitle animate-on-scroll">End-to-end AI solutions that run your business while you sleep</p>
        <div class="services-grid">
            <div class="service-card animate-on-scroll">
                <span class="icon">&#x1F916;</span>
                <h3>Autonomous AI Agents</h3>
                <p>Self-running agents that handle operations, decisions, and workflows — entirely on autopilot.</p>
            </div>
            <div class="service-card animate-on-scroll">
                <span class="icon">&#x1F310;</span>
                <h3>Smart Website Builder</h3>
                <p>Websites that build, update, and optimize themselves with dynamic content and SEO.</p>
            </div>
            <div class="service-card animate-on-scroll">
                <span class="icon">&#x1F4CA;</span>
                <h3>Analytics &amp; Reports</h3>
                <p>Real-time dashboards and automated weekly reports with actionable insights.</p>
            </div>
            <div class="service-card animate-on-scroll">
                <span class="icon">&#x1F3AC;</span>
                <h3>Video &amp; Reels Marketing</h3>
                <p>Auto-generated video scripts, thumbnails, and social content for YouTube, TikTok, and Instagram.</p>
            </div>
            <div class="service-card animate-on-scroll">
                <span class="icon">&#x1F4AC;</span>
                <h3>AI Customer Service</h3>
                <p>Intelligent chatbot that handles inquiries, books meetings, and nurtures leads 24/7.</p>
            </div>
            <div class="service-card animate-on-scroll">
                <span class="icon">&#x26A1;</span>
                <h3>Process Automation</h3>
                <p>Connect systems, automate workflows, and eliminate repetitive tasks across your stack.</p>
            </div>
            <div class="service-card animate-on-scroll">
                <span class="icon">&#x2699;&#xFE0F;</span>
                <h3>SAP &amp; Priority ERP</h3>
                <p>Full integration and automation for SAP and Priority ERP systems — data sync, reports, and workflows.</p>
            </div>
            <div class="service-card animate-on-scroll">
                <span class="icon">&#x1F4C5;</span>
                <h3>Monday.com &amp; Microsoft 365</h3>
                <p>Custom automations for Monday.com, SharePoint, Power Automate, Teams, and the entire M365 suite.</p>
            </div>
        </div>
    </section>

    <section class="testimonials">
        <h2 class="section-title animate-on-scroll">What Our Clients Say</h2>
        <p class="section-subtitle animate-on-scroll">Businesses already powered by myAI</p>
        <div class="testimonials-grid">
            <div class="testimonial-card animate-on-scroll">
                <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                <p class="text">"myAI replaced our entire marketing team's manual work. We grew 3x in 6 months."</p>
                <p class="author">— Sarah Chen, CEO at GrowthLab</p>
            </div>
            <div class="testimonial-card animate-on-scroll">
                <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                <p class="text">"The autonomous agent handles our customer support, content, and analytics. It's like having 10 employees."</p>
                <p class="author">— Marcus Johnson, Founder of ScaleUp</p>
            </div>
            <div class="testimonial-card animate-on-scroll">
                <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                <p class="text">"We went from zero to 500 leads/month using myAI's video marketing engine. Incredible ROI."</p>
                <p class="author">— Priya Patel, Head of Growth</p>
            </div>
        </div>
    </section>

    <section class="contact" id="contact">
        <h2 class="section-title animate-on-scroll">Get Started Today</h2>
        <p class="section-subtitle animate-on-scroll">14-day free trial. No credit card required.</p>
        <form class="contact-form animate-on-scroll" name="contact-main" method="POST" data-netlify="true" action="thank-you.html">
            <input type="hidden" name="form-name" value="contact-main">
            <div class="form-row">
                <input type="text" name="name" placeholder="Full Name" required>
                <input type="text" name="company" placeholder="Company" required>
            </div>
            <input type="email" name="email" placeholder="Work Email" required>
            <input type="tel" name="phone" placeholder="Phone (optional)">
            <select name="interest">
                <option value="">What are you interested in?</option>
                <option value="agents">Autonomous AI Agents</option>
                <option value="website">Smart Website Builder</option>
                <option value="video">Video &amp; Reels Marketing</option>
                <option value="analytics">Analytics &amp; Reports</option>
                <option value="chatbot">AI Customer Service</option>
                <option value="automation">Process Automation</option>
                <option value="sap">SAP Integration</option>
                <option value="priority">Priority ERP</option>
                <option value="monday">Monday.com Automation</option>
                <option value="m365">Microsoft 365 &amp; SharePoint</option>
                <option value="enterprise">Enterprise Solution</option>
            </select>
            <textarea name="message" placeholder="Tell us about your business goals..."></textarea>
            <button type="submit" class="cta-button">Start Free Trial</button>
        </form>
        <div class="form-success" id="formSuccess">
            &#x2705; Thanks! We'll be in touch within 24 hours. Check your inbox.
        </div>
    </section>

    {_footer(year)}

    <script>
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(e => {{ if(e.isIntersecting) e.target.classList.add('visible'); }});
        }}, {{ threshold: 0.1 }});
        document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

        // Particle Background
        const canvas = document.getElementById('particles');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const particles = [];
        for(let i=0;i<60;i++) particles.push({{
            x:Math.random()*canvas.width, y:Math.random()*canvas.height,
            vx:(Math.random()-.5)*.5, vy:(Math.random()-.5)*.5,
            r:Math.random()*2+.5, alpha:Math.random()*.3+.1
        }});
        function draw() {{
            ctx.clearRect(0,0,canvas.width,canvas.height);
            particles.forEach(p => {{
                p.x+=p.vx; p.y+=p.vy;
                if(p.x<0)p.x=canvas.width; if(p.x>canvas.width)p.x=0;
                if(p.y<0)p.y=canvas.height; if(p.y>canvas.height)p.y=0;
                ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
                ctx.fillStyle=`rgba(0,212,255,${{p.alpha}})`; ctx.fill();
            }});
            for(let i=0;i<particles.length;i++) for(let j=i+1;j<particles.length;j++) {{
                const dx=particles[i].x-particles[j].x, dy=particles[i].y-particles[j].y;
                const d=Math.sqrt(dx*dx+dy*dy);
                if(d<150) {{
                    ctx.beginPath(); ctx.moveTo(particles[i].x,particles[i].y);
                    ctx.lineTo(particles[j].x,particles[j].y);
                    ctx.strokeStyle=`rgba(123,47,247,${{.05*(1-d/150)}})`; ctx.stroke();
                }}
            }}
            requestAnimationFrame(draw);
        }}
        draw();
        window.addEventListener('resize',()=>{{ canvas.width=innerWidth; canvas.height=innerHeight; }});

        // Contact form
        function handleSubmit(e) {{
            e.preventDefault();
            const data = Object.fromEntries(new FormData(e.target).entries());
            const leads = JSON.parse(localStorage.getItem('myai_leads')||'[]');
            leads.push({{ ...data, timestamp: new Date().toISOString() }});
            localStorage.setItem('myai_leads', JSON.stringify(leads));
            e.target.style.display='none';
            document.getElementById('formSuccess').style.display='block';
        }}

        // Smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(a => {{
            a.addEventListener('click', function(e) {{
                e.preventDefault();
                const t = document.querySelector(this.getAttribute('href'));
                if(t) t.scrollIntoView({{ behavior:'smooth' }});
            }});
        }});
    </script>
</body>
</html>"""

    path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


# ═══════════════════════════════════════════════════
# ABOUT PAGE
# ═══════════════════════════════════════════════════

def generate_about_page(config):
    ensure_output_dir()
    year = datetime.now().year
    biz = config.get("business", {}).get("name", "myAI")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About — {biz}</title>
    <style>
        {BASE_CSS}
        {SHARED_NAV_CSS}
        .hero-mini {{
            padding:8rem 2rem 4rem; text-align:center;
            background:linear-gradient(135deg,#0a0a0a,#1a1a2e);
        }}
        .hero-mini h1 {{
            font-size:3rem;
            background:linear-gradient(90deg,#00d4ff,#7b2ff7);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
            margin-bottom:1rem;
        }}
        .hero-mini p {{ color:#888; font-size:1.2rem; max-width:600px; margin:0 auto; }}
        .content {{ max-width:900px; margin:0 auto; padding:4rem 2rem; }}
        .story {{ margin-bottom:3rem; }}
        .story h2 {{ color:#00d4ff; font-size:2rem; margin-bottom:1.5rem; }}
        .story p {{ color:#999; font-size:1.1rem; margin-bottom:1rem; }}
        .values-grid {{
            display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
            gap:2rem; margin:3rem 0;
        }}
        .value-card {{
            background:#111; border:1px solid #222; border-radius:16px;
            padding:2rem; text-align:center;
            transition:transform .3s,border-color .3s;
        }}
        .value-card:hover {{ transform:translateY(-5px); border-color:#7b2ff7; }}
        .value-card .icon {{ font-size:3rem; margin-bottom:1rem; display:block; }}
        .value-card h3 {{ color:#7b2ff7; margin-bottom:.5rem; }}
        .value-card p {{ color:#888; font-size:.95rem; }}
        .timeline {{ position:relative; padding-left:3rem; }}
        .timeline::before {{
            content:''; position:absolute; left:0; top:0; bottom:0; width:2px;
            background:linear-gradient(to bottom,#00d4ff,#7b2ff7);
        }}
        .timeline-item {{ position:relative; margin-bottom:2rem; }}
        .timeline-item::before {{
            content:''; position:absolute; left:-3.4rem; top:.5rem;
            width:12px; height:12px; border-radius:50%;
            background:#7b2ff7; border:2px solid #0a0a0a;
        }}
        .timeline-item .date {{ color:#00d4ff; font-weight:600; }}
        .timeline-item .desc {{ color:#999; }}
        .cta-section {{ text-align:center; padding:4rem 2rem; }}
        {SHARED_FOOTER_CSS}
    </style>
</head>
<body>
    {SHARED_NAV}
    <section class="hero-mini">
        <h1>About {biz}</h1>
        <p>The story behind the autonomous AI platform that's changing how businesses operate</p>
    </section>
    <div class="content">
        <div class="story">
            <h2>&#x1F680; Our Mission</h2>
            <p>We believe every business deserves the power of automation — regardless of size or budget. myAI was built with one bold vision: what if a digital business could build and maintain itself entirely on autopilot?</p>
            <p>Our autonomous agents handle everything — from building websites and writing content to marketing on social media and managing customer relationships. The system runs 24/7, learning and improving with every cycle.</p>
        </div>
        <div class="story">
            <h2>&#x1F4A1; Our Values</h2>
            <div class="values-grid">
                <div class="value-card"><span class="icon">&#x1F504;</span><h3>Full Autonomy</h3><p>Systems that manage, maintain, and improve themselves</p></div>
                <div class="value-card"><span class="icon">&#x1F4C8;</span><h3>Continuous Growth</h3><p>Every run makes the system smarter and more effective</p></div>
                <div class="value-card"><span class="icon">&#x1F50D;</span><h3>Total Transparency</h3><p>Every action logged, every decision documented</p></div>
                <div class="value-card"><span class="icon">&#x1F3AF;</span><h3>Results-Driven</h3><p>Clear goals, measurable outcomes, real ROI</p></div>
            </div>
        </div>
        <div class="story">
            <h2>&#x1F4C5; Our Journey</h2>
            <div class="timeline">
                <div class="timeline-item"><div class="date">Q1 2026 — Foundation</div><div class="desc">Built core architecture: autonomous agent, task manager, website generator, CRM</div></div>
                <div class="timeline-item"><div class="date">Q1 2026 — Content Engine</div><div class="desc">Blog system, email templates, market analysis module</div></div>
                <div class="timeline-item"><div class="date">Q2 2026 — Video Marketing</div><div class="desc">YouTube scripts, TikTok/Reels content, social media pipeline, content calendar</div></div>
                <div class="timeline-item"><div class="date">Q2 2026 — Global Launch</div><div class="desc">English platform, global pricing, multi-platform marketing</div></div>
            </div>
        </div>
        <div class="cta-section">
            <h2 style="color:#00d4ff;margin-bottom:1rem;">Ready to let AI run your business?</h2>
            <a href="index.html#contact" class="cta-button">Start Free Trial</a>
        </div>
    </div>
    {_footer(year)}
</body>
</html>"""

    path = os.path.join(OUTPUT_DIR, 'about.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


# ═══════════════════════════════════════════════════
# SERVICES PAGE
# ═══════════════════════════════════════════════════

def generate_services_page(config):
    ensure_output_dir()
    year = datetime.now().year

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Services — myAI</title>
    <style>
        {BASE_CSS}
        {SHARED_NAV_CSS}
        .hero-mini {{
            padding:8rem 2rem 4rem; text-align:center;
            background:linear-gradient(135deg,#0a0a0a,#1a1a2e);
        }}
        .hero-mini h1 {{
            font-size:3rem;
            background:linear-gradient(90deg,#00d4ff,#7b2ff7);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
            margin-bottom:1rem;
        }}
        .hero-mini p {{ color:#888; font-size:1.2rem; }}
        .services-detail {{ max-width:1000px; margin:0 auto; padding:4rem 2rem; }}
        .service-block {{
            display:grid; grid-template-columns:1fr 1fr; gap:3rem;
            margin-bottom:5rem; align-items:center;
        }}
        .service-block.reverse {{ direction:rtl; }}
        .service-block.reverse > * {{ direction:ltr; }}
        .service-info h2 {{ color:#00d4ff; font-size:1.8rem; margin-bottom:1rem; }}
        .service-info p {{ color:#999; margin-bottom:1rem; }}
        .service-info ul {{ list-style:none; }}
        .service-info ul li {{ padding:.4rem 0; color:#a0a0a0; }}
        .service-info ul li::before {{ content:'\\2713 '; color:#00d4ff; font-weight:bold; }}
        .service-visual {{
            background:#111; border:1px solid #222; border-radius:20px;
            padding:3rem; text-align:center; font-size:5rem;
        }}
        .process {{ padding:5rem 2rem; background:#0d0d0d; }}
        .process h2 {{ text-align:center; color:#00d4ff; font-size:2.5rem; margin-bottom:3rem; }}
        .process-steps {{
            max-width:900px; margin:0 auto;
            display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:2rem;
        }}
        .step {{ text-align:center; padding:2rem; }}
        .step .number {{
            width:50px; height:50px; border-radius:50%;
            background:linear-gradient(135deg,#00d4ff,#7b2ff7);
            display:flex; justify-content:center; align-items:center;
            font-size:1.5rem; font-weight:bold; margin:0 auto 1rem;
        }}
        .step h3 {{ color:#e0e0e0; margin-bottom:.5rem; }}
        .step p {{ color:#888; font-size:.9rem; }}
        .cta-section {{ text-align:center; padding:4rem 2rem; }}
        {SHARED_FOOTER_CSS}
        @media(max-width:768px) {{ .service-block {{ grid-template-columns:1fr; }} }}
    </style>
</head>
<body>
    {SHARED_NAV}
    <section class="hero-mini">
        <h1>Our Services</h1>
        <p>End-to-end autonomous AI solutions for modern businesses</p>
    </section>

    <div class="services-detail">
        <div class="service-block">
            <div class="service-info">
                <h2>&#x1F916; Autonomous AI Agents</h2>
                <p>Deploy intelligent agents that run your business processes end-to-end.</p>
                <ul>
                    <li>Automated data analysis &amp; decision-making</li>
                    <li>Task scheduling &amp; execution</li>
                    <li>Real-time monitoring &amp; reporting</li>
                    <li>Self-learning &amp; continuous improvement</li>
                </ul>
            </div>
            <div class="service-visual">&#x1F916;</div>
        </div>
        <div class="service-block reverse">
            <div class="service-visual">&#x1F3AC;</div>
            <div class="service-info">
                <h2>&#x1F3AC; Video &amp; Reels Marketing</h2>
                <p>Automated video content pipeline for all major platforms.</p>
                <ul>
                    <li>YouTube scripts (5-10 min educational content)</li>
                    <li>TikTok &amp; Instagram Reels (15-60 sec hooks)</li>
                    <li>Thumbnail generation &amp; A/B testing</li>
                    <li>Content calendar with optimal posting times</li>
                </ul>
            </div>
        </div>
        <div class="service-block">
            <div class="service-info">
                <h2>&#x1F310; Smart Website Builder</h2>
                <p>Websites that evolve autonomously with fresh content and design.</p>
                <ul>
                    <li>Responsive, modern design (auto-generated)</li>
                    <li>Dynamic content that updates itself</li>
                    <li>Built-in SEO optimization</li>
                    <li>Lead capture &amp; CRM integration</li>
                </ul>
            </div>
            <div class="service-visual">&#x1F310;</div>
        </div>
        <div class="service-block reverse">
            <div class="service-visual">&#x1F4E3;</div>
            <div class="service-info">
                <h2>&#x1F4E3; Social Media Automation</h2>
                <p>Full-stack social media presence on autopilot.</p>
                <ul>
                    <li>Multi-platform content (Twitter, LinkedIn, Instagram, TikTok)</li>
                    <li>Platform-specific captions &amp; hashtags</li>
                    <li>Scheduling based on peak engagement times</li>
                    <li>Performance tracking &amp; optimization</li>
                </ul>
            </div>
        </div>
        <div class="service-block">
            <div class="service-info">
                <h2>&#x1F4CA; Analytics &amp; Reporting</h2>
                <p>Data-driven insights delivered automatically.</p>
                <ul>
                    <li>Market &amp; competitor analysis</li>
                    <li>Weekly performance reports</li>
                    <li>Revenue forecasting</li>
                    <li>Interactive dashboards</li>
                </ul>
            </div>
            <div class="service-visual">&#x1F4CA;</div>
        </div>
        <div class="service-block reverse">
            <div class="service-visual">&#x1F4AC;</div>
            <div class="service-info">
                <h2>&#x1F4AC; AI Customer Service</h2>
                <p>Smart chatbot handling support and sales 24/7.</p>
                <ul>
                    <li>Natural language conversations</li>
                    <li>Automated meeting scheduling</li>
                    <li>Seamless handoff to human agents</li>
                    <li>Continuous learning from interactions</li>
                </ul>
            </div>
        </div>
        <div class="service-block">
            <div class="service-info">
                <h2>&#x2699;&#xFE0F; SAP &amp; ERP Integration</h2>
                <p>Seamless integration with SAP modules for enterprise-grade automation.</p>
                <ul>
                    <li>SAP Business One &amp; S/4HANA integration</li>
                    <li>Automated data sync &amp; reporting</li>
                    <li>Custom workflows &amp; approvals</li>
                    <li>Real-time dashboards from SAP data</li>
                </ul>
            </div>
            <div class="service-visual">&#x2699;&#xFE0F;</div>
        </div>
        <div class="service-block reverse">
            <div class="service-visual">&#x1F4CB;</div>
            <div class="service-info">
                <h2>&#x1F4CB; Priority ERP Automation</h2>
                <p>Automate your Priority ERP processes end-to-end.</p>
                <ul>
                    <li>Priority modules integration &amp; customization</li>
                    <li>Automated purchasing, inventory &amp; finance</li>
                    <li>Custom reports &amp; BI dashboards</li>
                    <li>API connections to external systems</li>
                </ul>
            </div>
        </div>
        <div class="service-block">
            <div class="service-info">
                <h2>&#x1F4C5; Monday.com Automation</h2>
                <p>Supercharge your Monday.com boards with AI-powered automations.</p>
                <ul>
                    <li>Custom automations &amp; integrations</li>
                    <li>Cross-board workflows &amp; dependencies</li>
                    <li>AI-driven task assignment &amp; prioritization</li>
                    <li>Real-time reporting &amp; notifications</li>
                </ul>
            </div>
            <div class="service-visual">&#x1F4C5;</div>
        </div>
        <div class="service-block reverse">
            <div class="service-visual">&#x2601;&#xFE0F;</div>
            <div class="service-info">
                <h2>&#x2601;&#xFE0F; Microsoft 365 &amp; SharePoint</h2>
                <p>Unlock the full power of your Microsoft 365 &amp; SharePoint environment.</p>
                <ul>
                    <li>SharePoint sites, lists &amp; document management</li>
                    <li>Power Automate flows &amp; Power Apps</li>
                    <li>Teams integrations &amp; bots</li>
                    <li>Microsoft 365 security &amp; compliance setup</li>
                </ul>
            </div>
        </div>
        <div class="service-block">
            <div class="service-info">
                <h2>&#x26A1; Business Process Automations</h2>
                <p>End-to-end process automations that eliminate manual work across all your systems.</p>
                <ul>
                    <li>Cross-platform integrations (APIs, webhooks, RPA)</li>
                    <li>Automated data pipelines &amp; ETL</li>
                    <li>Custom workflow engines</li>
                    <li>Zapier, Make, Power Automate &amp; custom solutions</li>
                </ul>
            </div>
            <div class="service-visual">&#x26A1;</div>
        </div>
    </div>

    <section class="process">
        <h2>How It Works</h2>
        <div class="process-steps">
            <div class="step"><div class="number">1</div><h3>Discovery</h3><p>We understand your business goals &amp; needs</p></div>
            <div class="step"><div class="number">2</div><h3>Setup</h3><p>Configure agents &amp; tools for your stack</p></div>
            <div class="step"><div class="number">3</div><h3>Launch</h3><p>Activate the system and validate results</p></div>
            <div class="step"><div class="number">4</div><h3>Autopilot</h3><p>The AI runs and improves continuously</p></div>
        </div>
    </section>

    <div class="cta-section">
        <h2 style="color:#00d4ff;margin-bottom:1rem;">Ready to automate?</h2>
        <a href="pricing.html" class="cta-button">See Pricing</a>
    </div>
    {_footer(year)}
</body>
</html>"""

    path = os.path.join(OUTPUT_DIR, 'services.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


# ═══════════════════════════════════════════════════
# PRICING PAGE
# ═══════════════════════════════════════════════════

def generate_pricing_page(config):
    ensure_output_dir()
    year = datetime.now().year
    plans = config.get("pricing", {}).get("plans", {})
    s = plans.get("starter", {}).get("price", 399)
    p = plans.get("pro", {}).get("price", 999)
    e = plans.get("enterprise", {}).get("price", 2499)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pricing — myAI</title>
    <style>
        {BASE_CSS}
        {SHARED_NAV_CSS}
        .hero-mini {{
            padding:8rem 2rem 4rem; text-align:center;
            background:linear-gradient(135deg,#0a0a0a,#1a1a2e);
        }}
        .hero-mini h1 {{
            font-size:3rem;
            background:linear-gradient(90deg,#00d4ff,#7b2ff7);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
            margin-bottom:1rem;
        }}
        .hero-mini p {{ color:#888; font-size:1.2rem; }}
        .pricing-grid {{
            max-width:1100px; margin:0 auto; padding:4rem 2rem;
            display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:2rem;
        }}
        .plan {{
            background:#111; border:1px solid #222; border-radius:20px;
            padding:3rem 2rem; text-align:center;
            transition:transform .3s,border-color .3s; position:relative;
        }}
        .plan:hover {{ transform:translateY(-5px); border-color:#333; }}
        .plan.featured {{ border-color:#7b2ff7; transform:scale(1.05); }}
        .plan.featured:hover {{ transform:scale(1.05) translateY(-5px); }}
        .plan .badge {{
            position:absolute; top:-12px; left:50%; transform:translateX(-50%);
            background:linear-gradient(90deg,#00d4ff,#7b2ff7);
            color:white; padding:.3rem 1.5rem; border-radius:20px;
            font-size:.85rem; font-weight:600;
        }}
        .plan h3 {{ color:#00d4ff; font-size:1.5rem; margin-bottom:.5rem; }}
        .plan .price {{ font-size:3rem; font-weight:800; margin:1rem 0; }}
        .plan .price span {{ font-size:1rem; color:#666; }}
        .plan .features {{ list-style:none; margin:2rem 0; text-align:left; }}
        .plan .features li {{ padding:.5rem 0; border-bottom:1px solid #1a1a1a; color:#999; }}
        .plan .features li::before {{ content:'\\2713 '; color:#00d4ff; }}
        .plan .features li.disabled {{ color:#444; }}
        .plan .features li.disabled::before {{ content:'\\2717 '; color:#444; }}
        .plan-btn {{
            display:inline-block; width:100%; padding:1rem; border:none;
            border-radius:50px; font-size:1.1rem; cursor:pointer;
            text-decoration:none; transition:all .3s;
        }}
        .plan-btn.primary {{ background:linear-gradient(90deg,#00d4ff,#7b2ff7); color:white; }}
        .plan-btn.secondary {{ background:transparent; border:2px solid #333; color:#a0a0a0; }}
        .plan-btn:hover {{ transform:translateY(-2px); }}
        .faq {{ max-width:800px; margin:0 auto; padding:4rem 2rem; }}
        .faq h2 {{ text-align:center; color:#00d4ff; font-size:2rem; margin-bottom:2rem; }}
        .faq-item {{
            background:#111; border:1px solid #222; border-radius:12px;
            margin-bottom:1rem; overflow:hidden;
        }}
        .faq-item summary {{ padding:1.2rem; cursor:pointer; color:#e0e0e0; font-weight:600; }}
        .faq-item summary:hover {{ color:#00d4ff; }}
        .faq-item p {{ padding:0 1.2rem 1.2rem; color:#888; }}
        {SHARED_FOOTER_CSS}
        @media(max-width:768px) {{
            .plan.featured {{ transform:scale(1); }}
            .plan.featured:hover {{ transform:translateY(-5px); }}
        }}
    </style>
</head>
<body>
    {SHARED_NAV}
    <section class="hero-mini">
        <h1>Simple, Transparent Pricing</h1>
        <p>14-day free trial on all plans. Cancel anytime.</p>
    </section>

    <div class="pricing-grid">
        <div class="plan">
            <h3>Starter</h3>
            <div class="price">${s}<span>/mo</span></div>
            <p style="color:#666;">For small businesses getting started with AI</p>
            <ul class="features">
                <li>1 AI Agent</li>
                <li>Landing page + blog</li>
                <li>5 social posts/week</li>
                <li>2 video scripts/month</li>
                <li>Monthly reports</li>
                <li class="disabled">AI Customer Service</li>
                <li class="disabled">Custom API</li>
            </ul>
            <a href="index.html#contact" class="plan-btn secondary">Start Free Trial</a>
        </div>
        <div class="plan featured">
            <div class="badge">Most Popular</div>
            <h3>Pro</h3>
            <div class="price">${p}<span>/mo</span></div>
            <p style="color:#666;">For growing businesses that want full automation</p>
            <ul class="features">
                <li>3 AI Agents</li>
                <li>Full website (5+ pages)</li>
                <li>Daily social posts (all platforms)</li>
                <li>8 video scripts/month + thumbnails</li>
                <li>Weekly reports</li>
                <li>AI Customer Service chatbot</li>
                <li class="disabled">Custom API</li>
            </ul>
            <a href="index.html#contact" class="plan-btn primary">Start Free Trial</a>
        </div>
        <div class="plan">
            <h3>Enterprise</h3>
            <div class="price">${e}<span>/mo</span></div>
            <p style="color:#666;">For organizations that need the full suite</p>
            <ul class="features">
                <li>Unlimited AI Agents</li>
                <li>Full website + web app</li>
                <li>Unlimited content</li>
                <li>Real-time dashboards</li>
                <li>Advanced AI Customer Service</li>
                <li>Multi-platform campaigns + SEO</li>
                <li>Custom API &amp; integrations</li>
            </ul>
            <a href="index.html#contact" class="plan-btn secondary">Contact Sales</a>
        </div>
    </div>

    <section class="faq">
        <h2>Frequently Asked Questions</h2>
        <details class="faq-item"><summary>Can I upgrade my plan?</summary><p>Yes! Upgrade anytime. Billing adjusts pro-rata for the remaining period.</p></details>
        <details class="faq-item"><summary>Is there a free trial?</summary><p>All plans include a 14-day free trial. No credit card required.</p></details>
        <details class="faq-item"><summary>What's the difference between agent types?</summary><p>Starter agents handle simple tasks from templates. Pro agents can learn, adapt, and make autonomous decisions based on data.</p></details>
        <details class="faq-item"><summary>How does support work?</summary><p>All plans include 24/7 AI chatbot support. Pro and Enterprise also get dedicated human support and onboarding.</p></details>
        <details class="faq-item"><summary>Can I get a custom solution?</summary><p>Enterprise customers get fully customized agents, APIs, and integrations tailored to their specific business needs.</p></details>
    </section>
    {_footer(year)}
</body>
</html>"""

    path = os.path.join(OUTPUT_DIR, 'pricing.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


# ═══════════════════════════════════════════════════
# BLOG PAGE
# ═══════════════════════════════════════════════════

def generate_blog_page(posts):
    ensure_output_dir()
    year = datetime.now().year

    posts_html = ""
    for post in posts:
        tags = ""
        if post.get("tags"):
            tags = "".join(f'<span class="tag">{t}</span>' for t in post["tags"])
        posts_html += f"""
        <article class="blog-post animate-on-scroll">
            <h2>{post['title']}</h2>
            <time>{post.get('date', datetime.now().strftime('%Y-%m-%d'))}</time>
            <div class="tags">{tags}</div>
            <p>{post['content']}</p>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog — myAI</title>
    <style>
        {BASE_CSS}
        {SHARED_NAV_CSS}
        .container {{ max-width:800px; margin:0 auto; padding:7rem 2rem 2rem; }}
        h1 {{ font-size:3rem; text-align:center; margin-bottom:3rem; color:#00d4ff; }}
        .blog-post {{
            background:#111; border:1px solid #222; border-radius:16px;
            padding:2rem; margin-bottom:2rem;
            transition:transform .3s,border-color .3s;
        }}
        .blog-post:hover {{ transform:translateY(-3px); border-color:#7b2ff7; }}
        .blog-post h2 {{ color:#7b2ff7; margin-bottom:.5rem; }}
        .blog-post time {{ color:#666; font-size:.9rem; }}
        .blog-post p {{ margin-top:1rem; color:#999; }}
        .tags {{ display:flex; gap:.5rem; margin-top:.5rem; flex-wrap:wrap; }}
        .tag {{
            background:rgba(123,47,247,.15); color:#7b2ff7;
            padding:.2rem .8rem; border-radius:20px; font-size:.8rem;
        }}
        {SHARED_FOOTER_CSS}
    </style>
</head>
<body>
    {SHARED_NAV}
    <div class="container">
        <h1>The myAI Blog</h1>
        {posts_html}
    </div>
    {_footer(year)}
    {SCROLL_JS}
</body>
</html>"""

    path = os.path.join(OUTPUT_DIR, 'blog.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path
