INSERT INTO customers (name, email, phone, loyalty_points, join_date) VALUES
('Alice Johnson', 'alice@email.com', '555-0101', 150, '2024-01-15'),
('Bob Smith', 'bob@email.com', '555-0102', 89, '2024-02-20'),
('Carol Davis', 'carol@email.com', '555-0103', 200, '2023-12-05'),
('David Wilson', 'david@email.com', '555-0104', 45, '2024-08-10'),
('Emma Brown', 'emma@email.com', '555-0105', 120, '2024-03-22'),
('Frank Miller', 'frank@email.com', '555-0106', 75, '2024-04-18'),
('Grace Lee', 'grace@email.com', '555-0107', 180, '2023-11-30'),
('Henry Taylor', 'henry@email.com', '555-0108', 95, '2024-05-22'),
('Isabel Garcia', 'isabel@email.com', '555-0109', 160, '2024-01-08'),
('Jack Anderson', 'jack@email.com', '555-0110', 110, '2024-03-15');

INSERT INTO products (name, category, price, cost, in_stock) VALUES
('Espresso', 'coffee', 3.50, 0.80, 1),
('Latte', 'coffee', 4.50, 1.20, 1),
('Cappuccino', 'coffee', 4.25, 1.10, 1),
('Americano', 'coffee', 3.25, 0.75, 1),
('Cold Brew', 'coffee', 4.75, 1.30, 1),
('Mocha', 'coffee', 5.25, 1.50, 1),
('Macchiato', 'coffee', 4.75, 1.25, 1),
('Frappuccino', 'coffee', 5.75, 1.80, 1),

('Green Tea', 'tea', 3.00, 0.50, 1),
('Chai Latte', 'tea', 4.00, 1.00, 1),
('Earl Grey', 'tea', 3.25, 0.60, 1),
('Herbal Tea', 'tea', 3.50, 0.70, 1),
('Matcha Latte', 'tea', 4.75, 1.40, 1),

('Croissant', 'pastry', 3.50, 1.20, 1),
('Blueberry Muffin', 'pastry', 3.75, 1.30, 1),
('Chocolate Chip Cookie', 'pastry', 2.50, 0.80, 1),
('Danish', 'pastry', 4.25, 1.50, 1),
('Scone', 'pastry', 3.25, 1.10, 1),
('Bagel', 'pastry', 2.75, 0.90, 1),
('Cinnamon Roll', 'pastry', 4.50, 1.60, 1),

('Coffee Mug', 'merchandise', 12.99, 5.00, 1),
('Travel Tumbler', 'merchandise', 18.99, 7.50, 1),
('Coffee Beans (1lb)', 'merchandise', 15.99, 8.00, 1),
('T-Shirt', 'merchandise', 22.99, 10.00, 1),
('Tote Bag', 'merchandise', 14.99, 6.00, 1);


INSERT INTO employees (name, position, hourly_rate, hire_date) VALUES
('Sarah Martinez', 'manager', 22.50, '2023-06-01'),
('John Kim', 'barista', 16.00, '2023-09-15'),
('Lisa Chen', 'barista', 16.50, '2024-01-10'),
('Mike Thompson', 'cashier', 15.50, '2024-03-20'),
('Anna Rodriguez', 'barista', 16.25, '2024-02-14'),
('Tom Wilson', 'cashier', 15.75, '2024-04-05');


INSERT INTO orders (customer_id, employee_id, order_date, total_amount, payment_method) VALUES
(1, 2, '2024-09-28 08:30:00', 7.75, 'card'),
(2, 3, '2024-09-28 09:15:00', 12.50, 'mobile'),
(3, 4, '2024-09-28 10:00:00', 6.25, 'cash'),
(1, 2, '2024-09-27 08:45:00', 9.25, 'card'),
(4, 3, '2024-09-27 11:30:00', 15.75, 'card'),
(5, 2, '2024-09-26 07:20:00', 8.50, 'mobile'),
(2, 4, '2024-09-26 14:45:00', 11.25, 'cash'),
(6, 3, '2024-09-25 16:30:00', 13.50, 'card'),
(1, 2, '2024-09-25 08:15:00', 4.50, 'mobile'),
(7, 4, '2024-09-24 12:00:00', 18.75, 'card');

INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES
-- Order 1: Latte + Cookie
(1, 2, 1, 4.50),
(1, 16, 1, 2.50),
-- Order 2: Cappuccino + Croissant + Coffee Mug
(2, 3, 1, 4.25),
(2, 14, 1, 3.50),
(2, 21, 1, 12.99),
-- Order 3: Americano + Muffin
(3, 4, 1, 3.25),
(3, 15, 1, 3.75),
-- Order 4: Mocha + Danish
(4, 6, 1, 5.25),
(4, 17, 1, 4.25),
-- Order 5: Cold Brew + Scone + Bagel
(5, 5, 1, 4.75),
(5, 18, 1, 3.25),
(5, 19, 1, 2.75),
-- Order 6: Chai Latte + Cinnamon Roll
(6, 10, 1, 4.00),
(6, 20, 1, 4.50),
-- Order 7: Frappuccino + Cookie + Muffin
(7, 8, 1, 5.75),
(7, 16, 1, 2.50),
(7, 15, 1, 3.75),
-- Order 8: Matcha Latte + Travel Tumbler
(8, 13, 1, 4.75),
(8, 22, 1, 18.99),
-- Order 9: Latte only
(9, 2, 1, 4.50),
-- Order 10: Espresso + Croissant + Coffee Beans
(10, 1, 2, 3.50),
(10, 14, 1, 3.50),
(10, 23, 1, 15.99);


INSERT INTO shifts (employee_id, shift_date, start_time, end_time) VALUES

(1, '2024-09-29', '09:00', '17:00'),
(1, '2024-09-28', '09:00', '17:00'),
(1, '2024-09-27', '09:00', '17:00'),
(1, '2024-09-26', '09:00', '17:00'),
(1, '2024-09-25', '09:00', '17:00'),
(1, '2024-09-24', '09:00', '17:00'),
(1, '2024-09-23', '09:00', '17:00'),


(2, '2024-09-29', '06:00', '14:00'),
(3, '2024-09-29', '14:00', '22:00'),
(4, '2024-09-29', '08:00', '16:00'),
(5, '2024-09-29', '12:00', '20:00'),

(2, '2024-09-28', '14:00', '22:00'),
(3, '2024-09-28', '06:00', '14:00'),
(4, '2024-09-28', '10:00', '18:00'),
(6, '2024-09-28', '16:00', '22:00'),

(2, '2024-09-27', '06:00', '14:00'),
(3, '2024-09-27', '14:00', '22:00'),
(5, '2024-09-27', '08:00', '16:00'),
(6, '2024-09-27', '12:00', '20:00'),

(3, '2024-09-26', '06:00', '14:00'),
(4, '2024-09-26', '14:00', '22:00'),
(5, '2024-09-26', '10:00', '18:00'),

(2, '2024-09-25', '14:00', '22:00'),
(3, '2024-09-25', '06:00', '14:00'),
(4, '2024-09-25', '16:00', '22:00'),
(6, '2024-09-25', '08:00', '16:00'),

(2, '2024-09-24', '06:00', '14:00'),
(4, '2024-09-24', '14:00', '22:00'),
(5, '2024-09-24', '12:00', '20:00'),

(3, '2024-09-23', '14:00', '22:00'),
(5, '2024-09-23', '06:00', '14:00'),
(6, '2024-09-23', '10:00', '18:00');


INSERT INTO inventory_restocks (product_id, quantity, restock_date, supplier) VALUES
(1, 50, '2024-09-25', 'Premium Coffee Suppliers'),
(2, 40, '2024-09-25', 'Premium Coffee Suppliers'),
(3, 35, '2024-09-25', 'Premium Coffee Suppliers'),
(4, 45, '2024-09-25', 'Premium Coffee Suppliers'),
(5, 30, '2024-09-24', 'Cold Brew Co.'),
(9, 25, '2024-09-26', 'Tea Masters Inc.'),
(10, 20, '2024-09-26', 'Tea Masters Inc.'),
(14, 30, '2024-09-27', 'Fresh Bakery Supply'),
(15, 24, '2024-09-27', 'Fresh Bakery Supply'),
(16, 48, '2024-09-27', 'Fresh Bakery Supply'),
(21, 15, '2024-09-20', 'Coffee Merchandise Co.'),
(22, 12, '2024-09-20', 'Coffee Merchandise Co.'),
(23, 20, '2024-09-22', 'Bean Roasters Ltd.');
