from fastapi import FastAPI
from pydantic import BaseModel
from app.core.orchestrator import run_squad
from app.core.context_builder import collect_context

app = FastAPI(title="Code-Review-Squad")


class ReviewRequest(BaseModel):
    task: str
    context: str | None = None
    repo_root: str | None = None
    files: list[str] | None = None
    include_globs: list[str] | None = None
    max_files: int = 20
    max_chars_per_file: int = 5000
    max_rounds: int = 2


@app.post("/review")
def review(req: ReviewRequest):
    context = req.context
    if not context:
        context = collect_context(
            repo_root=req.repo_root or ".",
            files=req.files,
            include_globs=req.include_globs,
            max_files=req.max_files,
            max_chars_per_file=req.max_chars_per_file,
        )
    return run_squad(req.task, context, max_rounds=req.max_rounds)
