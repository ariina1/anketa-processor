def summa(a, b):
    return a + b

def skidka(cena, procent):
    if procent < 0 or procent > 90:
        raise ValueError("процент скидки должен быть от 0 до 90")
    return round(cena * (100 - procent) / 100, 2)

def srednee(chisla):
    if len(chisla) == 0:
        raise ValueError("список пустой")
    return sum(chisla) / len(chisla)
