import sqlite3

from models import *

def get_connection(autocommit=True):
    if autocommit:
        return sqlite3.connect("onlineshop.db")
    else:
        return sqlite3.connect("onlineshop.db", isolation_level=None)

def create_db():
    query1 = """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    query2 = """
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            itemname TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    """
    query3 = """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            price INTEGER NOT NULL
        )
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        cur.execute(query1)
        con.commit()
        cur.execute(query2)
        con.commit()
        cur.execute(query3)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
    finally:
        con.close()

def auth(username, password):
    query = """
        SELECT * FROM users WHERE username = ? AND password = ?
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, (username, password,))
        res = cur.fetchone()
        user = User()
        user.id = res[0]
        user.username = res[1]
        user.password = res[2]
        return user
    except Exception as e:
        return None
    finally:
        con.close()

def search_users():
    query = """
        SELECT * FROM users
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        user_list = []
        for r in res:
            user = User()
            user.id = r[0]
            user.username = r[1]
            user.password = r[2]
            user_list.append(user)
        return user_list
    except Exception as e:
        return None
    finally:
        con.close()

def search_user_by_id(id):
    query = """
        SELECT * FROM users WHERE id = ?
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, (id,))
        res = cur.fetchone()
        user = User()
        user.id = res[0]
        user.username = res[1]
        user.password = res[2]
        return user
    except Exception as e:
        return None
    finally:
        con.close()

def search_user(username):
    query = """
        SELECT * FROM users WHERE username = ?
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, (username,))
        res = cur.fetchone()
        user = User()
        user.id = res[0]
        user.username = res[1]
        user.password = res[2]
        return user
    except Exception as e:
        return None
    finally:
        con.close()

def add_user(user):
    query = """
        INSERT INTO users (username, password) VALUES (?, ?) RETURNING id
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        cur.execute(query, (user.username, user.password,))
        user.id = cur.fetchone()
        con.commit()
        return user
    except Exception as e:
        con.rollback()
        return None
    finally:
        con.close()

def edit_user(user):
    query = """
        UPDATE users SET username = ?, password = ? WHERE id = ?
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        cur.execute(query, (user.username, user.password, user.id,))
        con.commit()
        return user
    except Exception as e:
        con.rollback()
        return None
    finally:
        con.close()

def remove_user(user):
    query = """
        DELETE FROM users WHERE id = ?
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        cur.execute(query, (user.id,))
        con.commit()
        return None
    except Exception as e:
        con.rollback()
        return user
    finally:
        con.close()

def search_items():
    query = """
        SELECT * FROM items
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        item_list = []
        for r in res:
            item = Item()
            item.id = r[0]
            item.owner_id = r[1]
            item.itemname = r[2]
            item.price = r[3]
            item_list.append(item)
        return item_list
    except Exception as e:
        return None
    finally:
        con.close()

def search_item_by_id(id):
    query = """
        SELECT * FROM items WHERE id = ?
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, (id,))
        res = cur.fetchone()
        item = Item()
        item.id = res[0]
        item.owner_id = res[1]
        item.itemname = res[2]
        item.price = res[3]
        return item
    except Exception as e:
        return None
    finally:
        con.close()

def search_items_by_owner_id(owner_id):
    query = """
        SELECT items.id, items.owner_id, users.username AS ownername, items.itemname, items.price 
        FROM items, users 
        WHERE items.owner_id = ? 
        AND items.owner_id = users.id 
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, (owner_id,))
        res = cur.fetchall()
        item_list = []
        for r in res:
            item = Item()
            item.id = r[0]
            item.owner_id = r[1]
            item.ownername = r[2]
            item.itemname = r[3]
            item.price = r[4]
            item_list.append(item)
        return item_list
    except Exception as e:
        return None
    finally:
        con.close()

def search_item(itemname):
    query = """
        SELECT * FROM items WHERE itemname LIKE ?
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, ("%" + itemname + "%",))
        res = cur.fetchall()
        item_list = []
        for r in res:
            item = Item()
            item.id = r[0]
            item.owner_id = r[1]
            item.itemname = r[2]
            item.price = r[3]
            item_list.append(item)
        return item_list
    except Exception as e:
        return None
    finally:
        con.close()

def add_item(item):
    query = """
        INSERT INTO items (owner_id, itemname, price) VALUES (?, ?, ?) RETURNING id
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        cur.execute(query, (item.owner_id, item.itemname, item.price,))
        item.id = cur.fetchone()
        con.commit()
        return item
    except Exception as e:
        con.rollback()
        return None
    finally:
        con.close()

