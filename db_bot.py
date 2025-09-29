import sqlite3
import os
from openai import OpenAI
import json
from datetime import datetime, timedelta
import random

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Database configuration
DB_NAME = "coffee_shop.db"

def init_database():
    """Create database and populate with sample data"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create tables (schema from artifact)
    schema_sql = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        loyalty_points INTEGER DEFAULT 0,
        join_date DATE DEFAULT CURRENT_DATE
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT CHECK(category IN ('coffee', 'tea', 'pastry', 'merchandise')),
        price DECIMAL(5,2) NOT NULL,
        cost DECIMAL(5,2) NOT NULL,
        in_stock BOOLEAN DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT CHECK(position IN ('barista', 'manager', 'cashier')),
        hourly_rate DECIMAL(5,2) NOT NULL,
        hire_date DATE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        employee_id INTEGER NOT NULL,
        order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_amount DECIMAL(7,2) NOT NULL,
        payment_method TEXT CHECK(payment_method IN ('cash', 'card', 'mobile')),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    );

    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        price_at_purchase DECIMAL(5,2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

    CREATE TABLE IF NOT EXISTS shifts (
        shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        shift_date DATE NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    );

    CREATE TABLE IF NOT EXISTS inventory_restocks (
        restock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        restock_date DATE DEFAULT CURRENT_DATE,
        supplier TEXT,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """
    
    for statement in schema_sql.split(';'):
        if statement.strip():
            cursor.execute(statement)
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        populate_sample_data(cursor)
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_NAME}")

def populate_sample_data(cursor):
    """Insert sample data"""
    # Customers
    customers = [
        ('Alice Johnson', 'alice@email.com', '555-0101', 150, '2024-01-15'),
        ('Bob Smith', 'bob@email.com', '555-0102', 89, '2024-02-20'),
        ('Carol Davis', 'carol@email.com', '555-0103', 200, '2023-12-05'),
        ('David Wilson', 'david@email.com', '555-0104', 45, '2024-08-10'),
        ('Emma Brown', 'emma@email.com', '555-0105', 120, '2024-03-22'),
    ]
    cursor.executemany(
        "INSERT INTO customers (name, email, phone, loyalty_points, join_date) VALUES (?, ?, ?, ?, ?)",
        customers
    )
    
    # Products
    products = [
        ('Espresso', 'coffee', 3.50, 0.80, 1),
        ('Latte', 'coffee', 4.50, 1.20, 1),
        ('Cappuccino', 'coffee', 4.25, 1.10, 1),
        ('Americano', 'coffee', 3.25, 0.75, 1),
        ('Cold Brew', 'coffee', 4.75, 1.30, 1),
        ('Green Tea', 'tea', 3.00, 0.50, 1),
        ('Chai Latte', 'tea', 4.00, 1.00, 1),
        ('Croissant', 'pastry', 3.50, 1.20, 1),
        ('Blueberry Muffin', 'pastry', 3.75, 1.30, 1),
        ('Chocolate Chip Cookie', 'pastry', 2.50, 0.80, 1),
        ('Coffee Mug', 'merchandise', 12.99, 5.00, 1),
        ('Travel Tumbler', 'merchandise', 18.99, 7.50, 1),
    ]
    cursor.executemany(
        "INSERT INTO products (name, category, price, cost, in_stock) VALUES (?, ?, ?, ?, ?)",
        products
    )
    
    # Employees
    employees = [
        ('Sarah Martinez', 'manager', 22.50, '2023-06-01'),
        ('John Kim', 'barista', 16.00, '2023-09-15'),
        ('Lisa Chen', 'barista', 16.50, '2024-01-10'),
        ('Mike Thompson', 'cashier', 15.50, '2024-03-20'),
    ]
    cursor.executemany(
        "INSERT INTO employees (name, position, hourly_rate, hire_date) VALUES (?, ?, ?, ?)",
        employees
    )
    
    # Orders (last 30 days)
    base_date = datetime.now() - timedelta(days=30)
    order_data = []
    order_items_data = []
    order_id = 1
    
    for i in range(100):
        days_offset = random.randint(0, 30)
        hours_offset = random.randint(6, 20)
        order_date = base_date + timedelta(days=days_offset, hours=hours_offset)
        customer_id = random.choice([1, 2, 3, 4, 5, None])  # Some orders without loyalty
        employee_id = random.randint(1, 4)
        payment = random.choice(['cash', 'card', 'mobile'])
        
        # Generate 1-3 items per order
        num_items = random.randint(1, 3)
        total = 0
        for _ in range(num_items):
            product_id = random.randint(1, 12)
            quantity = random.randint(1, 2)
            price = products[product_id-1][2]  # Get price from products list
            total += price * quantity
            order_items_data.append((order_id, product_id, quantity, price))
        
        order_data.append((customer_id, employee_id, order_date.strftime('%Y-%m-%d %H:%M:%S'), total, payment))
        order_id += 1
    
    cursor.executemany(
        "INSERT INTO orders (customer_id, employee_id, order_date, total_amount, payment_method) VALUES (?, ?, ?, ?, ?)",
        order_data
    )
    
    cursor.executemany(
        "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (?, ?, ?, ?)",
        order_items_data
    )
    
    # Shifts (last 7 days)
    shift_data = []
    for day_offset in range(7):
        shift_date = (datetime.now() - timedelta(days=day_offset)).strftime('%Y-%m-%d')
        for emp_id in [1, 2, 3, 4]:
            if emp_id == 1:  # Manager works 9-5
                shift_data.append((emp_id, shift_date, '09:00', '17:00'))
            else:  # Baristas/cashiers work various shifts
                if random.random() > 0.3:  # 70% chance of working
                    shift_type = random.choice(['morning', 'afternoon'])
                    if shift_type == 'morning':
                        shift_data.append((emp_id, shift_date, '06:00', '14:00'))
                    else:
                        shift_data.append((emp_id, shift_date, '14:00', '22:00'))
    
    cursor.executemany(
        "INSERT INTO shifts (employee_id, shift_date, start_time, end_time) VALUES (?, ?, ?, ?)",
        shift_data
    )
    
    print("Sample data populated successfully!")

