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

cursor = db_conn.cursor()

# createTableEmployees = "CREATE TABLE Employees (firstName VARCHAR(10),lastName VARCHAR(10), email VARCHAR(15), address VARCHAR(30), phoneNumber VARCHAR(15), emergencyPhoneNumber VARCHAR(15), gender VARCHAR(10), dateOfBirth DATE, department VARCHAR(10), primary key (firstName))"
# cursor.execute(createTableEmployees)
print(createTableEmployees) # retrieving the list of table 

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# cursor.execute("create database HRsystem")
# print(cursor)
