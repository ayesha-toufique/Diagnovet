"""One-pass environment verification for Diagnovet."""
import sys, os, sqlite3

results = []

def check(name, fn):
    try:
        val = fn()
        results.append((name, "PASS", val))
        print(f"  [PASS] {name}: {val}")
    except Exception as e:
        results.append((name, "FAIL", str(e)))
        print(f"  [FAIL] {name}: {e}")

print("=" * 60)
print("DIAGNOVET ENVIRONMENT VERIFICATION")
print("=" * 60)

# Python & pip
check("Python executable", lambda: sys.executable)
check("Python version", lambda: sys.version.split()[0])

import pip
check("Pip version", lambda: pip.__version__)

# Core packages
import streamlit; check("Streamlit", lambda: streamlit.__version__)
import pandas; check("Pandas", lambda: pandas.__version__)
import numpy; check("NumPy", lambda: numpy.__version__)
import plotly; check("Plotly", lambda: plotly.__version__)
import PIL; check("Pillow", lambda: PIL.__version__)

# Dev tools
import pytest; check("Pytest", lambda: pytest.__version__)
import coverage; check("Pytest-cov (coverage)", lambda: coverage.__version__)
import black; check("Black", lambda: black.__version__)
import flake8; check("Flake8", lambda: flake8.__version__)

# SQLite
check("SQLite import", lambda: sqlite3.sqlite_version)
def sqlite_test():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO test VALUES (1, 'diagnovet')")
    row = conn.execute("SELECT * FROM test").fetchone()
    conn.close()
    return f"OK - row={row}"
check("SQLite in-memory DB", sqlite_test)

# Paths
check("PIP_CACHE_DIR", lambda: os.environ.get("PIP_CACHE_DIR", "(not set)"))
check("TEMP", lambda: os.environ.get("TEMP", "(not set)"))
check("TMP", lambda: os.environ.get("TMP", "(not set)"))

# Disk space
import shutil
usage = shutil.disk_usage("D:\\")
free_gb = round(usage.free / (1024**3), 2)
check("D: free space", lambda: f"{free_gb} GB")

print("=" * 60)
passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
print(f"TOTAL: {passed} passed, {failed} failed out of {len(results)} checks")
print("=" * 60)
sys.exit(1 if failed > 0 else 0)
