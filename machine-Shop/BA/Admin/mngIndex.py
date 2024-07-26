from flask import Blueprint, render_template, request, redirect, url_for, session
from connect import get_db_connection
from mngItems import form_bp
from mngCategory import category_bp
from mngBranch import branch_bp

mngIndex_bp = Blueprint("mngIndex_bp", __name__,template_folder='../../horizontal-admin', static_folder='../../horizontal-admin/assets')

mngIndex_bp.register_blueprint(form_bp)
mngIndex_bp.register_blueprint(category_bp)
mngIndex_bp.register_blueprint(branch_bp)

@mngIndex_bp.route('/')
def Index():
    if 'name_acc' not in session:
        return render_template('login.html')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM account')
    account = cursor.fetchall()
    conn.close()
    return render_template('index.html', account=account)

@mngIndex_bp.route('/api/account/add', methods=['POST'])
def add_Account():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO account (name_acc, email_acc, password_acc, role_acc) VALUES (%s, %s, %s, %s)', (name, email, password, role))
    conn.commit()
    conn.close()
    return redirect(url_for('mngIndex_bp.Index'))
