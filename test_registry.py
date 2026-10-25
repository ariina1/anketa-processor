import pytest

from people import Student
from registry import Registry

STROKI = [
    "s;иванов иван петрович;IVANOV@mail.ru;+7 (912) 345-67-89;09с41",
    "s;Петрова;petrova@mail.ru;89123456780;09с41",
    "t;сидоров пётр ильич;sidorov@mail.ru;8 912 345 67 81;Информатика",
    "x;Некто Некто;nekto@mail.ru;89123456782;1",
    "s;яковлев яков;yak@mail.ru;89123456783;09с42",
    "s;Смирнов Олег;smirnov@mail.ru;123;09с41",
]


@pytest.fixture
def zhurnal(tmp_path):
    put = tmp_path / "anketa.txt"
    put.write_text("\n".join(STROKI) + "\n", encoding="utf-8")
    reg = Registry()
    reg.load(str(put))
    return reg


def test_pustoy_zhurnal_imeet_dlinu_nol():
    assert len(Registry()) == 0


def test_posle_zagruzki_tri_anketi(zhurnal):
    assert len(zhurnal) == 3


def test_v_brake_tri_zapisi(zhurnal):
    assert len(zhurnal.rejected) == 3


def test_nomera_strok_braka(zhurnal):
    nomera = [item["number"] for item in zhurnal.rejected]
    assert nomera == [2, 4, 6]


def test_nesushchestvuyushchiy_fayl(tmp_path):
    reg = Registry()
    assert reg.load(str(tmp_path / "net_takogo.txt")) is False


def test_schetchik_rolej(zhurnal):
    assert zhurnal.count_roles() == {"студент": 2, "преподаватель": 1}


def test_schetchik_grupp_tolko_studenty(zhurnal):
    assert zhurnal.count_groups() == {"09с41": 1, "09с42": 1}


def test_zhurnal_perebiraetsya_tsiklom_for(zhurnal):
    familii = []
    for p in zhurnal:
        familii.append(p.fio.split()[0])
    assert familii == ["Иванов", "Сидоров", "Яковлев"]


def test_sortirovka_po_alfavitu(zhurnal):
    zhurnal.sort()
    assert [str(p) for p in zhurnal] == [
        "Иванов Иван Петрович",
        "Сидоров Пётр Ильич",
        "Яковлев Яков",
    ]


def test_save_ok_po_stroke_na_cheloveka(zhurnal, tmp_path):
    put = tmp_path / "ok.txt"
    zhurnal.save_ok(str(put))
    stroki = put.read_text(encoding="utf-8").splitlines()
    assert len(stroki) == 3
    assert stroki[0] == "студент;Иванов Иван Петрович;ivanov@mail.ru;79123456789;09с41"


def test_save_errors_pishet_prichinu(zhurnal, tmp_path):
    put = tmp_path / "errors.txt"
    zhurnal.save_errors(str(put))
    stroki = put.read_text(encoding="utf-8").splitlines()
    assert len(stroki) == 3
    assert stroki[0].startswith("Строка 2:")
    assert "меньше двух слов" in stroki[0]


def test_sortirovka_s_bukvoy_yo():
    reg = Registry()
    reg.add(Student("Яковлев Яков", "a@mail.ru", "89123456781", "09с41"))
    reg.add(Student("Ёлкин Егор", "b@mail.ru", "89123456782", "09с41"))
    reg.add(Student("Абрамов Артём", "c@mail.ru", "89123456783", "09с41"))
    reg.sort()
    assert [p.fio.split()[0] for p in reg] == ["Абрамов", "Ёлкин", "Яковлев"]
