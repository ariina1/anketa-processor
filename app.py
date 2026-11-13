from flask import Flask, render_template, request, jsonify, redirect, url_for
from people import Student, Teacher, AnketaError
from registry import Registry

app = Flask(__name__)
zhurnal = Registry()

# Загружаем данные один раз при старте
if not zhurnal.load("anketa.txt"):
    print("ВНИМАНИЕ: файл не найден, журнал пуст")

# --- СТРАНИЦЫ ДЛЯ ЧЕЛОВЕКА ---

@app.route("/")
def index():
    return render_template("index.html", anketi=zhurnal.accepted, prinyato=len(zhurnal), otkloneno=len(zhurnal.rejected))

@app.route("/anketi/<int:nomer>")
def anketa_stranica(nomer):
    if nomer < 1 or nomer > len(zhurnal.accepted):
        return render_template("oshibka.html", message="Такой анкеты не существует."), 404
    p = zhurnal.accepted[nomer - 1]
    return render_template("anketa.html", p=p, nomer=nomer)

@app.route("/gruppa/<name>")
def gruppa(name):
    students = [p for p in zhurnal.accepted if p.role() == "студент" and p.extra() == name]
    return render_template("index.html", anketi=students, prinyato=len(students), otkloneno=0)

@app.route("/statistika")
def statistika():
    roles, gruppy = {}, {}
    for p in zhurnal.accepted:
        roles[p.role()] = roles.get(p.role(), 0) + 1
        if p.role() == "студент":
            gruppy[p.extra()] = gruppy.get(p.extra(), 0) + 1
    return render_template("statistika.html", prinyato=len(zhurnal), otkloneno=len(zhurnal.rejected), roles=roles, gruppy=gruppy, brak=zhurnal.rejected)

@app.route("/dobavit", methods=["GET", "POST"])
def dobavit():
    if request.method == "POST":
        tip = request.form.get("tip")
        fio = request.form.get("fio", "")
        mail = request.form.get("mail", "")
        phone = request.form.get("phone", "")
        extra = request.form.get("extra", "")
        
        try:
            if tip == "s": p = Student(fio, mail, phone, extra)
            elif tip == "t": p = Teacher(fio, mail, phone, extra)
            else: raise AnketaError("Неизвестный тип анкеты")
            
            zhurnal.add(p)
            return redirect(url_for("anketa_stranica", nomer=len(zhurnal.accepted)))
        except AnketaError as e:
            return render_template("dobavit.html", error=str(e), data=request.form), 400

    return render_template("dobavit.html", data={})

# --- API ДЛЯ ПРОГРАММ ---

@app.route("/api/anketi", methods=["GET", "POST"])
def api_anketi():
    if request.method == "POST":
        data = request.get_json(silent=True)
        if not data: return jsonify({"oshibka": "ожидался JSON"}), 400
        
        try:
            tip = data.get("tip")
            if tip == "s": p = Student(data.get("fio", ""), data.get("mail", ""), data.get("phone", ""), data.get("gruppa", ""))
            elif tip == "t": p = Teacher(data.get("fio", ""), data.get("mail", ""), data.get("phone", ""), data.get("kafedra", ""))
            else: raise AnketaError("неизвестный тип")
            
            zhurnal.add(p)
            return jsonify({"fio": p.fio, "mail": p.mail, "phone": p.phone, "tip": tip, "extra": p.extra()}), 201
        except AnketaError as e:
            return jsonify({"oshibka": str(e)}), 400

    rol = request.args.get("rol")
    if rol:
        filtered = [p for p in zhurnal.accepted if p.role() == rol]
        return jsonify([{"fio": p.fio, "role": p.role(), "extra": p.extra()} for p in filtered])
    return jsonify([{"fio": p.fio, "role": p.role(), "extra": p.extra()} for p in zhurnal.accepted])

@app.route("/api/anketi/<int:nomer>")
def api_anketa(nomer):
    if nomer < 1 or nomer > len(zhurnal.accepted):
        return jsonify({"oshibka": "анкета не найдена"}), 404
    p = zhurnal.accepted[nomer - 1]
    return jsonify({"nomer": nomer, "fio": p.fio, "mail": p.mail, "phone": p.phone, "role": p.role(), "extra": p.extra()})

@app.route("/api/statistika")
def api_statistika():
    roles, gruppy = {}, {}
    for p in zhurnal.accepted:
        roles[p.role()] = roles.get(p.role(), 0) + 1
        if p.role() == "студент":
            gruppy[p.extra()] = gruppy.get(p.extra(), 0) + 1
    return jsonify({"prinyato": len(zhurnal), "otkloneno": len(zhurnal.rejected), "po_rolyam": roles, "po_gruppam": gruppy})

@app.route("/api/brak")
def api_brak():
    return jsonify(zhurnal.rejected)

@app.errorhandler(404)
def net_stranicy(e):
    if request.path.startswith('/api/'):
        return jsonify({"oshibka": "такого адреса нет"}), 404
    return render_template("oshibka.html", message="Такого адреса не существует."), 404

if __name__ == "__main__":
    app.run(debug=True)