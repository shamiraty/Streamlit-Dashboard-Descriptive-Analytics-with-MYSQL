import streamlit as st
import pandas as pd 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from streamlit_extras.metric_cards import style_metric_cards
#from query import *
st.set_option('deprecation.showPyplotGlobalUse', False)

#navicon and header
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")  

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#current date
from datetime import datetime
current_datetime = datetime.now()
formatted_date = current_datetime.strftime('%Y-%m-%d')
formatted_day = current_datetime.strftime('%A')
 
st.header(" MACHINE LEARNING WORKFLOW | MYSQL  ")
st.markdown(
 """
 <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
 <hr>

<div class="card mb-3">
<div class="card">
  <div class="card-body">
    <h3 class="card-title"style="color:#007710;"><strong>⏱ MULTIPLE REGRESSION ANALYSIS DASHBOARD</strong></h3>
    <p class="card-text">There are three features, InterestRate, UnemploymentRate and PriceIndex. The purpose is to check how far linear relationship  is between these variables, where InterestRate and UnemploymentRate are X features and IndexPrice is Y feature. This is a classification problem using probabilistic multiple regression analysis for the data that exists in mysql. Finnaly visualizing measure of Variations and Line of best fit</p>
    <p class="card-text"><small class="text-body-secondary"> </small></p>
  </div>
</div>
</div>
 <style>
    [data-testid=stSidebar] {
         color: white;
         text-size:24px;
    }
</style>
""",unsafe_allow_html=True
)

#uncomment line 1,3 and 3 if you use mysql database
#1. read data from mysql
#2. result = view_all_data()
#3. df = pd.DataFrame(result,columns=["id","year","month","interest_rate","unemployment_rate","index_price"])

df=pd.read_csv("advanced_regression.csv")
#logo


with st.sidebar:
 st.markdown(f"<h4 class='text-success'>{formatted_day}: {formatted_date}</h4>Analytics Dashboard V: 01/2023<hr>", unsafe_allow_html=True)
 

# switcher
year_= st.sidebar.multiselect(
    "PICK YEAR:",
    options=df["year"].unique(),
    default=df["year"].unique()
)
month_ = st.sidebar.multiselect(
    "PICK MONTH:",
    options=df["month"].unique(),
    default=df["month"].unique(),
)

df_selection = df.query(
    "month == @month_ & year ==@year_"
)

#download csv
with st.sidebar:
 df_download = df_selection.to_csv(index=False).encode('utf-8')
 st.download_button(
    label="Download DataFrame from Mysql",
    data=df_download,
    key="download_dataframe.csv",
    file_name="my_dataframe.csv"
 )

#drop unnecessary fields
df_selection.drop(columns=["id","year","month"],axis=1,inplace=True)

#theme_plotly = None # None or streamlit

with st.expander("⬇ EXPLORATORY  ANALYSIS"):
 st.write("Examining the correlation between the independent variables (features) and the dependent variable before actually building and training a regression model. This is an important step in the initial data exploration and analysis phase to understand the relationships between variables.")
 col_a,col_b=st.columns(2)
 with col_a:
  st.subheader("Interest Vs Unemployment")
  plt.figure(figsize=(4, 4))
  sns.regplot(x=df_selection['interest_rate'], y=df_selection['unemployment_rate'],color="#007710")
  plt.xlabel('Interest Rate')
  plt.ylabel('Unemployment Rate')
  plt.title('Interest Rate vs UnemploymentRate: Regression Plot')
  st.pyplot()
   

with col_b:
 plt.figure(figsize=(4, 4))
 st.subheader("Interest Vs Index Price")
 sns.regplot(x=df_selection['interest_rate'], y=df_selection['index_price'],color="#007710")
 plt.xlabel('Interest Rate')
 plt.ylabel('Unemployment Rate')
 plt.title('InterestRate vs IndexPrice Regression Plot')
 st.pyplot()

 fig, ax = plt.subplots()
 st.subheader("Variables outliers",)
 sns.boxplot(data=df, orient='h',color="#FF4B4B")
 plt.show()
 st.pyplot()

with st.expander("⬇ EXPLORATORY VARIABLE DISTRIBUTIONS BY FREQUENCY: HISTOGRAM"):
  df_selection.hist(figsize=(16,8),color='#007710', zorder=2, rwidth=0.9,legend = ['unemployment_rate']);
  st.pyplot()

with st.expander("⬇ EXPLORATORY VARIABLES DISTRIBUTIONS:"):
 st.subheader("Correlation between variables",)
 #https://seaborn.pydata.org/generated/seaborn.pairplot.html
 pairplot = sns.pairplot(df_selection,plot_kws=dict(marker="+", linewidth=1), diag_kws=dict(fill=True))
 st.pyplot(pairplot)


#checking null value
with st.expander("⬇ NULL VALUES, TENDENCY & VARIABLE DISPERSION"):
 a1,a2=st.columns(2)
 a1.write("number of missing (NaN or None) values in each column of a DataFrame")
 a1.dataframe(df_selection.isnull().sum(),use_container_width=True)
 a2.write("insights into the central tendency, dispersion, and distribution of the data.")
 a2.dataframe(df_selection.describe().T,use_container_width=True)



