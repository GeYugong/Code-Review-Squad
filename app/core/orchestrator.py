from app.agents import dev, reviewer, tester, perfsec
from app.core.utils import try_parse_json

def run_squad(task: str, context: str) -> dict:
    patch = dev.run(task, context)

    review_raw = reviewer.run(task, context, patch)
    tests_raw = tester.run(task, context, patch)
    perf_raw = perfsec.run(task, context, patch)

    return {
        "patch": patch,
        "review": try_parse_json(review_raw),
        "tests": try_parse_json(tests_raw),
        "perfsec": try_parse_json(perf_raw),
    }