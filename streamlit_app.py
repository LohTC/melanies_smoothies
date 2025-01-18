#notes:
# - choose four spaces for each indentation level instead of tabs
# - first app: for customers to enter their orders
# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session #del
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

#text box
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be', name_on_order)

#droplist
#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)
#st.write("You selected:", option)

#print list from db 
#session = get_active_session() #del
cnx = st.connection("snowflake") #add
session = cnx.session() #add
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

#multi-select
#ingredients_list has datatype LIST
#ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe)
#display list
#st.write(ingredients_list)
#st.text(ingredients_list)
#allow 5 selections only | wonky because it seems to give you the alert 
#when you choose your fifth item instead of waiting until you try to add
#a 6th
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5 #new
)
#avoid printing empty brackets
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingredients_string)
    #Create a Place to Store Order Data    
    my_insert_stmt = """ insert into smoothies.public.orders
        (ingredients, name_on_order)
        values ('""" + ingredients_string + """','""" + name_on_order + \
        """')"""
    #st.write(my_insert_stmt)
    #st.stop() #stop exe for testin 
    time_to_insert = st.button('Submit Order')
    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")

#st.text(smoothiefroot_response.json())



