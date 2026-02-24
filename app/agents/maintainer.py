from app.core.llm import llm_call

SYS = """You are Maintainer agent.
Decide whether the proposed patch must be reworked before acceptance.
If there are blocker issues, request rework with concrete instructions.
Return strict JSON only."""


def run(task: str, context: str, patch: str, review: object, tests: object, perfsec: object) -> str:
    user = f"""TASK:
{task}

CONTEXT:
{context}

PATCH:
{patch}

REVIEW:
{review}

TESTS:
{tests}

PERFSEC:
{perfsec}

OUTPUT:
Return JSON object with fields:
- decision: one of ["accept", "rework"]
- reason: short string
- rework_instructions: list of concrete action items (empty list when accepted)
"""
    return llm_call(SYS, user)
