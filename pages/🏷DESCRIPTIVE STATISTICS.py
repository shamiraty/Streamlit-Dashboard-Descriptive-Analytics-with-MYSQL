import streamlit as st
import pandas as pd 
import plotly.express as px
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards 

st.set_page_config(page_title="Dashboard ", page_icon="📈", layout="wide")  
st.header("PERCENTILES AND NUMBER SUMMARY FOR CATEGORICAL DATA")
st.markdown("##")
 
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
     
df=pd.read_excel('descriptive_statistics.xlsx', sheet_name='Sheet1')

tab1, tab2 = st.tabs(["DATASET","SALES BY PERCENTILES"])

with tab1:
 with st.expander("Show Workbook"):
  #st.dataframe(df_selection,use_container_width=True)
  shwdata = st.multiselect('Filter :', df.columns, default=["SALES","ORDERDATE","STATUS","YEAR_ID","PRODUCTLINE","CUSTOMERNAME","CITY","COUNTRY"])
  st.dataframe(df[shwdata],use_container_width=True
  )

with tab2.caption("SALES BY PERCENTILES"):
 c1,c2,c3,c4,c5=st.columns(5)
 with c1:
   st.info('Percentile 25 %', icon="⏱")
   st.metric(label='USD', value=f"{np.percentile(df['SALES'], 25):,.2f}")
 with c2:
   st.info('Percentile 50 %', icon="⏱")
   st.metric(label='USD', value=f"{np.percentile(df['SALES'], 50):,.2f}")
 with c3:
   st.info('Percentile 75 %', icon="⏱")
   st.metric(label='USD', value=f"{np.percentile(df['SALES'], 75):,.2f}")
 with c4:
   st.info('Percentile 100 %', icon="⏱")
   st.metric(label='USD', value=f"{np.percentile(df['SALES'], 100):,.2f}")
 with c5:
   st.info('Percentile 0 %', icon="⏱")
   st.metric(label='USD', value=f"{np.percentile(df['SALES'], 0):,.2f}")

def ad():
 theme_plotly = None # None or streamlit
 column=st.sidebar.selectbox('select a column',['COUNTRY','PRODUCTLINE','CITY'])
 type_of_column=st.sidebar.radio("What kind of analysis",['Categorical','Numerical'])

 c1,c2=st.columns([2,1])
 with c1:
   if type_of_column=='Categorical':
    dist=pd.DataFrame(df[column].value_counts())
    fig=px.bar(dist, title='CATEGORIES BY FREQUENCY',orientation="v")
    fig.update_layout(
      legend_title=None,
        xaxis_title="Observation",
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
        font=dict(color='#cecdcd'),  # Set text color to black
          yaxis_title='Count')
    st.plotly_chart(fig,use_container_width=True)
    
   else:
    st.subheader("NUMBER SUMMARY ")
    st.dataframe(df['SALES'].describe(),use_container_width=True)

 with c2:
   st.subheader("Total Sales")
   st.metric(label='USD', value=f"{np.sum(df['SALES'], 0):,.2f}",help="sum",delta=np.average(df.SALES),
    delta_color="inverse")
style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")
  
    
ad()