def edit_item(item):
    query = """
        UPDATE items SET owner_id = ?, itemname = ?, price = ? WHERE id = ?
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        cur.execute(query, (item.owner_id, item.itemname, item.price, item.id,))
        con.commit()
        return item
    except Exception as e:
        con.rollback()
        return None
    finally:
        con.close()

def remove_item(item):
    query = """
        DELETE FROM items WHERE id = ?
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        cur.execute(query, (item.id,))
        con.commit()
        return None
    except Exception as e:
        con.rollback()
        return item
    finally:
        con.close()

def search_orders():
    query = """
        SELECT * FROM orders
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        order_list = []
        for r in res:
            order = Order()
            order.id = r[0]
            order.order_code = r[1]
            order.user_id = r[2]
            order.item_id = r[3]
            order.amount = r[4]
            order.price = r[5]
            order_list.append(order)
        return order_list
    except Exception as e:
        return None
    finally:
        con.close()

def search_order_by_id(id):
    query = """
        SELECT * FROM orders WHERE id = ?
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, (id,))
        res = cur.fetchone()
        order = Order()
        order.id = res[0]
        order.order_code = res[1]
        order.user_id = res[2]
        order.item_id = res[3]
        order.amount = res[4]
        order.price = res[5]
        return order
    except Exception as e:
        return None
    finally:
        con.close()

def search_order(order_code):
    query = """
        SELECT * FROM orders WHERE order_code = ?
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, (order_code, user_id,))
        res = cur.fetchall()
        order_list = []
        for r in res:
            order = Order()
            order.id = r[0]
            order.order_code = r[1]
            order.user_id = r[2]
            order.item_id = r[3]
            order.amount = r[4]
            order.price = r[5]
            order_list.append(order)
        return order_list
    except Exception as e:
        return None
    finally:
        con.close()

def add_order(order_list):
    query = """
        INSERT INTO orders (order_code, user_id, item_id, amount, price) 
        VALUES (?, ?, ?, ?, ?) RETURNING id
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        for order in order_list:
            cur.execute(query, (order.order_code, order.user_id, order.item_id, order.amount, order.price,))
            order.id = cur.fetchone()
        con.commit()
        return order_list
    except Exception as e:
        con.rollback()
        return None
    finally:
        con.close()

def edit_order(order):
    query = """
        UPDATE orders 
        SET order_code = ?, user_id = ?, item_id = ?, amount = ?, price = ? 
        WHERE id = ?
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        cur.execute(query, (order.order_code, order.uesr_id, order.item_id, order.amount, order.price,))
        con.commit()
        return order
    except Exception as e:
        con.rollback()
        return None
    finally:
        con.close()

def remove_order(order):
    query = """
        DELETE FROM orders WHERE id = ?
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        cur.execute(query, (order.id,))
        con.commit()
        return None
    except Exception as e:
        con.rollback()
        return order
    finally:
        con.close()

def search_items(itemname):
    query = """
        SELECT items.id, items.owner_id, users.username AS ownername, items.itemname, items.price 
        FROM items, users 
        WHERE itemname LIKE ? 
        AND items.owner_id = users.id 
    """
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, ("%" + itemname + "%",))
        res = cur.fetchall()
        item_list = []
        for r in res:
            item = Item()
            item.id = r[0]
            item.owner_id = r[1]
            item.ownername = r[2]
            item.itemname = r[3]
            item.price = r[4]
            item_list.append(item)
        return item_list
    except Exception as e:
        return None
    finally:
        con.close()

def add_order(order_list):
    query = """
        INSERT INTO orders (order_code, user_id, item_id, amount, price) 
        VALUES (?, ?, ?, ?, ?) RETURNING id
    """
    con = get_connection(autocommit=False)
    try:
        cur = con.cursor()
        for order in order_list:
            cur.execute(query, (order.order_code, order.user_id, order.item_id, order.amount, order.price,))
            order.id = cur.fetchone()
        con.commit()
        return order_list
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        con.close()

if __name__ == "__main__":
    create_db()

    user = User()
    user.username = "admin"
    user.password = "password"
    add_user(user)

    user = User()
    user.username = "user"
    user.password = "password"
    add_user(user)

    print(auth("admin", "password"))