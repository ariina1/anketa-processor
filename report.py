def mask_phone(phone):
    return f'+7 ({phone[1:4]}) ***-**-{phone[-2:]}'

def show_table(accepted):
    print(f'{"№":>3} {"ФИО":<28} {"Почта":<25} {"Телефон":<19} Группа')
    print('-' * 88)
    for number, item in enumerate(accepted, 1):
        print(f'{number:>3} {item["fio"][:28]:<28} {item["mail"][:25]:<25} '
              f'{mask_phone(item["phone"]):<19} {item["group"]}')
    print('-' * 88)