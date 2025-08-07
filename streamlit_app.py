import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

st.bar_chart(df, x="Category", y="Sales")

st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

#1
categories = df["Category"].unique()
selected_category = st.selectbox(
    "Select a Category",
    options=categories
)

#2
filtered_by_category = df[df["Category"] == selected_category]
sub_categories = filtered_by_category["Sub_Category"].unique()
selected_sub_categories = st.multiselect(
    "Select one or more Sub-Categories",
    options=sub_categories,
    default=sub_categories
)

if selected_sub_categories:
    final_filtered_df = filtered_by_category[
        filtered_by_category["Sub_Category"].isin(selected_sub_categories)
    ]
#3
    st.write(f"### Monthly Sales for {', '.join(selected_sub_categories)}")
    sales_for_selection = final_filtered_df.groupby(pd.Grouper(freq='M')).sum()
    st.line_chart(sales_for_selection, y="Sales")
    #4-5
    total_sales = final_filtered_df["Sales"].sum()
    total_profit = final_filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100

    overall_total_sales = df["Sales"].sum()
    overall_total_profit = df["Profit"].sum()
    overall_avg_profit_margin = (overall_total_profit / overall_total_sales) * 100
    
    profit_margin_delta = profit_margin - overall_avg_profit_margin

    st.write("### Metrics for Selection")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    
    with col2:
        st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    
    with col3:
        st.metric(
            label="Overall Profit Margin (%)",
            value=f"{profit_margin:,.2f}%",
            delta=f"{profit_margin_delta:,.2f}%"
        )
else:
    st.info("Please select at least one sub-category to see the chart and metrics.")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
