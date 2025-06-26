import os

def get_files_info(working_directory, directory=None):
    try:
        # 1. Si directory es None, usamos el working_directory
        target = working_directory if directory is None else directory

        # 2. Obtenemos las rutas absolutas
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, target))

        # 3. Validamos si está fuera del directorio permitido
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # 4. Verificamos si es una carpeta válida
        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'

        # 5. Armamos la lista con la info de cada archivo/carpeta
        lines = []
        for item in os.listdir(abs_target):
            full_path = os.path.join(abs_target, item)
            try:
                size = os.path.getsize(full_path)
                is_dir = os.path.isdir(full_path)
                lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                lines.append(f"- {item}: Error reading file ({str(e)})")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {str(e)}"



