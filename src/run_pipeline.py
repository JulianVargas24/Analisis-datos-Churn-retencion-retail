
# src/run_pipeline.py
import os, sys, traceback, datetime, subprocess
# Al inicio del script principal
import sys, os
try:
    # Forzar stdout/stderr a UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = r"C:\Users\Julian\Desktop\churn-retail"
SRC  = os.path.join(ROOT, "src")

SCRIPTS = [
    os.path.join(SRC, "01_extract_clean.py"),
    os.path.join(SRC, "02_load_sqlserver.py"),
    os.path.join(SRC, "03_kpis_churn_sqlserver.py"),
]

def run_step(pyexe, script):
    print(f"[{datetime.datetime.now():%H:%M:%S}] ▶ {os.path.basename(script)}")
    # Fuerza el cwd del proceso hijo al ROOT del proyecto
    proc = subprocess.run([pyexe, script], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr)
        raise RuntimeError(f"Fallo {script} (rc={proc.returncode})")
    print(proc.stdout)

def main():
    pyexe = r"C:\Users\Julian\Desktop\churn-retail\.venv\Scripts\python.exe"
    print(f"===== INICIO {datetime.datetime.now():%Y-%m-%d %H:%M:%S} (.venv) =====")
    # Aun así, fija el cwd del proceso actual por si hay lecturas en este mismo proceso
    os.chdir(ROOT)
    for s in SCRIPTS:
        run_step(pyexe, s)
    print("===== OK ✓ =====")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
