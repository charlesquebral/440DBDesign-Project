from flask import Flask, redirect, url_for, render_template, request, session
from flask_mysqldb import MySQL
from datetime import date
import random
import pandas as pd
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
    cursor.execute("CREATE TABLE IF NOT EXISTS `reviews` (`reviewid` INT AUTO_INCREMENT,`postid` INT,`poster` varchar(50) NOT NULL,`reviewer` varchar(50) NOT NULL,`feedback` varchar(50) NOT NULL,`review` varchar(255) NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`reviewid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
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
        #print(sql_query)
        msg = str(findings) + " results found!"

    return render_template('search.html', msg=msg, items=results)

@app.route('/item/<postid>', methods=['POST','GET'], endpoint='item')
def item(postid):
    msg = ''
    user = session['username']
    today = str(date.today())
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("CREATE TABLE IF NOT EXISTS `reviews` (`reviewid` INT AUTO_INCREMENT,`postid` INT,`poster` varchar(50) NOT NULL,`reviewer` varchar(50) NOT NULL,`feedback` varchar(50) NOT NULL,`review` varchar(255) NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`reviewid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    mysql.connection.commit()

    cursor.execute("SELECT * FROM posts WHERE postid =%s", (postid,))
    postresult = cursor.fetchone()
    title = postresult['title']
    poster = postresult['username']
    if request.method == 'POST':
        if request.form['feedback'] != '' and request.form['review'] != '':
            test = cursor.execute("SELECT * FROM reviews WHERE username =%s and date =%s", (user, today,))
            if (test < 3):
                #print(postresult['username'])
                if postresult['username'] != user:
                    feedback = request.form['feedback']
                    review = request.form['review']
                    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', (postid, poster, user, feedback, review, today,))
                    mysql.connection.commit()
                else:
                    msg = "Sorry, you cannot review your own product."
            else:
                msg = "Sorry, you have already posted 3 reviews today. Please try again later"

    cursor.execute("SELECT * FROM reviews WHERE postid =%s", (postid))
    results = cursor.fetchall()

    return render_template('item.html', msg=msg, items=results, postid=postid, title=title, poster=poster)

@app.route('/user_stats', methods=['POST','GET'])
def user_stats():
    return render_template('user_stats.html')

@app.route('/initdb', methods=['POST','GET'])
def initdb():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    today = str(date.today())

    cursor.execute("CREATE TABLE IF NOT EXISTS `accounts` (`username` varchar(50) NOT NULL,`firstname` varchar(50) NOT NULL,`lastname` varchar(50) NOT NULL,`password` varchar(255) NOT NULL,`email` varchar(100) NOT NULL,PRIMARY KEY (`username`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    currUser = session['username']
    cursor.execute('DELETE FROM accounts WHERE username <> %s', (currUser,))
    cursor.execute('ALTER TABLE accounts AUTO_INCREMENT = 2;')
    mysql.connection.commit()

    #CREATE USERS
    cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', ("silverstorm45", "Emily", "Johnson", "Password0*", "ejohnson@example.com",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', ("techsavvy87", "Jacob", "Martinez", "Password5*", "jmartinez@example.com",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', ("melody_wanderer", "Sophia", "Lee", "Password12*", "slee@example.com",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', ("adventureseeker22", "Liam", "Anderson", "Password7*", "landerson@example.com",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', ("code_ninja", "Ava", "Thompson", "Password88*", "athompson@example.com",))
    mysql.connection.commit()

    cursor.execute("SELECT * FROM accounts")
    results = cursor.fetchall()

    cursor.execute("CREATE TABLE IF NOT EXISTS `favorites` (`favoriteid` INT AUTO_INCREMENT,`username` varchar(50) NOT NULL,`favorite` varchar(100) NOT NULL,`type` varchar(50) NOT NULL,PRIMARY KEY (`favoriteid`)) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;")
    cursor.execute('DELETE FROM favorites WHERE username <> %s', (currUser,))
    cursor.execute('ALTER TABLE favorites AUTO_INCREMENT = 2;')
    mysql.connection.commit()

    #CREATE FAVORITES
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("silverstorm45", "melody_wanderer", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("silverstorm45", "code_ninja", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("adventureseeker22", "code_ninja", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("adventureseeker22", "techsavvy87", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("adventureseeker22", "melody_wanderer", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("melody_wanderer", "code_ninja", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("melody_wanderer", "adventureseeker22", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("melody_wanderer", "techsavvy87", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("techsavvy87", "silverstorm45", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("techsavvy87", "code_ninja", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("code_ninja", "adventureseeker22", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("code_ninja", "melody_wanderer", "users",))
    mysql.connection.commit()
    cursor.execute('INSERT INTO favorites (`username`, `favorite`, `type`) VALUES (%s, %s, %s);', ("code_ninja", "silverstorm45", "users",))
    mysql.connection.commit()

    cursor.execute("CREATE TABLE IF NOT EXISTS `posts` (`postid` INT AUTO_INCREMENT,`username` varchar(50) NOT NULL,`title` varchar(50) NOT NULL,`description` varchar(50) NOT NULL,`category` varchar(255) NOT NULL,`price` float NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`postid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    cursor.execute('DELETE FROM posts WHERE 1=1')
    cursor.execute('ALTER TABLE posts AUTO_INCREMENT = 1;')
    mysql.connection.commit()

    #CREATE POSTS
    cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", ("silverstorm45", "iPhone 12", "Used, Good Condition", "electronic, cellphone, apple", "300", "2023-05-01"))
    mysql.connection.commit()

    cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", ("silverstorm45", "iPhone 13", "Used, Good Condition", "electronic, cellphone, apple", "400", "2023-05-01"))
    mysql.connection.commit()

    cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", ("silverstorm45", "iPad", "Used, Good Condition", "electronic, tablet, apple", "700", "2023-05-01"))
    mysql.connection.commit()

    cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", ("melody_wanderer", "MacBook Pro", "Unopened, Mint Condition", "electronic, computer, apple", "1200", "2023-05-01"))
    mysql.connection.commit()

    cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", ("melody_wanderer", "Samsung GalaxyS", "Unopened, Mint Condition", "electronic, computer, apple", "1200", "2023-05-01"))
    mysql.connection.commit()

    cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", ("code_ninja", "Roland TD-30KV", "Used, Excellent Condition", "electronic, instrument, roland", "7000", "2023-08-12"))
    mysql.connection.commit()

    cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", ("techsavvy87", "Airpod Pros Gen 2", "Used, Fair Condition", "electronic, bluetooth, apple", "90", "2023-11-19"))
    mysql.connection.commit()

    cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", ("techsavvy87", "Gibson Les Paul Studio", "Used, Great Condition", "instrument, gibson", "2700", "2023-04-09"))
    mysql.connection.commit()

    cursor.execute("INSERT INTO posts (username, title, description, category, price, date) VALUES (%s, %s, %s, %s, %s, %s);", ("adventureseeker22", "Korg KP2", "Used, Good Condition", "instrument, korg, electronic", "350", "2023-10-27"))
    mysql.connection.commit()

    cursor.execute("CREATE TABLE IF NOT EXISTS `reviews` (`reviewid` INT AUTO_INCREMENT,`postid` INT,`poster` varchar(50) NOT NULL,`reviewer` varchar(50) NOT NULL,`feedback` varchar(50) NOT NULL,`review` varchar(255) NOT NULL,`date` varchar(50) NOT NULL,PRIMARY KEY (`reviewid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")
    cursor.execute('DELETE FROM reviews WHERE 1=1')
    cursor.execute('ALTER TABLE reviews AUTO_INCREMENT = 1;')
    mysql.connection.commit()
    
    #CREATE REVIEWS
    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("4", "melody_wanderer", "adventureseeker22", "Excellent", "This is excellent!", "2023-11-20",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("5", "melody_wanderer", "adventureseeker22", "Excellent", "This is excellent!", "2023-12-01",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("4", "melody_wanderer", "code_ninja", "Excellent", "This is excellent!", "2023-11-21",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("4", "melody_wanderer", "silverstorm45", "Excellent", "This is excellent!", "2023-11-21",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("2", "silverstorm45", "techsavvy87", "Poor", "This is poor!", "2023-11-25",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("3", "silverstorm45", "adventureseeker22", "Good", "This is good!", "2023-11-26",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("7", "techsavvy87", "code_ninja", "Good", "This is good!", "2023-11-21",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("1", "silverstorm45", "code_ninja", "Excellent", "This is Excellent!", "2023-11-19",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("2", "silverstorm45", "code_ninja", "Excellent", "This is Excellent!", "2023-11-19",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("3", "silverstorm45", "code_ninja", "Excellent", "This is Excellent!", "2023-11-19",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("9", "adventureseeker22", "code_ninja", "Good", "This is good!", "2023-11-19",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("8", "techsavvy87", "adventureseeker22", "Excellent", "This is Excellent!", "2023-11-20",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("9", "adventureseeker22", "techsavvy87", "Fair", "This is fair!", "2023-11-20",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("2", "silverstorm45", "melody_wanderer", "Poor", "This is poor!", "2023-11-25",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("6", "code_ninja", "melody_wanderer", "Poor", "This is poor!", "2023-11-25",))
    mysql.connection.commit()

    cursor.execute('INSERT INTO reviews (postid, poster, reviewer, feedback, review, date) VALUES (%s, %s, %s, %s, %s, %s)', ("6", "code_ninja", "silverstorm45", "Excellent", "This is Excellent!", "2023-11-19",))
    mysql.connection.commit()

    cursor.execute("SELECT * FROM accounts")
    results = cursor.fetchall()
    for r in results:
        r['password'] = r['password'][0] + r['password'][1] + r['password'][2] + '*' * (len(r['password']) - 3)

    cursor.execute("SELECT * FROM posts")
    postitems = cursor.fetchall()

    cursor.execute("SELECT * FROM reviews")
    reviewitems = cursor.fetchall()

    cursor.execute("SELECT * FROM favorites")
    favoriteitems = cursor.fetchall()

    return render_template('initdb.html', items=results, postitems=postitems, reviewitems=reviewitems, favoriteitems=favoriteitems)

@app.route('/req1', methods=['POST','GET'],)
def req1():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT * from posts')
    df = cursor.fetchall()
    newdf = pd.DataFrame(df)
    categories_list = newdf['category'].str.split(', ').explode().tolist()
    unique_values = list(set(categories_list))
    results = []
    for i in unique_values:
        sql_query = "SELECT * FROM posts WHERE 1 = 1"
        sql_query += f" AND category LIKE '%{str(i)}%' ORDER BY price DESC"
        cursor.execute(sql_query)
        res = cursor.fetchone()
        res['focus'] = str(i)
        results.append(res)

    results.sort(key=lambda x: x['focus'])
    
    return render_template('req1.html', msg=msg, categories=results)

@app.route('/req2', methods=['POST','GET'],)
def req2():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    catx=''
    caty=''

    if request.method == 'POST':
        if 'catx' in request.form and 'caty' in request.form:
            if str(request.form['catx']) != '' and str(request.form['caty']) != '':
                if request.form['catx'] != request.form['caty']:
                    catx = str(request.form['catx'])
                    caty = str(request.form['caty'])
                    cursor.execute(f"SELECT DISTINCT t2.username FROM posts t1 JOIN posts t2 ON t1.date = t2.date AND t1.postid <> t2.postid AND t1.username = t2.username WHERE (t1.category LIKE '%{catx}%' AND t2.category LIKE '%{caty}%') OR (t1.category LIKE '%{caty}%' AND t2.category LIKE '%{catx}%') GROUP BY t2.username, t2.date HAVING COUNT(t2.postid) >= 2;")
                    results = cursor.fetchall()
                else:
                    msg = "Categories X and Y cannot be the same!"
                    results = {}
            else:
                msg = "One or more categories are missing!"
                results = {}

    return render_template('req2.html', msg=msg, results=results, catx=catx, caty=caty)

@app.route('/req3', methods=['POST','GET'],)
def req3():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        if 'userx' in request.form:
            if str(request.form['userx']) != '':
                userx = str(request.form['userx'])
                cursor.execute(f"SELECT DISTINCT postid FROM reviews r1 WHERE NOT EXISTS (SELECT 1 FROM reviews r2 WHERE r1.postid = r2.postid AND r2.feedback IN ('Poor', 'Fair')) AND r1.poster = '{userx}';")
                results = cursor.fetchall()
                post_ids = [d['postid'] for d in results]
                posts=[]
                for i in post_ids:
                    cursor.execute(f"SELECT * FROM posts WHERE postid = '{i}'")
                    res = cursor.fetchone()
                    posts.append(res)
            else:
                msg = "User cannot be missing!"
                userx = ''
                posts=[]
                results = {}

    return render_template('req3.html', msg=msg, items=posts, user=userx)

@app.route('/req4', methods=['POST','GET'],)
def req4():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT username FROM posts WHERE date = "2023-05-01" GROUP BY username HAVING COUNT(*) = ( SELECT MAX(post_count) FROM (SELECT COUNT(*) AS post_count FROM posts WHERE date = "2023-05-01" GROUP BY username ) AS counts );')
    results = cursor.fetchall()
    
    return render_template('req4.html', msg=msg, results = results)

@app.route('/req5', methods=['POST','GET'],)
def req5():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        if 'userx' in request.form and 'usery' in request.form:
            if str(request.form['userx']) != '' and str(request.form['usery']) != '':
                if request.form['userx'] != request.form['usery']:
                    userx = str(request.form['userx'])
                    usery = str(request.form['usery'])
                    cursor.execute(f"SELECT DISTINCT favorite FROM favorites WHERE 1=1 AND type = 'users' AND (username = '{userx}' OR username = '{usery}') AND (favorite <> '{userx}' AND favorite <> '{usery}') GROUP BY favorite HAVING COUNT(*) > 1;")
                    results = cursor.fetchall()
                else:
                    msg = "Users X and Y cannot be the same!"
                    userx=''
                    usery=''
                    results = {}
            else:
                msg = "One or more users are missing!"
                userx=''
                usery=''
                results = {}
    
    return render_template('req5.html', msg=msg, results=results, userx=userx, usery=usery)

@app.route('/req6', methods=['POST','GET'],)
def req6():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT DISTINCT username FROM accounts WHERE username NOT IN (SELECT DISTINCT poster FROM reviews WHERE feedback = 'Excellent' GROUP BY poster, postid HAVING COUNT(*) >= 3);")
    results = cursor.fetchall()
    #print(results)
    return render_template('req6.html', msg=msg, results=results)

@app.route('/req7', methods=['POST','GET'],)
def req7():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT DISTINCT username FROM accounts WHERE username NOT IN ( SELECT DISTINCT reviewer FROM reviews WHERE feedback = 'Poor' GROUP BY reviewer HAVING COUNT(*) >= 1);")
    results = cursor.fetchall()
    #print(results)
    return render_template('req7.html', msg=msg, results=results)

@app.route('/req8', methods=['POST','GET'],)
def req8():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT DISTINCT reviewer FROM reviews r1 WHERE feedback = 'Poor' AND NOT EXISTS ( SELECT 1 FROM reviews r2 WHERE r1.reviewer = r2.reviewer AND r2.feedback != 'Poor');")
    results = cursor.fetchall()
    #print(results)
    return render_template('req8.html', msg=msg, results=results)

@app.route('/req9', methods=['POST','GET'],)
def req9():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT DISTINCT username FROM posts WHERE username NOT IN (SELECT DISTINCT poster FROM reviews WHERE feedback = 'Poor' GROUP BY poster HAVING COUNT(*) >= 1);")
    results = cursor.fetchall()
    #print(results)
    return render_template('req9.html', msg=msg, results=results)

@app.route('/req10', methods=['POST','GET'],)
def req10():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT r1.poster AS poster1, r1.reviewer AS reviewer1,(SELECT COUNT(*) FROM posts p WHERE p.username = r1.poster) AS post_count_r1 FROM reviews r1 JOIN reviews r2 ON r1.poster = r2.reviewer AND r1.reviewer = r2.poster WHERE (r1.feedback = 'Excellent' AND r2.feedback = 'Excellent') GROUP BY r1.poster, r1.reviewer, r2.poster, r2.reviewer, r2.feedback HAVING COUNT(r2.poster) = post_count_r1;")
    results = cursor.fetchall()
    #print(results)
    return render_template('req10.html', msg=msg, results=results)

if __name__ == "__main__":
    app.run(debug=1, host='0.0.0.0', port=5000)