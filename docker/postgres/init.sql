CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    status VARCHAR(30) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers (name, email) VALUES
    ('Acme s.r.o.', 'info@acme.cz'),
    ('Example Corp', 'info@example.com'),
    ('Test Company', 'test@example.com');

INSERT INTO orders (customer_id, status, amount) VALUES
    (1, 'new', 12500.00),
    (1, 'completed', 8400.00),
    (2, 'pending', 15300.00),
    (3, 'cancelled', 4200.00);