def get_schema_info():
    """Get database schema information for GPT"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = "DATABASE SCHEMA:\n\n"
    
    for table in tables:
        table_name = table[0]
        schema_info += f"Table: {table_name}\n"
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            schema_info += f"  - {col[1]} ({col[2]})"
            if col[5]:  # Primary key
                schema_info += " PRIMARY KEY"
            if col[3]:  # Not null
                schema_info += " NOT NULL"
            schema_info += "\n"
        schema_info += "\n"
    
    conn.close()
    return schema_info

def generate_sql_query(question, strategy="zero-shot"):
    """
    Generate SQL query from natural language using different prompting strategies
    
    Strategies:
    - zero-shot: Just schema and question
    - few-shot: Include example queries
    - chain-of-thought: Ask GPT to explain reasoning
    """
    schema = get_schema_info()
    
    if strategy == "zero-shot":
        system_prompt = f"""You are a SQL expert. Given a database schema and a question, generate a valid SQLite query.
Only respond with the SQL query, nothing else.

{schema}"""
        user_prompt = f"Question: {question}\n\nSQL Query:"
    
    elif strategy == "few-shot":
        system_prompt = f"""You are a SQL expert. Given a database schema and a question, generate a valid SQLite query.
Only respond with the SQL query, nothing else.

{schema}

EXAMPLES:
Question: How many customers do we have?
SQL: SELECT COUNT(*) as customer_count FROM customers;

Question: What is the most popular product?
SQL: SELECT p.name, COUNT(oi.order_item_id) as times_ordered FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_id ORDER BY times_ordered DESC LIMIT 1;

Question: Who is our top customer by total spending?
SQL: SELECT c.name, SUM(o.total_amount) as total_spent FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id ORDER BY total_spent DESC LIMIT 1;
"""
        user_prompt = f"Question: {question}\n\nSQL Query:"
    
    elif strategy == "chain-of-thought":
        system_prompt = f"""You are a SQL expert. Given a database schema and a question:
1. First, explain which tables and columns are needed
2. Then, generate the SQL query

Format your response as:
REASONING: [your explanation]
SQL: [the query]

