import sys
import os
import locale

if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

from registry import Registry

def main():
    filename = "anketa.txt"
    registry = Registry()
    print(f"Открывая файл: {os.path.abspath(filename)}")

    if not os.path.exists(filename):
        print(f"КРИТИЧЕСКАЯ ОШИБКА: Файл '{filename}' НЕ СУЩЕСТВУЕТ в этой папке!")
        print("Убедитесь, что вы создали файл anketa.txt в той же папке, где лежит main.py")
        sys.exit(1)

    if not registry.load(filename):
        print("Ошибка при чтении файла.")
        sys.exit(1)

    print(f"Файл прочитан. Найдено принятых: {len(registry)}, отклоненных: {len(registry.rejected)}")

    if len(registry) == 0 and len(registry.rejected) == 0:
        print("\nВНИМАНИЕ: Файл anketa.txt пустой или в нем нет подходящих строк.")
        print("Проверьте, что данные разделены точкой с запятой (;), а не запятой или пробелом.")
        return

    registry.print_report()
    
    registry.save()
    print("\nФайлы ok.txt и errors.txt успешно сохранены.")

if __name__ == "__main__":
    main()
