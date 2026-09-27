from reasoning_diff.cli import main
from reasoning_diff.io import read_json


def test_full_cli_smoke(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    lab = tmp_path / "lab"
    fit = tmp_path / "fit"
    cal = tmp_path / "cal"
    inter = tmp_path / "int"
    rep = tmp_path / "rep"
    an = tmp_path / "an"
    steps = [
        ["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)],
        ["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"],
        ["label", "--in-dir", str(prep), "--out-dir", str(lab)],
        ["fit", "--in-dir", str(col), "--labels-dir", str(lab), "--out-dir", str(fit), "--split", "probe_train"],
        ["calibrate", "--in-dir", str(fit), "--out-dir", str(cal), "--split", "calibration"],
        ["intervene", "--in-dir", str(col), "--out-dir", str(inter)],
        ["repair", "--in-dir", str(prep), "--out-dir", str(rep), "--mask", "task_oracle"],
        ["analyze", "--in-dir", str(lab), "--out-dir", str(an)],
    ]
    for argv in steps:
        assert main(argv) == 0
    report = read_json(an / "report.json")
    assert report.get("scientific_conclusion") is None
    assert report["week8"]["gates"]["gate0"]["decision"] == "unregistered"
    assert "report.json" in read_json(an / "manifest.json")["file_hashes"]
    assert (prep / "manifest.json").exists()
