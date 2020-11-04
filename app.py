from functions import *

import functools

from flaskext.mysql import MySQL
from flask import Flask, render_template, redirect, session, jsonify, request

####################
### CONFIG & DECORATOS
####################


Type = "Development" # Production or Development

# Pobieranie config'a z pliku config.py
app = Flask(__name__)
app.config.from_object("config." + Type + "Config")

# Aktywowanie modułu MySQL
mysql = MySQL()
mysql.init_app(app)

### DECORATOR ###

def protected(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "isLogged" not in session:
            return redirect("/login")
        return func(*args, **kwargs)

    return secure_function

@app.route('/get', methods=['GET'])
def getID():
    function = request.args.get('function', default="0", type=str)
    value = request.args.get('value', default="0", type=str)

    if str(function) == "Companies_SelectedID":
        session['Companies_SelectedID'] = value
        return redirect("/company_list")

####################
### INDEX
####################

@app.route('/')
@protected
def index():

    return render_template("index.html")

####################
### Login & Register & Logout
####################

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST" and request.form["action"] == "/login":
        login_mail = request.form.get('login_mail', "", type=str)
        login_password = request.form.get('login_password', "", type=str)

        # Development
        if Type == "Development":
            print("Login: " + login_mail)
            print("Hasło: " + login_password)

        # Logowanie
        if userLogin(login_mail, login_password):

            session['isLogged'] = True
            session['user'] = login_mail
            session['ID'] = getUserID(login_mail)

            return jsonify({"redirect": "/"})
        else:
            return jsonify({"title": "", "message": "Proszę wprowadzić poprawne dane!", "type": "danger"})

    return render_template("login.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST" and request.form["action"] == "/register":

        register_mail = request.form.get('register_mail', "", type=str)
        register_password = request.form.get('register_password', "", type=str)
        register_repeat_password = request.form.get('register_repeat_password', "", type=str)

        # Development
        if Type == "Development":
            print("Login: " + register_mail)
            print("Hasło: " + register_password)
            print("Hasło: " + register_repeat_password)

        # Weryfikacja danych
        if not checkMail(register_mail):
            return jsonify({"title": "", "message": "Prosze wprowadzić poprawny adres E-Mail!"})

        # Sprawdzenie czy hasła są identyczne
        if register_password != register_repeat_password:
            return jsonify({"title": "", "message": "Prosze wprowadzić identyczne hasła!"})

        # Rejestracja
        if userRegister(register_mail, register_password, register_repeat_password):

            session['isLogged'] = True
            session['user'] = register_mail
            session['ID'] = getUserID(register_mail)

            return jsonify({"redirect": "/"})
        else:
            return jsonify({"title": "", "message": "Proszę wprowadzić poprawne dane!"})

    return render_template("register.html")


@app.route('/logout')
@protected
def logout():
    session.pop('isLogged', None)
    return redirect("/")

####################
### Company
####################

@app.route('/company')
@protected
def company():
    return render_template("company.html")


@app.route('/company/add', methods=['POST', 'GET'])
@protected
def company_add():
    if request.method == 'POST':

        company_add_name = request.form['company_add_name']
        company_add_nip = request.form['company_add_nip']
        company_add_regon = request.form['company_add_regon']
        company_add_street = request.form['company_add_street']
        company_add_city = request.form['company_add_city']
        company_add_zip = request.form['company_add_zip']
        company_add_state = request.form['company_add_state']

        if checkCompany(company_add_nip, company_add_regon):
            return jsonify({"title": "", "message": "Podany NIP/Regon jest juz zarejstrowany!"})

        if companyRegister(getUserID(session['user']), company_add_name, company_add_nip, company_add_regon, company_add_street, company_add_city, company_add_zip, company_add_state):
            print("Udalo sie")
            # return jsonify({"redirect": "/"})


    return render_template("company_add.html", States=getStates())


@app.route('/company/list')
@protected
def company_list():
    return render_template("company_list.html")


@app.route('/company/workers')
@protected
def company_workers():
    return render_template("company_workers.html")

####################
### Account
####################

@app.route('/account/')
@protected
def account():
    return render_template("account.html")


@app.route('/account/password')
@protected
def account_password():
    return render_template("account_password.html")

####################
### Messages
####################

@app.route('/messages')
@protected
def messages():
    return render_template("messages.html")

####################
### Others
####################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=70)
