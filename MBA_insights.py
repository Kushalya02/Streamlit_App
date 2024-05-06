import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

#reading csv files
orders=pd.read_csv('GlobalSuperstoreLite.csv')
rules=pd.read_csv('association_rules.csv')

st.title('Key Insights Dashboard')
col1,col2=st.columns((2))
#Adding dashboard filter
st.sidebar.title("Dashboard Filters")



#making tabs
Order_details, association_rules=st.tabs(['Order Details','Market Basket Analysis Association Rules'])
with Order_details:
    st.header("Order Details")
    st.write(orders)
    #date picker
    orders['Order Date']=pd.to_datetime(orders['Order Date'])
    start_date=pd.to_datetime(orders['Order Date']).min()
    end_date=pd.to_datetime(orders['Order Date']).max()

    start=pd.to_datetime(st.sidebar.date_input('Pick start date',start_date))
    end=pd.to_datetime(st.sidebar.date_input('Pick end date',end_date))
    orders=orders[(orders['Order Date']>= start) & (orders['Order Date']<=end)].copy()

    #Quantity and product category
    
    category = st.sidebar.multiselect('Pick your category',orders['Category'].unique())

    if category:  
        filtered_df = orders[orders["Category"].isin(category)]
    else:
        filtered_df = orders.copy()  

    #Charts for the Orders dataset
    filtered_df.groupby(by=['Category'],as_index=False)['Sales'].sum()
    #Sales by sub category
    st.subheader('Sales by Sub Category')
    fig1=px.bar(filtered_df,x='Sub-Category',y='Sales', height=600,width=700)
        
    st.plotly_chart(fig1)


    #sales distrubution by category
    st.subheader('Sales distribution by category')
    catedf=orders.groupby(by=['Category'],as_index=False)['Sales'].sum()
    fig2=px.bar(catedf,x="Category",y="Sales")
    st.plotly_chart(fig2)
   
   
    #Profitability of categories
    st.subheader('Profitability of Categories')
    catedf=orders.groupby(by=['Category'],as_index=False)['Profit'].sum()
    fig3=px.bar(catedf,x="Category",y="Profit")
    st.plotly_chart(fig3)
   
   
    #Sales by country
    st.subheader ('Sales by country')
    fig4=px.pie(filtered_df,values='Sales', names='Country',hole=0.5,height=400,width=600)
    st.plotly_chart(fig4)

     #bar chart
    st.subheader('Sales distribution by country')
    catedf=orders.groupby(by=['Country'],as_index=False)['Sales'].sum()
    fig5=px.bar(catedf,x="Country",y="Sales",color="Country")
    st.plotly_chart(fig5)

   #line chart to show sales over time
    filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
    st.subheader('Sales Trend over time')

    line = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
    line = line.sort_values(by="month_year")
    fig6 = px.line(line, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1500,template="gridon")
    st.plotly_chart(fig6,use_container_width=True)


    #shipping cost vs sales 
    data1 = px.scatter(orders, x = "Shipping Cost", y = "Sales", size = "Quantity")
    data1['layout'].update(title="Shipping cost vs Sales",
                        titlefont = dict(size=20),xaxis = dict(title="Shipping Cost",titlefont=dict(size=19)),
                        yaxis = dict(title = "Sales", titlefont = dict(size=19)))
    st.plotly_chart(data1,use_container_width=True)


    #scatter plot to show discount impact on sales
    data2 = px.scatter(orders, x = "Discount", y = "Sales", size = "Quantity")
    data2['layout'].update(title="Discount impact on Sales",
                        titlefont = dict(size=20),xaxis = dict(title="Discount",titlefont=dict(size=19)),
                        yaxis = dict(title = "Sales", titlefont = dict(size=19)))
    st.plotly_chart(data2,use_container_width=True)


   #scatter plot to show relationship between quantity and profit
    data3 = px.scatter(orders, x = "Quantity", y = "Profit", size = "Quantity")
    data3['layout'].update(title="Relationship between Quantity and Profits using Scatter Plot.",
                        titlefont = dict(size=20),xaxis = dict(title="Quantity",titlefont=dict(size=19)),
                        yaxis = dict(title = "Profit", titlefont = dict(size=19)))
    st.plotly_chart(data3,use_container_width=True)

with association_rules:
    st.header("Market Basket Analysis Association Rules")
    st.write(rules)
    import seaborn as sns

    # Define x and y axis options
    x_axis_options = list(rules.columns)
    y_axis_options = list(rules.columns)

    # Create the heatmap based on selected axes
    pivot_data = rules.pivot_table(index='antecedents', columns='consequents', values='lift')  

    heatfig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_data, ax=ax, annot=True, cmap="viridis")  


    st.pyplot(heatfig)
