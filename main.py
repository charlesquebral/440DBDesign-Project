from flask import Flask, redirect, url_for, render_template, request, session
from flask_mysqldb import MySQL
from datetime import date
import MySQLdb.cursors
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
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username =%s AND password = %s', (useroremail, password,))

        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['firstname'] = account['firstname']
            session['lastname'] = account['lastname']
            session['email'] = account['email']
            
            #successful login
            return redirect(url_for('index'))
        else:

            cursor.execute('SELECT * FROM accounts WHERE email =%s AND password = %s', (useroremail, password))

            account = cursor.fetchone()

            if account:
                session['loggedin'] = True
                session['username'] = account['username']
                session['firstname'] = account['firstname']
                session['lastname'] = account['lastname']
                session['email'] = account['email']
            
                #successful login
                return redirect(url_for('index'))
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
        if request.form['password'] == request.form['cpassword']:
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
                #successful registration

                cursor.execute('SELECT * FROM accounts WHERE username =%s AND password = %s', (username, password,))

                account = cursor.fetchone()

                if account:
                    session['loggedin'] = True
                    session['username'] = account['username']
                    session['firstname'] = account['firstname']
                    session['lastname'] = account['lastname']
                    session['email'] = account['email']
                
                    #msg = 'Logged in successfully!'
                    return redirect(url_for('index'))
        else:
            msg = 'Passwords do not match.'

    elif request.method == 'POST':
        msg = 'Please complete all the fields and retry.'

    return render_template('signup.html', msg=msg)

@app.route('/index', methods=['POST','GET'])
def index():
    usernamedisplay = ''
    firstnamedisplay=''
    emaildisplay=''
    lastnamedisplay=''

    if session['loggedin']:
        usernamedisplay = session['username']
        firstnamedisplay = session['firstname']
        emaildisplay = session['email']
        lastnamedisplay = session['lastname']

    return render_template('index.html', usernamedisplay = usernamedisplay, firstnamedisplay = firstnamedisplay, emaildisplay = emaildisplay, lastnamedisplay = lastnamedisplay)


@app.route('/createpost', methods=['POST','GET'])
def createpost():
    msg = ''

    if request.method == 'POST' and 'title' in request.form and 'description' in request.form and 'category' in request.form and 'price' in request.form:

        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        user = str(session['username'])
        today = str(date.today())

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        todayposts = cursor.execute('SELECT * FROM posts WHERE username =%s AND date = %s', (user, today,))

        if (todayposts < 3):
            cursor.execute('INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s)', (user, title, description, category, price, today))
            mysql.connection.commit()
            return redirect(url_for('index'))
        else:
            msg = 'Sorry, but you have already posted 3 times today. Please try again later.'

    elif request.method == 'POST':
        msg = 'Please complete all the fields and retry.'

    return render_template('createpost.html', msg=msg)

@app.route('/search', methods=['POST','GET'])
def search():
    msg = ''
    results = []

    sql_query = "SELECT * FROM posts WHERE 1 = 1"

    if request.method == 'POST':
        user = str(session['username'])
        today = str(date.today())
        
        if 'title' in request.form:
            title = request.form['title']
            if title != '':
                sql_query += f" AND title = '{title}'"
        if 'description' in request.form:
            description = request.form['description']
            if description != '':
                sql_query += f" AND description = '{description}'"
        if 'category' in request.form:
            category = request.form['category']
            if category != '':
                sql_query += f" AND category = '{category}'"
        if 'price' in request.form:
            price = request.form['price']
            if price != '':
                sql_query += f" AND price = '{price}'"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        findings = cursor.execute(sql_query)
        results = cursor.fetchall()
        msg = str(findings) + " results found!"

    return render_template('search.html', msg=msg, items=results)

@app.route('/item/<postid>', methods=['POST','GET'], endpoint='item')
def item(postid):
    msg = ''
    user = session['username']
    today = str(date.today())
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        if request.form['feedback'] != '' and request.form['review'] != '':
            cursor.execute("SELECT * FROM reviews WHERE username =%s and date =%s", (user, today,))

    cursor.execute("SELECT * FROM reviews WHERE postid =%s", (postid))
    results = cursor.fetchall()

    return render_template('item.html', msg=msg, items=results, postid=postid)

if __name__ == "__main__":
    app.run(debug=1, host='0.0.0.0', port=5000)