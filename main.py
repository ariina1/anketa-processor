import sys
import os

if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

from registry import Registry

def main():
    filename = "anketa.txt"
    registry = Registry()

    if not os.path.exists(filename):
        print(f"Ошибка: файл '{filename}' не найден. Проверьте наличие файла.")
        sys.exit(1)

    if not registry.load(filename):
        print("Ошибка при чтении файла.")
        return

    registry.print_report()
    registry.save()
    print("\nФайлы ok.txt и errors.txt успешно сохранены.")

if __name__ == "__main__":
    main()
