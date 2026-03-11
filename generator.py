"""
Proposal Generator Engine
Takes form data, uses Claude to write proposal sections, generates HTML, pushes to GitHub Pages.
"""
import os
import re
import json
import base64
import urllib.request
from datetime import datetime
from pathlib import Path

from config.settings import (
    GITHUB_TOKEN, GITHUB_REPO, GITHUB_PAGES_BASE,
    ANTHROPIC_API_KEY, PROPOSALS_DIR, EMAILS_DIR
)
from template import generate_proposal_html


def slugify(text: str) -> str:
    """Convert company name to URL slug."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def filename_from_slug(slug: str) -> str:
    """Convert slug to filename."""
    return f"{slug.replace('-', '_')}_proposal.html"


def call_claude(prompt: str) -> str:
    """Call Claude API to generate proposal content."""
    data = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        method="POST"
    )
    req.add_header("x-api-key", ANTHROPIC_API_KEY)
    req.add_header("anthropic-version", "2023-06-01")
    req.add_header("content-type", "application/json")

    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    return result["content"][0]["text"]


def generate_proposal_content(form_data: dict) -> dict:
    """
    Use Claude to generate the Problem, Solution, and Scope sections
    from the brief form inputs.
    """
    prompt = f"""You are writing a professional service proposal for Love Shots Media (Cameron Williams, AI Automations Engineer).

RULES:
- Write in FIRST PERSON as Cameron. Say "I will" not "we will".
- NEVER use em dashes.
- NEVER use these phrases: "while you sleep", "on autopilot", "set it and forget it", "the future of", "game-changer", "revolutionize", "leverage AI", "harness the power", "in today's fast-paced", "no fluff", "case study", "link in bio"
- NEVER use the pattern "This isn't X, it's Y" or "It's not about X, it's about Y"
- Keep paragraphs short (2-3 sentences max)
- Use clear, direct language. No filler.
- Output ONLY valid HTML (p tags, ul/li tags, div tags with classes). No markdown.

CLIENT INFO:
- Company: {form_data['client_name']}
- Contact: {form_data['contact_name']}
- Industry: {form_data.get('industry', 'local service business')}
- Service requested: {form_data['service_type']}

PROBLEM CONTEXT (from Cameron's call notes):
{form_data['problem_notes']}

SOLUTION CONTEXT:
{form_data['solution_notes']}

TECH STACK:
{form_data['tech_stack']}

DELIVERABLES:
{form_data.get('deliverables', 'Video SOP, Text SOP, live training session')}

---

Generate THREE sections as a JSON object with these exact keys:

1. "problem_html" - The Problem section. 2-3 paragraphs explaining the client's pain points. Include a div with class "pain-points" containing a ul with 3-4 specific pain points (each li has a <strong> label followed by description). End with a closing paragraph about the cost of inaction.

2. "solution_html" - The Solution section. Start with a paragraph about what Cameron will build. Then use multiple divs with class "workflow-step", each containing a p with class "step-title" (formatted as "Step 01 - Title") and description paragraphs/lists. End with a summary paragraph about the impact.

3. "scope_html" - The Scope of Work section. Use h3 tags for each category (A. System Design, B. [Main Build], C. [Integrations], etc.). Under each h3, use ul/li for specific deliverables. Always end with an "F. Documentation & Training" section that includes video SOP, text SOP, and live training.

Return ONLY valid JSON. No explanation, no markdown code fences."""

    raw = call_claude(prompt)

    # Clean up potential markdown fences
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r'^```(?:json)?\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)

    return json.loads(raw)


def generate_includes_list(form_data: dict) -> list:
    """Generate the 'What's Included' list from form data."""
    includes = [
        "Full system design, build, integration, and testing",
    ]

    service = form_data.get('service_type', '').lower()
    if 'voice' in service or 'vapi' in form_data.get('tech_stack', '').lower():
        includes.append("Custom AI Voice Agent configuration and training")

    tech = form_data.get('tech_stack', '')
    if 'ghl' in tech.lower() or 'go high level' in tech.lower():
        includes.append("Go High Level CRM setup and automation workflows")
    if 'housecall' in tech.lower():
        includes.append("HouseCall Pro job routing and scheduling automation")
    if 'railway' in tech.lower():
        includes.append("Railway backend deployment for production reliability")
    if 'make' in tech.lower():
        includes.append("Make.com automation workflows")
    if 'twilio' in tech.lower():
        includes.append("Twilio call handling and conferencing setup")

    includes.append("Video SOP documenting every system component")
    includes.append("Written text SOP for quick reference")

    days = form_data.get('maintenance_days', 14)
    includes.append(f"{days} days of free maintenance post-launch for optimization and debugging")

    return includes


def push_to_github(filepath: str, content: str) -> bool:
    """Push a file to the GitHub repo via Contents API."""
    encoded = base64.b64encode(content.encode()).decode()

    # Check if file exists (to get SHA for updates)
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filepath}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")

    sha = None
    try:
        resp = urllib.request.urlopen(req)
        existing = json.loads(resp.read())
        sha = existing.get("sha")
    except urllib.error.HTTPError:
        pass

    payload = {
        "message": f"Add/update proposal: {filepath}",
        "content": encoded,
    }
    if sha:
        payload["sha"] = sha

    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="PUT")
    req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")

    try:
        urllib.request.urlopen(req)
        return True
    except urllib.error.HTTPError as e:
        print(f"GitHub push error: {e.code} {e.read().decode()[:200]}")
        return False


