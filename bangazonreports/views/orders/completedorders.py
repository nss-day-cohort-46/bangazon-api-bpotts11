import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection


def completedorder_list(request):
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
                WHERE o.payment_type_id IS NOT NULL
                GROUP BY o.id
            """)

            dataset = db_cursor.fetchall()

            completed_order_list = []

            for row in dataset:

                complete_order = {}
                complete_order["id"] = row["order_id"]
                complete_order["customer_name"] = row["customer_name"]
                complete_order["total"] = row["total"]

        completed_order_list.append(complete_order)

        template = 'orders/list_of_completed_orders.html'
        context = {
            'completedorder_list': completed_order_list
        }

        return render(request, template, context)
