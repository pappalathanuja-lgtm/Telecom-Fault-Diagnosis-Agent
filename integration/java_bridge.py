"""Compile and invoke the Java JSON graph engine."""
import json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "java_engine" / "src"
OUT = ROOT / "java_engine" / "out"
_COMPILED_SIGNATURE = None

class JavaUnavailable(RuntimeError): pass

def run_graph(request):
    global _COMPILED_SIGNATURE
    javac, java = shutil.which("javac"), shutil.which("java")
    if not javac or not java: raise JavaUnavailable("Java JDK 17+ is required. Install a JDK, add java and javac to PATH, restart the terminal, and run the diagnosis again.")
    sources = [str(p) for p in SRC.glob("*.java")]
    if not sources: raise RuntimeError("Java graph engine source files are missing.")
    OUT.mkdir(exist_ok=True)
    signature = tuple((path, Path(path).stat().st_mtime_ns) for path in sources)
    if signature != _COMPILED_SIGNATURE or not (OUT / "Main.class").exists():
        compiled = subprocess.run([javac, "-encoding", "UTF-8", "-d", str(OUT), *sources], capture_output=True, text=True, timeout=30)
        if compiled.returncode: raise RuntimeError("Java compilation failed: " + compiled.stderr[-1500:])
        _COMPILED_SIGNATURE = signature
    proc = subprocess.run([java, "-cp", str(OUT), "Main"], input=json.dumps(request), capture_output=True, text=True, timeout=15)
    if proc.returncode: raise RuntimeError("Java graph engine failed: " + proc.stderr[-1500:])
    return json.loads(proc.stdout)
