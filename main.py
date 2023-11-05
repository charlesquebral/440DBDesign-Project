from flask import Flask, redirect, url_for, render_template, request, session
from flask_mysqldb import MySQL
from datetime import date
import random
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
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("CREATE TABLE IF NOT EXISTS `accounts` (`username` varchar(50) NOT NULL,`firstname` varchar(50) NOT NULL,`lastname` varchar(50) NOT NULL,`password` varchar(255) NOT NULL,`email` varchar(100) NOT NULL,PRIMARY KEY (`username`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    mysql.connection.commit()
    msg = ''
    if request.method == "POST" and 'cred' in request.form and 'password' in request.form:
        useroremail = request.form['cred']
        password = request.form['password']
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
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("CREATE TABLE IF NOT EXISTS `accounts` (`username` varchar(50) NOT NULL,`firstname` varchar(50) NOT NULL,`lastname` varchar(50) NOT NULL,`password` varchar(255) NOT NULL,`email` varchar(100) NOT NULL,PRIMARY KEY (`username`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    mysql.connection.commit()
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'cpassword' in request.form and 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form:
        if request.form['password'] == request.form['cpassword']:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            firstname = request.form['firstname']
            lastname = request.form['lastname']

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
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("CREATE TABLE IF NOT EXISTS `posts` (`postid` INT AUTO_INCREMENT,`username` varchar(50) NOT NULL,`title` varchar(50) NOT NULL,`description` varchar(50) NOT NULL,`category` varchar(255) NOT NULL,`price` varchar(100) NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`postid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    mysql.connection.commit()
    msg = ''

    if request.method == 'POST' and 'title' in request.form and 'description' in request.form and 'category' in request.form and 'price' in request.form:

        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        user = str(session['username'])
        today = str(date.today())

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
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("CREATE TABLE IF NOT EXISTS `posts` (`postid` INT AUTO_INCREMENT,`username` varchar(50) NOT NULL,`title` varchar(50) NOT NULL,`description` varchar(50) NOT NULL,`category` varchar(255) NOT NULL,`price` varchar(100) NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`postid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    mysql.connection.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS `reviews` (`reviewid` INT AUTO_INCREMENT,`postid` INT,`username` varchar(50) NOT NULL,`feedback` varchar(50) NOT NULL,`review` varchar(255) NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`reviewid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    mysql.connection.commit()

    sql_query = "SELECT * FROM posts WHERE 1 = 1"

    if request.method == 'POST':
        user = str(session['username'])
        today = str(date.today())
        
        if 'title' in request.form:
            title = request.form['title']
            if title != '':
                sql_query += f" AND title LIKE '%{title}%'"
        if 'description' in request.form:
            description = request.form['description']
            if description != '':
                sql_query += f" AND description LIKE '%{description}%'"
        if 'category' in request.form:
            category = request.form['category']
            if category != '':
                categories = category.split(",")
                for cat in categories:
                    newcat = cat.replace(" ", "")
                    sql_query += f" AND category LIKE '%{newcat}%'"
        if 'price' in request.form:
            price = request.form['price']
            if price != '':
                sql_query += f" AND price <= {int(price)}"
        findings = cursor.execute(sql_query)
        results = cursor.fetchall()
        print(sql_query)
        msg = str(findings) + " results found!"

    return render_template('search.html', msg=msg, items=results)

@app.route('/item/<postid>', methods=['POST','GET'], endpoint='item')
def item(postid):
    msg = ''
    user = session['username']
    today = str(date.today())
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("CREATE TABLE IF NOT EXISTS `reviews` (`reviewid` INT AUTO_INCREMENT,`postid` INT,`username` varchar(50) NOT NULL,`feedback` varchar(50) NOT NULL,`review` varchar(255) NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`reviewid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    mysql.connection.commit()

    if request.method == 'POST':
        if request.form['feedback'] != '' and request.form['review'] != '':
            test = cursor.execute("SELECT * FROM reviews WHERE username =%s and date =%s", (user, today,))
            if (test < 3):
                cursor.execute("SELECT * FROM posts WHERE postid =%s", (postid))
                postresult = cursor.fetchone()
                print(postresult['username'])
                if postresult['username'] != user:
                    feedback = request.form['feedback']
                    review = request.form['review']
                    cursor.execute('INSERT INTO reviews (postid, username, feedback, review, date) VALUES (%s, %s, %s, %s, %s)', (postid, user, feedback, review, today,))
                    mysql.connection.commit()
                else:
                    msg = "Sorry, you cannot review your own product."
            else:
                msg = "Sorry, you have already posted 3 reviews today. Please try again later"

    cursor.execute("SELECT * FROM reviews WHERE postid =%s", (postid))
    results = cursor.fetchall()

    return render_template('item.html', msg=msg, items=results, postid=postid)

@app.route('/initdb', methods=['POST','GET'])
def initdb():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    today = str(date.today())

    cursor.execute("CREATE TABLE IF NOT EXISTS `accounts` (`username` varchar(50) NOT NULL,`firstname` varchar(50) NOT NULL,`lastname` varchar(50) NOT NULL,`password` varchar(255) NOT NULL,`email` varchar(100) NOT NULL,PRIMARY KEY (`username`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    currUser = session['username']
    cursor.execute('DELETE FROM accounts WHERE username <> %s', (currUser,))
    cursor.execute('ALTER TABLE accounts AUTO_INCREMENT = 2;')
    mysql.connection.commit()
    for i in range(0, 5):
        username = "user" + str(i)
        firstname = "username" + str(i)
        lastname = "lastname" + str(i)
        password = "Password" + str(i) + "*"
        email = "email" + str(i) + "@email.com"
        cursor.execute('SELECT * FROM accounts WHERE username =%s AND email = %s', (username, email,))
        account = cursor.fetchone()
        if not account:
            cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', (username, firstname, lastname, password, email,))
            mysql.connection.commit()

    cursor.execute("SELECT * FROM accounts")
    results = cursor.fetchall()

    cursor.execute("CREATE TABLE IF NOT EXISTS `posts` (`postid` INT AUTO_INCREMENT,`username` varchar(50) NOT NULL,`title` varchar(50) NOT NULL,`description` varchar(50) NOT NULL,`category` varchar(255) NOT NULL,`price` varchar(100) NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`postid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    cursor.execute('DELETE FROM posts WHERE 1=1')
    cursor.execute('ALTER TABLE posts AUTO_INCREMENT = 1;')
    mysql.connection.commit()
    for i in range(0, 5):
        username = "username" + str(i)
        title = "username" + str(i) + "'s post " + str(i)
        description = "Description for post " + str(i)
        category = "Category0"
        numCat = random.randint(1, 5)
        for j in range(1, numCat):
            category = category + ", Category" +str(j) 
        price = random.randint(5, 1000)
        cursor.execute('SELECT * FROM posts WHERE username =%s', (username,))
        post = cursor.fetchone()
        if not post:
            cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", (username, title, description, category, price, today))
            mysql.connection.commit()

    cursor.execute("CREATE TABLE IF NOT EXISTS `reviews` (`reviewid` INT AUTO_INCREMENT,`postid` INT,`username` varchar(50) NOT NULL,`feedback` varchar(50) NOT NULL,`review` varchar(255) NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`reviewid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    cursor.execute('DELETE FROM reviews WHERE 1=1')
    cursor.execute('ALTER TABLE reviews AUTO_INCREMENT = 1;')
    mysql.connection.commit()
    for i in range(0, 5):
        random_int = random.randint(0, 4)
        postid = random_int
        username = "username" + str(i)
        options = ["Excellent", "Good", "Fair", "Poor"]
        feedback = random.choice(options)
        review = "username" + str(i) + " finds this product " + feedback
        cursor.execute('SELECT * FROM reviews WHERE username =%s', (username,))
        rev = cursor.fetchone()
        if not rev:
            cursor.execute('INSERT INTO reviews (postid, username, feedback, review, date) VALUES (%s, %s, %s, %s, %s)', (postid, username, feedback, review, today,))
            mysql.connection.commit()

    cursor.execute("SELECT * FROM accounts")
    results = cursor.fetchall()
    for r in results:
        r['password'] = r['password'][0] + r['password'][1] + r['password'][2] + '*' * (len(r['password']) - 3)

    cursor.execute("SELECT * FROM posts")
    postitems = cursor.fetchall()

    cursor.execute("SELECT * FROM reviews")
    reviewitems = cursor.fetchall()

    return render_template('initdb.html', items=results, postitems=postitems, reviewitems=reviewitems)

if __name__ == "__main__":
    app.run(debug=1, host='0.0.0.0', port=5000)