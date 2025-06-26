import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        abs_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_dir_abs = os.path.abspath(working_directory)

        if not abs_path.startswith(working_dir_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_path):
            return f'Error: File "{file_path}" not found.'

        if not abs_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
            ["python3", abs_path],
            capture_output=True,
            text=True,
            cwd=working_dir_abs,
            timeout=30
        )

        output = []

        if result.stdout:
            output.append("STDOUT:\n" + result.stdout.strip())
        if result.stderr:
            output.append("STDERR:\n" + result.stderr.strip())

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if not output:
            return "No output produced."

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
