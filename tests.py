from functions.get_files_info import get_files_info

if __name__ == "__main__":
    print(get_files_info("calculator", "."))
    print()
    print(get_files_info("calculator", "pkg"))
    print()
    print(get_files_info("calculator", "/bin"))  # debería mostrar error
    print()
    print(get_files_info("calculator", "../"))   # también debería mostrar error
