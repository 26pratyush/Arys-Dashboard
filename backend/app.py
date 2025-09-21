from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Find the repo root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data_cleaned.csv")

# Load cleaned data
df = pd.read_csv(DATA_PATH)

# Root endpoint (health check)
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Arys Garage Sales Dashboard API running..."})

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
    granularity = request.args.get('granularity', 'year')  # year, quarter, month
    if granularity.upper() not in ['YEAR', 'MONTH', 'QUARTER']:
        return jsonify({"error": "Invalid granularity"}), 400
    
    grouped = df.groupby(granularity.upper())['SALES'].sum().reset_index()
    return jsonify(grouped.to_dict(orient="records"))

# 3. Sales by category (PRODUCTLINE)
@app.route('/sales-by-category', methods=['GET'])
def sales_by_category():
    grouped = df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
    return jsonify(grouped.to_dict(orient="records"))

# 4. Sales by country
@app.route('/sales-by-country', methods=['GET'])
def sales_by_country():
    grouped = df.groupby('COUNTRY')['SALES'].sum().reset_index()
    return jsonify(grouped.to_dict(orient="records"))

# 5. Top customers
@app.route('/top-customers', methods=['GET'])
def top_customers():
    n = int(request.args.get('n', 5))
    grouped = df.groupby('CUSTOMERNAME')['SALES'].sum().reset_index()
    top_n = grouped.sort_values(by='SALES', ascending=False).head(n)
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
