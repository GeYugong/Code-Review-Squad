from app.core.llm import llm_call

SYS = """You are Perf/Sec agent. Look for:
- input validation gaps
- injection/path traversal/unsafe eval
- unbounded loops/regex DoS
- obvious O(n^2) hotspots
Return concrete recommendations."""

def run(task: str, context: str, patch: str) -> str:
    user = f"""TASK:\n{task}\n\nCONTEXT:\n{context}\n\nPATCH:\n{patch}\n\nOUTPUT:
Return JSON with fields: risks (list), perf_notes (list), security_notes (list), mitigations (list).
"""
    return llm_call(SYS, user)