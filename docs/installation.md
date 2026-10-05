# Installation and execution

## Requirements

- Python 3.10 or later with pip.
- JDK 17 or later with both `java` and `javac` on `PATH`.
- VS Code is optional; open this folder and use its PowerShell terminal.

## Windows local setup

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
java -version
javac -version
streamlit run app.py
```

If activation is blocked by the current PowerShell process policy, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate. Streamlit opens a localhost URL in the browser.

## Java integration

No manual Java build is needed for ordinary use. `integration/java_bridge.py` checks the JDK, compiles the source files when changed and starts `Main` with a JSON request. Compilation output is stored under the ignored `java_engine/out` directory. Errors and timeouts are reported in the app. Run Java directly with `java -cp java_engine/out Main` and one JSON object on stdin after the bridge has compiled it.

## Tests

Run `python -m unittest discover -s tests -v`. Streamlit page smoke tests use `streamlit.testing.v1.AppTest`; Java graph integration tests compile and invoke the real Java source.

## Streamlit Community Cloud

Choose `app.py` as the app entry point. Cloud dependencies are declared in `requirements.txt`; `packages.txt` installs OpenJDK 17 JDK so the Java source can compile. Keep `java_engine/src/` in the repository. Do not commit `.venv`, `java_engine/out`, system logs or secrets.