def generate_email_draft(form_data: dict, proposal_url: str) -> str:
    """Generate a casual email draft."""
    name = form_data.get('contact_name', 'there')
    service = form_data.get('service_type', 'the system')

    return f"""{name},

Good talking to you. Here's the full proposal for the {service.lower()} we discussed:

{proposal_url}

Everything's broken down in there - the problem, how I'm solving it, timeline, and pricing. The payment link is at the bottom when you're ready to move forward.

Let me know if you have any questions.

Cameron"""


def run_proposal_generation(form_data: dict) -> dict:
    """
    Main entry point. Takes form data, generates everything, returns results.

    Returns:
        {
            "proposal_url": str,
            "email_draft": str,
            "local_path": str,
            "success": bool,
            "error": str | None
        }
    """
    try:
        # 1. Generate content via Claude
        content = generate_proposal_content(form_data)

        # 2. Build template data
        price = form_data['total_price']
        price_num = float(re.sub(r'[^\d.]', '', price))
        deposit_num = price_num / 2

        slug = slugify(form_data['client_name'])
        filename = filename_from_slug(slug)

        template_data = {
            "client_name": form_data['client_name'],
            "contact_name": form_data['contact_name'],
            "project_title": form_data['project_title'],
            "project_subtitle": form_data.get('project_subtitle', ''),
            "date": form_data.get('date', datetime.now().strftime("%B %d, %Y")),
            "problem_html": content['problem_html'],
            "solution_html": content['solution_html'],
            "scope_html": content['scope_html'],
            "timeline_rows": form_data.get('timeline_rows', []),
            "timeline_total": form_data.get('timeline_total', '2 - 4 Weeks'),
            "total_price": f"${price_num:,.0f}",
            "total_price_raw": price_num,
            "deposit_amount": f"${deposit_num:,.2f}",
            "final_amount": f"${deposit_num:,.2f}",
            "includes": generate_includes_list(form_data),
            "software_rows": form_data.get('software_rows', []),
            "software_note": form_data.get('software_note', ''),
            "payment_link": form_data.get('payment_link', '#PAYMENT_LINK_PLACEHOLDER'),
            "maintenance_days": form_data.get('maintenance_days', 14),
        }

        # 3. Generate HTML
        html = generate_proposal_html(template_data)

        # 4. Save locally
        local_path = PROPOSALS_DIR / filename
        local_path.write_text(html, encoding="utf-8")

        # 5. Push to GitHub Pages
        github_path = f"proposals/{filename}"
        pushed = push_to_github(github_path, html)

        proposal_url = f"{GITHUB_PAGES_BASE}/{github_path}"

        # 6. Generate email draft
        email = generate_email_draft(form_data, proposal_url)
        email_path = EMAILS_DIR / f"{slug}_email.txt"
        email_path.write_text(email, encoding="utf-8")

        return {
            "success": True,
            "proposal_url": proposal_url,
            "email_draft": email,
            "local_path": str(local_path),
            "pushed_to_github": pushed,
            "error": None,
        }

    except Exception as e:
        return {
            "success": False,
            "proposal_url": None,
            "email_draft": None,
            "local_path": None,
            "error": str(e),
        }
