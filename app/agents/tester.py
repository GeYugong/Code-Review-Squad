from app.core.llm import llm_call

SYS = """You are Tester agent. Propose tests that cover normal, edge, and failure cases.
Prefer small, deterministic unit tests."""

def run(task: str, context: str, patch: str) -> str:
    user = f"""TASK:\n{task}\n\nCONTEXT:\n{context}\n\nPATCH:\n{patch}\n\nOUTPUT:
Return a JSON object:
tests_to_add (list), key_cases (list), and optional test_code (unified diff).
"""
    return llm_call(SYS, user)