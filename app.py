from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")


def init_users():
    if not os.path.exists(USERS_FILE):
        users = {
            "Talha": {"password":"0627","role":"admin","grades":{}},
            "Yiğit": {"password":"0205","role":"student","level":"2. Seviye",
                      "grades":{"1_donem":{"yazili1":None,"yazili2":None,"perf1":None,"perf2":None},
                                "2_donem":{"yazili1":None,"yazili2":None,"perf1":None,"perf2":None,"proje":None}}},
            "Berke": {"password":"0895","role":"student","level":"1. Seviye",
                      "grades":{"1_donem":{"yazili1":None,"yazili2":None,"perf1":None,"perf2":None},
                                "2_donem":{"yazili1":None,"yazili2":None,"perf1":None,"perf2":None,"proje":None}}},
            "Emre": {"password":"1234","role":"student","level":"2. Seviye",
                      "grades":{"1_donem":{"yazili1":None,"yazili2":None,"perf1":None,"perf2":None},
                                "2_donem":{"yazili1":None,"yazili2":None,"perf1":None,"perf2":None,"proje":None}}},
            "Mert": {"password":"0389","role":"student","level":"2. Seviye",
                      "grades":{"1_donem":{"yazili1":None,"yazili2":None,"perf1":None,"perf2":None},
                                "2_donem":{"yazili1":None,"yazili2":None,"perf1":None,"perf2":None,"proje":None}}}
        }
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)


def load_users():
    init_users()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def avg(d):
    vals = [v for v in d.values() if isinstance(v, (int, float))]
    return round(sum(vals) / len(vals), 2) if vals else 0


@app.route('/', methods=['GET','POST'])
def login():
    users = load_users()

    if request.method == "POST":
        u = request.form.get("username","").strip()
        p = request.form.get("password","").strip()

        if u in users and users[u]["password"] == p:
            if users[u]["role"] == "admin":
                return redirect(url_for("admin_panel", username=u))
            return redirect(url_for("student_panel", username=u))

        return "Hatalı giriş!"

    return render_template("login.html")


@app.route('/logout')
def logout():
    return redirect(url_for("login"))


@app.route('/student/<username>')
def student_panel(username):
    users = load_users()
    user = users.get(username)

    grades = user["grades"]

    a1 = avg(grades["1_donem"])
    a2 = avg(grades["2_donem"])

    return render_template(
        "student.html",
        username=username,
        grades=grades,
        average=a1,
        average2=a2,
        year_average=round((a1 + a2) / 2, 2)
    )


@app.route('/admin/<username>', methods=['GET','POST'])
def admin_panel(username):
    users = load_users()

    if username not in users or users[username]["role"] != "admin":
        return "Yetkisiz!"

    if request.method == "POST":
        form_type = request.form.get("form_type")

        for u, info in users.items():
            if info["role"] != "student":
                continue

            if form_type == "1":
                for k in info["grades"]["1_donem"]:
                    v = request.form.get(f"grades_1_{u}_{k}")
                    if v is not None:
    v = v.strip()
    if v == "":
        info["grades"]["1_donem"][k] = None
    else:
        info["grades"]["1_donem"][k] = float(v)

            elif form_type == "2":
                for k in info["grades"]["2_donem"]:
                    v = request.form.get(f"grades_2_{u}_{k}")
                    if v is not None:
    v = v.strip()
    if v == "":
        info["grades"]["2_donem"][k] = None
    else:
        info["grades"]["2_donem"][k] = float(v)

        save_users(users)
        return redirect(url_for("admin_panel", username=username))

    return render_template("admin.html", users=users, username=username)


if __name__ == "__main__":
    app.run()