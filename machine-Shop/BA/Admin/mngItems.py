from flask import Blueprint, request,redirect,url_for,render_template
from werkzeug.utils import secure_filename
import os
from connect import get_db_connection

form_bp= Blueprint('form',__name__)

@form_bp.route('/form')
def Form():
    return render_template('form.html')


@form_bp.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html',items=items)

@form_bp.route('/api/items/add', methods=['POST'])
def add():
    name = request.form['name']
    category = request.form['category']
    brand = request.form['brand']
    price = request.form['price']
    file = request.files['image']
    filename = secure_filename(file.filename)
    
    file_path = os.path.join('giftos-html','assets','images', filename)
    file.save(file_path)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, category, brand, price, image) VALUES (%s, %s, %s, %s, %s)', (name, category, brand, price, file_path))
    conn.commit()
    conn.close()
    return redirect(url_for('mngIndex.Index'))

@form_bp.route('/api/items/update/<int:id>', methods=['POST'])
def update(id):
    name=request.form['name']
    category=request.form['category']
    brand=request.form['brand']
    price=request.form['price']
    file = request.files['image']
    filename = secure_filename(file.filename)
    
    file_path = os.path.join('giftos-html','assets','images', filename)
    file.save(file_path)
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute('UPDATE items SET name=%s, category=%s, brand=%s, price=%s, image=%s WHERE id=%s', (name, category, brand, price, file_path, id))
    conn.commit()
    conn.close()
    return redirect(url_for('mngIndex.Index'))
