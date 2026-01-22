import os
import sqlite3


def init_db():
    # Remove existing database to start fresh
    if os.path.exists('shopease.db'):
        os.remove('shopease.db')
        print("Old database removed. Creating new database...")
    
    # ... rest of your database initialization code
    
    # Rest of your existing init_db code continues here...
    conn = sqlite3.connect('shopease.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
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
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
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
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data - UPDATE THIS PART WITH NEW IMAGE PATHS
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        categories = [
            ('Electronics', 'Latest electronic gadgets and devices'),
            ('Clothing', 'Fashionable clothing for all'),
            ('Books', 'Books for all ages and interests'),
            ('Home & Garden', 'Items for your home and garden')
        ]
        cursor.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)
        
        # UPDATED PRODUCTS WITH SPECIFIC IMAGE PATHS
        products = [
            ('Smartphone X', 'Latest smartphone with advanced features', 699.99, 50, 1, '/static/images/smartphone.jpg'),
            ('Laptop Pro', 'High-performance laptop for professionals', 1299.99, 30, 1, '/static/images/laptop.jpg'),
            ('Wireless Headphones', 'Noise-cancelling wireless headphones', 199.99, 100, 1, '/static/images/headphones.jpg'),
            ('Casual T-Shirt', 'Comfortable cotton t-shirt', 29.99, 200, 2, '/static/images/tshirt.jpg'),
            ('Jeans', 'Classic blue jeans', 49.99, 150, 2, '/static/images/jeans.jpg'),
            ('Programming Book', 'Learn Python programming', 49.99, 80, 3, '/static/images/book.jpg'),
            ('Garden Tools Set', 'Complete gardening tool set', 79.99, 40, 4, '/static/images/gardentools.jpg'),
            ('Smart Watch', 'Feature-rich smartwatch', 299.99, 60, 1, '/static/images/smartwatch.jpg')
        ]
        cursor.executemany("INSERT INTO products (name, description, price, stock_quantity, category_id, image_url) VALUES (?, ?, ?, ?, ?, ?)", products)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with new image paths!")