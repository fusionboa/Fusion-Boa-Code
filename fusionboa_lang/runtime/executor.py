"""
FusionBoa Language Runtime Executor

Runs compiled Fusion code in the target language.
Supports Python, JavaScript, Ruby, Go, Rust, TypeScript,
C++, Julia, R, Kotlin, Swift, Java, C#, and Lua execution.
"""

import subprocess
import tempfile
import os
import sys
from typing import Optional


class RuntimeError(Exception):
    """Error raised when runtime execution fails."""
    pass


def execute_python(code: str) -> tuple[str, str, int]:
    """Execute Python code and return (stdout, stderr, exit_code)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Execution timed out after 30 seconds", 1
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def execute_javascript(code: str) -> tuple[str, str, int]:
    """Execute JavaScript code using Node.js and return (stdout, stderr, exit_code)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".js", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            ["node", tmp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "Node.js is not installed. Please install Node.js to run JavaScript output.", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out after 30 seconds", 1
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def execute_ruby(code: str) -> tuple[str, str, int]:
    """Execute Ruby code."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".rb", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(["ruby", tmp_path], capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "Ruby is not installed. Install from https://ruby-lang.org", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(tmp_path)
        except OSError: pass


def execute_go(code: str) -> tuple[str, str, int]:
    """Execute Go code."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".go", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(["go", "run", tmp_path], capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "Go is not installed. Install from https://go.dev", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(tmp_path)
        except OSError: pass


def execute_rust(code: str) -> tuple[str, str, int]:
    """Execute Rust code."""
    return "", "Rust requires compilation. Use 'fusionboa build file.fusboa --target rust' and compile with rustc.", 0


def execute_typescript(code: str) -> tuple[str, str, int]:
    """Execute TypeScript code via ts-node or deno."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ts", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name
    try:
        # Try ts-node first, then deno
        result = subprocess.run(["npx", "ts-node", tmp_path], capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        try:
            result = subprocess.run(["deno", "run", tmp_path], capture_output=True, text=True, timeout=30)
            return result.stdout, result.stderr, result.returncode
        except FileNotFoundError:
            return "", "Install ts-node (npm install -g ts-node) or deno (https://deno.com) to run TypeScript.", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(tmp_path)
        except OSError: pass


def execute_cpp(code: str) -> tuple[str, str, int]:
    """Execute C++ code by compiling with g++ then running."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False, encoding="utf-8") as f:
        f.write(code)
        src_path = f.name

    exe_path = src_path.replace(".cpp", ".exe" if sys.platform == "win32" else "")

    try:
        # Compile
        compile_result = subprocess.run(
            ["g++", "-std=c++17", "-o", exe_path, src_path],
            capture_output=True, text=True, timeout=30
        )
        if compile_result.returncode != 0:
            return "", f"Compilation failed:\n{compile_result.stderr}", compile_result.returncode

        # Run
        run_result = subprocess.run([exe_path], capture_output=True, text=True, timeout=30)
        return run_result.stdout, run_result.stderr, run_result.returncode
    except FileNotFoundError:
        return "", "g++ not found. Install GCC/G++ or use 'fusionboa build file.fusboa --target cpp' to generate code and compile manually.", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(src_path)
        except OSError: pass
        try: os.unlink(exe_path)
        except OSError: pass


def execute_julia(code: str) -> tuple[str, str, int]:
    """Execute Julia code."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jl", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(["julia", tmp_path], capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "Julia is not installed. Install from https://julialang.org", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(tmp_path)
        except OSError: pass


def execute_r(code: str) -> tuple[str, str, int]:
    """Execute R code."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".r", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(["Rscript", tmp_path], capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "R is not installed. Install from https://cran.r-project.org", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(tmp_path)
        except OSError: pass


def execute_kotlin(code: str) -> tuple[str, str, int]:
    """Execute Kotlin code via kotlin compiler or kotlinc."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".kt", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(["kotlin", tmp_path], capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        try:
            result = subprocess.run(["kotlinc", "-script", tmp_path], capture_output=True, text=True, timeout=30)
            return result.stdout, result.stderr, result.returncode
        except FileNotFoundError:
            return "", "Kotlin is not installed. Install from https://kotlinlang.org", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(tmp_path)
        except OSError: pass


def execute_swift(code: str) -> tuple[str, str, int]:
    """Execute Swift code."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".swift", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(["swift", tmp_path], capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "Swift is not installed. Install from https://swift.org (macOS/Linux)", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(tmp_path)
        except OSError: pass


def execute_java(code: str) -> tuple[str, str, int]:
    """Execute Java code by compiling with javac then running."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".java", delete=False, encoding="utf-8") as f:
        f.write(code)
        src_path = f.name

    # Java requires filename matching class name; use temp dir
    tmp_dir = tempfile.mkdtemp()
    java_file = os.path.join(tmp_dir, "FusionBoaProgram.java")

    try:
        os.rename(src_path, java_file)
        src_path = None

        # Compile
        compile_result = subprocess.run(
            ["javac", java_file],
            capture_output=True, text=True, timeout=30
        )
        if compile_result.returncode != 0:
            return "", f"Compilation failed:\n{compile_result.stderr}", compile_result.returncode

        # Run
        run_result = subprocess.run(
            ["java", "-cp", tmp_dir, "FusionBoaProgram"],
            capture_output=True, text=True, timeout=30
        )
        return run_result.stdout, run_result.stderr, run_result.returncode
    except FileNotFoundError:
        return "", "Java JDK not found. Install from https://adoptium.net", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        if src_path:
            try: os.unlink(src_path)
            except OSError: pass
        try:
            import shutil
            shutil.rmtree(tmp_dir)
        except OSError:
            pass


def execute_csharp(code: str) -> tuple[str, str, int]:
    """Execute C# code using dotnet-script or csc."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csx", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(["dotnet-script", tmp_path], capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        try:
            result = subprocess.run(["dotnet", "script", tmp_path], capture_output=True, text=True, timeout=30)
            return result.stdout, result.stderr, result.returncode
        except FileNotFoundError:
            return "", ".NET SDK not found. Install from https://dotnet.microsoft.com or use 'dotnet script' for .csx files.", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(tmp_path)
        except OSError: pass


def execute_lua(code: str) -> tuple[str, str, int]:
    """Execute Lua code."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".lua", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(["lua", tmp_path], capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "Lua is not installed. Install from https://lua.org or use 'fusionboa build file.fusboa --target lua' to generate code.", 1
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", 1
    finally:
        try: os.unlink(tmp_path)
        except OSError: pass


def execute(code: str, target: str = "python") -> tuple[str, str, int]:
    """Execute compiled code in the target language."""
    runners = {
        "python": execute_python, "py": execute_python,
        "javascript": execute_javascript, "js": execute_javascript,
        "ruby": execute_ruby, "rb": execute_ruby,
        "go": execute_go, "golang": execute_go,
        "rust": execute_rust, "rs": execute_rust,
        "typescript": execute_typescript, "ts": execute_typescript,
        "cpp": execute_cpp, "c++": execute_cpp,
        "julia": execute_julia, "jl": execute_julia,
        "r": execute_r,
        "kotlin": execute_kotlin, "kt": execute_kotlin,
        "swift": execute_swift,
        "java": execute_java,
        "csharp": execute_csharp, "cs": execute_csharp, "c#": execute_csharp,
        "lua": execute_lua,
    }
    runner = runners.get(target)
    if runner is None:
        raise RuntimeError(f"Unsupported target language: {target}")
    return runner(code)
