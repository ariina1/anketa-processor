from people import Person, Student, Teacher, AnketaError, parse_line


class Registry:
    def __init__(self):
        self.accepted = []
        self.rejected = []

    def add(self, person):
        self.accepted.append(person)

    def reject(self, number, line, reason):
        self.rejected.append({
            "number": number,
            "line": line,
            "reason": reason
        })

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            return False

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            try:
                self.add(parse_line(line))
            except AnketaError as e:
                self.reject(i, line, str(e))
        return True

    def count_roles(self):
        roles = {}
        for p in self.accepted:
            roles[p.role()] = roles.get(p.role(), 0) + 1
        return roles

    def count_groups(self):
        groups = {}
        for p in self.accepted:
            if p.role() == "студент":
                groups[p.extra()] = groups.get(p.extra(), 0) + 1
        return groups

    def sort(self):
        self.accepted.sort()

    def save_ok(self, filename="ok.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for p in self.accepted:
                f.write(f"{p.role()};{p.fio};{p.mail};{p.phone};{p.extra()}\n")

    def save_errors(self, filename="errors.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for item in self.rejected:
                f.write(f"Строка {item['number']}: {item['reason']} | {item['line']}\n")

    def save(self):
        self.save_ok("ok.txt")
        self.save_errors("errors.txt")

    def print_report(self):
        self.sort()

        print("\n" + "=" * 80)
        print(f"{'№':<3} | {'ФИО':<30} | {'Роль':<15} | {'Группа/кафедра':<15} | Телефон")
        print("-" * 80)

        for i, p in enumerate(self.accepted, 1):
            print(f"{i:<3} | {p.fio:<30} | {p.role():<15} | {p.extra():<15} | {p.masked_phone()}")
        print("=" * 80)

        print("\nОТКЛОНЕННЫЕ СТРОКИ:")
        for item in self.rejected:
            print(f"Строка {item['number']}: {item['reason']}")
        print(f"\nПринято: {len(self.accepted)} | Отклонено: {len(self.rejected)}")

        print("\nПо ролям:")
        for r, count in self.count_roles().items():
            print(f"  {r}: {count}")
        print("\nПо группам:")
        for g, count in self.count_groups().items():
            print(f"  {g}: {count}")

    def __len__(self):
        return len(self.accepted)

    def __iter__(self):
        return iter(self.accepted)
