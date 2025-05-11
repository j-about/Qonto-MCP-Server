import os
import argparse

ENV = os.getenv("ENV", "production")

if ENV == "production":
    BASE_URL="https://thirdparty.qonto.com/v2"
    parser = argparse.ArgumentParser(description="Qonto MCP Server Argument Parser")
    parser.add_argument("--api-key", required=True, type=str, help="Qonto API key")
    args = parser.parse_args()
    API_KEY = args.api_key
else:
    BASE_URL="https://thirdparty-sandbox.staging.qonto.co/v2"
    API_KEY = os.getenv('QONTO_API_KEY')

STAGING_TOKEN = os.getenv('QONTO_STAGING_TOKEN', None)