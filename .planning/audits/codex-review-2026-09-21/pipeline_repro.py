"""Independent review reproductions; does not modify source or test files."""
import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root / "src"))

from reasoning_diff.cli import main
from reasoning_diff.io import read_json, read_jsonl
from reasoning_diff.splits import assign_split

files = sorted(root.joinpath("src/reasoning_diff").rglob("*.py"))
files += sorted(root.joinpath("tests").rglob("*.py"))
files.append(root / "pyproject.toml")
h = hashlib.sha256()
for path in files:
    h.update(path.relative_to(root).as_posix().encode())
    h.update(b"\x00")
    h.update(path.read_bytes())
result = {"source_hash": h.hexdigest(), "source_files": len(files)}
fixture = root / "tests/fixtures/t1_tiny.json"
seed = next(i for i in range(100) if assign_split("fix-t1-001", seed=i) == "test")
other_seed = next(i for i in range(100) if assign_split("fix-t1-001", seed=i) == "probe_train")
with TemporaryDirectory(prefix="reasoning_diff_review_") as td:
    temp = Path(td)
    prep, feat, fit, cal = (temp / n for n in ("prep", "feat", "fit", "cal"))
    main(["prepare", "--fixture", str(fixture), "--out-dir", str(prep), "--split-seed", str(seed)])
    before = (prep / "manifest.json").read_bytes()
    assigned = read_jsonl(prep / "splits.jsonl")
    main(["prepare", "--fixture", str(fixture), "--out-dir", str(prep), "--split-seed", str(other_seed), "--resume"])
    result["resume_changed_seed"] = {"original_seed": seed, "new_seed": other_seed, "expected_new_role": "probe_train", "unchanged_manifest": before == (prep / "manifest.json").read_bytes(), "persisted_split": assigned}
    main(["collect", "--fixture", str(fixture), "--in-dir", str(prep), "--out-dir", str(feat), "--backend", "offline"])
    fit_rc = main(["fit", "--in-dir", str(feat), "--labels-dir", str(prep), "--out-dir", str(fit), "--eval-mode", "scientific"])
    cal_rc = main(["calibrate", "--in-dir", str(fit), "--features-dir", str(feat), "--labels-dir", str(prep), "--out-dir", str(cal), "--eval-mode", "scientific"])
    result["test_data_fitted_and_calibrated"] = {"actual_split": assigned, "fit_returncode": fit_rc, "calibrate_returncode": cal_rc, "calibration": read_jsonl(cal / "calibration.jsonl")}
    bad = temp / "failed_fit"
    args = ["fit", "--in-dir", str(temp / "missing"), "--out-dir", str(bad)]
    try:
        main(args)
    except Exception as exc:
        result["initial_failure"] = type(exc).__name__
    result["resume_failed_fit"] = {"returncode": main(args + ["--resume"]), "manifest": read_json(bad / "manifest.json"), "probes_exist": (bad / "probes.jsonl").exists()}

Path(__file__).with_name("pipeline_repro_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
