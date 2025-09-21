from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Find the repo root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data_cleaned.csv")

# Load cleaned data
df = pd.read_csv(DATA_PATH)

# Root endpoint (health check)-
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Arys Garage Sales Dashboard API is running..."})

# 1. KPI endpoint
@app.route('/kpis', methods=['GET'])
def get_kpis():
    total_sales = round(df['SALES'].sum(), 2)
    total_orders = df['ORDERNUMBER'].nunique()
    avg_order_value = round(total_sales / total_orders, 2)
    return jsonify({
        "total_sales": total_sales,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value
    })

# 2. Sales over time
@app.route('/sales-over-time', methods=['GET'])
def sales_over_time():
    granularity = request.args.get('granularity', 'year').lower()

    if granularity == 'year':
        grouped = df.groupby('YEAR')['SALES'].sum().reset_index()
        grouped = grouped.sort_values('YEAR')
    elif granularity == 'quarter':
        grouped = df.groupby('QUARTER')['SALES'].sum().reset_index()
        grouped = grouped.sort_values('QUARTER')
    elif granularity == 'month':
        grouped = df.groupby('MONTH')['SALES'].sum().reset_index()
        grouped = grouped.sort_values('MONTH')
    else:
        return jsonify({"error": "Invalid granularity"}), 400

    grouped['SALES'] = grouped['SALES'].round(2)
    return jsonify(grouped.to_dict(orient="records"))

# 3. Sales by category (PRODUCTLINE)
@app.route('/sales-by-category', methods=['GET'])
def sales_by_category():
    grouped = df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
    grouped['SALES'] = grouped['SALES'].round(2)
    return jsonify(grouped.to_dict(orient="records"))

# 4. Sales by country
@app.route('/sales-by-country', methods=['GET'])
def sales_by_country():
    grouped = df.groupby('COUNTRY')['SALES'].sum().reset_index()
    grouped['SALES'] = grouped['SALES'].round(2)
    return jsonify(grouped.to_dict(orient="records"))

# 5. Top customers
@app.route('/top-customers', methods=['GET'])
def top_customers():
    n = int(request.args.get('n', 5))
    grouped = df.groupby('CUSTOMERNAME')['SALES'].sum().reset_index()
    top_n = grouped.sort_values(by='SALES', ascending=False).head(n)
    top_n['SALES'] = top_n['SALES'].round(2)     
    return jsonify(top_n.to_dict(orient="records"))

# 6. Order Status Distribution
@app.route('/order-status', methods=['GET'])
def order_status():
    grouped = df['STATUS'].value_counts().reset_index()
    grouped.columns = ['STATUS', 'COUNT']
    return jsonify(grouped.to_dict(orient="records"))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
