"""Ведомость: читает результаты работ группы и считает итоги."""

PORAG = 60          

def parse_line(line):
    parts = line.strip().split(";")
    if len(parts) != 2:
        raise ValueError("нужно два поля: " + line.strip())
    return parts[0].strip(), int(parts[1])

def load(filename):
    f = open(filename, "r", encoding="utf-8")
    stroki = f.readlines()
    f.close()

    result = []
    for line in stroki:
        if line.strip() == "":
            continue
        result.append(parse_line(line))
    return result

def zachteno(ball):
    return ball >= PORAG

def srednee(balli):
    if len(balli) == 0:
        raise ValueError("список пустой")
    return sum(balli) / len(balli)

def procent_zachetov(zapisi):
    skolko = 0
    for familiya, ball in zapisi:
        if zachteno(ball):
            skolko += 1
    return round(skolko / len(zapisi) * 100, 1)

def reyting(zapisi):
    po_ballu = sorted(zapisi, key=lambda para: para[1], reverse=True)
    return [familiya for familiya, ball in po_ballu]

def luchshiy(zapisi):
    luchshaya = zapisi[0][0]
    luchshiy_ball = zapisi[0][1]
    for familiya, ball in zapisi:
        if ball > luchshiy_ball:
            luchshaya = familiya
            luchshiy_ball = ball
    return luchshaya
