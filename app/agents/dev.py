from app.core.llm import llm_call

SYS = """You are Dev agent. Produce a unified diff patch when possible.
Follow repo style. Avoid breaking changes. Be explicit about assumptions."""

def run(task: str, context: str) -> str:
    user = f"""TASK:\n{task}\n\nCONTEXT (code/docs):\n{context}\n\nOUTPUT:
1) If changes are needed, output a unified diff (git style).
2) Then a short explanation.
"""
    return llm_call(SYS, user)