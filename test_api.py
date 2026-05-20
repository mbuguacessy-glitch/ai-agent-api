import requests
import json
from datetime import datetime
from pathlib import Path

API = "https://ai-agent-api-w7uh.onrender.com"
OUTPUT = Path(__file__).parent / \
    f"api_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"


def write(f, heading, content):
    f.write(f"\n{'='*60}\n{heading}\n{'='*60}\n{content}\n")


print("Testing all three endpoints...")
print("This may take 2-3 minutes for the research endpoint.\n")

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(f"AI AGENT API TEST RESULTS\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"API: {API}\n")

    # --- /ask ---
    print("1. Calling /ask...")
    try:
        res = requests.post(f"{API}/ask", json={
            "question": "What are the top 3 AI automation opportunities for small businesses in Nairobi in 2026?",
            "context": "We are an AI automation agency based in Nairobi specialising in n8n workflows, Python integrations, RAG systems, and multi-agent pipelines."
        }, timeout=60)
        answer = res.json().get("answer", "No answer returned")
        write(f, "ENDPOINT: /ask", answer)
        print("   Done.\n")
    except Exception as e:
        write(f, "ENDPOINT: /ask", f"ERROR: {e}")
        print(f"   Error: {e}\n")

    # --- /analyse ---
    print("2. Calling /analyse...")
    try:
        res = requests.post(f"{API}/analyse", json={
            "data": "Month,Revenue,Clients,Deals\nJanuary,450000,12,8\nFebruary,380000,9,6\nMarch,620000,15,11\nApril,710000,18,13\nMay,590000,14,10",
            "context": "AI automation agency monthly performance data for 2026"
        }, timeout=60)
        analysis = res.json().get("analysis", "No analysis returned")
        write(f, "ENDPOINT: /analyse", analysis)
        print("   Done.\n")
    except Exception as e:
        write(f, "ENDPOINT: /analyse", f"ERROR: {e}")
        print(f"   Error: {e}\n")

    # --- /research ---
    print("3. Calling /research (takes 30-60 seconds)...")
    try:
        res = requests.post(f"{API}/research", json={
            "topic": "AI automation opportunities for small businesses in East Africa 2026"
        }, timeout=120)
        data = res.json()
        research = data.get("research", "No research returned")
        report = data.get("report", "No report returned")
        write(f, "ENDPOINT: /research — RESEARCH NOTES", research)
        write(f, "ENDPOINT: /research — FULL REPORT", report)
        print("   Done.\n")
    except Exception as e:
        write(f, "ENDPOINT: /research", f"ERROR: {e}")
        print(f"   Error: {e}\n")

print(f"All results saved to:\n{OUTPUT}")
