from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

db_conn = connections.Connection(
    host='hr-database.cleurfoto8r2.us-east-1.rds.amazonaws.com',
    port=3306,
    user='HR-Database',
    password='hr-password',
)

cursor = db_conn.cursor
cursor.execute("create database HRsystem")
print(cursor)