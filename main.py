from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///felhasznalok.db'  # SQLite adatbázis konfiguráció
app.secret_key = 'c5e7fe5e7aa2eae27ba0d2369b3be802'  # Fontos, hogy titkos kulcsot használj a munkamenetekhez
db = SQLAlchemy(app)

# Felhasználó modell létrehozása
class Felhasznalo(db.Model):
    
    def __init__(self, felhasznalonev, jelszo):
        self.felhasznalonev = felhasznalonev
        self.jelszo = jelszo
        
    id = db.Column(db.Integer, primary_key=True)
    felhasznalonev = db.Column(db.String(50), unique=True, nullable=False)
    jelszo = db.Column(db.String(100), nullable=False)




with app.app_context():
    db.create_all()

@app.route('/')
def kezdolap():
    return render_template('kezdolap.html')

@app.route('/regisztracio', methods=['GET', 'POST'])
def regisztracio():
    if request.method == 'POST':
        felhasznalonev = request.form['felhasznalonev']
        jelszo = request.form['jelszo']
        # Ellenőrizzük, hogy a felhasználónév már létezik-e az adatbázisban
        felhasznalo_foglalt = Felhasznalo.query.filter_by(felhasznalonev=felhasznalonev).first()
        if felhasznalo_foglalt:
            hiba = "Ez a felhasználónév már foglalt. Kérlek, válassz másikat."
            return render_template('regisztracio.html', hiba=hiba)
        # Ha nem létezik ilyen felhasználónév, akkor hozzáadjuk az adatbázishoz
        uj_felhasznalo = Felhasznalo(felhasznalonev=felhasznalonev, jelszo=jelszo)
        db.session.add(uj_felhasznalo)
        db.session.commit()
        return redirect(url_for('bejelentkezes'))
    return render_template('regisztracio.html')


@app.route('/bejelentkezes', methods=['GET', 'POST'])
def bejelentkezes():
    if request.method == 'POST':
        felhasznalonev = request.form['felhasznalonev']
        jelszo = request.form['jelszo']
        felhasznalo = Felhasznalo.query.filter_by(felhasznalonev=felhasznalonev, jelszo=jelszo).first()
        if felhasznalo:
            # Sikeres bejelentkezés
            session['felhasznalonev'] = felhasznalonev
            return redirect(url_for('fooldal'))
        else:
            # Sikertelen bejelentkezés
            hiba = "Hibás felhasználónév vagy jelszó"
            return render_template('bejelentkezes.html', hiba=hiba)
    return render_template('bejelentkezes.html')

@app.route('/fooldal')
def fooldal():
    if 'felhasznalonev' in session:
        return render_template('fooldal.html', felhasznalonev=session['felhasznalonev'])
    return redirect(url_for('bejelentkezes'))

@app.route('/kijelentkezes')
def kijelentkezes():
    session.pop('felhasznalonev', None)
    return redirect(url_for('kezdolap'))

if __name__ == '__main__':
    app.run(debug=True)
