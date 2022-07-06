import os
import re

from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from cs50 import SQL
from helpers import apology
from werkzeug.security import check_password_hash, generate_password_hash

# configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# SQLite database
db = SQL("sqlite:///registrants.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/index')
def index():
    return redirect("/")

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # require input username, password, confirmation
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # username is blank
        if not username:
            return apology("Voer een gebruikersnaam in", 400)

        # username already exists
        elif len(rows) != 0:
            return apology("Gebruikersnaam is al in gebruik", 400)

        # password is blank
        if not password:
            return apology("Voer een wachtwoord in", 400)

        # confirmation is blank
        if not request.form.get("confirmation"):
            return apology("Bevestig wachtwoord", 400)

        # password to have more than 8 characters
        if len(password) < 8:
            return apology("Wachtwoord moet meer dan 8 karakters hebben")

        # password to have at least 1 number
        if re.search('[0-9]', password) is None:
            return apology("Wachtwoord moet op zijn minst 1 nummer hebben")

        # password to have at least 1 symbol
        if re.search('[A-Z]', password) is None:
            return apology("Wachtwoord moet op zijn minst 1 hoofdletter hebben")

        # passwords do not match
        if password != confirmation:
            return apology("Wachtwoorden komen niet overeen")

        else:
            # generate password to hash password
            hash = generate_password_hash(password)

            # insert new user
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

            return redirect("/login")

        # route via GET
    else:
        return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("voer een gebruikersnaam in", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("voer een wachtwoord in", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("ongeldige gebruikersnaam en/of wachtwoord", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/products')
def products():
    return render_template("products.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

# producten pagina's
@app.route('/products/1')
def product1():
    return render_template("producten/product1.html")

@app.route('/products/2')
def product2():
    return render_template("producten/product2.html")

@app.route('/products/3')
def product3():
    return render_template("producten/product3.html")