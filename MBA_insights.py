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

   
