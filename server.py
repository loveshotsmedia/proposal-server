"""
Proposal Generator - Static Proposal Server
Serves branded HTML proposals via clean URLs.
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

app = FastAPI(title="Love Shots Media - Proposals")

PROPOSALS_DIR = Path(__file__).parent / "proposals"


@app.get("/proposals/{slug}")
async def serve_proposal(slug: str):
    """Serve a proposal by slug. e.g. /proposals/martinelli-plumbing"""
    # Convert slug to filename: martinelli-plumbing -> martinelli_plumbing_proposal.html
    filename = f"{slug.replace('-', '_')}_proposal.html"
    filepath = PROPOSALS_DIR / filename

    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Proposal not found")

    html_content = filepath.read_text(encoding="utf-8")
    return HTMLResponse(content=html_content)


@app.get("/")
async def root():
    return {"status": "Love Shots Media - Proposal Server"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
