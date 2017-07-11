from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "ShhhDontTell"
mysql = MySQLConnector(app, 'email_validation_wdb')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods = ['POST'])
def validation():
    email_address = request.form['email_address']
    data = {'email_address': email_address}
    # Check to see if email is already in database
    query = 'select id from email_addresses where email_address = :email_address'
    db_check = mysql.query_db(query, data)
    errors=True
    # Validations and error messages
    if len(db_check)>0:
        flash("Email already in the database!")
    elif len(email_address) < 1:
        flash("Email cannot be blank!")
    elif not EMAIL_REGEX.match(email_address):
        flash("Invalid Email Address!")
    else:
        errors=False
    # if not in database AND no errors, update database and go to success page
    if errors:
        return redirect('/')
    else:
        update = 'insert into email_addresses (email_address, created_at) values(:email_address, NOW())'
        mysql.query_db(update, data)
        flash("The email address you entered is a VALID email address! Thank you!")
        return redirect ('/success')

@app.route('/success')
def successful_validation():
    query = 'select email_address, created_at from email_addresses'
    emails = mysql.query_db(query)
    return render_template('success.html', emails = emails)

app.run(debug=True)