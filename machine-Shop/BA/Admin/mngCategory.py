from flask import Blueprint, request, jsonify,redirect,url_for,render_template
from connect import get_db_connection

category_bp=Blueprint('category',__name__)

@category_bp.route('/ui')
def Category():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM category')
    categories = cursor.fetchall()
    conn.close()
    print(categories)
    return render_template('ui.html', categories=categories)


@category_bp.route('/api/category/add', methods=['POST'])
def add_Categories():
    name = request.form['name']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO category (category_name) VALUES (%s)', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('mngIndex.Index'))

@category_bp.route('/api/category/update/<int:id>', methods=['POST'])
def update_Categories(id):
    name=request.form['name']
    conn = get_db_connection()
    cursor=conn.cursor()
    cursor.execute('UPDATE category SET category_name=%s where category_id=%s', (name,id))
    conn.commit()
    conn.close()
    return redirect(url_for('mngIndex.Index'))

@category_bp.route('/api/category/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM category WHERE category_id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('mngIndex.Index'))
