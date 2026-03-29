from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

USERS_FILE = "users.json"

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
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=2)


@app.route('/', methods=['GET', 'POST'])
def login():
    users = load_users()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username in users and users[username]["password"] == password:
            role = users[username].get("role", "student")
            if role == "admin":
                return redirect(url_for("admin_panel", username=username))
            else:
                return redirect(url_for("student_panel", username=username))

        return "Hatalı kullanıcı adı veya şifre!"

    return render_template("login.html")


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/student/<username>')
def student_panel(username):
    users = load_users()
    user = users.get(username)

    if not user:
        return "Kullanıcı bulunamadı!"

    grades = user.get("grades", {})

    def calc_average(grades_dict):
        vals = [v for v in grades_dict.values() if isinstance(v, (int, float))]
        return round(sum(vals)/len(vals), 2) if vals else 0

    average_1 = calc_average(grades.get("1_donem", {}))
    average_2 = calc_average(grades.get("2_donem", {}))
    year_average = round((average_1 + average_2) / 2, 2) if (average_1 or average_2) else 0

    return render_template(
        "student.html",
        username=username,
        grades=grades,
        average=average_1,
        average2=average_2,
        year_average=year_average
    )


@app.route('/admin/<username>', methods=['GET', 'POST'])
def admin_panel(username):
    users = load_users()

    if username not in users or users[username].get("role") != "admin":
        return "Yetkisiz erişim!"

    if request.method == "POST":
        form_type = request.form.get("form_type")

        for u, info in users.items():
            if info.get("role") != "student":
                continue

            # 1. DÖNEM
            if form_type == "1":
                for key in info["grades"]["1_donem"]:
                    val = request.form.get(f"grades_1_{u}_{key}")
                    if val is not None and val.strip().isdigit():
                        info["grades"]["1_donem"][key] = int(val.strip())

            # 2. DÖNEM
            elif form_type == "2":
                for key in info["grades"]["2_donem"]:
                    val = request.form.get(f"grades_2_{u}_{key}")
                    if val is not None and val.strip().isdigit():
                        info["grades"]["2_donem"][key] = int(val.strip())

        save_users(users)
        return redirect(url_for("admin_panel", username=username))

    return render_template("admin.html", users=users, username=username)


if __name__ == "__main__":
    app.run(debug=True)