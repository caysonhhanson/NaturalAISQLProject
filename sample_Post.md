Coffee Shop SQL AI Project
My project models data about a coffee shop, including customers, orders, products, inventory restocks, and employees. The goal is to answer business questions such as sales trends, top customers, employee performance, and product popularity.
<img src="coffee_schema.png">
Query I thought it did well on
Question: Who are the top 5 customers by total spending?
GPT SQL Response:
SELECT c.customer_id, c.name, SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 5;
Friendly Response:
Bob Smith – $23.75
Alice Johnson – $21.50
Grace Lee – $18.75
David Wilson – $15.75
Frank Miller – $13.50
ChatGPT successfully generated SQL and returned meaningful, readable results. The friendly summary accurately conveys the top spenders.
Question that it tripped up on
Question: How much did we spend on ingredients last month?
GPT SQL Response:
SELECT SUM(quantity * cost) AS total_spent
FROM inventory_restocks
JOIN products ON inventory_restocks.product_id = products.product_id
WHERE strftime('%Y-%m', restock_date) = strftime('%Y-%m', 'now', '-1 month');
SQL Result: [(None,)]
Friendly Response:
It looks like the database didn’t provide any specific details on last month’s spending for ingredients. You might want to double-check the data entry or try running the query again.
Even though the SQL syntax was mostly correct, the query returned no data because either no inventory restocks occurred last month or data is missing. ChatGPT’s friendly response is generic and doesn’t fully interpret why the result is empty.
Multi-step insight
Question: Which product combinations are most commonly bought together?
GPT SQL Response:
SELECT p1.name AS product1, p2.name AS product2, COUNT(*) AS combo_count
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
JOIN products p1 ON oi1.product_id = p1.product_id
JOIN products p2 ON oi2.product_id = p2.product_id
GROUP BY oi1.product_id, oi2.product_id
ORDER BY combo_count DESC;
SQL Result:
[('Americano', 'Blueberry Muffin', 1), 
 ('Blueberry Muffin', 'Chocolate Chip Cookie', 1), 
 ('Cappuccino', 'Croissant', 1)]
Friendly Response:
Customers frequently pair drinks with pastries! Examples include: Americano with Blueberry Muffin, Cappuccino with Croissant, and Blueberry Muffin with Chocolate Chip Cookie.
Here, ChatGPT produced both correct SQL and an interpretable friendly response. Multi-step analysis like this can help identify upselling opportunities.
Conclusion
ChatGPT is very effective at generating SQL for straightforward queries like top customers, busiest hours, and product popularity.
For queries with missing or incomplete data, the friendly responses can become generic and may not fully explain why results are empty.
Multi-step queries or aggregations over multiple tables work well in SQL, but interpreting results in a business-friendly way can still require human oversight.
Overall, this tool is valuable for quickly prototyping SQL queries for data analysis but should not be relied on alone for final business insights.
