import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")

# ✅ Load and clean the data
df = pd.read_csv("Superstore_Sales_utf8.csv", header=1, parse_dates=True)
df.columns = df.columns.str.strip().str.replace(" ", "_")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])  # Ensure datetime

st.dataframe(df)

# ✅ This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# ✅ Aggregated bar chart
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# ✅ Aggregated by time (full dataset)
sales_by_month = df.filter(items=['Sales', 'Order_Date']).groupby(pd.Grouper(key='Order_Date', freq='M')).sum()
st.dataframe(sales_by_month)
# st.line_chart(sales_by_month, y="Sales")  # Commented out to prevent conflict

# ✅ Category Dropdown
category_list = df['Category'].unique()
selected_category = st.selectbox("Select a Category", options=category_list)

# ✅ Sub-Category Multiselect based on selected category
filtered_df = df[df['Category'] == selected_category]
sub_category_list = filtered_df['Sub_Category'].unique()
selected_subcategories = st.multiselect("Select Sub-Categories", options=sub_category_list)

# ✅ Filtered Line Chart of Monthly Sales
if selected_subcategories:
    sub_df = filtered_df[filtered_df['Sub_Category'].isin(selected_subcategories)].copy()

    st.write("DEBUG - Sub DF Shape:", sub_df.shape)
    st.write("DEBUG - First 5 Rows of Sub DF:", sub_df.head())
    st.write("DEBUG - Selected Sub-Categories:", selected_subcategories)


    sales_by_month_filtered = (
        sub_df
        .groupby(pd.Grouper(key='Order_Date', freq='M'))['Sales']
        .sum()
    )

    st.write("### Monthly Sales for Selected Sub-Categories")
    st.line_chart(sales_by_month_filtered)

else:
    st.info("Please select at least one sub-category to see the line chart.")

# ✅ Assignment instructions (unchanged)
st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
