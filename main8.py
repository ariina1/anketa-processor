import json
from client import get_all_ankety, check_mail, get_statistika, ServerNedostupen
from people import Student, Teacher, AnketaError
from registry import Registry

def main():
    registry = Registry()
    source = "Сервер"
    
    print("Пытаюсь получить данные с сервера...")
    try:
        anketi = get_all_ankety()
    except ServerNedostupen as e:
        print(f"Ошибка: {e}")
        print("Переключаюсь на запасной источник (файл anketa.txt)...")
        if registry.load("anketa.txt"):
            source = "Файл anketa.txt"
        else:
            print("Нет ни сервера, ни файла anketa.txt. Завершение.")
            return
    
    if source == "Сервер":
        for item in anketi:
            try:
                tip = item.get("tip")
                if tip == "s":
                    p = Student(item["fio"], item["mail"], item["phone"], item["gruppa"])
                elif tip == "t":
                    p = Teacher(item["fio"], item["mail"], item["phone"], item["kafedra"])
                else:
                    raise AnketaError(f"неизвестный тип: {tip}")
                registry.add(p)
            except AnketaError as e:
                registry.reject(item.get("nomer", "?"), str(item), str(e))
    
    print(f"\n=== ИСТОЧНИК ДАННЫХ: {source} ===")
    registry.print_report()
    
    if source == "Сервер":
        try:
            srv_stat = get_statistika()
            print(f"\nСтатистика самого сервера: всего {srv_stat['vsego']}, по ролям: {srv_stat['po_rolyam']}")
        except ServerNedostupen:
            print("\nНе удалось получить статистику сервера.")

    print("\nПроверка почт принятых анкет через /proverka:")
    for p in registry.accepted:
        try:
            ok = check_mail(p.mail)
            print(f"  {p.fio}: {'OK' if ok else 'Неверная почта'}")
        except ServerNedostupen:
            print("  Сервер пропал во время проверки почты.")

    report_data = {
        "istochnik": source,
        "prinyato": len(registry),
        "otkloneno": len(registry.rejected),
        "spisok_prinyatyh": [p.fio for p in registry.accepted],
        "spisok_otklonennyh": registry.rejected
    }
    with open("otchet.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    print("\nИтоговый отчёт сохранён в файл otchet.json")

if __name__ == "__main__":
    main()