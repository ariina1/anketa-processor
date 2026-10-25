import pytest
from people import Person, Student, Teacher, AnketaError, parse_line

@pytest.mark.parametrize("vhod, ozhidaemoe", [
    ("иванов иван иванович", "Иванов Иван Иванович"),
    ("ПЕТРОВА АННА", "Петрова Анна"),
    ("  сидоров   пётр  ", "Сидоров Пётр"),
    ("кОзЛоВ оЛеГ сЕрГеЕвИч", "Козлов Олег Сергеевич"),
])
def test_fio_privoditsya_k_odnomu_vidu(vhod, ozhidaemoe):
    assert Person.check_fio(vhod) == ozhidaemoe

def test_fio_iz_odnogo_slova_otklonyaetsya():
    with pytest.raises(AnketaError):
        Person.check_fio("Иванов")

@pytest.mark.parametrize("vhod, ozhidaemoe", [
    ("IVANOV@Mail.RU", "ivanov@mail.ru"),
    ("  Anna.Petrova@Gmail.com ", "anna.petrova@gmail.com"),
])
def test_pochta_v_nizhniy_registr(vhod, ozhidaemoe):
    assert Person.check_mail(vhod) == ozhidaemoe

@pytest.mark.parametrize("plohaya", [
    "ivanov.mail.ru", "ivanov@@mail.ru", "@mail.ru", "ivanov@mailru", "ivanov@.ru", "ivanov@mail.",
])
def test_plohaya_pochta_otklonyaetsya(plohaya):
    with pytest.raises(AnketaError):
        Person.check_mail(plohaya)

@pytest.mark.parametrize("zapis", [
    "+7 (912) 345-67-89", "8 912 345 67 89", "89123456789", "7-912-345-67-89",
])
def test_telefon_privoditsya_k_odnomu_vidu(zapis):
    assert Person.check_phone(zapis) == "79123456789"

@pytest.mark.parametrize("plohoy", [
    "123", "8912345678", "+1 912 345 67 89", "",
])
def test_plohoy_telefon_otklonyaetsya(plohoy):
    with pytest.raises(AnketaError):
        Person.check_phone(plohoy)

def test_telefon_s_maskoy():
    p = Person("Иванов Иван", "a@mail.ru", "89123456789")
    assert p.masked_phone() == "+7 (912) ***-***-89"

def test_fio_do_initsialov():
    p = Person("иванов иван петрович", "a@mail.ru", "89123456789")
    assert p.short_fio() == "Иванов И. П."

def test_student_i_prepodavatel_otvechayut_po_raznomu():
    s = Student("Иванов Иван", "a@mail.ru", "89123456789", "09с41")
    t = Teacher("Сидоров Пётр", "b@mail.ru", "89123456780", "Информатика")
    assert s.role() == "студент"
    assert t.role() == "преподаватель"
    assert s.extra() == "09с41"
    assert t.extra() == "Информатика"

def test_student_bez_gruppy_otklonyaetsya():
    with pytest.raises(AnketaError):
        Student("Иванов Иван", "a@mail.ru", "89123456789", "   ")

def test_razbor_stroki_studenta():
    p = parse_line("s;иванов иван;IVANOV@mail.ru;8 912 345 67 89;09с41")
    assert isinstance(p, Student)
    assert p.fio == "Иванов Иван"
    assert p.group == "09с41"

def test_razbor_stroki_prepodavatelya():
    p = parse_line("t;сидоров пётр;sidorov@mail.ru;89123456780;Информатика")
    assert isinstance(p, Teacher)
    assert p.department == "Информатика"

@pytest.mark.parametrize("plohaya_stroka", [
    "x;Иванов Иван;a@mail.ru;89123456789;09с41", "s;Иванов Иван;a@mail.ru", "",
])
def test_plohaya_stroka_otklonyaetsya(plohaya_stroka):
    with pytest.raises(AnketaError):
        parse_line(plohaya_stroka)
