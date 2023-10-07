from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def base():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST','GET'])
def login():
    error= None
    if request.method == "POST":
        user = request.form['cred']
        email = request.form['cred']
        password = request.form['password']
    return render_template('login.html', error=error)

@app.route('/signup', methods=['POST','GET'])
def signup():
    error= None
    return render_template('signup.html', error=error)

if __name__ == "__main__":
    app.run(debug=1, host='0.0.0.0', port=5000)