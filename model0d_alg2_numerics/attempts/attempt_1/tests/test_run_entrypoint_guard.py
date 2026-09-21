import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_rejects_missing_deterministic_environment_before_output_creation(tmp_path):
    out = tmp_path / "should_not_exist"
    env = os.environ.copy()
    for key in ("PYTHONHASHSEED", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        env.pop(key, None)
    proc = subprocess.run(
        [sys.executable, str(ROOT / "run_experiment.py"),
         "--config", str(ROOT / "configs" / "baseline_2uav_0obs.json"),
         "--output", str(out)],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert proc.returncode != 0
    assert "Approved deterministic execution environment not active" in proc.stderr
    assert not out.exists()
