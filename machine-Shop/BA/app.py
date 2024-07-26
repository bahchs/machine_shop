from flask import Flask, render_template, request, redirect, url_for, session
from Admin.connect import get_db_connection
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Admin'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'User'))

from Admin.mngIndex import mngIndex_bp
from User.indexUser import user_bp

app = Flask(__name__,static_folder="")

app.register_blueprint(user_bp)
app.register_blueprint(mngIndex_bp)  


app.secret_key = 'bachbach'

@app.route('/')
def home():
    if 'name_acc' in session:
        if session['role_acc'] == 'User':
            return redirect(url_for('user_bp.IndexUser'))
        elif session['role_acc'] == 'Admin':
            return redirect(url_for('mngIndex_bp.Index'))
    else:
        return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name_acc, password_acc, role_acc FROM account WHERE email_acc = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        if user and password == user[1]:
            session['name_acc'] = user[0]
            session['role_acc'] = user[2]
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('name_acc', None)
    session.pop('role_acc', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
