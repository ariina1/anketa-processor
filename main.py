from validators import parse_line
from collections import Counter

INPUT_FILE = 'anketa.txt'
OK_FILE = 'ok.txt'
ERROR_FILE = 'errors.txt'

def mask_phone(phone):
    return f'+7 ({phone[1:4]}) ***-**-{phone[-2:]}'

def show_table(accepted):
    print(f'{"№":>3} {"ФИО":<28} {"Почта":<25} {"Телефон":<19} Группа')
    print('-' * 88)
    for number, item in enumerate(accepted, 1):
        print(f'{number:>3} {item["fio"][:28]:<28} {item["mail"][:25]:<25} '
              f'{mask_phone(item["phone"]):<19} {item["group"]}')
    print('-' * 88)

def main():
    accepted = []
    rejected = []
    try:
        with open(INPUT_FILE, encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f'Файл {INPUT_FILE} не найден')
        return

    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        item, error = parse_line(line.rstrip('\n'))
        if error:
            rejected.append({'number': number, 'line': line.rstrip('\n'), 'reason': error})
        else:
            accepted.append(item)

    accepted.sort(key=lambda item: item['fio'].casefold())
    show_table(accepted)

    print(f'Отклонено строк: {len(rejected)}')
    for item in rejected:
        print(f'  строка {item["number"]}: {item["reason"]}')
        print(f'      {item["line"]}')

    print(f'\nВсего строк в файле: {len(lines)}')
    print(f'Принято: {len(accepted)} | Отклонено: {len(rejected)}')
    print('\nПо группам:')
    for group, count in sorted(Counter(item['group'] for item in accepted).items()):
        print(f'  {group:<8} {count}')

    with open(OK_FILE, 'w', encoding='utf-8') as file:
        for item in accepted:
            file.write(f'{item["fio"]};{item["mail"]};{item["phone"]};{item["group"]}\n')
    with open(ERROR_FILE, 'w', encoding='utf-8') as file:
        for item in rejected:
            file.write(f'Строка {item["number"]}: {item["reason"]} | {item["line"]}\n')
    print(f'\nСохранено: {OK_FILE} и {ERROR_FILE}')

if __name__ == '__main__':
    main()