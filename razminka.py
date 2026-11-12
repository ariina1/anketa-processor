import requests

BASE = "http://127.0.0.1:5000"

print("    ЗАДАЧА Н1    ")
r = requests.get(BASE + "/")
print("Код ответа:", r.status_code)
print("Тип r.text:", type(r.text))
print("Тип r.json():", type(r.json()))
print("Название сервиса:", r.json()["servis"])

print("\n    ЗАДАЧА Н2    ")
r = requests.get(BASE + "/anketi")
data = r.json()
print("Сколько анкет пришло:", len(data))
print("ФИО первой:", data[0]["fio"])

print("\n    ЗАДАЧА Н3    ")
r = requests.get(BASE + "/anketi/99")
print("Код ответа:", r.status_code)
print("Значение r.ok:", r.ok)
print("Текст ошибки от сервера:", r.json()["oshibka"])

print("\n    ЗАДАЧА Н4    ")
r = requests.get(BASE + "/anketi", params={"tip": "t"})
print("Адрес запроса:", r.url)
for prepod in r.json():
    print(f"ФИО: {prepod['fio']} | Кафедра: {prepod['kafedra']}")

print("\n    ЗАДАЧА Н5    ")
for mail in ["ivanov@mail.ru", "kuznetsov.mail.ru"]:
    r = requests.post(BASE + "/proverka", json={"mail": mail})
    prinyato = r.json().get("prinyato")
    print(f"Почта: {mail} | Код ответа: {r.status_code} | Принято: {prinyato}")