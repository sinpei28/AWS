from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
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

def searchEmployeeRecordsFromRDS (employeeID) :
    cursor = db_conn.cursor()

    seacrhQuery = "SELECT * FROM Employees WHERE employeeID = %s"
    cursor.execute(seacrhQuery, employeeID)

    searchRecords = cursor.fetchall()
    print(searchRecords)

    return searchRecords
    

@app.route("/", methods=['GET', 'POST'])
def index():

    cursor = db_conn.cursor()
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)

    # read data from RDS
        select_query = "Select * from Employees"
        cursor.execute(select_query)
        records = cursor.fetchall()
        print(records)

    return render_template('index.html')

# @app.route("/payroll")
# def payroll():
#     return render_template('Payroll.html')

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

    cursor = db_conn.cursor()

    if imageFile.filename == "":
        return "Please select a file"

    try:
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
            print(object_url)

        except Exception as e:
            return str(e)
        
        # write data into RDS
        insert_sql = "INSERT INTO Employees VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(insert_sql, (employeeID, firstName, lastName, email, currentAddress, phoneNumber, emergencyContactNumber, gender, dob, department, object_url))
        db_conn.commit()

    finally:
        cursor.close()
    
    # add succesfully pages 
    # return render_template('searchEmp.html')
    return redirect(url_for('addSuccess'))

@app.route("/addSuccess", methods=['POST'])
def addSuccess():
    cursor = db_conn.cursor()

    select_query = "Select * from Employees"
    cursor.execute(select_query)
    records = cursor.fetchall()
    print(records)

    result = records[-1]

    return render_template('empSuccess.html', result=result)

@app.route("/searchEmployee")
def searchEmp():
    return render_template('searchEmp.html')


# seacrhSpecificEmployeeID
@app.route("/searchEmployee", methods=['POST'])
def searchEmployee():
    employeeID = request.form['employeeID']
    print(employeeID)

    records = searchEmployeeRecordsFromRDS(employeeID)
    result = records[0]

    return render_template('empSuccess.html', result=result)


@app.route("/deleteEmployee", methods=['POST'])
def deleteEmp():
    cursor = db_conn.cursor()
    employeeID = request.form['employeeID']

    delete_statement = "DELETE FROM Employees WHERE employeeID = %s"

    cursor.execute(delete_statement, (employeeID))

    db_conn.commit()
    cursor.close()

    return 'Deleting Employee'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)