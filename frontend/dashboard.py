import streamlit as st
import requests
import plotly.express as px

# API base URL
API_URL = "https://arys-backend.onrender.com"

st.set_page_config(page_title="Arys Garage Sales Dashboard", layout="wide")
st.title("🚗 Arys Garage Sales Dashboard")

# 1. KPI Cards
st.subheader("📌 Key Performance Indicators")

kpis = requests.get(f"{API_URL}/kpis").json()
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${kpis['total_sales']:,.2f}")
col2.metric("Total Orders", kpis['total_orders'])
col3.metric("Avg Order Value", f"${kpis['avg_order_value']:,.2f}")

# 2. Sales Over Time (Line Chart)
st.subheader("📈 Sales Over Time")

granularity = st.radio("Choose Time Granularity", ["year", "quarter", "month"], horizontal=True)
sales_time = requests.get(f"{API_URL}/sales-over-time?granularity={granularity}").json()
fig_time = px.line(sales_time, x=granularity.upper(), y="SALES", markers=True, title=f"Sales by {granularity.capitalize()}")
st.plotly_chart(fig_time, use_container_width=True)

# 3. Product Line Distribution
st.subheader("📊 Sales by Product Line")

sales_category = requests.get(f"{API_URL}/sales-by-category").json()
fig_category = px.pie(sales_category, names="PRODUCTLINE", values="SALES", title="Sales Distribution by Product Line")
st.plotly_chart(fig_category, use_container_width=True)

# 4. Sales by Country (Bar Chart)
st.subheader("🌍 Sales by Country")

sales_country = requests.get(f"{API_URL}/sales-by-country").json()
fig_country = px.bar(sales_country, x="COUNTRY", y="SALES", title="Sales by Country", text_auto=True)
st.plotly_chart(fig_country, use_container_width=True)

# 5. Order Status Donut Chart
st.subheader("📦 Order Status Distribution")

order_status = requests.get(f"{API_URL}/order-status").json()
fig_status = px.pie(order_status, names="STATUS", values="COUNT", hole=0.4,
                    title="Order Status Distribution")
st.plotly_chart(fig_status, use_container_width=True)

# 6. Top Customers (Table)
st.subheader("🏆 Top Customers")

top_customers = requests.get(f"{API_URL}/top-customers?n=5").json()
st.table(top_customers)
