import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("guard", ROOT / "scripts" / "check_no_data.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def names(text, rel="docs/x.md"):
    return {f.split(": ", 1)[1] for f in guard.check_text(rel, text)}


def test_clean_documentation_passes():
    assert names("We estimate reach using a public trial registry and a national health survey.") == set()


def test_blocks_identifiers_pii_and_paths():
    nct = "NCT" + "12345678"
    assert "trial registry identifier" in names(f"see {nct} for details")
    assert "email address" in names("contact " + "someone" + "@" + "example.org")
    assert "phone number" in names("call 555" + "-123-" + "4567")
    assert "absolute local path" in names("saved to /Users/" + "someone/work")
    assert "data directory path" in names("read from (data/" + "trials.json)")
    assert "survey respondent id" in names("SEQ" + "N 12345")
    assert "survey respondent id" not in names("the SEQ" + "N column links the tables")
    assert "data file URL" in names("download https://example.org/files/table" + ".xpt now")
    assert "secret-like token" in names("key " + "ghp_" + "a" * 36)


def test_allows_noreply_commit_email():
    assert names("Author: 1234+name@" + "users.noreply.github.com") == set()


def test_blocks_data_file_types_and_directories():
    assert guard.check_path("anything/table" + ".csv")
    assert guard.check_path("raw/readme.md")
    assert not guard.check_path("src/trial_reach/__init__.py")


def test_repository_itself_is_clean():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_no_data.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
