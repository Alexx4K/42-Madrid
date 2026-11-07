#!/usr/bin/env python3

import importlib.util
import sys


def check_dependency(mod_name: str) -> tuple[bool, str]:
    spec = importlib.util.find_spec(mod_name)
    if spec is None:
        return False, ""
    try:
        mod = importlib.import_module(mod_name)
        version = getattr(mod, "__version__", "unknown")
        return True, str(version)
    except Exception:
        return False, ""


def main() -> None:
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")

    deps = ["pandas", "numpy", "requests", "matplotlib"]
    status: dict[str, tuple[bool, str]] = {}
    all_ok = True

    for dep in deps:
        ok, ver = check_dependency(dep)
        status[dep] = (ok, ver)
        if not ok and dep != "requests":
            all_ok = False

    descriptions = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "requests": "Network access ready",
        "matplotlib": "Visualization ready",
    }

    for dep in deps:
        ok, ver = status[dep]
        if ok:
            print(f"[OK] {dep} ({ver})")
            print(f"  -> {descriptions[dep]}")
        else:
            if dep == "requests":
                continue
            print(f"[MISSING] {dep}")

    if not all_ok:
        print("\nError: Missing required dependencies!")
        print("\nTo install via pip:")
        print("pip install -r requirements.txt")
        print("\nTo install via Poetry:")
        print("poetry install")
        sys.exit(1)

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    print("\nAnalyzing Matrix data...")
    print("Processing 1000 data points...")

    np.random.seed(42)
    raw_data = np.random.randn(1000)
    df = pd.DataFrame({"signal": raw_data})
    df["moving_avg"] = df["signal"].rolling(window=20).mean()

    print("Generating visualization...")
    plt.figure(figsize=(10, 5))
    plt.plot(df["signal"], alpha=0.3, label="Raw Matrix Signal")
    plt.plot(df["moving_avg"], color="green", label="Moving Average")
    plt.title("Matrix Data Stream Analysis")
    plt.xlabel("Data Point Index")
    plt.ylabel("Signal Value")
    plt.legend()
    plt.grid(True)
    plt.savefig("matrix_analysis.png")
    plt.close()

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
