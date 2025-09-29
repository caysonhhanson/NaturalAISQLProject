-- Coffee Shop Database Schema

-- Customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    loyalty_points INTEGER DEFAULT 0,
    join_date DATE DEFAULT CURRENT_DATE
);

-- Products table (coffee, pastries, merchandise)
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT CHECK(category IN ('coffee', 'tea', 'pastry', 'merchandise')),
    price DECIMAL(5,2) NOT NULL,
    cost DECIMAL(5,2) NOT NULL,
    in_stock BOOLEAN DEFAULT 1
);

-- Employees table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT CHECK(position IN ('barista', 'manager', 'cashier')),
    hourly_rate DECIMAL(5,2) NOT NULL,
    hire_date DATE NOT NULL
);

-- Orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    employee_id INTEGER NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(7,2) NOT NULL,
    payment_method TEXT CHECK(payment_method IN ('cash', 'card', 'mobile')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Order Items table (many-to-many between orders and products)
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    price_at_purchase DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Shifts table
CREATE TABLE shifts (
    shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    shift_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Inventory Restocks table
CREATE TABLE inventory_restocks (
    restock_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    restock_date DATE DEFAULT CURRENT_DATE,
    supplier TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
