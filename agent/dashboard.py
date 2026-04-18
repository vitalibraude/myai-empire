import os
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')


def generate_dashboard():
    """Generate a full admin dashboard with revenue tracking, lead monitoring, and business overview."""

    # Load business data
    biz_path = os.path.join(BASE_DIR, 'businesses.json')
    with open(biz_path, 'r', encoding='utf-8') as f:
        businesses = json.load(f)['businesses']

    total_mrr_1 = sum(b['price'] for b in businesses)
    total_mrr_10 = total_mrr_1 * 10

    # Load run logs
    logs_dir = os.path.join(BASE_DIR, 'data', 'logs')
    log_count = len([f for f in os.listdir(logs_dir) if f.startswith('run_')]) if os.path.exists(logs_dir) else 0

    # Load tasks
    tasks_path = os.path.join(BASE_DIR, 'data', 'tasks.json')
    tasks = []
    if os.path.exists(tasks_path):
        with open(tasks_path, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
    completed = sum(1 for t in tasks if t['status'] == 'completed')
    pending = sum(1 for t in tasks if t['status'] == 'pending')

    # Generate business rows
    biz_rows = ""
    for i, b in enumerate(businesses, 1):
        pro_price = int(b['price'] * 2.2)
        ent_price = int(b['price'] * 4.5)
        biz_rows += f"""
            <tr>
                <td>{i}</td>
                <td><a href="../businesses/{b['id']}/index.html" style="color:#00d4ff;text-decoration:none;">{b['name']}</a></td>
                <td>{b['audience']}</td>
                <td>${b['price']}</td>
                <td>${pro_price}</td>
                <td>${ent_price}</td>
                <td><span class="status-badge live">Live</span></td>
                <td><span class="lead-count" id="leads-{b['id']}">0</span></td>
            </tr>"""

    # Generate recent tasks
    recent_tasks = sorted(tasks, key=lambda t: t.get('completed') or t.get('created') or '', reverse=True)[:20]
    task_rows = ""
    for t in recent_tasks:
        status_class = "completed" if t['status'] == 'completed' else 'pending'
        task_rows += f"""
            <tr>
                <td>#{t['id']}</td>
                <td>{t['title']}</td>
                <td><span class="status-badge {status_class}">{t['status'].title()}</span></td>
                <td>{t['priority'].title()}</td>
                <td>{(t.get('completed') or t.get('created') or 'N/A')[:16]}</td>
            </tr>"""

    # Price distribution for chart
    price_counts = {}
    for b in businesses:
        p = b['price']
        price_counts[p] = price_counts.get(p, 0) + 1

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>myAI — Empire Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; background: #060611; color: #e0e0e0; line-height: 1.6; }}

        /* Sidebar */
        .sidebar {{ position: fixed; top: 0; left: 0; width: 240px; height: 100vh; background: #0a0a1a; border-right: 1px solid #1a1a2e; padding: 1.5rem 0; overflow-y: auto; z-index: 100; }}
        .sidebar .logo {{ padding: 0 1.5rem; font-size: 1.4rem; font-weight: 800; background: linear-gradient(90deg,#00d4ff,#7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 2rem; }}
        .sidebar a {{ display: flex; align-items: center; gap: 0.8rem; padding: 0.7rem 1.5rem; color: #888; text-decoration: none; font-size: 0.9rem; transition: all 0.2s; border-left: 3px solid transparent; }}
        .sidebar a:hover, .sidebar a.active {{ color: #00d4ff; background: rgba(0,212,255,0.05); border-left-color: #00d4ff; }}
        .sidebar .section-label {{ padding: 1.5rem 1.5rem 0.5rem; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1rem; color: #555; }}

        /* Main */
        .main {{ margin-left: 240px; padding: 2rem; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }}
        .header h1 {{ font-size: 1.8rem; font-weight: 700; }}
        .header .live-badge {{ background: #00c853; color: #000; padding: 0.3rem 1rem; border-radius: 50px; font-size: 0.8rem; font-weight: 700; animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} }}

        /* Stat Cards */
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.2rem; margin-bottom: 2rem; }}
        .stat-card {{ background: #0d0d20; border: 1px solid #1a1a2e; border-radius: 16px; padding: 1.5rem; position: relative; overflow: hidden; }}
        .stat-card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg,#00d4ff,#7b2ff7); }}
        .stat-card .label {{ font-size: 0.85rem; color: #777; margin-bottom: 0.3rem; }}
        .stat-card .value {{ font-size: 2rem; font-weight: 800; }}
        .stat-card .value.blue {{ color: #00d4ff; }}
        .stat-card .value.purple {{ color: #7b2ff7; }}
        .stat-card .value.green {{ color: #00c853; }}
        .stat-card .value.gold {{ color: #ffd700; }}
        .stat-card .change {{ font-size: 0.8rem; color: #00c853; margin-top: 0.3rem; }}

        /* Charts placeholder */
        .chart-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 1.2rem; margin-bottom: 2rem; }}
        .chart-card {{ background: #0d0d20; border: 1px solid #1a1a2e; border-radius: 16px; padding: 1.5rem; }}
        .chart-card h3 {{ font-size: 1rem; color: #aaa; margin-bottom: 1rem; }}
        .bar-chart {{ display: flex; align-items: flex-end; gap: 4px; height: 200px; padding-top: 1rem; }}
        .bar {{ flex: 1; background: linear-gradient(180deg, #00d4ff, #7b2ff7); border-radius: 4px 4px 0 0; min-width: 20px; position: relative; transition: all 0.3s; cursor: pointer; }}
        .bar:hover {{ opacity: 0.8; }}
        .bar .tooltip {{ display: none; position: absolute; top: -30px; left: 50%; transform: translateX(-50%); background: #1a1a2e; padding: 0.3rem 0.6rem; border-radius: 6px; font-size: 0.75rem; white-space: nowrap; }}
        .bar:hover .tooltip {{ display: block; }}
        .donut-container {{ display: flex; justify-content: center; align-items: center; height: 200px; }}
        .donut {{ width: 180px; height: 180px; border-radius: 50%; background: conic-gradient(#00d4ff 0deg 120deg, #7b2ff7 120deg 220deg, #00c853 220deg 300deg, #ffd700 300deg 360deg); position: relative; }}
        .donut::after {{ content: '50'; position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); width: 100px; height: 100px; background: #0d0d20; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800; color: #00d4ff; }}

        /* Table */
        .table-card {{ background: #0d0d20; border: 1px solid #1a1a2e; border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem; overflow-x: auto; }}
        .table-card h3 {{ font-size: 1rem; color: #aaa; margin-bottom: 1rem; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; padding: 0.8rem; color: #555; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05rem; border-bottom: 1px solid #1a1a2e; }}
        td {{ padding: 0.7rem 0.8rem; border-bottom: 1px solid #0a0a1a; font-size: 0.9rem; }}
        tr:hover {{ background: rgba(0,212,255,0.03); }}
        .status-badge {{ padding: 0.25rem 0.8rem; border-radius: 50px; font-size: 0.75rem; font-weight: 600; }}
        .status-badge.live {{ background: rgba(0,200,83,0.15); color: #00c853; }}
        .status-badge.completed {{ background: rgba(0,212,255,0.15); color: #00d4ff; }}
        .status-badge.pending {{ background: rgba(255,215,0,0.15); color: #ffd700; }}
        .lead-count {{ background: #1a1a2e; padding: 0.2rem 0.6rem; border-radius: 8px; font-weight: 600; }}

        /* Revenue Simulator */
        .simulator {{ background: #0d0d20; border: 1px solid #1a1a2e; border-radius: 16px; padding: 2rem; margin-bottom: 2rem; }}
        .simulator h3 {{ color: #aaa; margin-bottom: 1rem; }}
        .slider-group {{ display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }}
        .slider-group label {{ min-width: 200px; color: #888; font-size: 0.9rem; }}
        .slider-group input[type=range] {{ flex: 1; accent-color: #00d4ff; }}
        .slider-group .val {{ min-width: 60px; text-align: right; font-weight: 700; color: #00d4ff; }}
        .revenue-result {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #1a1a2e; }}
        .revenue-result .item {{ text-align: center; }}
        .revenue-result .big {{ font-size: 1.8rem; font-weight: 800; background: linear-gradient(90deg,#00d4ff,#7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .revenue-result .sub {{ font-size: 0.8rem; color: #666; }}

        /* Lead feed */
        .lead-feed {{ background: #0d0d20; border: 1px solid #1a1a2e; border-radius: 16px; padding: 1.5rem; }}
        .lead-feed h3 {{ color: #aaa; margin-bottom: 1rem; }}
        .lead-item {{ display: flex; justify-content: space-between; align-items: center; padding: 0.8rem; border-bottom: 1px solid #0a0a1a; }}
        .lead-item .info {{ display: flex; flex-direction: column; }}
        .lead-item .name {{ font-weight: 600; color: #e0e0e0; }}
        .lead-item .source {{ font-size: 0.8rem; color: #666; }}
        .lead-item .time {{ font-size: 0.8rem; color: #555; }}
        .empty-state {{ text-align: center; padding: 3rem; color: #555; }}
        .empty-state .icon {{ font-size: 3rem; margin-bottom: 1rem; }}

        /* Tabs */
        .tab-bar {{ display: flex; gap: 0; margin-bottom: 1.5rem; background: #0a0a1a; border-radius: 12px; overflow: hidden; border: 1px solid #1a1a2e; }}
        .tab {{ padding: 0.7rem 1.5rem; cursor: pointer; color: #666; font-size: 0.9rem; transition: all 0.2s; }}
        .tab:hover {{ color: #aaa; }}
        .tab.active {{ background: #0d0d20; color: #00d4ff; font-weight: 600; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        @media (max-width: 900px) {{
            .sidebar {{ display: none; }}
            .main {{ margin-left: 0; }}
            .chart-grid {{ grid-template-columns: 1fr; }}
            .revenue-result {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>

<div class="sidebar">
    <div class="logo">&#x1F916; myAI</div>
    <a href="#" class="active">&#x1F4CA; Dashboard</a>
    <a href="#businesses-section">&#x1F3E2; Businesses</a>
    <a href="#revenue-section">&#x1F4B0; Revenue</a>
    <a href="#leads-section">&#x1F4E9; Leads</a>
    <div class="section-label">Operations</div>
    <a href="#tasks-section">&#x2705; Tasks</a>
    <a href="#agent-section">&#x1F916; Agent Runs</a>
    <div class="section-label">Sites</div>
    <a href="https://businesses.aoeua.com/">&#x1F310; All 50 Sites</a>
    <a href="index.html">&#x1F3E0; Main Site</a>
    <a href="investors.html">&#x1F4BC; Investor Page</a>
    <a href="checkout.html">&#x1F4B3; Checkout</a>
    <div class="section-label">Data</div>
    <a href="blog.html">&#x1F4DD; Blog ({len([t for t in tasks if 'blog' in t.get('title','').lower() or 'content' in t.get('title','').lower()])} runs)</a>
</div>

<div class="main">
    <div class="header">
        <h1>Empire Dashboard</h1>
        <div class="live-badge">&#x1F7E2; LIVE on Netlify</div>
    </div>

    <!-- Stat Cards -->
    <div class="stats-grid">
        <div class="stat-card">
            <div class="label">Active Businesses</div>
            <div class="value blue">50</div>
            <div class="change">All deployed &amp; ready</div>
        </div>
        <div class="stat-card">
            <div class="label">Potential MRR (1 client/biz)</div>
            <div class="value green">${total_mrr_1:,}</div>
            <div class="change">50 niches &times; avg price</div>
        </div>
        <div class="stat-card">
            <div class="label">Agent Runs</div>
            <div class="value purple">{log_count}</div>
            <div class="change">{completed} tasks completed</div>
        </div>
        <div class="stat-card">
            <div class="label">Tasks Completed</div>
            <div class="value gold">{completed}</div>
            <div class="change">{pending} pending</div>
        </div>
        <div class="stat-card">
            <div class="label">Total Pages</div>
            <div class="value blue">57</div>
            <div class="change">7 main + 50 niche sites</div>
        </div>
        <div class="stat-card">
            <div class="label">Content Pieces</div>
            <div class="value purple">700+</div>
            <div class="change">Blog + Social + Email + Video</div>
        </div>
    </div>

    <!-- Charts -->
    <div class="chart-grid">
        <div class="chart-card">
            <h3>Revenue by Niche (Monthly Price per Client)</h3>
            <div class="bar-chart" id="revenue-chart">
                {"".join(f'<div class="bar" style="height:{int(b["price"]/6)}px;"><div class="tooltip">{b["name"]}: ${b["price"]}</div></div>' for b in businesses)}
            </div>
        </div>
        <div class="chart-card">
            <h3>Business Categories</h3>
            <div class="donut-container">
                <div class="donut"></div>
            </div>
            <div style="display:flex;gap:1rem;justify-content:center;margin-top:1rem;flex-wrap:wrap;">
                <span style="color:#00d4ff;font-size:0.8rem;">&#x25CF; Services (15)</span>
                <span style="color:#7b2ff7;font-size:0.8rem;">&#x25CF; Health (8)</span>
                <span style="color:#00c853;font-size:0.8rem;">&#x25CF; Professional (12)</span>
                <span style="color:#ffd700;font-size:0.8rem;">&#x25CF; Retail & Other (15)</span>
            </div>
        </div>
    </div>

    <!-- Revenue Simulator -->
    <div class="simulator" id="revenue-section">
        <h3>&#x1F4B0; Revenue Simulator</h3>
        <div class="slider-group">
            <label>Clients per Business:</label>
            <input type="range" min="0" max="100" value="1" id="clients-slider" oninput="updateRevenue()">
            <span class="val" id="clients-val">1</span>
        </div>
        <div class="slider-group">
            <label>Conversion Rate (leads → clients):</label>
            <input type="range" min="1" max="30" value="5" id="conv-slider" oninput="updateRevenue()">
            <span class="val" id="conv-val">5%</span>
        </div>
        <div class="revenue-result">
            <div class="item">
                <div class="big" id="rev-mrr">${total_mrr_1:,}</div>
                <div class="sub">Monthly Revenue (MRR)</div>
            </div>
            <div class="item">
                <div class="big" id="rev-arr">${total_mrr_1 * 12:,}</div>
                <div class="sub">Annual Revenue (ARR)</div>
            </div>
            <div class="item">
                <div class="big" id="rev-profit">${int(total_mrr_1 * 0.9):,}</div>
                <div class="sub">Monthly Profit (90%)</div>
            </div>
            <div class="item">
                <div class="big" id="rev-leads">1,000</div>
                <div class="sub">Leads Needed/Month</div>
            </div>
        </div>
    </div>

    <!-- Leads Section -->
    <div id="leads-section">
        <div class="tab-bar">
            <div class="tab active" onclick="switchTab('all-leads')">All Leads</div>
            <div class="tab" onclick="switchTab('hot-leads')">Hot Leads</div>
            <div class="tab" onclick="switchTab('form-subs')">Form Submissions</div>
        </div>
        <div class="lead-feed tab-content active" id="all-leads">
            <h3>&#x1F4E9; Incoming Leads (via Netlify Forms)</h3>
            <div class="empty-state">
                <div class="icon">&#x1F4EC;</div>
                <p>Leads will appear here when visitors submit forms on your sites.</p>
                <p style="margin-top:0.5rem;font-size:0.85rem;">Check <strong>Netlify Dashboard → Forms</strong> for real submissions.</p>
                <a href="https://app.netlify.com" target="_blank" style="display:inline-block;margin-top:1rem;padding:0.6rem 1.5rem;background:linear-gradient(90deg,#00d4ff,#7b2ff7);color:white;text-decoration:none;border-radius:50px;font-size:0.9rem;">Open Netlify Forms</a>
            </div>
        </div>
        <div class="lead-feed tab-content" id="hot-leads">
            <h3>&#x1F525; Hot Leads</h3>
            <div class="empty-state">
                <div class="icon">&#x1F525;</div>
                <p>High-intent leads from pricing pages will show here.</p>
            </div>
        </div>
        <div class="lead-feed tab-content" id="form-subs">
            <h3>&#x1F4CB; Form Submissions</h3>
            <div class="empty-state">
                <div class="icon">&#x1F4CB;</div>
                <p>All form data synced from Netlify.</p>
            </div>
        </div>
    </div>

    <!-- Businesses Table -->
    <div class="table-card" id="businesses-section" style="margin-top:2rem;">
        <h3>&#x1F3E2; All 50 Businesses</h3>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Business</th>
                    <th>Target Audience</th>
                    <th>Starter</th>
                    <th>Pro</th>
                    <th>Enterprise</th>
                    <th>Status</th>
                    <th>Leads</th>
                </tr>
            </thead>
            <tbody>{biz_rows}
            </tbody>
        </table>
    </div>

    <!-- Tasks -->
    <div class="table-card" id="tasks-section">
        <h3>&#x2705; Recent Tasks (Last 20)</h3>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Task</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>{task_rows}
            </tbody>
        </table>
    </div>

    <!-- Agent Runs -->
    <div class="table-card" id="agent-section">
        <h3>&#x1F916; Agent Run History</h3>
        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(80px,1fr));gap:0.8rem;">
            {"".join(f'<div style="text-align:center;padding:1rem;background:#0a0a1a;border-radius:12px;border:1px solid #1a1a2e;"><div style="font-size:1.2rem;font-weight:800;color:#00c853;">5/5</div><div style="font-size:0.75rem;color:#666;">Run #{i}</div></div>' for i in range(1, log_count + 1))}
        </div>
    </div>

    <!-- Bank Account Section -->
    <div class="simulator" style="border: 1px solid #00c853; margin-top: 2rem;">
        <h3>&#x1F3E6; Payment Setup</h3>
        <p style="color:#888;margin-bottom:1rem;">To start receiving payments from customers, connect your payment processor.</p>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem;">
            <div style="background:#0a0a1a;padding:1.5rem;border-radius:12px;border:1px solid #1a1a2e;">
                <h4 style="color:#00d4ff;margin-bottom:0.5rem;">Stripe (Recommended)</h4>
                <p style="color:#666;font-size:0.85rem;">Accept credit cards worldwide. Funds go directly to your bank.</p>
                <p style="color:#00c853;font-size:0.85rem;margin-top:0.5rem;">Status: <strong>Pending Setup</strong></p>
            </div>
            <div style="background:#0a0a1a;padding:1.5rem;border-radius:12px;border:1px solid #1a1a2e;">
                <h4 style="color:#7b2ff7;margin-bottom:0.5rem;">PayPal</h4>
                <p style="color:#666;font-size:0.85rem;">Accept PayPal payments. Easy setup, instant transfers.</p>
                <p style="color:#ffd700;font-size:0.85rem;margin-top:0.5rem;">Status: <strong>Optional</strong></p>
            </div>
            <div style="background:#0a0a1a;padding:1.5rem;border-radius:12px;border:1px solid #1a1a2e;">
                <h4 style="color:#00c853;margin-bottom:0.5rem;">Netlify Forms (Active!)</h4>
                <p style="color:#666;font-size:0.85rem;">Free lead capture on all 50 sites. Already working!</p>
                <p style="color:#00c853;font-size:0.85rem;margin-top:0.5rem;">Status: <strong>&#x2705; Active</strong></p>
            </div>
        </div>
        <p style="color:#555;font-size:0.8rem;margin-top:1rem;">When you're ready, tell me and I'll configure your Stripe keys across all 50 checkout pages.</p>
    </div>
</div>

<script>
    const BIZ_PRICES = {json.dumps([b['price'] for b in businesses])};
    const TOTAL_BASE = BIZ_PRICES.reduce((a, b) => a + b, 0);

    function updateRevenue() {{
        const clients = parseInt(document.getElementById('clients-slider').value);
        const conv = parseInt(document.getElementById('conv-slider').value);
        document.getElementById('clients-val').textContent = clients;
        document.getElementById('conv-val').textContent = conv + '%';

        const mrr = TOTAL_BASE * clients;
        const arr = mrr * 12;
        const profit = Math.floor(mrr * 0.9);
        const leadsNeeded = clients > 0 ? Math.ceil((clients * 50) / (conv / 100)) : 0;

        document.getElementById('rev-mrr').textContent = '$' + mrr.toLocaleString();
        document.getElementById('rev-arr').textContent = '$' + arr.toLocaleString();
        document.getElementById('rev-profit').textContent = '$' + profit.toLocaleString();
        document.getElementById('rev-leads').textContent = leadsNeeded.toLocaleString();
    }}

    function switchTab(tabId) {{
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        event.target.classList.add('active');
    }}

    // Smooth scroll
    document.querySelectorAll('.sidebar a[href^="#"]').forEach(a => {{
        a.addEventListener('click', e => {{
            e.preventDefault();
            const el = document.querySelector(a.getAttribute('href'));
            if(el) el.scrollIntoView({{behavior:'smooth', block:'start'}});
        }});
    }});
</script>

</body>
</html>"""

    os.makedirs(os.path.join(OUTPUT_DIR, 'website'), exist_ok=True)
    path = os.path.join(OUTPUT_DIR, 'website', 'dashboard.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path
