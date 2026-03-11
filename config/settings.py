"""
Proposal Generator Settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from The_Machine_God_Mode
ENV_PATH = Path(__file__).parent.parent.parent / ".env"
load_dotenv(ENV_PATH)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "loveshotsmedia/proposal-server"
GITHUB_PAGES_BASE = "https://loveshotsmedia.github.io/proposal-server"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

PROPOSALS_DIR = Path(__file__).parent.parent / "proposals"
EMAILS_DIR = Path(__file__).parent.parent / "emails"

# Ensure directories exist
PROPOSALS_DIR.mkdir(exist_ok=True)
EMAILS_DIR.mkdir(exist_ok=True)
