from pymysql import connections
from datetime import date
import boto3

db_conn = connections.Connection(
    host='hr-database.cleurfoto8r2.us-east-1.rds.amazonaws.com',
    port=3306,
    user='main',
    password='lab-password',
)

cursor = db_conn.cursor()
create_database = "CREATE DATABASE HR"
cursor.execute(create_database)
cursor.execute("USE HR")

createTableEmployees = "CREATE TABLE Employees (employeeID VARCHAR(5),firstName VARCHAR(10),lastName VARCHAR(10),email VARCHAR(15),address VARCHAR(30),phoneNumber VARCHAR(15),emergencyPhoneNumber VARCHAR(15),gender VARCHAR(10),dateOfBirth DATE,department VARCHAR(10),imageFile VARCHAR(50),primaryKey (employeeID)))"

cursor.execute(createTableEmployees)
db_conn.commit()
cursor.close()