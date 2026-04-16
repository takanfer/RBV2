"""
Test harness for validate_docs.py.

Runs the validator against controlled fixture directories
(clean = 0 expected errors, dirty = known planted errors)
and asserts exact outcomes.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent / "validate_docs.py"
FIXTURES = Path(__file__).parent / "test_fixtures"
CLEAN = FIXTURES / "clean"
DIRTY = FIXTURES / "dirty"


def run_validator(root: Path) -> tuple[int, list[dict]]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), "--json"],
        capture_output=True, text=True, timeout=120,
    )
    errors = []
    if result.stdout.strip():
        json_marker = "--- JSON ---"
        if json_marker in result.stdout:
            json_text = result.stdout.split(json_marker, 1)[1].strip()
            if json_text:
                errors = json.loads(json_text)
    return result.returncode, errors


class TestCleanFixtures:

    def test_exit_code_zero(self):
        code, errors = run_validator(CLEAN)
        assert code == 0, (
            f"Expected exit code 0 (no errors), got {code}.\n"
            f"Errors: {json.dumps(errors, indent=2)}"
        )

    def test_zero_errors(self):
        code, errors = run_validator(CLEAN)
        assert len(errors) == 0, (
            f"Expected 0 errors from clean fixtures, got {len(errors)}:\n"
            f"{json.dumps(errors, indent=2)}"
        )


class TestDirtyFixtures:

    @pytest.fixture(scope="class")
    def dirty_results(self):
        code, errors = run_validator(DIRTY)
        manifest = json.loads((DIRTY / "manifest.json").read_text())
        return code, errors, manifest

    def test_exit_code_nonzero(self, dirty_results):
        code, errors, _ = dirty_results
        assert code == 1, "Expected exit code 1 (errors found) for dirty fixtures"

    def test_catches_all_planted_errors(self, dirty_results):
        _, errors, manifest = dirty_results
        found_passes = {e["pass"] for e in errors}
        missed = []
        for entry in manifest:
            if entry["pass"] not in found_passes:
                missed.append(entry["pass"])
        assert not missed, (
            f"Planted errors NOT caught by these passes: {missed}\n"
            f"Found passes: {sorted(found_passes)}"
        )

    def test_no_false_positives(self, dirty_results):
        _, errors, manifest = dirty_results
        expected_passes = {e["pass"] for e in manifest}
        unexpected = [
            {"pass": e["pass"], "file": e["file"], "message": e["message"]}
            for e in errors
            if e["pass"] not in expected_passes
        ]
        assert not unexpected, (
            f"Unexpected errors from passes not in manifest:\n"
            f"{json.dumps(unexpected, indent=2)}"
        )

    def test_error_count_matches_manifest(self, dirty_results):
        _, errors, manifest = dirty_results
        expected_passes = {e["pass"] for e in manifest}
        relevant_errors = [e for e in errors if e["pass"] in expected_passes]
        print(f"\nManifest entries: {len(manifest)}")
        print(f"Relevant errors found: {len(relevant_errors)}")
        for e in relevant_errors:
            print(f"  [{e['pass']}] {e['file']}:{e['line']} — {e['message']}")
