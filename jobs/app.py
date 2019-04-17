## IMPORTS
from flask import Flask, render_template, g, request, redirect, url_for
import sqlite3
import datetime

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

## Job Route Decorators
@app.route('/job/<job_id>')
## Job Route Function
def job(job_id):
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
    return render_template('job.html', job=job)

## Employer Route Decorators
@app.route('/employer/<employer_id>')
## Employer Route Function
def employer(employer_id):
    employer = execute_sql('SELECT * FROM employer WHERE id=?', [employer_id], single=True)
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?', [employer_id])
    reviews = execute_sql('SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?', [employer_id])
    return render_template('employer.html', employer=employer, jobs=jobs, reviews=reviews)

## Review Route Decorators
@app.route('/employer/<employer_id>/review', methods=('GET', 'POST'))
## Review Route Function
def review(employer_id):
    if request.method == 'POST':
        review = request.form['review']
        rating = request.form['rating']
        title = request.form['title']
        status = request.form['status']
        date = datetime.datetime.now().strftime("%m/%d/%Y")
        execute_sql('INSERT INTO review (review, rating, title, date, status, employer_id) VALUES (?, ?, ?, ?, ?, ?)', (review, rating, title, date, status, employer_id), commit=True)
        return redirect(url_for('employer', employer_id=employer_id))
    return render_template('review.html', employer_id=employer_id)