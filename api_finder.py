#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Vampire Squad - API Key Finder Tool (Ethical Purpose Only)

import os
import json
import datetime
from mitmproxy import http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options

LOG_FILE = "logs/captured_apis.json"

captured = []

def save_logs():
    with open(LOG_FILE, "w") as f:
        json.dump(captured, f, indent=4)

class APIFinder:
    def __init__(self):
        self.total = 0

    def request(self, flow: http.HTTPFlow):
        self.total += 1
        request = flow.request

        log_entry = {
            "timestamp": str(datetime.datetime.now()),
            "url": request.pretty_url,
            "method": request.method,
            "headers": dict(request.headers),
            "host": request.host,
            "path": request.path,
            "user_agent": request.headers.get("user-agent", "N/A"),
            "api_key_guess": self.find_api_key(request)
        }

        print(f"\n[{self.total}] 📡 {request.method} {request.pretty_url}")
        if log_entry["api_key_guess"]:
            print(f"🔑 Possible API Key Found: {log_entry['api_key_guess']}")
        captured.append(log_entry)
        save_logs()

    def find_api_key(self, req):
        # Search headers and URL for possible API keys
        guesses = []
        for key, value in req.headers.items():
            if "api" in key.lower() or "key" in key.lower():
                guesses.append(f"{key}: {value}")
        if "key=" in req.pretty_url:
            guesses.append(req.pretty_url.split("key=")[-1].split("&")[0])
        return guesses if guesses else None

def run():
    opts = Options(listen_host='0.0.0.0', listen_port=8080)
    m = DumpMaster(opts, with_termlog=False, with_dumper=False)
    m.addons.add(APIFinder())
    print("🧛‍♂️ Vampire-API-Finder Running on Port 8080")
    print("📲 Set proxy on your mobile to 192.168.X.X:8080\n")
    try:
        m.run()
    except KeyboardInterrupt:
        print("\n🛑 Stopped by User.")
        save_logs()

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    run()
