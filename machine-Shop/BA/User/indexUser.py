from flask import Blueprint, render_template, session,request,redirect
from connect import get_db_connection

user_bp = Blueprint("user_bp", __name__,template_folder='../../giftos-html', static_folder='../../giftos-html/assets')

@user_bp.route('/', methods=['GET','POST'])
def IndexUser():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method =='POST':
        if 'name_acc' not in session:
            return render_template('login.html')
        else:
            try:
                item_id=request.form.get("item_id",None)
                cursor.execute("SELECT * FROM cart WHERE item_id = %s", (item_id,))
                item=cursor.fetchall()

                if item:
                    return "ITEM IS ALREADY ADDED"
                else:
                    cursor.execute("INSERT INTO cart (item_id) VALUES(%s)", (item_id,))
                    conn.commit()
                return redirect("/")
            except Exception:
                return "ERROR OCCURRED"    
    else:
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        conn.close()
        return render_template('index.html', items=items)

@user_bp.route('/shop',methods=['GET','POST'])
def Shop():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method =='POST':
        try:
            item_id=request.form.get("item_id",None)
            cursor.execute("SELECT * FROM cart WHERE item_id = %s", (item_id,))
            item=cursor.fetchall()

            if item:
                return "ITEM IS ALREADY ADDED"
            else:
                cursor.execute("INSERT INTO cart (item_id) VALUES(%s)", (item_id,))
                conn.commit()
                return redirect("/")
        except Exception:
            return "ERROR OCCURRED"
    else:
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        conn.close()
        return render_template('shop.html', items=items)

@user_bp.route('/why')
def Why():
    return render_template('why.html')

@user_bp.route('/contact')
def Contact():
    return render_template('contact.html')

@user_bp.route('/cart')
def Cart():
    if 'name_acc' not in session:
        return render_template('login.html')
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT cart.cart_id, items.name AS item_name, items.price FROM cart INNER JOIN items ON cart.item_id = items.id')
        cart=cursor.fetchall()
        return render_template('cart.html', cart=cart)
