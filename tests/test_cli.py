import subprocess
import sys


def test_cli_help():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "agentaudit.cli",
            "--help",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "AgentAudit" in result.stdout
    assert "--failure" in result.stdout
    assert "--runs" in result.stdout