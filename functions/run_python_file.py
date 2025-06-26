import os
def run_python_file(working_directory, file_path, args=None):
    import subprocess
    try:
        abs_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        cmd = ["python3", abs_path]
        if args:
            cmd.extend(args)

        result = subprocess.run(cmd, cwd=working_directory, capture_output=True, text=True, timeout=30)

        output = ""
        if result.stdout:
            output += "STDOUT:\n" + result.stdout
        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"

        return output if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
