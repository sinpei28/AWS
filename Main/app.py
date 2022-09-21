from flask import Flask, render_template, request
from pymysql import connections
from datetime import date

app = Flask(__name__)

db_conn = connections.Connection(
    host='hr-database.cleurfoto8r2.us-east-1.rds.amazonaws.com',
    port=3306,
    user='main',
    password='lab-password',
    db = 'HR'
)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# cursor = db_conn.cursor()
# cursor.execute("create database HRsystem")
# print(cursor)