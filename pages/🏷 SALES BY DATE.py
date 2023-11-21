import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns 
import altair as alt
from UI import *
from matplotlib import pyplot as plt
from datetime import date, timedelta
#pip install streamlit-extras
#https://pypi.org/project/streamlit-extras/
from streamlit_extras.dataframe_explorer import dataframe_explorer


#page layout
st.set_page_config(page_title="Sales", page_icon="🌎", layout="wide")

st.header("SALES  KPI  &  TRENDS  | DESCRIPTIVE WEB ANALYTICS  ")
st.write("Pick a date range from sidebar to view sales trends | the default date is today")

#streamlit theme=none
theme_plotly = None 

# load CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
#load user interface file
UI()

#load dataset
df = pd.read_csv('sales.csv')


#filter date to view sales
with st.sidebar:
 st.title("Select Date Range")
 start_date=st.sidebar.date_input("Start Date",date.today()-timedelta(days=365*4))

with st.sidebar:
 end_date=st.date_input(label="End Date")
st.error("Business Metrics between[ "+str(start_date)+"] and ["+str(end_date)+"]")

#compare date
df2 = df[(df['OrderDate'] >= str(start_date)) & (df['OrderDate'] <= str(end_date))]

#dataframe
with st.expander("Filter Excel Dataset"):
 filtered_df = dataframe_explorer(df2, case=False)
 st.dataframe(filtered_df, use_container_width=True)

b1, b2=st.columns(2)
with b1:  
 from add_data import *
 st.subheader('Add New record to Excel File',)
 #this function is called from another file named 'add_data.py' file  
 add_data()

 #metric cards
 with b2:
    st.subheader('Dataset Metrics',)
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2, = st.columns(2)
    col1.metric(label="All Inventory Products ", value=df2.Product.count(), delta="Number of Items in stock")
    col2.metric(label="Sum of Product Price USD:", value= f"{df2.TotalPrice.sum():,.0f}",delta=df2.TotalPrice.median())
    
    col11, col22,col33, = st.columns(3)
    col11.metric(label="Maximum Price  USD:", value= f"{ df2.TotalPrice.max():,.0f}",delta="High Price")
    col22.metric(label="Minimum Price  USD:", value= f"{ df2.TotalPrice.min():,.0f}",delta="Low Price")
    col33.metric(label="Total Price Range  USD:", value= f"{ df2.TotalPrice.max()-df2.TotalPrice.min():,.0f}",delta="Annual Salary Range")
    #style the metric
    style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")

#dot Plot
a1,a2=st.columns(2)
with a1:
 st.subheader('Products & Total Price',)
 source = df2
 chart = alt.Chart(source).mark_circle().encode(
    x='Product',
    y='TotalPrice',
    color='Category',
 ).interactive()
 st.altair_chart(chart, theme="streamlit", use_container_width=True)


with a2:
 st.subheader('Products & Unit Price',)
 energy_source = pd.DataFrame({
    "Product": df2["Product"],
    "UnitPrice ($)":  df2["UnitPrice"],
    "Date": df2["OrderDate"]
    })
 
 #bar Graph
 bar_chart = alt.Chart(energy_source).mark_bar().encode(
        x="month(Date):O",
        y="sum(UnitPrice ($)):Q",
        color="Product:N"
    )
 st.altair_chart(bar_chart, use_container_width=True,theme=theme_plotly)
 
 
 #select only numeric or number data
 #pip install pandas-select
 #https://pypi.org/project/pandas-select/
p1,p2=st.columns(2) 
with p1:
# Select features to display scatter plot
 st.subheader('Features by Frequency',)
 feature_x = st.selectbox('Select feature for x Qualitative data', df2.select_dtypes("object").columns)
 feature_y = st.selectbox('Select feature for y Quantitative Data', df2.select_dtypes("number").columns)

# Display scatter plot
 fig, ax = plt.subplots()
 sns.scatterplot(data=df2, x=feature_x, y=feature_y, hue=df2.Product, ax=ax)
 st.pyplot(fig)

with p2:
 st.subheader('Products & Qantities',)
 source = pd.DataFrame({
        "Quantity ($)": df2["Quantity"],
        "Product": df2["Product"]
      })
 
 bar_chart = alt.Chart(source).mark_bar().encode(
        x="sum(Quantity ($)):Q",
        y=alt.Y("Product:N", sort="-x")
    )
 st.altair_chart(bar_chart, use_container_width=True,theme=theme_plotly)
st.sidebar.image("data/logo1.png")

 















 


