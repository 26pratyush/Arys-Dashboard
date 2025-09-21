import streamlit as st
import requests
import plotly.express as px
import pandas as pd

# API base URL
API_URL = "https://arys-backend.onrender.com"

st.set_page_config(page_title="Arys Garage Sales Dashboard", layout="wide")
st.title("🚗 Arys Garage Sales Dashboard")

# 1. KPI Cards
st.subheader("📌 Key Performance Indicators")

kpis = requests.get(f"{API_URL}/kpis").json()

# Format values
total_sales_m = kpis["total_sales"] / 1_000_000   # convert to millions
avg_order_value = kpis["avg_order_value"]

col1, col2, col3 = st.columns(3)

# Total Sales (in Millions, 2 decimals)
col1.metric("Total Sales", f"${total_sales_m:,.2f}M")

# Total Orders (integer with commas)
col2.metric("Total Orders", f"{kpis['total_orders']:,}")

# Avg Order Value (currency with commas, 2 decimals)
col3.metric("Avg Order Value", f"${avg_order_value:,.2f}")

# 2. Sales Over Time (Line Chart)
st.subheader("📈 Sales Over Time")

granularity = st.radio("Choose Time Granularity", ["Year", "Quarter", "Month"], horizontal=True)
sales_time = requests.get(f"{API_URL}/sales-over-time?granularity={granularity}").json()

df_time = pd.DataFrame(sales_time)
x_col = granularity.upper()

if granularity == "Year":
    df_time["SALES_SCALED"] = df_time["SALES"] / 1_000_000
    y_label = "Sales (M)"
    hover_unit = "M"
elif granularity == "Quarter":
    df_time["SALES_SCALED"] = df_time["SALES"] / 1_000_000
    y_label = "Sales (M)"
    hover_unit = "M"
else:  # Month
    df_time["SALES_SCALED"] = df_time["SALES"] / 1_000
    y_label = "Sales (K)"
    hover_unit = "K"

fig_time = px.line(
    df_time,
    x=x_col, y="SALES_SCALED", markers=True,
    title=f"Sales by {granularity.capitalize()}",
    labels={x_col: granularity, "SALES_SCALED": y_label}
)

fig_time.update_traces(
    hovertemplate=f"{granularity}=%{{x}}<br>Sales=%{{y:.2f}}{hover_unit}<extra></extra>"
)
fig_time.update_yaxes(tickformat=".2f", title=y_label)

st.plotly_chart(fig_time, use_container_width=True)

# 3. Product Line Distribution
st.subheader("🎯Sales Distribution by Product Line")

sales_category = requests.get(f"{API_URL}/sales-by-category").json()
df_cat = pd.DataFrame(sales_category)

# Scale to millions
df_cat["SALES_M"] = df_cat["SALES"] / 1_000_000
fig_category = px.pie(df_cat, names="PRODUCTLINE", values="SALES_M", title="Hover to view exact sales values (M)")

# Format hover to 2 decimals with M suffix
fig_category.update_traces(
    hovertemplate="Product Line=%{label}<br>Sales=%{value:.2f}M<extra></extra>"
)

st.plotly_chart(fig_category, use_container_width=True)

# 4. Sales by Country (Bar Chart)
st.subheader("🌍 Sales by Country")

sales_country = requests.get(f"{API_URL}/sales-by-country").json()
df_country = pd.DataFrame(sales_country)

# Scale to millions
df_country["SALES_M"] = df_country["SALES"] / 1_000_000

fig_country = px.bar(
    df_country,
    x="COUNTRY",
    y="SALES_M",
    title="Sales by Country",
    labels={"SALES_M": "Sales (M)"},
    text_auto=".2f"   # show 2 decimals on bars
)

fig_country.update_traces(
    hovertemplate="Country=%{x}<br>Sales=%{y:.2f}M<extra></extra>"
)

# Format y-axis
fig_country.update_yaxes(tickformat=".2f", title="Sales (M)")

st.plotly_chart(fig_country, use_container_width=True)

# 5. Order Status Donut Chart
st.subheader("🍩 Order Status Distribution")

order_status = requests.get(f"{API_URL}/order-status").json()
fig_status = px.pie(order_status, names="STATUS", values="COUNT", hole=0.4,
                    title="Order Status Distribution")
st.plotly_chart(fig_status, use_container_width=True)

# 6. Top Customers (Table)
st.subheader("🏆 Top 5 Customers")

top_customers = requests.get(f"{API_URL}/top-customers?n=5").json()
df_top = pd.DataFrame(top_customers)

# Scale to millions and force 2 decimal places as string
df_top["SALES"] = (df_top["SALES"] / 1_000_000).map(lambda x: f"{x:.2f}")

# Add Rank column manually
df_top.insert(0, "Rank", range(1, len(df_top) + 1))

# Rename column
df_top.rename(columns={"SALES": "Sales (M)"}, inplace=True)

# Display table without Streamlit index
st.table(df_top.reset_index(drop=True))


