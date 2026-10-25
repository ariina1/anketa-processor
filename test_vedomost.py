import pytest
from vedomost import parse_line, load, zachteno, srednee, procent_zachetov, reyting, luchshiy

def test_zachteno_porog():
    assert zachteno(60) == True 

def test_load_bez_posledney_stroki(tmp_path):
    f = tmp_path / "ved.txt"
    f.write_text("Иванов;80\nПетров;90", encoding="utf-8")
    assert len(load(str(f))) == 2

def test_reyting_po_ubyvaniyu():
    zapisi = [("Иванов", 80), ("Петров", 90)]
    assert reyting(zapisi) == ["Петров", "Иванов"]

def test_luchshiy_ball_obnovlyaetsya():
    zapisi = [("Иванов", 80), ("Петров", 90), ("Сидоров", 70)]
    assert luchshiy(zapisi) == "Петров"

def test_srednee_pustoy_spisok():
    with pytest.raises(ValueError):
        srednee([])