{schema}"""
        user_prompt = f"Question: {question}"
    
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    
    result = response.choices[0].message.content.strip()
    
    # Extract SQL from chain-of-thought response
    if strategy == "chain-of-thought":
        if "SQL:" in result:
            sql = result.split("SQL:")[1].strip()
            reasoning = result.split("SQL:")[0].replace("REASONING:", "").strip()
            return sql, reasoning
        else:
            return result, ""
    
    return result, None

def execute_query(sql):
    """Execute SQL query and return results"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        conn.close()
        return results, columns, None
    except Exception as e:
        return None, None, str(e)

def generate_natural_language_response(question, sql, results, columns):
    """Convert SQL results back to natural language"""
    if not results:
        return "No results found for your query."
    
    # Format results as text
    results_text = f"Query returned {len(results)} row(s):\n"
    results_text += f"Columns: {', '.join(columns)}\n"
    for row in results[:10]:  # Limit to first 10 rows
        results_text += f"{row}\n"
    
    if len(results) > 10:
        results_text += f"... and {len(results) - 10} more rows"
    
    prompt = f"""Given this question and SQL query results, provide a natural, conversational answer.

Question: {question}

SQL Query: {sql}

{results_text}

Provide a clear, concise answer in natural language:"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that explains database query results in plain English."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

def ask_question(question, strategy="zero-shot", verbose=False):
    """Main function to process natural language question"""
    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")
    print(f"STRATEGY: {strategy}")
    print(f"{'='*60}\n")
    
    # Step 1: Generate SQL
    if verbose:
        print("Step 1: Generating SQL query...")
    
    sql_result = generate_sql_query(question, strategy)
    if isinstance(sql_result, tuple):
        sql, reasoning = sql_result
        if reasoning and verbose:
            print(f"REASONING: {reasoning}\n")
    else:
        sql = sql_result
    
    print(f"GENERATED SQL:\n{sql}\n")
    
    # Step 2: Execute query
    if verbose:
        print("Step 2: Executing query...")
    
    results, columns, error = execute_query(sql)
    
    if error:
        print(f"❌ ERROR: {error}\n")
        return {
            "question": question,
            "strategy": strategy,
            "sql": sql,
            "error": error,
            "success": False
        }
    
    if verbose:
        print(f"Retrieved {len(results)} row(s)\n")
    
    # Step 3: Generate natural language response
    if verbose:
        print("Step 3: Generating natural language response...\n")
    
    nl_response = generate_natural_language_response(question, sql, results, columns)
    
    print(f"RESPONSE:\n{nl_response}\n")
    
    return {
        "question": question,
        "strategy": strategy,
        "sql": sql,
        "results": results,
        "columns": columns,
        "response": nl_response,
        "success": True
    }

def run_examples():
    """Run example queries with different strategies"""
    examples = [
        "How many total customers do we have?",
        "What is the most popular product?",
        "What was our total revenue yesterday?",
        "Which employee has processed the most orders?",
        "What is the average order value?",
        "Show me all products that are pastries",
        "Who is our best customer by loyalty points?",
        "How many lattes were sold in the last week?",
    ]
    
    print("\n" + "="*60)
    print("RUNNING EXAMPLE QUERIES")
    print("="*60)
    
    results = []
    
    # Try different strategies on first few questions
    for i, question in enumerate(examples[:3]):
        strategy = ["zero-shot", "few-shot", "chain-of-thought"][i % 3]
        result = ask_question(question, strategy=strategy, verbose=True)
        results.append(result)
    
    # Rest with few-shot (typically best balance)
    for question in examples[3:]:
        result = ask_question(question, strategy="few-shot", verbose=False)
        results.append(result)
    
    return results

def interactive_mode():
    """Interactive mode for asking questions"""
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("Type your questions (or 'quit' to exit)")
    print("="*60 + "\n")
    
    while True:
        question = input("Your question: ").strip()
        if question.lower() in ['quit', 'exit', 'q']:
            break
        if not question:
            continue
        
        ask_question(question, strategy="few-shot", verbose=True)

if __name__ == "__main__":
    # Initialize database
    init_database()
    
    # Run example queries
    run_examples()
    
    # Start interactive mode
    # Uncomment the line below to enable interactive questioning
    # interactive_mode()
