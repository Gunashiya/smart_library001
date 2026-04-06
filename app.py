from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("dashboard.html", books=books)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    author = request.form["author"]
    db = get_db()
    db.execute("INSERT INTO books (title, author, available) VALUES (?, ?, 1)", (title, author))
    db.commit()
    return redirect("/")

@app.route("/issue/<int:id>")
def issue(id):
    db = get_db()
    db.execute("UPDATE books SET available=0 WHERE id=?", (id,))
    db.commit()
    return redirect("/")

@app.route("/return/<int:id>")
def return_book(id):
    db = get_db()
    db.execute("UPDATE books SET available=1 WHERE id=?", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    db = sqlite3.connect("database.db")
    db.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, available INTEGER)")
    db.commit()
    app.run(debug=True)
