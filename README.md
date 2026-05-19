# AI Agent API: Deployed Production Service

## What this does
A production-ready FastAPI service combining three AI capabilities; 
question answering, multi-agent research, and data analysis; deployed
to Render's cloud hosting and permanently accessible at a public URL
24/7 without a local machine running.

## The problem it solves
Every AI system built locally is a demo, not a product. It goes offline
when the laptop closes. Clients cannot access it. n8n Cloud cannot reach
it without ngrok. This project deploys the full AI agent stack to the
cloud, giving it a permanent URL that anyone can call from anywhere,
anytime.

## Live URL
https://ai-agent-api-w7uh.onrender.com

## Measurable result
- Deployment platform: Render (free tier)
- Uptime: 24/7, no local machine required
- Endpoints: 3 (/ask, /research, /analyse)
- Health check: live at https://ai-agent-api-w7uh.onrender.com
- Interactive API docs: https://ai-agent-api-w7uh.onrender.com/docs
- Cold start time on free tier: 30 to 60 seconds after inactivity
- Response time after warm: under 5 seconds

## Tech stack — 2026 versions
- Python 3.12.0
- FastAPI + Uvicorn
- Anthropic SDK 0.40+
- Claude claude-sonnet-4-6
- Tavily Search API
- Render (cloud deployment)
- python-dotenv

## Tools used and why

### Render: the cloud host
Deploys the FastAPI service permanently from the GitHub repository.
Detects every git push and redeploys automatically. Stores API keys
as environment variables so they are never in the code or GitHub.

### FastAPI: the API framework
Handles all three endpoints with automatic input validation, error
responses, and interactive documentation at /docs. Production-ready
without any changes from local development.

### Claude API: the intelligence
Powers all three endpoints with different system prompts for each
role; assistant, researcher, and analyst.

### Tavily: web search for the research endpoint
Gives the research pipeline access to live web results so the agent
can research any topic with current information.

### requirements.txt: the dependency manifest
Tells Render exactly which packages to install on the cloud server.
Every imported package must be listed here or the deployment fails.

### GitHub: the deployment bridge
Every git push to main triggers an automatic redeployment on Render.
The code never touches the server directly — GitHub is the bridge.

## API endpoints

### GET /
Health check: confirms service is running
Response: {"status": "running", "service": "AI Agent API", ...}

### POST /ask
Answer any question with optional context
Request: {"question": "your question", "context": "optional context"}
Response: {"answer": "...", "question": "..."}

### POST /research
Run a full three-agent research pipeline on any topic
Request: {"topic": "your topic"}
Response: {"topic": "...", "research": "...", "report": "..."}

### POST /analyse
Analyse any data passed as a string
Request: {"data": "your csv or text data", "context": "optional"}
Response: {"analysis": "..."}

## How to call from n8n Cloud
Add an HTTP Request node with:
URL: https://ai-agent-api-w7uh.onrender.com/ask
Method: POST
Body: {"question": "{{ $json.your_field }}"}

No ngrok. No localhost. Works from n8n Cloud directly.

## How to redeploy after changes
git add .
git commit -m "description of change"
git push origin main

Render detects the push and redeploys automatically.

## Error handling
- 500 on all requests: API keys not set in Render environment variables
- Cold start delay: free tier sleeps after 15min inactivity, first
  request takes 30-60 seconds to wake up
- Build failed: check requirements.txt has all imported packages listed
- Start command failed: confirm file is named exactly main.py
- .env pushed to GitHub: rotate all API keys immediately

## Screenshots
[https://ai-agent-api-w7uh.onrender.com]
[https://imgur.com/QG5Hmpx]
[https://imgur.com/ID0glad]



