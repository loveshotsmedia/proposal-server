"""
Proposal Generator - Local Form Server
Run this, fill out the form at localhost:9090, get a live proposal link.
"""
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from generator import run_proposal_generation

app = FastAPI(title="Proposal Generator")

FORM_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proposal Generator - Love Shots Media</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a0a; color: #b0b0b0; font-family: 'Outfit', sans-serif; line-height: 1.6; }
        .container { max-width: 740px; margin: 0 auto; padding: 40px 32px; }

        h1 { font-size: 32px; color: #ffffff; margin-bottom: 4px; }
        .subtitle { font-family: 'Space Mono', monospace; font-size: 12px; color: #d4af37; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 40px; }

        .form-section { margin-bottom: 36px; }
        .form-section-title {
            font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: 2px;
            text-transform: uppercase; color: #d4af37; margin-bottom: 16px;
            padding-bottom: 8px; border-bottom: 1px solid rgba(212,175,55,0.15);
        }

        .form-row { display: flex; gap: 16px; margin-bottom: 16px; }
        .form-row.single { flex-direction: column; }
        .form-group { flex: 1; display: flex; flex-direction: column; }

        label {
            font-size: 13px; color: #e0e0e0; margin-bottom: 6px; font-weight: 500;
        }
        input, textarea, select {
            background: #0f0f0f; border: 1px solid rgba(255,255,255,0.1);
            border-radius: 6px; padding: 12px 14px; color: #e8e8e8;
            font-family: 'Outfit', sans-serif; font-size: 14px;
            transition: border-color 0.2s;
        }
        input:focus, textarea:focus, select:focus {
            outline: none; border-color: rgba(212,175,55,0.5);
        }
        textarea { resize: vertical; min-height: 100px; }
        select { cursor: pointer; }
        select option { background: #0f0f0f; }

        .help-text { font-size: 12px; color: rgba(255,255,255,0.25); margin-top: 4px; }

        /* Timeline rows */
        .timeline-builder { margin-top: 8px; }
        .timeline-row { display: flex; gap: 12px; margin-bottom: 8px; align-items: center; }
        .timeline-row input { flex: 1; }
        .timeline-row input:first-child { flex: 0.4; }
        .timeline-row input:last-of-type { flex: 0.3; }
        .remove-row { background: none; border: 1px solid rgba(255,0,0,0.3); color: #ff4444; border-radius: 4px; padding: 8px 12px; cursor: pointer; font-size: 12px; }
        .remove-row:hover { border-color: #ff4444; }
        .add-row-btn { background: none; border: 1px solid rgba(212,175,55,0.3); color: #d4af37; border-radius: 4px; padding: 8px 16px; cursor: pointer; font-family: 'Space Mono', monospace; font-size: 12px; margin-top: 8px; }
        .add-row-btn:hover { border-color: #d4af37; }

        /* Software rows */
        .software-row { display: flex; gap: 12px; margin-bottom: 8px; align-items: center; }
        .software-row input { flex: 1; }

        /* Submit */
        .submit-btn {
            display: block; width: 100%; padding: 18px;
            background: linear-gradient(135deg, #d4af37, #b8962e);
            color: #0a0a0a; font-family: 'Space Mono', monospace;
            font-size: 14px; font-weight: 700; letter-spacing: 2px;
            text-transform: uppercase; border: none; border-radius: 6px;
            cursor: pointer; transition: all 0.3s; margin-top: 32px;
            box-shadow: 0 4px 24px rgba(212,175,55,0.3);
        }
        .submit-btn:hover { box-shadow: 0 6px 32px rgba(212,175,55,0.5); transform: translateY(-1px); }
        .submit-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

        /* Result */
        .result { display: none; margin-top: 32px; padding: 32px; background: #0f0f0f; border: 1px solid rgba(212,175,55,0.25); border-radius: 8px; }
        .result.show { display: block; }
        .result.error { border-color: rgba(255,0,0,0.3); }
        .result h3 { color: #d4af37; margin-bottom: 16px; font-size: 18px; }
        .result-url { background: #1a1a1a; padding: 12px 16px; border-radius: 4px; margin: 12px 0; word-break: break-all; }
        .result-url a { color: #d4af37; text-decoration: none; }
        .result-url a:hover { text-decoration: underline; }
        .result-email { background: #1a1a1a; padding: 16px; border-radius: 4px; margin: 12px 0; white-space: pre-wrap; font-size: 14px; color: #e0e0e0; }
        .copy-btn {
            background: none; border: 1px solid rgba(212,175,55,0.3); color: #d4af37;
            padding: 6px 14px; border-radius: 4px; cursor: pointer;
            font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: 1px;
        }
        .copy-btn:hover { border-color: #d4af37; }

        .loading { display: none; text-align: center; margin-top: 24px; }
        .loading.show { display: block; }
        .loading p { color: #d4af37; font-family: 'Space Mono', monospace; font-size: 13px; }
        .spinner { width: 40px; height: 40px; border: 3px solid rgba(212,175,55,0.15); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
<div class="container">
    <h1>Proposal Generator</h1>
    <p class="subtitle">Love Shots Media</p>

    <form id="proposalForm">

        <!-- CLIENT INFO -->
        <div class="form-section">
            <p class="form-section-title">Client Information</p>
            <div class="form-row">
                <div class="form-group">
                    <label>Company Name</label>
                    <input type="text" name="client_name" required placeholder="e.g. Martinelli Plumbing">
                </div>
                <div class="form-group">
                    <label>Contact First Name</label>
                    <input type="text" name="contact_name" required placeholder="e.g. Jason">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Industry</label>
                    <input type="text" name="industry" placeholder="e.g. Plumbing, Med Spa, Insurance">
                </div>
                <div class="form-group">
                    <label>Contact Email</label>
                    <input type="email" name="contact_email" placeholder="For your records">
                </div>
            </div>
        </div>

        <!-- PROJECT INFO -->
        <div class="form-section">
            <p class="form-section-title">Project Details</p>
            <div class="form-row">
                <div class="form-group">
                    <label>Project Title</label>
                    <input type="text" name="project_title" required placeholder="e.g. AI Voice Assistant">
                </div>
                <div class="form-group">
                    <label>Project Subtitle</label>
                    <input type="text" name="project_subtitle" placeholder="e.g. Inbound Call Automation System">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Service Type</label>
                    <select name="service_type">
                        <option value="AI Voice Agent">AI Voice Agent</option>
                        <option value="CRM Automation">CRM Automation</option>
                        <option value="Meta Ad Campaign">Meta Ad Campaign</option>
                        <option value="Cold Email System">Cold Email System</option>
                        <option value="Full Funnel Build">Full Funnel Build</option>
                        <option value="Custom AI System">Custom AI System</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Tech Stack</label>
                    <input type="text" name="tech_stack" required placeholder="e.g. Vapi, GHL, OpenAI, Railway">
                </div>
            </div>
        </div>

        <!-- PROBLEM & SOLUTION -->
        <div class="form-section">
            <p class="form-section-title">Problem & Solution Notes</p>
            <div class="form-row single">
                <div class="form-group">
                    <label>Problem (your call notes)</label>
                    <textarea name="problem_notes" required placeholder="What's the client's pain? What triggered this conversation? What's broken or missing?"></textarea>
                    <p class="help-text">Write like you're telling me what happened on the call. Claude will turn this into professional copy.</p>
                </div>
            </div>
            <div class="form-row single">
                <div class="form-group">
                    <label>Solution (what you're building)</label>
                    <textarea name="solution_notes" required placeholder="What system will you build? What will it do? How does the flow work?"></textarea>
                    <p class="help-text">Describe the system and how it works step by step.</p>
                </div>
            </div>
            <div class="form-row single">
                <div class="form-group">
                    <label>Deliverables</label>
                    <input type="text" name="deliverables" value="Video SOP, Text SOP, live training session" placeholder="e.g. Video SOP, Text SOP, live training">
                </div>
            </div>
        </div>

        <!-- TIMELINE -->
        <div class="form-section">
            <p class="form-section-title">Timeline</p>
            <div class="timeline-builder" id="timelineBuilder">
                <div class="timeline-row">
                    <input type="text" placeholder="Phase 1" disabled style="opacity:0.5">
                    <input type="text" name="tl_deliverable[]" placeholder="Deliverable" value="System Architecture & Design">
                    <input type="text" name="tl_duration[]" placeholder="Duration" value="2-3 Days">
                    <button type="button" class="remove-row" onclick="this.parentElement.remove()">x</button>
                </div>
                <div class="timeline-row">
                    <input type="text" placeholder="Phase 2" disabled style="opacity:0.5">
                    <input type="text" name="tl_deliverable[]" placeholder="Deliverable">
                    <input type="text" name="tl_duration[]" placeholder="Duration">
                    <button type="button" class="remove-row" onclick="this.parentElement.remove()">x</button>
                </div>
            </div>
            <button type="button" class="add-row-btn" onclick="addTimelineRow()">+ Add Phase</button>
            <div class="form-row" style="margin-top: 16px;">
                <div class="form-group">
                    <label>Total Timeline</label>
                    <input type="text" name="timeline_total" value="2 - 3 Weeks" placeholder="e.g. 2 - 3 Weeks">
                </div>
            </div>
        </div>

        <!-- PRICING -->
        <div class="form-section">
            <p class="form-section-title">Investment</p>
            <div class="form-row">
                <div class="form-group">
                    <label>Total Price</label>
                    <input type="text" name="total_price" required placeholder="e.g. $5,250">
                </div>
                <div class="form-group">
                    <label>Maintenance Days (post-launch)</label>
                    <input type="number" name="maintenance_days" value="14">
                </div>
            </div>
            <div class="form-row single">
                <div class="form-group">
                    <label>PayPal Payment Link</label>
                    <input type="url" name="payment_link" placeholder="https://www.paypal.com/invoice/p/...">
                    <p class="help-text">Leave blank if not ready yet. You can update later.</p>
                </div>
            </div>
        </div>

        <!-- SOFTWARE -->
        <div class="form-section">
            <p class="form-section-title">Ongoing Software Requirements</p>
            <div id="softwareBuilder">
                <div class="software-row">
                    <input type="text" name="sw_name[]" placeholder="Software" value="Go High Level (GHL)">
                    <input type="text" name="sw_purpose[]" placeholder="Purpose" value="CRM, lead tracking, follow-up automation">
                    <input type="text" name="sw_cost[]" placeholder="Cost" value="$97/month">
                    <button type="button" class="remove-row" onclick="this.parentElement.remove()">x</button>
                </div>
                <div class="software-row">
                    <input type="text" name="sw_name[]" placeholder="Software">
                    <input type="text" name="sw_purpose[]" placeholder="Purpose">
                    <input type="text" name="sw_cost[]" placeholder="Cost">
                    <button type="button" class="remove-row" onclick="this.parentElement.remove()">x</button>
                </div>
            </div>
            <button type="button" class="add-row-btn" onclick="addSoftwareRow()">+ Add Software</button>
            <div class="form-row single" style="margin-top: 16px;">
                <div class="form-group">
                    <label>Software Note</label>
                    <input type="text" name="software_note" placeholder="e.g. Vapi and AI model costs scale with call volume...">
                </div>
            </div>
        </div>

        <button type="submit" class="submit-btn" id="submitBtn">Generate Proposal</button>
    </form>

    <div class="loading" id="loading">
        <div class="spinner"></div>
        <p>Generating proposal via Claude...</p>
        <p style="color: rgba(255,255,255,0.25); font-size: 12px; margin-top: 8px;">This takes about 15-30 seconds</p>
    </div>

    <div class="result" id="result">
        <h3>Proposal Generated</h3>
        <p style="margin-bottom: 12px;">Live proposal link:</p>
        <div class="result-url">
            <a id="proposalLink" href="#" target="_blank"></a>
            <button class="copy-btn" style="float:right; margin-top: -4px;" onclick="copyToClipboard(document.getElementById('proposalLink').href)">Copy Link</button>
        </div>
        <p style="margin-top: 24px; margin-bottom: 12px;">Email draft (ready to copy):</p>
        <div class="result-email" id="emailDraft"></div>
        <button class="copy-btn" style="margin-top: 8px;" onclick="copyToClipboard(document.getElementById('emailDraft').textContent)">Copy Email</button>
    </div>
</div>

<script>
    let phaseCount = 2;

    function addTimelineRow() {
        phaseCount++;
        const row = document.createElement('div');
        row.className = 'timeline-row';
        row.innerHTML = `
            <input type="text" placeholder="Phase ${phaseCount}" disabled style="opacity:0.5">
            <input type="text" name="tl_deliverable[]" placeholder="Deliverable">
            <input type="text" name="tl_duration[]" placeholder="Duration">
            <button type="button" class="remove-row" onclick="this.parentElement.remove()">x</button>
        `;
        document.getElementById('timelineBuilder').appendChild(row);
    }

    function addSoftwareRow() {
        const row = document.createElement('div');
        row.className = 'software-row';
        row.innerHTML = `
            <input type="text" name="sw_name[]" placeholder="Software">
            <input type="text" name="sw_purpose[]" placeholder="Purpose">
            <input type="text" name="sw_cost[]" placeholder="Cost">
            <button type="button" class="remove-row" onclick="this.parentElement.remove()">x</button>
        `;
        document.getElementById('softwareBuilder').appendChild(row);
    }

    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            const btn = event.target;
            const original = btn.textContent;
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = original, 1500);
        });
    }

    document.getElementById('proposalForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const form = e.target;
        const btn = document.getElementById('submitBtn');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');

        btn.disabled = true;
        loading.classList.add('show');
        result.classList.remove('show');

        // Collect form data
        const fd = new FormData(form);
        const data = {};

        // Simple fields
        for (const [key, val] of fd.entries()) {
            if (!key.endsWith('[]')) data[key] = val;
        }

        // Timeline rows
        const deliverables = fd.getAll('tl_deliverable[]');
        const durations = fd.getAll('tl_duration[]');
        data.timeline_rows = [];
        for (let i = 0; i < deliverables.length; i++) {
            if (deliverables[i].trim()) {
                data.timeline_rows.push({
                    deliverable: deliverables[i],
                    duration: durations[i] || 'TBD'
                });
            }
        }

        // Software rows
        const swNames = fd.getAll('sw_name[]');
        const swPurposes = fd.getAll('sw_purpose[]');
        const swCosts = fd.getAll('sw_cost[]');
        data.software_rows = [];
        for (let i = 0; i < swNames.length; i++) {
            if (swNames[i].trim()) {
                data.software_rows.push({
                    name: swNames[i],
                    purpose: swPurposes[i],
                    cost: swCosts[i]
                });
            }
        }

        data.maintenance_days = parseInt(data.maintenance_days) || 14;

        try {
            const resp = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const res = await resp.json();

            if (res.success) {
                const link = document.getElementById('proposalLink');
                link.href = res.proposal_url;
                link.textContent = res.proposal_url;
                document.getElementById('emailDraft').textContent = res.email_draft;
                result.classList.remove('error');
                result.classList.add('show');
            } else {
                result.innerHTML = `<h3 style="color: #ff4444;">Error</h3><p>${res.error}</p>`;
                result.classList.add('show', 'error');
            }
        } catch (err) {
            result.innerHTML = `<h3 style="color: #ff4444;">Error</h3><p>${err.message}</p>`;
            result.classList.add('show', 'error');
        }

        btn.disabled = false;
        loading.classList.remove('show');
    });
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def form_page():
    return FORM_HTML


@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    result = run_proposal_generation(data)
    return JSONResponse(result)


if __name__ == "__main__":
    print("\n  Proposal Generator running at http://localhost:9090\n")
    uvicorn.run(app, host="127.0.0.1", port=9090)
