import pytest
from people import Person, Student, AnketaError
from registry import Registry

def test_dvoynaya_familiya():
    # Проверка ошибки 1
    assert Person.check_fio("петров-водкин кузьма") == "Петров-Водкин Кузьма"

def test_probel_vnutri_adresa():
    # Проверка ошибки 2
    with pytest.raises(AnketaError):
        Person.check_mail("iv anov@mail.ru")

def test_sortirovka_s_bukvoy_yo():
    # Проверка ошибки 3
    reg = Registry()
    reg.add(Student("Яковлев Яков", "a@mail.ru", "89123456781", "09с41"))
    reg.add(Student("Ёлкин Егор", "b@mail.ru", "89123456782", "09с41"))
    reg.add(Student("Абрамов Артём", "c@mail.ru", "89123456783", "09с41"))
    reg.sort()
    assert [p.fio.split()[0] for p in reg] == ["Абрамов", "Ёлкин", "Яковлев"]
