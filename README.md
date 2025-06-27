# AI Coding Agent con Gemini

Este proyecto implementa un **agente inteligente** que puede razonar y ejecutar tareas de programación sobre un entorno controlado. Utiliza la API de **Gemini** (Google AI) para interpretar instrucciones del usuario y operar sobre funciones definidas, como inspeccionar archivos, modificar código, y ejecutar scripts Python.

## ⚙️ Funcionalidades

El agente es capaz de:

- 📁 **Listar archivos y carpetas** en el directorio de trabajo.
- 📄 **Leer contenido de archivos** fuente.
- ✏️ **Escribir o sobrescribir archivos**.
- 🧪 **Ejecutar archivos Python** y leer su salida.
- 🔁 Mantener un **bucle iterativo**, decidiendo qué función ejecutar paso a paso, como lo haría un agente autónomo.

## 🧠 Ejemplos de Prompts

```bash
python main.py "how does the calculator render results to the console?"
```

El agente analiza el entorno, inspecciona archivos, modifica código si es necesario y ejecuta pruebas para validar los cambios.

🧪 Dependencias
Python 3.10+

google-generativeai

python-dotenv

🧠 Próximos pasos
Mejorar la capacidad del agente para interpretar prompts más vagos.

Agregar funciones más complejas como análisis de errores o refactorización.

Integrar feedback directo en las respuestas del agente.