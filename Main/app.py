from flask import Flask, render_template, request
from pymysql import connections
from datetime import date
import boto3

app = Flask(__name__)

db_conn = connections.Connection(
    host='hr-database.cleurfoto8r2.us-east-1.rds.amazonaws.com',
    port=3306,
    user='main',
    password='lab-password',
    db = 'HR'
)

custombucket = 'tantzexuan-bucket'
customregion = 'us-east-1'

    # createTableEmployees = "CREATE TABLE Employees (employeeID varchar(5),firstName VARCHAR(10),lastName VARCHAR(10), email VARCHAR(50), address VARCHAR(30), phoneNumber VARCHAR(15), emergencyPhoneNumber VARCHAR(15), gender VARCHAR(10), dateOfBirth DATE, department VARCHAR(10), primary key (employeeID))"
    # cursor.execute(createTableEmployees)

@app.route("/", methods=['GET', 'POST'])
def index():

    cursor = db_conn.cursor()
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)

    delete_record = "DELETE FROM Employees"

    cursor.execute(delete_record)
    print('Delete records')
    db_conn.commit()    

    # alter_department = 'ALTER TABLE Employees MODIFY COLUMN department varchar(30)'

    # cursor.execute(alter_department)
    # print('Altered department Column')

    return render_template('index.html')

@app.route("/payroll")
def payroll():
    return render_template('Payroll.html')

@app.route("/add_employees", methods=['POST'])
def AddEmp():
    employeeID = request.form['employeeID']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    currentAddress = request.form['currentAddress']
    phoneNumber = request.form['phoneNumber']
    emergencyContactNumber = request.form['emergencyContactNumber']
    gender =  request.form['gender']
    dob = request.form['dob']
    department = request.form['department']
    imageFile = request.files['imageFile']

    print('The data capture from the website : ')
    print(employeeID, firstName, lastName, email, currentAddress, phoneNumber, emergencyContactNumber, gender, dob, department)

    insert_sql = "INSERT INTO Employees VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        # write data into RDS
        cursor.execute(insert_sql, (employeeID, firstName, lastName, email, currentAddress, phoneNumber, emergencyContactNumber, gender, dob, department))
        db_conn.commit()

        # read data from RDS
        select_query = "Select * from Employees"
        cursor.execute(select_query)
        records = cursor.fetchall()
        print(records)

        # S3
        emp_name = "" + firstName + " " + lastName
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(employeeID) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=imageFile)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)
            print("Image Stored location : ", object_url)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    # cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
    # db_conn.commit()

    return render_template('Payroll.html')


# cursor.execute("create database HRsystem")
# print(cursor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)