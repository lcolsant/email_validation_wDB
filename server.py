from flask import Flask, request, redirect, render_template, flash, session
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
mysql = MySQLConnector(app,'email_validation')
app.secret_key = 'secretKey'

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/email', methods=['POST'])
def create():

    if '_flashes' in session:
        session.pop('_flashes', None)
    
    errors = 0

    if len(request.form['email']) < 1:
        flash('Email cannot be empty!','error')
        errors+=1
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid Email Address!')
        errors+=1
    else:
        email = request.form['email']    
        print email
    
    if errors == 0:
        session['email'] = request.form['email']
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW() )"
        # We'll then create a dictionary of data from the POST data received.
        data = {
                'email': request.form['email'],
            }
        # Run query, with dictionary values injected into the query.
        mysql.query_db(query, data)

        #now run query to retrieve all emails
        query = "SELECT * FROM emails"
        emails = mysql.query_db(query)
        print emails
        return render_template('success.html', all_emails=emails)


    return redirect('/')

@app.route('/return', methods=['POST'])
def return_():
    return redirect('/')


app.run(debug=True)