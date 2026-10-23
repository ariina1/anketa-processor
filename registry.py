from people import Person, Student, Teacher, AnketaError

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
            
            fields = [f.strip() for f in line.split(";")]
            if len(fields) != 5:
                self.reject(i, line, f"полей должно быть 5, найдено {len(fields)}")
                continue

            ank_type, fio, mail, phone, extra = fields

            try:
                if ank_type == 's':
                    person = Student(fio, mail, phone, extra)
                elif ank_type == 't':
                    person = Teacher(fio, mail, phone, extra)
                else:
                    raise AnketaError(f"неизвестный тип: {ank_type}")
                
                self.add(person)
            except AnketaError as e:
                self.reject(i, line, str(e))
        return True

    def save(self):
        with open("ok.txt", "w", encoding="utf-8") as f:
            for p in self.accepted:
                f.write(f"{p.role()};{p.fio};{p.mail};{p.phone};{p.extra()}\n")

        with open("errors.txt", "w", encoding="utf-8") as f:
            for item in self.rejected:
                f.write(f"Строка {item['number']}: {item['reason']} | {item['line']}\n")

    def print_report(self):
        self.accepted.sort()
        
        print("\n" + "=" * 80)
        print(f"{'№':<3} | {'ФИО':<30} | {'Роль':<15} | {'Группа/кафедра':<15} | Телефон")
        print("-" * 80)
        
        for i, p in enumerate(self.accepted, 1):
            # Нет ни одного isinstance!
            print(f"{i:<3} | {p.fio:<30} | {p.role():<15} | {p.extra():<15} | {p.masked_phone()}")    
        print("=" * 80)
        print("\nОТКЛОНЕННЫЕ СТРОКИ:")
        for item in self.rejected:
            print(f"Строка {item['number']}: {item['reason']}")
        print(f"\nПринято: {len(self.accepted)} | Отклонено: {len(self.rejected)}")     
        roles = {}
        groups = {}
        for p in self.accepted:
            roles[p.role()] = roles.get(p.role(), 0) + 1
            if p.role() == "студент":
                groups[p.extra()] = groups.get(p.extra(), 0) + 1

        print("\nПо ролям:")
        for r, count in roles.items():
            print(f"  {r}: {count}")

        print("\nПо группам:")
        for g, count in groups.items():
            print(f"  {g}: {count}")

    def __len__(self):
        return len(self.accepted)
