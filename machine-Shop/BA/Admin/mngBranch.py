from flask import Blueprint, request, jsonify,redirect,url_for,render_template
from connect import get_db_connection

branch_bp = Blueprint('branch',__name__)

@branch_bp.route('/ul')
def Branch():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM branch')
    branch = cursor.fetchall()
    conn.close()
    return render_template('ul.html', branch=branch)


@branch_bp.route('/api/branch/add', methods=['POST'])
def add_Branch():
    name = request.form['name']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO branch (branch_name) VALUES (%s)', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('mngIndex.Index'))

@branch_bp.route('/api/branch/update/<int:id>', methods=['POST'])
def update_Branch(id):
    name=request.form['name']
    conn = get_db_connection()
    cursor=conn.cursor()
    cursor.execute('UPDATE branch SET branch_name=%s where branch_id=%s', (name,id))
    conn.commit()
    conn.close()
    return redirect(url_for('mngIndex.Index'))

@branch_bp.route('/api/branch/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM branch WHERE branch_id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('mngIndex.Index'))