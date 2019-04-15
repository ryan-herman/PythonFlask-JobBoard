## IMPORTS
from flask import Flask, render_template, g
import sqlite3

## CONSTANTS
PATH = 'db/jobs.sqlite' 

## Create Flask App
app = Flask(__name__)

## Global Database Attribute
def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = sqlite3.connect(PATH)
        g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection

## Database Query
def execute_sql(sql, values = (), commit = False, single = False):
    connection = open_connection()
    cursor = connection.execute(sql, values)

    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()
    cursor.close()
    return results

## Close Connection Decorator
@app.teardown_appcontext
## Close Database Connection
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection != None:
        connection.close()

## Index Route Decorators
@app.route('/')
@app.route('/jobs')
## Index Route Function
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)


