import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Optional
import unittest


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "sync-env.py"
EXAMPLE = ROOT / "env" / ".env.example"


class SyncEnvTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.home = Path(self.temp_dir.name)
        self.env_path = self.home / ".env"
        self.keys = re.findall(
            r"^\s*export\s+([A-Za-z_][A-Za-z0-9_]*)\s*=",
            EXAMPLE.read_text(encoding="utf-8"),
            re.MULTILINE,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_sync(self) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(self.home)
        return subprocess.run(
            ["python3", str(SCRIPT)],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

    def complete_env(self, excluded: Optional[set[str]] = None) -> str:
        excluded = excluded or set()
        return "".join(
            f"export {key}={key.lower()}\n"
            for key in self.keys
            if key not in excluded
        )

    def test_preserves_exported_assignments(self) -> None:
        original = self.complete_env()
        self.env_path.write_text(original, encoding="utf-8")

        self.run_sync()

        self.assertEqual(self.env_path.read_text(encoding="utf-8"), original)

    def test_exports_unexported_assignment_without_overwriting_value(self) -> None:
        original = self.complete_env({"EXA_API_KEY"}) + "EXA_API_KEY=secret\n"
        self.env_path.write_text(original, encoding="utf-8")

        self.run_sync()

        self.assertEqual(
            self.env_path.read_text(encoding="utf-8"),
            original
            + "# Added by make install (synchronized from env/.env.example)\n"
            + "export EXA_API_KEY\n",
        )

    def test_appends_missing_assignment(self) -> None:
        original = self.complete_env({"EXA_API_KEY"})
        self.env_path.write_text(original, encoding="utf-8")

        self.run_sync()

        self.assertTrue(
            self.env_path.read_text(encoding="utf-8").endswith(
                "export EXA_API_KEY=\n"
            )
        )

    def test_ignores_commented_assignment(self) -> None:
        original = self.complete_env({"EXA_API_KEY"}) + "# export EXA_API_KEY=secret\n"
        self.env_path.write_text(original, encoding="utf-8")

        self.run_sync()

        self.assertTrue(
            self.env_path.read_text(encoding="utf-8").endswith(
                "export EXA_API_KEY=\n"
            )
        )

    def test_does_not_append_duplicate_exported_assignment(self) -> None:
        original = (
            self.complete_env({"EXA_API_KEY"})
            + "export EXA_API_KEY=first\n"
            + "export EXA_API_KEY=second\n"
        )
        self.env_path.write_text(original, encoding="utf-8")

        self.run_sync()

        self.assertEqual(self.env_path.read_text(encoding="utf-8"), original)

    def test_preserves_bare_export_declaration(self) -> None:
        original = self.complete_env({"EXA_API_KEY"}) + "export EXA_API_KEY\n"
        self.env_path.write_text(original, encoding="utf-8")

        self.run_sync()

        self.assertEqual(self.env_path.read_text(encoding="utf-8"), original)

    def test_install_dry_run_does_not_create_env_file(self) -> None:
        env = os.environ.copy()
        env["HOME"] = str(self.home)

        subprocess.run(
            ["make", "-n", "install"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

        self.assertFalse(self.env_path.exists())


if __name__ == "__main__":
    unittest.main()
