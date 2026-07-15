"""Tests for warmhold's page-cache rewarm helpers."""

import sys

import warmhold


def test_rewarm_reads_files_and_reports_totals(tmp_path):
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"x" * 1000)
    b.write_bytes(b"y" * 500)
    missing = tmp_path / "gone.bin"

    files, total = warmhold.rewarm([str(a), str(b), str(missing)])

    assert files == 2  # missing file skipped, not fatal
    assert total == 1500


def test_module_files_includes_pyc_for_py_modules():
    files = warmhold.module_files()

    # warmhold itself is imported from a .py file, so both the source and
    # its bytecode cache path must be listed (a fresh python reads the .pyc).
    assert warmhold.__file__ in files
    assert any(f.endswith(".pyc") and "warmhold" in f for f in files)
    # C extension modules only have their .so/.pyd listed, never a fake .pyc.
    assert all(f.endswith((".py", ".pyc")) or ".so" in f or ".pyd" in f for f in files)
    assert len(files) >= len([m for m in sys.modules.values() if getattr(m, "__file__", None)])
