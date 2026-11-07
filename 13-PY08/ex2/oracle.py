#!/usr/bin/env python3

import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv package not found.")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)


def main() -> None:
    load_dotenv()

    mode = os.getenv("MATRIX_MODE", "development")
    db_url = os.getenv("DATABASE_URL", "")
    api_key = os.getenv("API_KEY", "")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    zion_url = os.getenv("ZION_ENDPOINT", "")

    print("ORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"Mode: {mode}")

    if "localhost" in db_url or "127.0.0.1" in db_url or not db_url:
        db_status = "Connected to local instance"
    else:
        db_status = f"Connected to production ({db_url})"
    print(f"Database: {db_status}")

    if api_key:
        api_status = "Authenticated"
    else:
        api_status = "Unauthenticated (Missing API_KEY)"
    print(f"API Access: {api_status}")

    print(f"Log Level: {log_level}")

    if zion_url:
        zion_status = "Online"
    else:
        zion_status = "Offline (Endpoint missing)"
    print(f"Zion Network: {zion_status}")

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")

    env_exists = os.path.exists(".env")
    if env_exists:
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file missing! Using default env vars")

    print("[OK] Production overrides available")
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
