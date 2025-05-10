import os

BASE_URL="https://thirdparty.qonto.com/v2"
API_IDENTIFIER = os.environ.get("QONTO_API_IDENTIFIER")
API_SECRET_KEY = os.environ.get("QONTO_API_SECRET_KEY")
API_KEY=f"{API_IDENTIFIER}:{API_SECRET_KEY}"