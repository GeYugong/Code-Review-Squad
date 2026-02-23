from fastapi import FastAPI
from pydantic import BaseModel
from app.core.orchestrator import run_squad

app = FastAPI(title="Code-Review-Squad")

class ReviewRequest(BaseModel):
    task: str
    context: str

@app.post("/review")
def review(req: ReviewRequest):
    return run_squad(req.task, req.context)