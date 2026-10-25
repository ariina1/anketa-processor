import pytest
from wordcount import chastota

@pytest.fixture
def fayl_s_tekstom(tmp_path):
    put = tmp_path / "text.txt"
    put.write_text("Мама мыла раму. Рама, мама, рама!", encoding="utf-8")
    return put

def test_mama_i_rama(fayl_s_tekstom):
    result = chastota(fayl_s_tekstom)
    assert result["мама"] == 2
    assert result["рама"] == 2

def test_net_znakov_prepinaniya(fayl_s_tekstom):
    result = chastota(fayl_s_tekstom)
    assert "рама," not in result
    assert "раму." not in result

def test_chetyre_raznyh_slova(fayl_s_tekstom):
    result = chastota(fayl_s_tekstom)
    assert len(result) == 4
