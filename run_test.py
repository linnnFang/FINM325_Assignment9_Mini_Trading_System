import io
import os
import contextlib
import pytest

def main():
    # Make sure we run pytest from the project root (where this file lives)
    ROOT = os.path.dirname(os.path.abspath(__file__))
    os.chdir(ROOT)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        retcode = pytest.main([
            "-q",
            "--maxfail=1",
            "--disable-warnings",
            "--cov=.",                 # <--- measure all code in this directory
            "--cov-report=term-missing",
        ])

    test_output = buf.getvalue()

    report_md = "# Test & Coverage Report\n\n"
    if retcode == 0:
        report_md += "- ✅ All tests passed successfully.\n\n"
    else:
        report_md += f"- ⚠️ Pytest exited with return code `{retcode}`.\n\n"

    report_md += "## Detailed Pytest & Coverage Output\n\n```text\n"
    report_md += test_output
    report_md += "\n```\n"

    with open("coverage_report.md", "w") as f:
        f.write(report_md)

if __name__ == "__main__":
    main()
