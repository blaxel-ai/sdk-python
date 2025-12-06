"""
Test webhook signature verification with ngrok.

This script:
1. Starts a local webhook server (Flask)
2. Exposes it via ngrok
3. Shows you the URL to configure in async-sidecar
4. Asks for your CALLBACK_SECRET
5. Verifies incoming webhooks

Prerequisites:
    pip install flask requests

Usage:
    python tests/integration/core/webhook_ngrok.py
"""

import subprocess
import sys
import time
from datetime import datetime

import requests
from flask import Flask, request

from blaxel.core import verify_webhook_from_request

app = Flask(__name__)
PORT = 3456
CALLBACK_SECRET: str | None = None


@app.route("/webhook", methods=["POST"])
def webhook():
    """Webhook endpoint for async-sidecar callbacks."""
    print("\n" + "=" * 60)
    print("📥 Incoming webhook")
    print("=" * 60)

    signature = request.headers.get("X-Blaxel-Signature")
    timestamp = request.headers.get("X-Blaxel-Timestamp")

    print("Headers:")
    print(f"  X-Blaxel-Signature: {signature or '❌ MISSING'}")
    print(f"  X-Blaxel-Timestamp: {timestamp or '❌ MISSING'}")

    # Verify signature using SDK
    if not CALLBACK_SECRET:
        print("\n❌ CALLBACK_SECRET not configured")
        return {"error": "Secret not configured"}, 500

    # Create a simple request wrapper
    class RequestWrapper:
        def __init__(self, flask_request):
            self._request = flask_request

        @property
        def body(self) -> bytes:
            return self._request.get_data()

        @property
        def headers(self) -> dict:
            # Convert headers to lowercase keys for consistent lookup
            return {k.lower(): v for k, v in self._request.headers.items()}

    is_valid = verify_webhook_from_request(RequestWrapper(request), CALLBACK_SECRET)

    if not is_valid:
        print("\n❌ SIGNATURE VERIFICATION FAILED")
        print("   Check that the CALLBACK_SECRET matches on both sides")
        return {"error": "Invalid signature"}, 401

    print("\n✅ SIGNATURE VERIFIED SUCCESSFULLY")

    # Parse and display the callback data
    try:
        data = request.json
        print("\nCallback Data:")
        print(f"  Status Code: {data['status_code']}")
        print(f"  Response Length: {data['response_length']} bytes")
        timestamp_dt = datetime.fromtimestamp(data["timestamp"])
        print(f"  Timestamp: {timestamp_dt.isoformat()}")
        print("  Response Body:")

        response_body = data["response_body"]
        if len(response_body) > 200:
            print(f"    {response_body[:200]}...")
        else:
            print(f"    {response_body}")

        print("\n" + "=" * 60)

        return {"received": True, "verified": True}
    except Exception as e:
        print(f"\n❌ Failed to parse callback payload: {e}")
        return {"error": "Invalid payload"}, 400


@app.route("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


def start_ngrok() -> str | None:
    """Start ngrok tunnel and return the public URL."""
    print("🌐 Starting ngrok tunnel...")

    try:
        # Start ngrok in background
        subprocess.Popen(
            ["ngrok", "http", str(PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print("⏳ Waiting for ngrok to start...\n")
        time.sleep(3)

        # Fetch URL from ngrok API
        for attempt in range(4):
            try:
                response = requests.get("http://localhost:4040/api/tunnels", timeout=2)
                data = response.json()

                if data.get("tunnels"):
                    # Find HTTPS tunnel
                    tunnel = next(
                        (t for t in data["tunnels"] if t["proto"] == "https"),
                        data["tunnels"][0],
                    )
                    return tunnel["public_url"]

                if attempt < 3:
                    print("⏳ Still waiting for ngrok...")
                    time.sleep(2)
            except requests.RequestException:
                if attempt < 3:
                    time.sleep(2)

        print("❌ Could not connect to ngrok API")
        print("   Make sure ngrok is installed and running")
        print("   Install with: brew install ngrok")
        print("   Or download from: https://ngrok.com/download")
        return None

    except FileNotFoundError:
        print("❌ ngrok not found")
        print("   Install with: brew install ngrok (macOS)")
        print("   Or download from: https://ngrok.com/download")
        return None


def display_instructions(ngrok_url: str):
    """Display configuration instructions."""
    print("\n" + "=" * 60)
    print("✅ Ngrok tunnel established!")
    print("=" * 60)
    print("\n📋 Configuration for async-sidecar:")
    print(f"\n  CALLBACK_URL={ngrok_url}/webhook")
    print("\n" + "=" * 60)


def ask_for_secret():
    """Ask user for the callback secret."""
    global CALLBACK_SECRET

    print("\n🔐 Enter your CALLBACK_SECRET:")
    print("   (This should match the CALLBACK_SECRET in async-sidecar)\n")

    secret = input("Secret: ").strip()

    if not secret:
        print("❌ Secret cannot be empty!")
        sys.exit(1)

    CALLBACK_SECRET = secret

    print("\n✅ Secret configured")
    print("\n" + "=" * 60)
    print("🎯 Ready to receive webhooks!")
    print("=" * 60)
    print("\nWaiting for incoming webhooks...")
    print("Press Ctrl+C to stop\n")


def main():
    """Main function to start the webhook server and ngrok."""
    print("🚀 Webhook server starting...")
    print(f"   Local: http://localhost:{PORT}/webhook\n")

    # Start ngrok
    ngrok_url = start_ngrok()

    if not ngrok_url:
        print("\n⚠️  Could not get ngrok URL")
        print(f"   You can still use: http://localhost:{PORT}/webhook")
        print("   But it won't be publicly accessible\n")
        ask_for_secret()
    else:
        display_instructions(ngrok_url)
        ask_for_secret()

    # Start Flask server
    print("Starting Flask server...\n")
    try:
        app.run(host="0.0.0.0", port=PORT, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
