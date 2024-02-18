from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# A session objektum használatához szükséges titkos kulcs
app.secret_key = 'super_secret_key'

# Dummy adatbázis a felhasználók tárolására
users = {}

# Egyéb útvonalak...


@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        session['username'] = username
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            # Sikeres bejelentkezés
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # Sikertelen bejelentkezés
            error = "Hibás felhasználónév vagy jelszó"
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
