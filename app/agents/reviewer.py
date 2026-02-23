from app.core.llm import llm_call

SYS = """You are Reviewer agent. Find issues and categorize them:
blocker, major, minor, nit. Always cite file/function names from context."""

def run(task: str, context: str, patch: str) -> str:
    user = f"""TASK:\n{task}\n\nCONTEXT:\n{context}\n\nPATCH:\n{patch}\n\nOUTPUT:
Return a JSON array of review items with fields:
severity, file, location, issue, rationale, fix_suggestion.
"""
    return llm_call(SYS, user)