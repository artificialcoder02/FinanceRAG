from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.pipeline import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FinanceRAG API", description="API for FinanceRAG Multi-Agent System")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: list
    evaluation: dict

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    logger.info(f"Received query: {request.query}")
    try:
        result = pipeline.run(request.query)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            evaluation=result["evaluation"]
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
