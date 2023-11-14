#import libraries
import streamlit as st
import pandas as pd 

#load data set


def add_data():
   df=pd.read_csv("sales.csv")
   #clear hutumika kufuta form akishasubmit form 
   with st.form("form 2",clear_on_submit=True):
    col1,col2=st.columns(2)
    orderdate=col1.date_input(label="order date")
    region=col2.selectbox("region",df["Region"].unique())

    col11,col22=st.columns(2)
    city=col11.selectbox("city",df["City"].unique())
    category=col22.selectbox("category",df["Category"].unique())
    
    col111,col222,col333=st.columns(3)
    product=col111.selectbox("product name",df["Product"].unique())
    quantity=col222.number_input("quantity")
    unitprice=col333.number_input("unitprice")
    
    #Button
    btn=st.form_submit_button("Save Data To Excel", type="primary")

    #if btn is clicked
    #validate
    if btn:
        if orderdate=="" or region=="" or city==""or category==""or product==""or quantity==""or unitprice==""or quantity==0.00 or unitprice==0.00:
            st.warning("All fields are required")
            return False
        else:
           df = pd.concat([df, pd.DataFrame.from_records([{ 
           'OrderDate': orderdate,
           'Region':region,
           'City':city,
           'Category':category,
           'Product':product,
           'Quantity':quantity,
           'UnitPrice':float(unitprice),
           'TotalPrice':float(quantity)*float(unitprice),
           }])])
        try:
            df.to_csv("data.csv",index=False)
            st.success(product+ " Has been Added successfully !")
            return True
            
        except:
            st.warning("Unable to write, Please close your dataset !!") 
            return False
    st.experimental_rerun 


