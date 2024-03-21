import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title='Supermarkt Sales', page_icon=':bar_chart:', layout='wide', initial_sidebar_state='expanded')

@st.cache_data
def open_df():
    df = pd.read_excel('supermarkt_sales.xlsx', sheet_name='Sales', engine='openpyxl', skiprows=3, usecols='B:R', nrows=1000)
    return df
    


df = open_df()
city = st.sidebar.multiselect('Select the City',options =  df['City'].unique(), default = df['City'].unique()) #have all the options selected by default
customer = st.sidebar.multiselect('Select the Customer', options = df['Customer_type'].unique(), default = df['Customer_type'].unique())
gender = st.sidebar.multiselect('Select the Gender', options = df['Gender'].unique(), default = df['Gender'].unique())

#To filter the data, we use the query method, i.e select the data based on the user input for city, customer, and gender.
df_filtered = df.query('City == @city and Customer_type == @customer and Gender == @gender')
#st.dataframe(df_filtered.head(10))


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "7 worst cities",
        "Main Towns in England",
        "Incidents within Care Boards",
        "City Details",
        "Details within X miles radius of city",
        "Incidents Within Fire Services",
    ]
)


#-------Main Page--------
st.title(':bar_chart: Supermarkt Sales')
total_sales = int(df_filtered['Total'].sum())
average_rating = round(df_filtered['Rating'].mean(),1)
star_rating = ":star:" * int(average_rating)
average_sale_by_transaction = round(df_filtered['Total'].mean(),2)

left_column,middle_column, right_column = st.columns(3)
with left_column:
    st.write('Total Sales')
    st.write(f'${total_sales:,}')
with middle_column:
    st.write('Average Rating')
    st.write(f'{star_rating} {average_rating}')
with right_column:
    st.write('Average Sales by Transaction')
    st.write(f'${average_sale_by_transaction:,}')

st.markdown('---')

#-------Plotting--------
sales_by_product = df_filtered.groupby('Product line')['Total'].sum().reset_index()
fig_product_sales = px.bar(sales_by_product,  
                           y='Product line', 
                           x='Total', 
                            title='<b>Total Sales by Product Line<b>', 
                            orientation='h',
                         
                            opacity=0.7,

                           )


st.plotly_chart(fig_product_sales, use_container_width=True)

#custom css
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """ 
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#Hdden Files included for css code