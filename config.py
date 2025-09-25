# Fundezy Trading Platform Configuration
# WARNING: Do not hardcode real credentials here. Use environment variables.

import os

# Non-sensitive default (can be overridden via env)
FTP_API_BASE_URL = os.environ.get("FTP_API_BASE_URL", "https://platform.fundezy.io")

# Sensitive values must come from environment variables
FTP_EMAIL = os.environ.get("FTP_EMAIL", "your-email@example.com")
FTP_PASSWORD = os.environ.get("FTP_PASSWORD", "your-password")
FTP_BROKER_ID = os.environ.get("FTP_BROKER_ID", "your-broker-id")
