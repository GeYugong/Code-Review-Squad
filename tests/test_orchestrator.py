import json

from app.core.orchestrator import run_squad


def test_run_squad_reworks_when_blocker(monkeypatch):
    state = {"dev_calls": 0}

    def fake_dev(task, context):
        state["dev_calls"] += 1
        return f"patch-round-{state['dev_calls']}"

    def fake_reviewer(task, context, patch):
        if patch.endswith("1"):
            return json.dumps(
                [
                    {
                        "severity": "blocker",
                        "file": "a.py",
                        "location": "f()",
                        "issue": "bad",
                        "rationale": "bad",
                        "fix_suggestion": "fix",
                    }
                ]
            )
        return "[]"

    def fake_tester(task, context, patch):
        return '{"tests_to_add":[],"key_cases":[]}'

    def fake_perf(task, context, patch):
        return '{"risks":[],"perf_notes":[],"security_notes":[],"mitigations":[]}'

    def fake_maintainer(task, context, patch, review, tests, perfsec):
        if patch.endswith("1"):
            return '{"decision":"rework","reason":"blocker","rework_instructions":["fix blocker"]}'
        return '{"decision":"accept","reason":"ok","rework_instructions":[]}'

    monkeypatch.setattr("app.core.orchestrator.dev.run", fake_dev)
    monkeypatch.setattr("app.core.orchestrator.reviewer.run", fake_reviewer)
    monkeypatch.setattr("app.core.orchestrator.tester.run", fake_tester)
    monkeypatch.setattr("app.core.orchestrator.perfsec.run", fake_perf)
    monkeypatch.setattr("app.core.orchestrator.maintainer.run", fake_maintainer)

    out = run_squad("t", "ctx", max_rounds=2)
    assert out["rounds_used"] == 2
    assert out["patch"] == "patch-round-2"
    assert state["dev_calls"] == 2
