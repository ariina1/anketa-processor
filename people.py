import re

class AnketaError(Exception):
    """Своё исключение для ошибок в анкете."""
    pass

class Person:
    def __init__(self, fio, mail, phone):
        self.fio = self.check_fio(fio)
        self.mail = self.check_mail(mail)
        self.phone = self.check_phone(phone)

    @staticmethod
    def check_fio(fio):
        words = fio.strip().split()
        if len(words) < 2:
            raise AnketaError("в ФИО меньше двух слов")
        if not all(re.fullmatch(r"[А-ЯЁа-яёA-Za-z-]+", w) for w in words):
            raise AnketaError("ФИО содержит недопустимые символы")
        return " ".join(w.capitalize() for w in words)

    @staticmethod
    def check_mail(mail):
        mail = mail.strip().lower()
        if mail.count("@") != 1:
            raise AnketaError(f"Почта неверная: {mail}")
        local, domain = mail.split("@")
        if not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise AnketaError(f"Почта неверная: {mail}")
        return mail

    @staticmethod
    def check_phone(phone):
        digits = "".join(c for c in phone if c.isdigit())
        if len(digits) != 11 or digits[0] not in "78":
            raise AnketaError(f"Телефон неверный: {phone.strip()}")
        if digits[0] == "8":
            digits = "7" + digits[1:]
        return digits

    def short_fio(self):
        parts = self.fio.split()
        return f"{parts[0]} {parts[1][0]}. {parts[2][0]}." if len(parts) > 2 else f"{parts[0]} {parts[1][0]}."

    def masked_phone(self):
        return f"+{self.phone[0]} ({self.phone[1:4]}) ***-***-{self.phone[-2:]}"

    def role(self):
        return "неизвестно"

    def extra(self):
        return ""

    def __str__(self):
        return f"{self.fio}"

    def __lt__(self, other):
        return self.fio < other.fio

class Student(Person):
    def __init__(self, fio, mail, phone, group):
        super().__init__(fio, mail, phone)
        if not group.strip():
            raise AnketaError("пустая группа")
        self.group = group.strip()

    def role(self):
        return "студент"

    def extra(self):
        return self.group

class Teacher(Person):
    def __init__(self, fio, mail, phone, department):
        super().__init__(fio, mail, phone)
        if not department.strip():
            raise AnketaError("пустая кафедра")
        self.department = department.strip()

    def role(self):
        return "преподаватель"

    def extra(self):
        return self.department
