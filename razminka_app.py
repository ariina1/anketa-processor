from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
SPISOK = ["Иванов", "Петров", "Сидоров"]

@app.route("/")
def f1():
    return "Привет! Это приложение из 5 строк (Задача F1)."

@app.route("/privet/<imya>")
def f2_privet(imya):
    return f"Здравствуйте, {imya}!"

@app.route("/kvadrat/<int:chislo>")
def f2_kvadrat(chislo):
    return f"Число: {chislo}, Квадрат: {chislo**2}"

@app.route("/spisok")
def f3_spisok():
    return jsonify(SPISOK)

@app.route("/spisok/dlina")
def f3_dlina():
    return jsonify({"dlina": len(SPISOK)})

@app.route("/spisok/<int:nomer>")
def f4_spisok(nomer):
    if nomer < 1 or nomer > len(SPISOK):
        return jsonify({"oshibka": "нет такого номера"}), 404
    return jsonify({"nomer": nomer, "fio": SPISOK[nomer - 1]})

@app.route("/dobavit", methods=["POST"])
def f5_dobavit():
    data = request.get_json(silent=True)
    if not data or "fio" not in data:
        return jsonify({"oshibka": "нет поля fio"}), 400
    SPISOK.append(data["fio"])
    return jsonify({"status": "добавлено", "fio": data["fio"]}), 201

@app.route("/stranica")
def f6_stranica():
    # Передаем список в шаблон
    return render_template("spisok.html", spisok=SPISOK)

if __name__ == "__main__":
    app.run(debug=True, port=5001) # Запускаем на другом порту, чтобы не мешал основному app.py