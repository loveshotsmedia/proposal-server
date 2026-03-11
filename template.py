"""
Proposal HTML Template Generator
Produces branded Love Shots Media proposals.
"""


def generate_proposal_html(data: dict) -> str:
    """
    Generate a full branded HTML proposal from structured data.

    data keys:
        client_name: str - Company name
        contact_name: str - Contact person's first name
        project_title: str - e.g. "AI Voice Assistant"
        project_subtitle: str - e.g. "Inbound Call Automation & Job Scheduling System"
        date: str - e.g. "March 10, 2026"
        problem_html: str - Problem section content (HTML)
        solution_html: str - Solution section content (HTML)
        scope_html: str - Scope of work section content (HTML)
        timeline_rows: list[dict] - [{phase, deliverable, duration}, ...]
        timeline_total: str - e.g. "2 - 3 Weeks"
        total_price: str - e.g. "$5,250"
        total_price_raw: float - e.g. 5250.0
        deposit_amount: str - e.g. "$2,625"
        final_amount: str - e.g. "$2,625"
        includes: list[str] - What's included bullet points
        software_rows: list[dict] - [{name, purpose, cost}, ...]
        software_note: str - Note below software table
        payment_link: str - PayPal payment URL
        maintenance_days: int - Post-launch maintenance days (default 14)
    """

    # Build timeline rows HTML
    timeline_html = ""
    for i, row in enumerate(data.get("timeline_rows", []), 1):
        timeline_html += f"""
                    <tr>
                        <td><span class="phase-label">Phase {i}</span></td>
                        <td>{row['deliverable']}</td>
                        <td>{row['duration']}</td>
                    </tr>"""

    # Build includes HTML
    includes_html = ""
    for item in data.get("includes", []):
        includes_html += f"\n                    <li>{item}</li>"

    # Build software rows HTML
    software_html = ""
    for row in data.get("software_rows", []):
        software_html += f"""
                    <tr>
                        <td>{row['name']}</td>
                        <td>{row['purpose']}</td>
                        <td>{row['cost']}</td>
                    </tr>"""

    payment_link = data.get("payment_link", "#")
    deposit = data.get("deposit_amount", "$0")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['project_title']} Proposal &mdash; {data['client_name']}</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background-color: #0a0a0a; color: #b0b0b0; font-family: 'Outfit', sans-serif; line-height: 1.7; -webkit-font-smoothing: antialiased; }}
        .proposal-container {{ max-width: 820px; margin: 0 auto; padding: 0 32px; }}
        .hero {{ background: linear-gradient(180deg, #0f0f0f 0%, #0a0a0a 100%); border-bottom: 1px solid rgba(212, 175, 55, 0.15); padding: 60px 0 48px; text-align: center; }}
        .brand-name {{ font-family: 'Space Mono', monospace; font-size: 14px; letter-spacing: 4px; text-transform: uppercase; color: #d4af37; margin-bottom: 40px; }}
        .hero h1 {{ font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 38px; color: #ffffff; margin-bottom: 8px; line-height: 1.2; }}
        .hero .subtitle {{ font-family: 'Outfit', sans-serif; font-weight: 300; font-size: 18px; color: #b0b0b0; margin-bottom: 8px; }}
        .hero .prepared-for {{ font-family: 'Space Mono', monospace; font-size: 13px; color: rgba(212, 175, 55, 0.5); letter-spacing: 2px; text-transform: uppercase; margin-top: 32px; }}
        .hero .client-name {{ font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 22px; color: #d4af37; margin-top: 8px; }}
        .hero .date-line {{ font-family: 'Space Mono', monospace; font-size: 12px; color: rgba(255, 255, 255, 0.25); margin-top: 16px; }}
        .section {{ padding: 56px 0; border-bottom: 1px solid rgba(212, 175, 55, 0.1); }}
        .section:last-of-type {{ border-bottom: none; }}
        .section-number {{ font-family: 'Space Mono', monospace; font-size: 12px; color: #d4af37; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 8px; }}
        .section h2 {{ font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 28px; color: #ffffff; margin-bottom: 24px; }}
        .section h3 {{ font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 18px; color: #e8e8e8; margin-top: 32px; margin-bottom: 12px; }}
        .section p {{ font-size: 15px; color: #b0b0b0; margin-bottom: 16px; line-height: 1.8; }}
        .section ul {{ list-style: none; padding-left: 0; margin-bottom: 16px; }}
        .section ul li {{ position: relative; padding-left: 24px; margin-bottom: 10px; font-size: 15px; color: #b0b0b0; line-height: 1.7; }}
        .section ul li::before {{ content: '\\25B8'; position: absolute; left: 0; color: #d4af37; font-size: 14px; }}
        .highlight-text {{ color: #e0e0e0; font-weight: 500; }}
        .gold-text {{ color: #d4af37; font-weight: 600; }}
        .pain-points {{ background: #0f0f0f; border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 8px; padding: 28px 32px; margin: 24px 0; }}
        .pain-points li {{ margin-bottom: 14px; }}
        .pain-points li strong {{ color: #e8e8e8; }}
        .workflow-step {{ background: #0f0f0f; border-left: 3px solid #d4af37; padding: 20px 24px; margin-bottom: 16px; border-radius: 0 6px 6px 0; }}
        .workflow-step .step-title {{ font-family: 'Space Mono', monospace; font-size: 13px; color: #d4af37; letter-spacing: 1px; margin-bottom: 8px; }}
        .workflow-step p {{ margin-bottom: 8px; font-size: 14px; }}
        .workflow-step ul {{ margin-top: 8px; }}
        .workflow-step ul li {{ font-size: 14px; margin-bottom: 6px; }}
        .timeline-table {{ width: 100%; border-collapse: collapse; margin: 24px 0; }}
        .timeline-table thead th {{ font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: #d4af37; text-align: left; padding: 12px 16px; border-bottom: 1px solid rgba(212, 175, 55, 0.3); }}
        .timeline-table tbody td {{ font-size: 14px; color: #b0b0b0; padding: 14px 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }}
        .timeline-table tbody tr:hover {{ background: rgba(212, 175, 55, 0.05); }}
        .timeline-table .phase-label {{ font-family: 'Space Mono', monospace; font-size: 12px; color: rgba(212, 175, 55, 0.5); }}
        .timeline-total {{ background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 6px; padding: 16px 24px; margin-top: 16px; display: flex; justify-content: space-between; align-items: center; }}
        .timeline-total span:first-child {{ font-family: 'Space Mono', monospace; font-size: 13px; color: #e8e8e8; letter-spacing: 1px; }}
        .timeline-total span:last-child {{ font-family: 'Space Mono', monospace; font-size: 15px; color: #d4af37; font-weight: 700; }}
        .investment-card {{ background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 12px; padding: 40px; margin: 24px 0; text-align: center; }}
        .investment-card .total-label {{ font-family: 'Space Mono', monospace; font-size: 12px; color: rgba(212, 175, 55, 0.5); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 8px; }}
        .investment-card .total-amount {{ font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 48px; color: #d4af37; margin-bottom: 4px; }}
        .investment-card .total-sub {{ font-size: 14px; color: rgba(255, 255, 255, 0.25); margin-bottom: 32px; }}
        .payment-split {{ display: flex; gap: 24px; margin-top: 24px; }}
        .payment-split .split-box {{ flex: 1; background: rgba(212, 175, 55, 0.06); border: 1px solid rgba(212, 175, 55, 0.12); border-radius: 8px; padding: 20px; }}
        .split-box .split-label {{ font-family: 'Space Mono', monospace; font-size: 11px; color: rgba(212, 175, 55, 0.5); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }}
        .split-box .split-amount {{ font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 24px; color: #e8e8e8; margin-bottom: 6px; }}
        .split-box .split-note {{ font-size: 13px; color: #b0b0b0; }}
        .includes-list {{ background: #0f0f0f; border-radius: 8px; padding: 28px 32px; margin: 24px 0; }}
        .includes-list .includes-title {{ font-family: 'Space Mono', monospace; font-size: 12px; color: #d4af37; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px; }}
        .includes-list ul li::before {{ content: '\\2713'; color: #d4af37; font-weight: 700; }}
        .software-table {{ width: 100%; border-collapse: collapse; margin: 24px 0; }}
        .software-table thead th {{ font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: #d4af37; text-align: left; padding: 12px 16px; border-bottom: 1px solid rgba(212, 175, 55, 0.3); }}
        .software-table tbody td {{ font-size: 14px; color: #b0b0b0; padding: 14px 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }}
        .software-table tbody td:first-child {{ color: #e8e8e8; font-weight: 500; }}
        .software-table tbody tr:hover {{ background: rgba(212, 175, 55, 0.05); }}
        .software-note {{ font-size: 13px; color: rgba(255, 255, 255, 0.25); font-style: italic; margin-top: 16px; }}
        .cta-section {{ text-align: center; padding: 56px 0 40px; }}
        .cta-section h2 {{ font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 28px; color: #ffffff; margin-bottom: 16px; }}
        .cta-section p {{ font-size: 15px; color: #b0b0b0; margin-bottom: 32px; }}
        .cta-button {{ display: inline-block; background: linear-gradient(135deg, #d4af37 0%, #b8962e 100%); color: #0a0a0a; font-family: 'Space Mono', monospace; font-size: 14px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; text-decoration: none; padding: 18px 48px; border-radius: 6px; transition: all 0.3s ease; box-shadow: 0 4px 24px rgba(212, 175, 55, 0.3); }}
        .cta-button:hover {{ box-shadow: 0 6px 32px rgba(212, 175, 55, 0.5); transform: translateY(-2px); }}
        .footer {{ border-top: 1px solid rgba(212, 175, 55, 0.1); padding: 40px 0; text-align: center; }}
        .footer .footer-brand {{ font-family: 'Space Mono', monospace; font-size: 12px; letter-spacing: 3px; color: rgba(212, 175, 55, 0.5); text-transform: uppercase; margin-bottom: 8px; }}
        .footer p {{ font-size: 13px; color: rgba(255, 255, 255, 0.2); margin-bottom: 4px; }}
        .footer a {{ color: rgba(212, 175, 55, 0.5); text-decoration: none; }}
        .footer a:hover {{ color: #d4af37; }}
        .gold-divider {{ width: 60px; height: 2px; background: linear-gradient(90deg, #d4af37, rgba(212, 175, 55, 0.2)); margin: 0 auto 32px; }}
        @media (max-width: 640px) {{
            .hero h1 {{ font-size: 28px; }}
            .investment-card .total-amount {{ font-size: 36px; }}
            .payment-split {{ flex-direction: column; gap: 12px; }}
            .proposal-container {{ padding: 0 20px; }}
            .investment-card {{ padding: 28px 20px; }}
        }}
        @media print {{
            body {{ background: #0a0a0a; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .cta-button {{ box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <header class="hero">
        <div class="proposal-container">
            <div class="brand-name">Love Shots Media</div>
            <h1>{data['project_title']}</h1>
            <p class="subtitle">{data['project_subtitle']}</p>
            <p class="prepared-for">Prepared For</p>
            <p class="client-name">{data['client_name']}</p>
            <p class="date-line">{data['date']}</p>
        </div>
    </header>

    <main class="proposal-container">

        <section class="section">
            <p class="section-number">01</p>
            <h2>Problem</h2>
            {data['problem_html']}
        </section>

        <section class="section">
            <p class="section-number">02</p>
            <h2>Solution</h2>
            {data['solution_html']}
        </section>

        <section class="section">
            <p class="section-number">03</p>
            <h2>Scope of Work</h2>
            {data['scope_html']}
        </section>

        <section class="section">
            <p class="section-number">04</p>
            <h2>Timeline</h2>
            <table class="timeline-table">
                <thead>
                    <tr>
                        <th>Phase</th>
                        <th>Deliverable</th>
                        <th>Duration</th>
                    </tr>
                </thead>
                <tbody>{timeline_html}
                </tbody>
            </table>
            <div class="timeline-total">
                <span>Total Estimated Timeline</span>
                <span>{data['timeline_total']}</span>
            </div>
        </section>

        <section class="section">
            <p class="section-number">05</p>
            <h2>Investment</h2>
            <div class="investment-card">
                <p class="total-label">Total Project Investment</p>
                <p class="total-amount">{data['total_price']}</p>
                <p class="total-sub">One-time engineering and setup fee</p>
                <div class="payment-split">
                    <div class="split-box">
                        <p class="split-label">Due at Signing</p>
                        <p class="split-amount">{data['deposit_amount']}</p>
                        <p class="split-note">50% upfront to begin project</p>
                    </div>
                    <div class="split-box">
                        <p class="split-label">Due at Delivery</p>
                        <p class="split-amount">{data['final_amount']}</p>
                        <p class="split-note">50% upon full system delivery &amp; verification</p>
                    </div>
                </div>
            </div>
            <div class="includes-list">
                <p class="includes-title">What's Included</p>
                <ul>{includes_html}
                </ul>
            </div>
        </section>

        <section class="section">
            <p class="section-number">06</p>
            <h2>Ongoing Software Requirements</h2>
            <table class="software-table">
                <thead>
                    <tr>
                        <th>Software</th>
                        <th>Purpose</th>
                        <th>Cost</th>
                    </tr>
                </thead>
                <tbody>{software_html}
                </tbody>
            </table>
            <p class="software-note">{data.get('software_note', '')}</p>
        </section>

        <section class="cta-section">
            <div class="gold-divider"></div>
            <h2>Ready to Get Started?</h2>
            <p>Click below to submit your first payment of {deposit} and I'll begin building your system immediately.</p>
            <a href="{payment_link}" class="cta-button">Submit Payment &mdash; {deposit}</a>
            <p style="margin-top: 24px; font-size: 13px; color: rgba(255,255,255,0.2);">Secure payment processed via PayPal</p>
        </section>

    </main>

    <footer class="footer">
        <div class="proposal-container">
            <p class="footer-brand">Love Shots Media</p>
            <p>Cameron Williams &mdash; AI Automations Engineer</p>
            <p><a href="https://loveshotsmedia.com">loveshotsmedia.com</a></p>
            <p style="margin-top: 16px;">Instagram: <a href="https://instagram.com/rich_off_ai_">@rich_off_ai_</a> &middot; YouTube: <a href="https://youtube.com/@rich_off_ai_">@rich_off_ai_</a></p>
        </div>
    </footer>
</body>
</html>"""
