import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from agent_loop import run_agent_loop

def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user makes a request, do not attempt to answer it directly unless absolutely necessary.
Instead, you should reason step by step and decide which function(s) to call from the available tools.
Your available tools are:

- get_files_info: List files and directories
- get_file_content: Read file contents
- write_file: Write or overwrite files
- run_python_file: Execute Python files

If the user mentions a bug or that a calculation is wrong, always assume it is your job to:
1. Investigate the code,
2. Find and fix the problem,
3. Test that it works correctly.

Use all tools available to gather information and verify fixes. Do not ask the user for clarification if you can find the answer by inspecting the code.

All file paths should be relative to the working directory. Do not specify the working directory as an argument.
"""

    if len(sys.argv) < 2:
        print("Error: Debes ingresar un prompt como argumento.")
        print("Uso: python3 main.py 'Tu pregunta aquí' [--verbose]")
        return

    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY no está definido en el archivo .env")
        return

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    if verbose:
        print(f"User prompt: {user_prompt}")

    # Ejecutar bucle del agente
    run_agent_loop(client=client, messages=messages, system_prompt=system_prompt, verbose=verbose)

if __name__ == "__main__":
    main()
