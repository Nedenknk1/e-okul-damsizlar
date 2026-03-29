from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# -----------------------
# DB
# -----------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT,
        seviye INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        term INTEGER,
        yazili1 INTEGER,
        yazili2 INTEGER,
        perf1 INTEGER,
        perf2 INTEGER,
        proje INTEGER,
        ort REAL,
        yilsonu REAL,
        UNIQUE(student_id, term)
    )
    """)

    cur.execute("SELECT * FROM users")
    if not cur.fetchall():
        users = [
            ("Talha", "0627", "teacher", None),
            ("Berke", "0895", "student", 1),
            ("Emre", "1234", "student", 2),
            ("Yiğit", "0205", "student", 2),
            ("Mert", "0389", "student", 2)
        ]
        cur.executemany(
            "INSERT INTO users (username,password,role,seviye) VALUES (?,?,?,?)",
            users
        )

    conn.commit()
    conn.close()


# -----------------------
# LOGIN
# -----------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]

            if user[3] == "teacher":
                return redirect("/teacher")
            else:
                return redirect("/student")

    return render_template("login.html", error="Kullanıcı adı veya şifre yanlış")


# -----------------------
# TEACHER
# -----------------------
@app.route("/teacher")
def teacher():
    if session.get("role") != "teacher":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT users.id, users.username, users.seviye,
           grades.yazili1, grades.yazili2,
           grades.perf1, grades.perf2,
           grades.proje, grades.ort, grades.yilsonu
    FROM users
    LEFT JOIN grades ON users.id = grades.student_id AND grades.term=1
    WHERE users.role='student'
    """)
    term1 = cur.fetchall()

    cur.execute("""
    SELECT users.id, users.username, users.seviye,
           grades.yazili1, grades.yazili2,
           grades.perf1, grades.perf2,
           grades.proje, grades.ort, grades.yilsonu
    FROM users
    LEFT JOIN grades ON users.id = grades.student_id AND grades.term=2
    WHERE users.role='student'
    """)
    term2 = cur.fetchall()

    conn.close()

    return render_template("teacher.html", term1=term1, term2=term2)


# -----------------------
# GRADE UPSERT
# -----------------------
@app.route("/add_grade", methods=["POST"])
def add_grade():
    if session.get("role") != "teacher":
        return redirect("/")

    student_id = int(request.form["student_id"])
    term = int(request.form["term"])

    def to_int(x):
        return int(x) if x else None

    yazili1 = to_int(request.form.get("yazili1"))
    yazili2 = to_int(request.form.get("yazili2"))
    perf1 = to_int(request.form.get("perf1"))
    perf2 = to_int(request.form.get("perf2"))
    proje = to_int(request.form.get("proje"))

    notlar = [x for x in [yazili1, yazili2, perf1, perf2] if x is not None]
    if term == 2 and proje is not None:
        notlar.append(proje)

    ort = round(sum(notlar)/len(notlar), 2) if notlar else None

    yilsonu = None
    if term == 2:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT ort FROM grades WHERE student_id=? AND term=1",
            (student_id,)
        )
        d1 = cur.fetchone()
        conn.close()

        if d1 and d1[0] and ort:
            yilsonu = round((d1[0] + ort) / 2, 2)

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO grades (
        student_id, term,
        yazili1, yazili2, perf1, perf2,
        proje, ort, yilsonu
    )
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT(student_id, term) DO UPDATE SET
        yazili1=excluded.yazili1,
        yazili2=excluded.yazili2,
        perf1=excluded.perf1,
        perf2=excluded.perf2,
        proje=excluded.proje,
        ort=excluded.ort,
        yilsonu=excluded.yilsonu
    """, (student_id, term, yazili1, yazili2, perf1, perf2, proje, ort, yilsonu))

    conn.commit()
    conn.close()

    return redirect("/teacher")


# -----------------------
# STUDENT
# -----------------------
@app.route("/student")
def student():
    if session.get("role") != "student":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM grades WHERE student_id=?",
        (session["user_id"],)
    )
    data = cur.fetchall()
    conn.close()

    return render_template(
        "student.html",
        data=data,
        username=session["username"]
    )


# -----------------------
# LOGOUT
# -----------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -----------------------
# RUN
# -----------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)