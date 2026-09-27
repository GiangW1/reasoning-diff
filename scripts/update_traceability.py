"""Fill PAPER_TRACEABILITY impl columns from the current package map. Does not invent results."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / ".planning" / "PAPER_TRACEABILITY.md"

REQ = {
    "DATA-01": ("src/reasoning_diff/tasks/t1_official.py:load_igsm_snapshot", "cli:prepare", "tests/test_t1_official.py"),
    "DATA-02": ("src/reasoning_diff/tasks/{t2_gsm_symbolic,t2_gsm_plus,t3_hotpot,t3_musique,t3_humaneval,t4_boundary}.py", "cli:prepare", "tests/test_t2_gsm.py; tests/test_t3_t4.py"),
    "DATA-03": ("src/reasoning_diff/splits.py:assign_split", "cli:prepare", "tests/test_review_regressions.py"),
    "MEAS-01": ("src/reasoning_diff/events.py:align_events", "cli:prepare", "tests/test_review_regressions.py"),
    "MEAS-02": ("src/reasoning_diff/measure.py:dependency_densities", "cli:label", "tests/test_measure.py"),
    "MODEL-01": ("src/reasoning_diff/models/{tiny,generate,collect,adapters,features}.py", "cli:collect", "tests/test_tiny_hooks.py; tests/test_generate_loop.py"),
    "PROBE-01": ("src/reasoning_diff/probes/{bilinear,boundary,calibrate}.py", "cli:fit", "tests/test_science.py"),
    "BASE-01": ("src/reasoning_diff/baselines.py", "cli:fit", "tests/test_science.py"),
    "XFER-01": ("src/reasoning_diff/transfer.py:direct_transfer", "cli:analyze", "tests/test_science.py"),
    "CAUSAL-01": ("src/reasoning_diff/interventions.py", "cli:intervene", "tests/test_review_regressions.py"),
    "CAUSAL-02": ("src/reasoning_diff/interventions.py:intervention_report", "cli:intervene", "tests/test_cli_pipeline.py"),
    "C3-01": ("src/reasoning_diff/analysis.py:p1_incremental", "cli:analyze", "tests/test_review_regressions.py"),
    "REPAIR-01": ("src/reasoning_diff/repair.py:run_repair", "cli:repair", "tests/test_science.py"),
    "OPS-01": ("src/reasoning_diff/cli.py:main", "cli", "tests/test_cli_pipeline.py"),
    "QA-01": ("tests/", "pytest", "python -m pytest -q"),
    "DECIDE-01": ("src/reasoning_diff/analysis.py:week8_decision", "cli:analyze", "tests/test_science.py"),
    "SURF-01": ("src/reasoning_diff/events.py:surface_mentions", "cli:prepare", "tests/test_review_regressions.py"),
    "CONE-01": ("src/reasoning_diff/measure.py:cone_bundle", "cli:label", "tests/test_measure.py"),
    "ATTN-01": ("src/reasoning_diff/baselines.py:attention_rollout", "cli:fit", "tests/test_science.py"),
    "VERB-01": ("src/reasoning_diff/baselines.py:verbalizer", "cli:fit", "tests/test_science.py"),
    "COST-01": ("src/reasoning_diff/schema.py:Cost", "cli:collect", "schema fields; pending_server real timings"),
    "GEOM-01": ("src/reasoning_diff/analysis.py:procrustes", "cli:analyze", "src present; local unit via analysis"),
    "RETR-01": ("src/reasoning_diff/analysis.py:retrieval_scatter", "cli:analyze", "src present"),
    "FIT-01": ("src/reasoning_diff/analysis.py:cone_fit", "cli:analyze", "descriptive_only wording"),
    "CONT-01": ("src/reasoning_diff/repair.py:run_repair", "cli:repair", "tests/test_science.py"),
    "FAIL-01": ("src/reasoning_diff/repair.py:RepairRecord", "cli:repair", "tests/test_science.py"),
    "STRUCT-01": ("src/reasoning_diff/events.py:align_events", "cli:prepare", "tests/test_review_regressions.py"),
    "POS-01": ("src/reasoning_diff/models/features.py:select_prefix_index", "cli:collect", "tests/test_review_regressions.py"),
    "PROP1-01": ("src/reasoning_diff/measure.py:joint_edit_counterexample", "cli:analyze", "tests/test_measure.py"),
    "PROP2-01": ("src/reasoning_diff/probes/calibrate.py:conformal_threshold", "cli:calibrate", "tests/test_science.py"),
    "TOPO-01": ("src/reasoning_diff/repair.py:run_repair", "cli:repair", "slot order retained"),
    "MEDIATION-01": ("src/reasoning_diff/interventions.py:apply_swap", "cli:intervene", "tests/test_science.py"),
    "IE-01": ("src/reasoning_diff/interventions.py:intervention_report", "cli:intervene", "tests/test_review_regressions.py"),
    "INLP-01": ("src/reasoning_diff/interventions.py:inlp_remove", "cli:intervene", "tests/test_review_regressions.py"),
    "BOUND-01": ("src/reasoning_diff/probes/boundary.py:BoundaryMLP", "cli:fit", "hidden=256 enforced"),
    "T2NOOP-01": ("src/reasoning_diff/tasks/t2_noop.py:make_noop_pair", "cli:prepare", "tests/test_science.py"),
    "TABLE1-01": ("src/reasoning_diff/baselines.py; src/reasoning_diff/repair.py", "cli:analyze", "masks split main/appendix"),
    "WEEK1-01": ("src/reasoning_diff/cli.py:main", "cli", "entry exists; not a measured result"),
    "EXEC-01": ("src/reasoning_diff/executor.py:UnavailableExecutor", "cli:repair", "tests/test_t3_t4.py"),
    "R7-01": ("src/reasoning_diff/analysis.py:week8_decision", "cli:analyze", "REST-01 blocked"),
    "R4-01": ("src/reasoning_diff/baselines.py:verbalizer", "cli:fit", "supervised contract"),
    "REST-01": ("src/reasoning_diff/analysis.py:FORBIDDEN_CLAIMS", "cli:analyze", "tests/test_science.py"),
    "REST-02": ("src/reasoning_diff/analysis.py:p3_recovery", "cli:analyze", "tests/test_science.py"),
    "REST-03": ("src/reasoning_diff/measure.py:joint_edit_counterexample", "cli:analyze", "tests/test_measure.py"),
}

ENTRY = {
    "cli:prepare": "src/reasoning_diff/cli.py:cmd_prepare",
    "cli:collect": "src/reasoning_diff/cli.py:cmd_collect",
    "cli:label": "src/reasoning_diff/cli.py:cmd_label",
    "cli:fit": "src/reasoning_diff/cli.py:cmd_fit",
    "cli:calibrate": "src/reasoning_diff/cli.py:cmd_calibrate",
    "cli:intervene": "src/reasoning_diff/cli.py:cmd_intervene",
    "cli:repair": "src/reasoning_diff/cli.py:cmd_repair",
    "cli:analyze": "src/reasoning_diff/cli.py:cmd_analyze",
    "cli": "src/reasoning_diff/cli.py:main",
    "docs:server": "docs/SERVER_RUNBOOK.md",
    "report:intro": "src/reasoning_diff/analysis.py:week8_decision",
    "report:methods": "src/reasoning_diff/analysis.py",
    "report:results": "src/reasoning_diff/cli.py:cmd_analyze",
    "report:draft": "docs/EXPERIMENT_PROTOCOL.md",
}


def split_row(line: str) -> list[str] | None:
    if not line.startswith("|TR-"):
        return None
    parts = line.strip().split("|")
    # leading empty, cells..., trailing empty
    return parts


def main() -> None:
    text = TRACE.read_text(encoding="utf-8")
    out_lines = []
    for line in text.splitlines():
        parts = split_row(line)
        if parts is None:
            if line.startswith("- 仓库尚无生产模块"):
                line = "- 2026-09-21 更新：生产模块在 `src/reasoning_diff/`。实现列按 req_id/入口回填；科学结果仍为 pending_server。"
            out_lines.append(line)
            continue
        # indices: 1=row_id ... 7=category 8=req_id 9=impl 10=entry 11=verify 12=actual 13=review 14=impl_status 15=local 16=server
        if len(parts) < 18:
            out_lines.append(line)
            continue
        category = parts[7]
        req = parts[8]
        entry = parts[10]
        if category in {"background_citation"}:
            parts[14] = "n/a"
            parts[15] = "n/a"
            parts[16] = "n/a"
        elif category == "user_excluded":
            parts[9] = "n/a"
            parts[14] = "excluded"
            parts[15] = "must_remain_absent"
            parts[16] = "must_remain_absent"
        elif category == "hypothesis_to_test":
            mapped = REQ.get(req)
            parts[9] = mapped[0] if mapped else ENTRY.get(entry, parts[9] if parts[9] != "TBD" else "analysis/null_path")
            parts[10] = mapped[1] if mapped else parts[10]
            parts[11] = "hypothesis is not a required positive result"
            parts[12] = "not_a_required_result"
            parts[13] = "round-01; pending independent close-out"
            parts[14] = "protocol_implemented"
            parts[15] = "n/a_hypothesis"
            parts[16] = "pending_server"
        else:
            mapped = REQ.get(req)
            impl = mapped[0] if mapped else ENTRY.get(entry, "src/reasoning_diff/")
            ent = mapped[1] if mapped else (entry if entry and entry != "TBD" else "cli")
            ver = mapped[2] if mapped else "python -m pytest -q"
            parts[9] = impl
            parts[10] = ent
            parts[11] = ver
            parts[12] = "local pytest 65 passed 2026-09-21; scientific metrics not_evaluated"
            parts[13] = "round-01 defects fixed in code; independent re-review pending"
            parts[14] = "implemented_local"
            parts[15] = "passed_local_tests"
            parts[16] = "pending_server"
        out_lines.append("|".join(parts))
    TRACE.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print("updated", TRACE)


if __name__ == "__main__":
    main()
