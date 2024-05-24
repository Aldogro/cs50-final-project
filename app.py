from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, usd
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Custom filter | formatter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
@login_required
def index():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    db.close()
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    db = get_db()

    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            flash("Email and Password are required", "danger text-white")

        user_db = db.execute("SELECT * FROM people WHERE email = ?", [email]).fetchone()
        db.close()

        if not user_db or not check_password_hash(user_db["password"], password):
            flash("User not found or wrong password", "danger text-white")
            return render_template("/login.html")
        
        session["user_id"] = user_db["id"]
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        document_number = request.form.get("document_number")
        phone = request.form.get("phone")
        user_address = request.form.get("user_address")
        birth_date = request.form.get("birth_date")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        db = get_db()
        existent_user = db.execute("SELECT * FROM people WHERE email = ?", [email]).fetchone()

        if existent_user:
            flash(f"User with email {email} already exists", "danger text-white")
        elif password != confirm:
            flash("Password and Confirm should match", "danger text-white")
        
        hashed_password = generate_password_hash(password)
        try:
            db.execute(
                "INSERT INTO people (first_name, last_name, document_number, phone, user_address, birth_date, email, password) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    first_name,
                    last_name,
                    document_number,
                    phone,
                    user_address,
                    birth_date,
                    email,
                    hashed_password
                ]
            )
            db.commit()
            db.close()
        except sqlite3.Error as error:
            print("Error al interactuar con la base de datos", error)

        return redirect("/login")