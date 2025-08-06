import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", header=1, parse_dates=True)
df.columns = df.columns.str.strip()
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
#st.line_chart(sales_by_month, y="Sales")

df.reset_index(inplace=True)

category_list = df['Category'].unique()
selected_category = st.selectbox("Select a Category", options=category_list)

filtered_df = df[df['Category'] == selected_category]
st.write("Filtered rows:", filtered_df.shape[0])
st.write("Filtered sub-categories:", filtered_df['Sub_Category'].unique())
sub_category_list = filtered_df['Sub_Category'].unique()
st.write("Available columns:", filtered_df.columns)
selected_subcategories = st.multiselect("Select Sub-Categories", options=sub_category_list)

if selected_subcategories:
    sub_df = filtered_df[filtered_df['Sub-Category'].isin(selected_subcategories)].copy()

    sub_df['Order_Date'] = pd.to_datetime(sub_df['Order_Date'])
    sales_by_month_filtered = (
        sub_df
        .groupby(pd.Grouper(key='Order_Date', freq='M'))['Sales']
        .sum()
    )

    st.write("### Monthly Sales for Selected Sub-Categories")
    st.line_chart(sales_by_month_filtered)
else:
    st.info("Please select at least one sub-category to see the line chart.")


st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
