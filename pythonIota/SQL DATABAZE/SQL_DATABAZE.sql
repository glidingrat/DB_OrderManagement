-- Lukáš Krejčiřík, C4a, Aplikace pro správu objednávek, krejcirik@spsejecna.cz

-- Vytvoření databáze
CREATE DATABASE OrderManagement;
USE OrderManagement;

-- Tabulka zákazníků
CREATE TABLE customers (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,         
    last_name VARCHAR(50) NOT NULL,          
    email VARCHAR(100) UNIQUE NOT NULL,      
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
);

-- Tabulka produktů
CREATE TABLE products (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,              
    description VARCHAR(150),                
    price FLOAT NOT NULL,                    
    Stock INT NOT NULL,
    category ENUM('Electronics', 'Clothing', 'Books', 'Other') NOT NULL 
);

-- Tabulka objednávek
CREATE TABLE orders (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,                
    employee_id INT,                         
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
    total_price FLOAT NOT NULL,              
    is_processed BOOL DEFAULT FALSE,        
    FOREIGN KEY (customer_id) REFERENCES customers(ID),
    FOREIGN KEY (employee_id) REFERENCES employees(ID) ON DELETE SET NULL
);

-- Tabulka položek objednávky (M:N vztah mezi produkty a objednávkami)
CREATE TABLE order_items (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,                   
    product_id INT NOT NULL,                 
    quantity INT NOT NULL,                   
    price_per_unit FLOAT NOT NULL,           
    total_price FLOAT NOT NULL,              
    FOREIGN KEY (order_id) REFERENCES orders(ID) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(ID)
);

-- Tabulka zaměstnanců
CREATE TABLE employees (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,         
    last_name VARCHAR(50) NOT NULL,     
    email VARCHAR(100) UNIQUE NOT NULL,
    position ENUM('Manager', 'Storekeeper', 'Support') NOT NULL 
);

-- Pohledy
CREATE VIEW customer_summary AS
SELECT 
    c.ID AS customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email AS customer_email,
    COUNT(o.ID) AS total_orders,
    COALESCE(SUM(o.total_price), 0) AS total_spent
FROM 
    customers c
LEFT JOIN 
    orders o ON c.ID = o.customer_id
GROUP BY 
    c.ID, c.first_name, c.last_name, c.email;

CREATE VIEW order_summary AS
SELECT 
    o.ID AS order_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email AS customer_email,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    e.email AS employee_email,
    o.order_date,
    o.total_price,
    CASE 
        WHEN o.is_processed THEN 'Processed'
        ELSE 'Pending'
    END AS order_status
FROM 
    orders o
LEFT JOIN 
    customers c ON o.customer_id = c.ID
LEFT JOIN 
    employees e ON o.employee_id = e.ID;

-- Testovací data:
INSERT INTO employees (first_name, last_name, email, position) VALUES
('Lukáš', 'Krejčiřík',"lukas.krejcirik@example.com", 'Manager'),
('Bob', 'Smith',"bob.smith@example.com", 'Storekeeper'),
('Charlie', 'Brown',"charlie.brown@example.com", 'Support');

INSERT INTO Customers (first_name, last_name, email) VALUES
('Billy', 'Bobbinz', 'billy.bobbinz@example.com');

INSERT INTO Products (Name, Description, Price, Stock, Category) VALUES
('Notebook', 'Výkonný notebook', 15000.00, 10, 'Electronics'),
('Tričko', 'Bílé tričko velikosti L', 250.00, 50, 'Clothing'),
('Kniha', 'Dobrodružný román', 300.00, 20, 'Books');



