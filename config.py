# Fundezy Trading Platform Configuration
# WARNING: Do not hardcode real credentials here. Use environment variables.
#
# Setup Instructions:
# 1. Create a .env file in the project root
# 2. Copy the template below and fill with your real values:
#
# ===== .env file template =====
# FTP_API_BASE_URL=https://platform.fundezy.io
# FTP_EMAIL=your-email@example.com
# FTP_PASSWORD=your-password
# FTP_BROKER_ID=107
# ===== end of template =====

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Non-sensitive default (can be overridden via env)
FTP_API_BASE_URL = os.environ.get("FTP_API_BASE_URL", "https://platform.fundezy.io")

# Sensitive values must come from environment variables
FTP_EMAIL = os.environ.get("FTP_EMAIL", "your-email@example.com")
FTP_PASSWORD = os.environ.get("FTP_PASSWORD", "your-password")
FTP_BROKER_ID = os.environ.get("FTP_BROKER_ID", "107")
