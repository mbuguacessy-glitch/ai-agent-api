import os
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic
from tavily import TavilyClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
tavily_client = TavilyClient(
    api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None


class QuestionRequest(BaseModel):
    question: str
    context: str = ""


class ResearchRequest(BaseModel):
    topic: str


class AnalysisRequest(BaseModel):
    data: str
    context: str = ""


app = FastAPI(title="AI Agent API", version="1.0.0")


@app.get("/")
def health():
    return {
        "status": "running",
        "service": "AI Agent API",
        "version": "1.0.0",
        "endpoints": ["/ask", "/research", "/analyse"]
    }


@app.post("/ask")
async def ask(request: QuestionRequest):
    try:
        system = "You are a helpful AI assistant. Answer questions accurately and concisely."
        if request.context:
            system += f"\n\nUse this context to answer:\n{request.context}"

        message = anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=system,
            messages=[{"role": "user", "content": request.question}]
        )
        return {"answer": message.content[0].text, "question": request.question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/research")
async def research(request: ResearchRequest):
    try:
        if not tavily_client:
            raise HTTPException(
                status_code=503, detail="Tavily API key not configured")

        search = tavily_client.search(query=request.topic, max_results=5)
        results_text = "\n\n".join(
            [f"Source: {r['url']}\n{r['content']}" for r in search["results"]])

        research_msg = anthropic_client.messages.create(
            model="claude-sonnet-4-6", max_tokens=1500,
            system="You are a research specialist. Extract key facts, statistics, and insights.",
            messages=[
                {"role": "user", "content": f"Topic: {request.topic}\n\nResults:\n{results_text}"}]
        )
        research_notes = research_msg.content[0].text

        report_msg = anthropic_client.messages.create(
            model="claude-sonnet-4-6", max_tokens=2000,
            system="You are a professional report writer. Write structured reports with clear headings.",
            messages=[
                {"role": "user", "content": f"Topic: {request.topic}\n\nNotes:\n{research_notes}"}]
        )
        report = report_msg.content[0].text

        return {"topic": request.topic, "research": research_notes, "report": report}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyse")
async def analyse(request: AnalysisRequest):
    try:
        prompt = f"""Analyse this business data and provide:
1. Key metrics and summary statistics
2. Notable trends or patterns
3. Top performers or outliers
4. Recommended actions

Data:
{request.data}

{f'Additional context: {request.context}' if request.context else ''}"""

        message = anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"analysis": message.content[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)
