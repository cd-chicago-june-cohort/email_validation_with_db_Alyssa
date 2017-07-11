from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'email_validation_wdb')

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug=True)