import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
df.columns = df.columns.str.strip()  # Clean any whitespace

st.dataframe(df)

# Original bar chart: raw data
st.bar_chart(df, x="Category", y="Sales")

# Aggregated by Category (solid bars)
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregated by Month (original chart)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
#df.set_index("Order_Date", inplace=True)
sales_by_month = (
    df.groupby(pd.Grouper(key="Order_Date", freq='M'))["Sales"]
    .sum()
)

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

# Reset index for further filtering
df.reset_index(inplace=True)

# ✅ (1) Dropdown for Category
category_list = df["Category"].unique()
selected_category = st.selectbox("Select a Category", category_list)

# ✅ (2) Multiselect for Sub_Category in selected Category
filtered_df = df[df["Category"] == selected_category]
sub_category_list = filtered_df["Sub_Category"].unique()
selected_subcategories = st.multiselect("Select Sub-Categories", options=sub_category_list)

# ✅ (3) Line chart of sales for selected items
# Show filtered sales by month only when subcategories are selected
if selected_subcategories:
    sub_df = filtered_df[filtered_df["Sub-Category"].isin(selected_subcategories)].copy()

    # Convert Order_Date and group
    sub_df["Order_Date"] = pd.to_datetime(sub_df["Order_Date"])
    sales_by_month_filtered = (
        sub_df
        .groupby(pd.Grouper(key="Order_Date", freq="M"))["Sales"]
        .sum()
    )

    st.write("### Monthly Sales for Selected Sub-Categories")
    st.line_chart(sales_by_month_filtered)
else:
    st.info("Please select at least one sub-category to see the filtered line chart.")


# ✅ Instructions (unchanged)
st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
