from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def get_function_declarations():
    return [
        types.FunctionDeclaration(
            name="get_files_info",
            description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "directory": types.Schema(
                        type=types.Type.STRING,
                        description="The directory to list files from, relative to the working directory.",
                    ),
                },
            ),
        ),
        types.FunctionDeclaration(
            name="get_file_content",
            description="Reads and returns the content of a file, constrained to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The relative path to the file to read.",
                    ),
                },
            ),
        ),
        types.FunctionDeclaration(
            name="write_file",
            description="Writes or overwrites a file with the given content, constrained to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The relative path to the file to write.",
                    ),
                    "content": types.Schema(
                        type=types.Type.STRING,
                        description="The content to write to the file.",
                    ),
                },
            ),
        ),
        types.FunctionDeclaration(
            name="run_python_file",
            description="Executes a Python file within the working directory and returns its output.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The relative path to the Python file to run.",
                    ),
                },
            ),
        ),
    ]

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args or {}
    args["working_directory"] = "calculator"

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        function_result = function_map[function_name](**args)
    except Exception as e:
        function_result = f"Error while executing function: {str(e)}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

def run_agent_loop(client, messages, system_prompt, verbose=False):
    tools = types.Tool(function_declarations=get_function_declarations())
    MAX_ITERATIONS = 20

    for i in range(MAX_ITERATIONS):
        if verbose:
            print(f"\n--- Iteración {i + 1} ---")

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[tools],
                system_instruction=system_prompt,
            ),
        )

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        candidate = response.candidates[0]
        content = candidate.content
        #if verbose:
        #    print("DEBUG: response.candidates[0].content.parts:")
        #    for part in content.parts:
        #        print(" -", type(part), getattr(part, "function_call", None), getattr(part, "text", None))

        messages.append(content)  # Agrega lo que el modelo "dijo"

        final_response = None

        for part in content.parts:
            if part.function_call:
                function_call = part.function_call
                tool_response = call_function(function_call, verbose)
                messages.append(tool_response)
                break  # después de llamar una función, saltamos a la siguiente iteración
            elif part.text:
                final_response = part.text

        # Si no pidió ejecutar función, ya terminó
        if not any(part.function_call for part in content.parts):
            print("Final response:")
            print(final_response)
            break
