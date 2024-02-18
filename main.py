# from flask import Flask, render_template, request, redirect, url_for, session

# app = Flask(__name__)

# # A session objektum használatához szükséges titkos kulcs
# app.secret_key = 'super_secret_key'

# # Dummy adatbázis a felhasználók tárolására
# users = {}

# # Egyéb útvonalak...


# @app.route('/')
# def index():
#     if 'username' in session:
#         return render_template('home.html', username=session['username'])
#     return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         users[username] = password
#         session['username'] = username
#         return redirect(url_for('login'))
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if users.get(username) == password:
#             # Sikeres bejelentkezés
#             session['username'] = username
#             return redirect(url_for('index'))
#         else:
#             # Sikertelen bejelentkezés
#             error = "Hibás felhasználónév vagy jelszó"
#             return render_template('login.html', error=error)
#     return render_template('login.html')


# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.secret_key = 'super_secret_key'
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite adatbázis konfiguráció
app.secret_key = 'super_secret_key'  # Fontos, hogy titkos kulcsot használj a munkamenetekhez
db = SQLAlchemy(app)

# Felhasználó modell létrehozása
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Dummy adatbázis a felhasználók tárolására
# users = {}

with app.app_context():
    # Az adatbázis létrehozása
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Felhasználó hozzáadása az adatbázishoz
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Sikeres bejelentkezés
            session['username'] = username
            return redirect(url_for('home'))
        else:
            # Sikertelen bejelentkezés
            error = "Hibás felhasználónév vagy jelszó"
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
