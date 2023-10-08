from flask import Flask, redirect, url_for, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
app = Flask(__name__)
app.secret_key = 'gttbafytsitstillyhj!*'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ch@rlessql01*'
app.config['MYSQL_DB'] = 'pythonlogin'
mysql = MySQL(app)

@app.route('/')
def base():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST','GET'])
def login():
    msg = ''
    if request.method == "POST" and 'cred' in request.form and 'password' in request.form:
        useroremail = request.form['cred']
        password = request.form['password']

        # hash = password + app.secret_key
        # hash = hashlib.sha1(hash.encode())
        # password = hash.hexdigest()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username =%s AND password = %s', (useroremail, password,))

        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            
            msg = 'Logged in successfully!'
        else:

            cursor.execute('SELECT * FROM accounts WHERE email =%s AND password = %s', (useroremail, password))

            account = cursor.fetchone()

            if account:
                session['loggedin'] = True
                session['username'] = account['username']
            
                msg = 'Logged in successfully!'
            else:
                msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST','GET'])
def signup():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'cpassword' in request.form and 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form:
        if 'password' == 'cpassword':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            firstname = request.form['firstname']
            lastname = request.form['lastname']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            user = cursor.fetchone()
            cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
            em = cursor.fetchone()

            if user or em:
                msg = 'A user with that username or email already exists.'
            else:
                cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', (username, firstname, lastname, password, email,))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
        else:
            msg = 'Passwords do not match.'

    elif request.method == 'POST':
        msg = 'Please complete all the fields and retry.'

    return render_template('signup.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=1, host='0.0.0.0', port=5000)