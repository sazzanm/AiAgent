import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Aquí importa tus funciones reales, asumiendo que están en 'functions' (modifícalo si es necesario)
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def get_function_declarations():
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
                ),
            },
        ),
    )
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads and returns the content of a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The relative path to the file to read."
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes or overwrites a file with the given content, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The relative path to the file to write."
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file."
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to run."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python script.",
            )
        },
        required=["file_path"]
    ),
)
    return [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args  # ya es un diccionario, no json.loads

    if verbose:
        print(f"Calling function: {function_name}({args})")

    # Añadir working_directory automáticamente
    args["working_directory"] = "./calculator"

    functions_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in functions_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ],
        )

    try:
        result = functions_map[function_name](**args)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Exception during function call: {e}"}
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result}
            )
        ],
     )
def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    if verbose:
        print(f"User prompt: {user_prompt}")

    tools = types.Tool(function_declarations=get_function_declarations())

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[tools],
            system_instruction=system_prompt
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    print("Response:")

    # Aquí chequeamos si el modelo quiere llamar a una función
    if response.candidates and response.candidates[0].content.parts:
        part = response.candidates[0].content.parts[0]
        if part.function_call:
            # Llamar a la función
            function_call_result = call_function(part.function_call, verbose=verbose)
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            # Imprimir el resultado
            print(function_call_result.parts[0].function_response.response.get("result", ""))
        else:
            # No es una llamada a función, solo texto normal
            for part in response.candidates[0].content.parts:
                if part.text:
                    print(part.text)
    else:
        print("[No response from model]")

if __name__ == "__main__":
    main()
