import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    # Verificar que al menos hay un argumento (el prompt)
    if len(sys.argv) < 2:
        print("Error: Debes ingresar un prompt como argumento.")
        print("Uso: python3 main.py 'Tu pregunta aquí' [--verbose]")
        return

    # Leer argumentos
    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    # Cargar API key desde el archivo .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY no está definido en el archivo .env")
        return

    # Inicializar cliente
    client = genai.Client(api_key=api_key)

    # Crear mensaje con el rol "user"
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    # Mostrar info detallada si verbose está activado
    if verbose:
        print(f"User prompt: {user_prompt}")

    # Generar respuesta
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    # Mostrar tokens solo si verbose está activado
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Imprimir respuesta del modelo
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()

