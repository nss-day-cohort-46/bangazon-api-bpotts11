import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def incompleteorder_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT 
                o.id order_id,
                u.first_name ||" "|| u.last_name customer_name,
                SUM(p.price) total
            FROM bangazonapi_order o
                JOIN bangazonapi_customer c ON o.customer_id = c.id
                JOIN bangazonapi_orderproduct op ON o.id = op.order_id
                JOIN bangazonapi_product p ON p.id = op.product_id
                JOIN auth_user u ON u.id = c.user_id
                WHERE o.payment_type_id IS NULL
                GROUP BY o.id
            """)

            dataset = db_cursor.fetchall()

            incomplete_order_list = []

            for row in dataset:

                incomplete_order = {}
                incomplete_order["id"] = row["order_id"]
                incomplete_order["customer_name"] = row["customer_name"]
                incomplete_order["total"] = row["total"]
                incomplete_order_list.append(incomplete_order)

            template = 'orders/list_of_incomplete_orders.html'
            context = {
                'incompleteorder_list': incomplete_order_list
            }

            return render(request, template, context)
