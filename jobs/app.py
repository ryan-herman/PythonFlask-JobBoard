## IMPORTS
from flask import Flask, render_template

## Create Flask App
app = Flask(__name__)

## Index Route Decorators
@app.route('/')
@app.route('/jobs')
## Index Route Function
def jobs():
    return render_template('index.html')


