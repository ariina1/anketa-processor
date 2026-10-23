def normalize_fio(value):
    words = value.split()
    if len(words) < 2:
        return None, 'в ФИО меньше двух слов'
    return ' '.join(word.capitalize() for word in words), None

def check_mail(value):
    mail = value.strip().lower()
    if mail.count('@') != 1:
        return None, f'почта неверная: {value.strip()}'
    local, domain = mail.split('@')
    if not local or not domain or '.' not in domain:
        return None, f'почта неверная: {value.strip()}'
    if domain.startswith('.') or domain.endswith('.'):
        return None, f'почта неверная: {value.strip()}'
    return mail, None

def check_phone(value):
    digits = ''.join(ch for ch in value if ch.isdigit())
    if len(digits) != 11 or digits[0] not in '78':
        return None, f'телефон неверный: {value.strip()}'
    if digits[0] == '8':
        digits = '7' + digits[1:]
    return digits, None

def parse_line(line):
    fields = line.split(';')
    if len(fields) != 4:
        return None, f'полей должно быть 4, получено {len(fields)}'
    fio, mail, phone, group = (field.strip() for field in fields)
    fio, error = normalize_fio(fio)
    if error:
        return None, error
    mail, error = check_mail(mail)
    if error:
        return None, error
    phone, error = check_phone(phone)
    if error:
        return None, error
    group = ''.join(group.split()).lower()
    if not group:
        return None, 'группа пустая'
    return {'fio': fio, 'mail': mail, 'phone': phone, 'group': group}, None