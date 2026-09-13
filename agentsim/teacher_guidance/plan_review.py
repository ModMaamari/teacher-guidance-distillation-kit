"""Helpers for the optional plan-review preflight phase."""

from __future__ import annotations

from typing import Any, Dict, List


def _tools_in_plan(plan: Dict[str, Any]) -> List[str]:
    # A small student sometimes writes steps as plain strings, or `steps` itself as a string.
    # Calling .get on those raised "'str' object has no attribute 'get'" and ended the whole
    # episode in error, so treat anything that is not the expected shape as a step with no tool.
    steps = plan.get("steps", []) if isinstance(plan, dict) else []
    if not isinstance(steps, list):
        return []
    return [str(step.get("intended_tool", "")) if isinstance(step, dict) else "" for step in steps]


def compute_plan_review_metrics(
    initial_plan: Dict[str, Any],
    revised_plan: Dict[str, Any],
    review_full: Dict[str, Any],
) -> Dict[str, Any]:
    """Lightweight, deterministic plan-review metrics."""
    initial_tools = _tools_in_plan(initial_plan)
    revised_tools = _tools_in_plan(revised_plan)
    # The teacher sometimes returns private_diagnosis as text rather than an object; the
    # schema check flags that, but these metrics ran anyway and raised on private.get(...).
    rf = review_full if isinstance(review_full, dict) else {}
    private = rf.get("private_diagnosis")
    if not isinstance(private, dict):
        private = {}
    decision = rf.get("teacher_decision")
    return {
        "initial_step_count": len(initial_tools),
        "revised_step_count": len(revised_tools),
        "plan_changed": initial_tools != revised_tools,
        "revision_skipped": decision == "accept_plan",
        "initial_tools": initial_tools,
        "revised_tools": revised_tools,
        "initial_covers_verification": "verify" in initial_tools,
        "revised_covers_verification": "verify" in revised_tools,
        "teacher_decision": decision,
        "premature_answering_risk": bool(private.get("premature_answering_risk", False)),
    }
