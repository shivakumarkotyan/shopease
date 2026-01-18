CREATE DATABASE IF NOT EXISTS shopease;
USE shopease;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address TEXT,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image_url VARCHAR(255)
);

-- Products table (Updated with Indian prices)
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL,
    category_id INT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Cart table
CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered') DEFAULT 'pending',
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order items table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert sample data with Indian prices
INSERT INTO categories (name, description) VALUES 
('Electronics', 'Latest electronic gadgets and devices'),
('Clothing', 'Fashionable clothing for all'),
('Books', 'Books for all ages and interests'),
('Home & Garden', 'Items for your home and garden');

-- Products with Indian Rupee prices
INSERT INTO products (name, description, price, stock_quantity, category_id, image_url) VALUES 
('Smartphone X', 'Latest smartphone with advanced features', 69999.99, 50, 1, '/static/images/smartphone.jpg'),
('Laptop Pro', 'High-performance laptop for professionals', 129999.99, 30, 1, '/static/images/laptop.jpg'),
('Wireless Headphones', 'Noise-cancelling wireless headphones', 19999.99, 100, 1, '/static/images/headphones.jpg'),
('Casual T-Shirt', 'Comfortable cotton t-shirt', 1999.99, 200, 2, '/static/images/tshirt.jpg'),
('Jeans', 'Classic blue jeans', 3499.99, 150, 2, '/static/images/jeans.jpg'),
('Python Programming Book', 'Learn Python programming', 899.99, 80, 3, '/static/images/book.jpg'),
('Garden Tools Set', 'Complete gardening tool set', 4999.99, 40, 4, '/static/images/gardentools.jpg'),
('Smart Watch', 'Feature-rich smartwatch', 24999.99, 60, 1, '/static/images/smartwatch.jpg');