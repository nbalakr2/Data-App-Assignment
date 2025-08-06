import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")

# ✅ Read and clean CSV
df = pd.read_csv("Superstore_Sales_utf8.csv", header=1, parse_dates=True)
df.columns = df.columns.str.strip().str.replace(" ", "_")  # Ensures consistent column names

st.dataframe(df)

# ✅ Category and Sub-Category Dropdowns
category_list = df['Category'].unique()
selected_category = st.selectbox("Select a Category", options=category_list)

filtered_df = df[df['Category'] == selected_category]
sub_category_list = filtered_df['Sub_Category'].unique()

selected_subcategories = st.multiselect("Select Sub-Categories", options=sub_category_list)

# ✅ Filtered Line Chart of Sales Over Time
if selected_subcategories:
    sub_df = filtered_df[filtered_df['Sub_Category'].isin(selected_subcategories)].copy()

    # Ensure Order_Date is datetime
    sub_df['Order_Date'] = pd.to_datetime(sub_df['Order_Date'])

    # Group by month and sum sales
    sales_by_month_filtered = (
        sub_df
        .groupby(pd.Grouper(key='Order_Date', freq='M'))['Sales']
        .sum()
    )

    st.write("### Monthly Sales for Selected Sub-Categories")
    st.line_chart(sales_by_month_filtered)

    # Optional debug
    # st.write("DEBUG: Filtered Data", sub_df)
    # st.write("DEBUG: Monthly Sales", sales_by_month_filtered)

else:
    st.info("Please select at least one sub-category to see the line chart.")

# ✅ Optional: Initial Visuals (can leave or remove for final version)
st.write("### Full Dataset Bar Charts")

# Bar chart by Category (non-aggregated)
st.bar_chart(df, x="Category", y="Sales")

# Bar chart with aggregation
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregated monthly sales for whole dataset (not filtered)
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
sales_by_month_all = df.groupby(pd.Grouper(key='Order_Date', freq='M'))['Sales'].sum()
st.line_chart(sales_by_month_all)

# ✅ Assignment instructions at the bottom
st.write("## Your additions")
st.write("### (1) add a drop down for Category")
st.write("### (2) add a multi-select for Sub_Category in the selected Category")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics: total sales, total profit, and overall profit margin (%)")
st.write("### (5) use delta in profit margin to compare to average across all categories")
