from flask import Flask, jsonify, request, url_for
import requests
import json
from config import SHOPIFY_STORE_URL, SHOPIFY_API_VERSION, SHOPIFY_ACCESS_TOKEN

app = Flask(__name__)

# Define the Shopify headers
SHOPIFY_HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}


@app.route('/')
def index():
    # Generate HTML with links to all endpoints
    html = """
    <h1>Welcome to the Shopify Data Handling App!</h1>
    <ul>
        <li><a href="{}">Orders</a></li>
        <li><a href="{}">Order #5676247515386</a></li>
        <li><a href="{}">Mock Shipbob Order</a></li>
    </ul>
    """.format(
        url_for('get_orders'),
        url_for('get_order', order_id=5676247515386),
        url_for('mock_shipbob_order', order_id=5676247515386)
    )
    return html


@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        url = f"https://{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/orders.json?status=any"
        response = requests.get(url, headers=SHOPIFY_HEADERS)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        orders = response.json().get('orders', [])
        order_numbers = [order['id'] for order in orders]
        return jsonify({"number_of_orders": len(orders), "order_numbers": order_numbers})
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"URL: {url}")
        print(f"Response content: {response.content}")
        return jsonify({"error": str(http_err)}), response.status_code
    except Exception as err:
        print(f"An error occurred: {err}")
        return jsonify({"error": str(err)}), 500


@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        url = f"https://{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/orders/{order_id}.json?fields=id,line_items,name,total_price,line_items.inventory_item_id"
        response = requests.get(url, headers=SHOPIFY_HEADERS)
        response.raise_for_status()
        order = response.json().get('order', {})
        if not order:
            return jsonify({"error": "Order not found"}), 404  # Return 404 response if order is not found
        product_names = [item['name'] for item in order.get('line_items', [])]
        return jsonify({"product_names": product_names})
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"URL: {url}")
        print(f"Response content: {response.content}")
        return jsonify({"error": str(http_err)}), response.status_code
    except Exception as err:
        print(f"An error occurred: {err}")
        return jsonify({"error": str(err)}), 500


def get_inventory_status(inventory_item_ids):
    if not inventory_item_ids:
        return {}  # Return an empty dict if no inventory item IDs are provided
    inventory_status = {}
    try:
        url = f"https://{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/inventory_levels.json?inventory_item_ids={','.join(map(str, inventory_item_ids))}"
        response = requests.get(url, headers=SHOPIFY_HEADERS)
        response.raise_for_status()
        inventory_levels = response.json().get('inventory_levels', [])
        for level in inventory_levels:
            inventory_status[level['inventory_item_id']] = level['available']
        return inventory_status
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"URL: {url}")
        print(f"Response content: {response.content}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None


@app.route('/mock-shipbob-order/<int:order_id>', methods=['GET'])
def mock_shipbob_order(order_id):
    try:
        url = f"https://{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/orders/{order_id}.json?fields=id,line_items,shipping_address,created_at,line_items.inventory_item_id"
        response = requests.get(url, headers=SHOPIFY_HEADERS)
        response.raise_for_status()
        order = response.json().get('order', {})

        # Fetch product names
        product_names = [item['name'] for item in order.get('line_items', [])]

        # Mock Shipbob order request
        shipbob_order = {
            "order_id": str(order['id']),
            "order_date": order['created_at'],
            "order_items": [
                {
                    "product_id": item['product_id'],
                    "quantity": item['quantity']
                } for item in order.get('line_items', [])
            ],
            "shipping_address": order['shipping_address']
        }

        # Print Shipbob order request
        print(json.dumps(shipbob_order, indent=4))

        # Fetch inventory status
        inventory_item_ids = [item['inventory_item_id'] for item in order.get('line_items', []) if
                              'inventory_item_id' in item]
        inventory_status = get_inventory_status(inventory_item_ids)
        if inventory_status:
            print("Inventory Status:")
            for item_id, available_quantity in inventory_status.items():
                print(f"Product ID: {item_id}, Available Quantity: {available_quantity}")
        else:
            print("Inventory Status: No inventory status available for the products in this order.")

        return jsonify({"message": "Mock Shipbob order request printed to console", "product_names": product_names})
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"URL: {url}")
        print(f"Response content: {response.content}")
        return jsonify({"error": str(http_err)}), response.status_code
    except Exception as err:
        print(f"An error occurred: {err}")
        return jsonify({"error": str(err)}), 500



if __name__ == '__main__':
    app.run(debug=True)