# train and test split
with st.expander("⬇ DEFAULT CORRELATION"):
 st.dataframe(df_selection.corr())
 st.subheader("Correlation",)
 st.write("correlation coefficients between Interest Rate Rate & Unemployment Rate")
 plt.scatter(df_selection['interest_rate'], df_selection['unemployment_rate'])
 plt.ylabel("Unemployment rate")
 plt.xlabel("Interest rate")
 st.pyplot()

try:

 # independent and dependent features
 X=df_selection.iloc[:,:-1] #left a last column
 y=df_selection.iloc[:,-1] #take a last column

 # train test split
 from sklearn.model_selection import train_test_split
 X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=42)


 with st.expander("⬇ UNIFORM  DISTRIBUTION "):
  st.subheader("Standard Scores (Z-Scores)",)
  st.write("transform data so that it has a mean (average) of 0 and a standard deviation of 1. This process is also known as [feature scaling] or [standardization.]")
  from sklearn.preprocessing import StandardScaler
  scaler=StandardScaler()
  X_train=scaler.fit_transform(X_train)
  X_test=scaler.fit_transform(X_test)
  st.dataframe(X_train)


 from sklearn.linear_model import LinearRegression
 regression=LinearRegression()
 regression.fit(X_train,y_train)

#cross validation
 from sklearn.model_selection import cross_val_score
 validation_score=cross_val_score(regression,X_train,y_train,scoring='neg_mean_squared_error',cv=3)

 col1, col3,col4,col5 = st.columns(4)
 col1.metric(label="🟡 MEAN VALIDATION SCORE", value=np.mean(validation_score), delta=f"{ np.mean(validation_score):,.0f}")

 #prediction
 y_pred=regression.predict(X_test)


# performance metrics
 from sklearn.metrics import mean_squared_error, mean_absolute_error
 meansquareerror=mean_squared_error(y_test,y_pred)
 meanabsluteerror=mean_absolute_error(y_test,y_pred)
 rootmeansquareerror=np.sqrt(meansquareerror)

 col3.metric(label="🟡 MEAN SQUARED ERROR ", value=np.mean(meansquareerror), delta=f"{ np.mean(meansquareerror):,.0f}")
 col4.metric(label="🟡 MEAN ABSOLUTE ERROR", value=np.mean(meanabsluteerror), delta=f"{ np.mean(meanabsluteerror):,.0f}")
 col5.metric(label="🟡 ROOT MEAN SQUARED ERROR", value=np.mean(rootmeansquareerror), delta=f"{ np.mean(rootmeansquareerror):,.0f}")


 with st.expander("⬇ COEFFICIENT OF DETERMINATION | R2"):
  from sklearn.metrics import r2_score
  score=r2_score(y_test,y_pred)
  st.metric(label="🔷 r", value=score, delta=f"{ score:,.0f}")

 with st.expander("⬇ ADJUSTED CORRERATION COEFFICIENT | R"):
  #display adjusted R_squared
  st.metric(label="🔷 Adjusted R", value=((1-(1-score)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1))), delta=f"{ ((1-(1-score)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1))):,.0f}")
 

 with st.expander("⬇ CORRERATION COEFFICIENT | r"):
  #display correlation
  st.write(regression.coef_)
 

 #https://seaborn.pydata.org/generated/seaborn.regplot.html
 c1,c2,c3=st.columns(3)
 with c1:
  with st.expander("⬇ LINE OF BEST FIT"):
   st.write("regression line that best represents the relationship between the independent variable(s) and the dependent variable in a linear regression model. This line is determined through a mathematical process that aims to minimize the error between the observed data points and the predicted values generated by the model.")
   plt.figure(figsize=(8, 6))
   sns.regplot(x=y_test, y=y_pred,color="#FF4B4B",line_kws=dict(color="#007710"))
   plt.xlabel('Interest Rate')
   plt.ylabel('Unemployment Rate')
   plt.title('Interest Rate vs Unemployment_Rate Regression Plot')
   st.pyplot()

 with c2:
  with st.expander("⬇ RESIDUAL"):
   st.write("residuals: refers to the differences between the actual observed values (the dependent variable, often denoted as y) and the predicted values made by a regression model (often denoted as y_pred). These residuals represent how much the model's predictions deviate from the actual data points")
   residuals=y_test-y_pred
   st.dataframe(residuals)

 with c3:
  with st.expander("⬇ MODEL PERFORMANCE | NORMAL DISTRIBUTION CURVE"):
   st.write("distribution of a continuous random variable where data tends to be symmetrically distributed around a mean (average) value. It is a fundamental concept in statistics and probability theory.")
   sns.displot(residuals,kind='kde',legend=True,color="#007710") #kernel density estimator
   st.pyplot()


 with st.expander("⬇ OLS, or Ordinary Least Squares Method"): 
  import statsmodels.api as sm
  model=sm.OLS(y_train,X_train).fit()
  st.write(model.summary())

 st.sidebar.image("data/logo1.png")
 style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")

except:
 st.error("❌ THE AMOUNT OF DATA YOU SELECTED IS NOT ENOUGH FOR THE MODEL TO PERFORM PROPERLY")

 


