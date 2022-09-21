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
def index():
    alter_email = 'ALTER TABLE Employees MODIFY COLUMN email varchar(50)'

    cursor = db_conn.cursor()
    cursor.execute(alter_email)
    print('Altered Email Column')

    return render_template('index.html')

@app.route("/payroll")
def payroll():
    return render_template('Payroll.html')

# cursor = db_conn.cursor()

# createTableEmployees = "CREATE TABLE Employees (firstName VARCHAR(10),lastName VARCHAR(10), email VARCHAR(15), address VARCHAR(30), phoneNumber VARCHAR(15), emergencyPhoneNumber VARCHAR(15), gender VARCHAR(10), dateOfBirth DATE, department VARCHAR(10), primary key (firstName))"
# cursor.execute(createTableEmployees)
# cursor.execute("SHOW TABLES")
# for x in cursor:
#     print(x)

@app.route("/add_employees", methods=['POST'])
def AddEmp():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    currentAddress = request.form['currentAddress']
    phoneNumber = request.form['phoneNumber']
    emergencyContactNumber = request.form['emergencyContactNumber']
    gender =  request.form['gender']
    dob = request.form['dob']
    department = request.form['department']

    print(firstName, lastName, email, currentAddress, phoneNumber, emergencyContactNumber, gender, dob, department)

    insert_sql = "INSERT INTO Employees VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        # write data
        cursor.execute(insert_sql, (firstName, lastName, email, currentAddress, phoneNumber, emergencyContactNumber, gender, dob, department))
        db_conn.commit()

        # read data
        select_query = "Select * from Employees"
        cursor.execute(select_query)
        records = cursor.fetchall()

        print(records)

    finally:
        cursor.close()

    # cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
    # db_conn.commit()

    return render_template('Payroll.html')


# cursor.execute("create database HRsystem")
# print(cursor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)