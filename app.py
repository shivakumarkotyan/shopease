import os
import sqlite3
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-12345'

# Database setup
def init_db():
    if os.path.exists('shopease.db'):
        os.remove('shopease.db')
        print("Old database removed. Creating new database...")
    
    conn = sqlite3.connect('shopease.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL,
            category_id INTEGER,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, product_id)
        )
    ''')
    
    # Insert sample data with Indian prices
    categories = [
        ('Electronics', 'Latest electronic gadgets and devices'),
        ('Clothing', 'Fashionable clothing for all'),
        ('Books', 'Books for all ages and interests'),
        ('Home & Garden', 'Items for your home and garden')
    ]
    cursor.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)
    
    # Products with Indian Rupee prices
    products = [
        ('Smartphone X', 'Latest smartphone with advanced features', 69999.99, 50, 1, '/static/images/smartphone.jpg'),
        ('Laptop Pro', 'High-performance laptop for professionals', 129999.99, 30, 1, '/static/images/laptop.jpg'),
        ('Wireless Headphones', 'Noise-cancelling wireless headphones', 19999.99, 100, 1, '/static/images/headphones.jpg'),
        ('Casual T-Shirt', 'Comfortable cotton t-shirt', 1999.99, 200, 2, '/static/images/tshirt.jpg'),
        ('Jeans', 'Classic blue jeans', 3499.99, 150, 2, '/static/images/jeans.jpg'),
        ('Python Programming Book', 'Learn Python programming', 899.99, 80, 3, '/static/images/book.jpg'),
        ('Garden Tools Set', 'Complete gardening tool set', 4999.99, 40, 4, '/static/images/gardentools.jpg'),
        ('Smart Watch', 'Feature-rich smartwatch', 24999.99, 60, 1, '/static/images/smartwatch.jpg')
    ]
    cursor.executemany("INSERT INTO products (name, description, price, stock_quantity, category_id, image_url) VALUES (?, ?, ?, ?, ?, ?)", products)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with Indian prices!")

def get_db_connection():
    conn = sqlite3.connect('shopease.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_current_user():
    return session.get('user')

def login_user(user):
    session['user'] = user

def logout_user():
    session.pop('user', None)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            flash('Please log in.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize database
init_db()

# ===== ROUTES =====

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products LIMIT 8').fetchall()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('index.html', featured_products=products, categories=categories, current_user=get_current_user())

@app.route('/products')
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT p.*, c.name as category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id').fetchall()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('products.html', products=products, categories=categories, current_user=get_current_user())

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT p.*, c.name as category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id WHERE p.id = ?', (product_id,)).fetchone()
    conn.close()
    if product:
        return render_template('product_detail.html', product=product, current_user=get_current_user())
    flash('Product not found!', 'danger')
    return redirect(url_for('products'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        hashed_password = hash_password(password)
        
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, email, password_hash, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
                (username, email, hashed_password, first_name, last_name)
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'danger')
        finally:
            conn.close()
    
    return render_template('register.html', current_user=get_current_user())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and user['password_hash'] == hash_password(password):
            user_dict = {'id': user['id'], 'username': user['username'], 'email': user['email']}
            login_user(user_dict)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html', current_user=get_current_user())

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    user_id = get_current_user()['id']
    conn = get_db_connection()
    cart_items = conn.execute('''
        SELECT c.*, p.name, p.price, p.image_url, 
               (c.quantity * p.price) as total_price
        FROM cart c JOIN products p ON c.product_id = p.id 
        WHERE c.user_id = ?
    ''', (user_id,)).fetchall()
    
    # Calculate grand total
    grand_total = sum(item['total_price'] for item in cart_items) if cart_items else 0
    
    conn.close()
    return render_template('cart.html', 
                         cart_items=cart_items, 
                         grand_total=grand_total,
                         current_user=get_current_user())

@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    user_id = get_current_user()['id']
    
    conn = get_db_connection()
    
    # Check if product exists and has stock
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if not product:
        flash('Product not found!', 'danger')
        return redirect(request.referrer or url_for('index'))
    
    existing = conn.execute('SELECT * FROM cart WHERE user_id = ? AND product_id = ?', (user_id, product_id)).fetchone()
    
    if existing:
        new_quantity = existing['quantity'] + quantity
        if new_quantity <= product['stock_quantity']:
            conn.execute('UPDATE cart SET quantity = ? WHERE id = ?', (new_quantity, existing['id']))
            flash('Product added to cart!', 'success')
        else:
            flash('Not enough stock available!', 'danger')
    else:
        if quantity <= product['stock_quantity']:
            conn.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)', (user_id, product_id, quantity))
            flash('Product added to cart!', 'success')
        else:
            flash('Not enough stock available!', 'danger')
    
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for('index'))

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    user_id = get_current_user()['id']
    
    conn = get_db_connection()
    
    # Check stock availability
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if quantity > 0 and quantity <= product['stock_quantity']:
        conn.execute(
            'UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?',
            (quantity, user_id, product_id)
        )
        flash('Cart updated successfully!', 'success')
    elif quantity > product['stock_quantity']:
        flash(f'Only {product["stock_quantity"]} items available in stock!', 'danger')
    else:
        # Remove item if quantity is 0
        conn.execute(
            'DELETE FROM cart WHERE user_id = ? AND product_id = ?',
            (user_id, product_id)
        )
        flash('Item removed from cart!', 'success')
    
    conn.commit()
    conn.close()
    return redirect('/cart')

@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    user_id = get_current_user()['id']
    
    conn = get_db_connection()
    conn.execute('DELETE FROM cart WHERE user_id = ? AND product_id = ?', (user_id, product_id))
    conn.commit()
    conn.close()
    
    flash('Item removed from cart!', 'success')
    return redirect('/cart')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category_id = request.args.get('category_id', type=int)
    
    conn = get_db_connection()
    
    sql = '''
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE 1=1
    '''
    params = []
    
    if query:
        sql += ' AND (p.name LIKE ? OR p.description LIKE ?)'
        params.extend([f'%{query}%', f'%{query}%'])
    
    if category_id:
        sql += ' AND p.category_id = ?'
        params.append(category_id)
    
    products = conn.execute(sql, params).fetchall()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    
    return render_template('products.html', 
                         products=products, 
                         categories=categories,
                         search_query=query, 
                         current_category=category_id,
                         current_user=get_current_user())

@app.route('/api/cart_count')
def cart_count():
    user = get_current_user()
    if not user:
        return jsonify({'count': 0})
    
    conn = get_db_connection()
    result = conn.execute('SELECT SUM(quantity) as total FROM cart WHERE user_id = ?', (user['id'],)).fetchone()
    conn.close()
    count = result['total'] if result['total'] else 0
    return jsonify({'count': count})

if __name__ == '__main__':
    print("ShopEase starting...")
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule}")
    app.run(debug=True, host='0.0.0.0', port=5000)