import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('donations.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            amount INTEGER
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
''')

    conn.commit()
    conn.close()

init_db()
# HOME
@app.route("/")
def home():
    return render_template("index.html")


# ABOUT
@app.route("/about")
def about():
    return render_template("about.html")


# WORK
@app.route("/work")
def work():
    return render_template("work.html")


# PROJECTS
@app.route("/projects")
def projects():
    return render_template("projects.html")


# MEDIA
@app.route("/media")
def media():
    return render_template("media.html")


# GET INVOLVED
@app.route("/getinvolved")
def getinvolved():
    return render_template("getinvolved.html")


# BLOG
@app.route("/blog")
def blog():

    conn = sqlite3.connect("donations.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM blog")
    posts = cursor.fetchall()

    conn.close()

    return render_template("blog.html", posts=posts)


# CONTACT
@app.route("/contact")
def contact():
    return render_template("contact.html")


# DONATE
@app.route("/donate", methods=["GET","POST"])
def donate():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        amount = request.form["amount"]

        conn = sqlite3.connect("donations.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO donations (name,email,amount) VALUES (?,?,?)",
            (name,email,amount)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("admin"))

    return render_template("donate.html")
@app.route("/admin")
def admin():

    conn = sqlite3.connect("donations.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM donations")
    donations = cursor.fetchall()

    conn.close()

    return render_template("admin.html", donations=donations)
@app.route("/addblog", methods=["GET","POST"])
def addblog():

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        conn = sqlite3.connect("donations.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO blog (title,content) VALUES (?,?)",
            (title,content)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("blog"))

    return render_template("addblog.html")

if __name__ == "__main__":
    app.run(debug=True)