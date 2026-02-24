from app.agents import dev, reviewer, tester, perfsec, maintainer
from app.core.utils import try_parse_json


def _has_blocker(review: object) -> bool:
    if not isinstance(review, list):
        return False
    for item in review:
        if not isinstance(item, dict):
            continue
        severity = str(item.get("severity", "")).lower()
        if severity == "blocker":
            return True
    return False


def run_squad(task: str, context: str, max_rounds: int = 2) -> dict:
    patch = ""
    review = []
    tests = {}
    perf = {}
    maint = {}
    rounds_used = 0

    for current_round in range(1, max(1, max_rounds) + 1):
        rounds_used = current_round
        patch = dev.run(task, context if current_round == 1 else f"{context}\n\nRework request:\n{maint}")

        review_raw = reviewer.run(task, context, patch)
        tests_raw = tester.run(task, context, patch)
        perf_raw = perfsec.run(task, context, patch)

        review = try_parse_json(review_raw)
        tests = try_parse_json(tests_raw)
        perf = try_parse_json(perf_raw)

        maint_raw = maintainer.run(task, context, patch, review, tests, perf)
        maint = try_parse_json(maint_raw)

        if isinstance(maint, dict) and str(maint.get("decision", "")).lower() == "accept":
            break
        if _has_blocker(review):
            continue
        break

    return {
        "patch": patch,
        "review": review,
        "tests": tests,
        "perfsec": perf,
        "maintainer": maint,
        "rounds_used": rounds_used,
    }
