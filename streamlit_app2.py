#notes:
# - choose four spaces for each indentation level instead of tabs
# - 2nd app: for kitchen staff to see open orders and mark them complete
#       when they've been filled and given to customer
#To-Do #2 - A 2nd SiS App for the Kitchen
#Checking All Objects for SYSADMIN Ownership
# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
    """Orders that need to filled.
    """
)

session = get_active_session()
#df below not editable
#my_dataframe = session.table("smoothies.public.orders") \
#    .select(col('ingredients'),col('name_on_order'),
#            col('order_filled'))
#st.dataframe(data=my_dataframe, use_container_width=True)
my_dataframe = session.table("smoothies.public.orders") \
    .filter(col("ORDER_FILLED")==0).collect()

if my_dataframe: #prevent empty table,submit button from showing
    #df now editable
    editable_df = st.data_editor(my_dataframe)
    #TIP: Unlike in the header where we can type something like :thumbs_up: 
    #     to get an emoji, the SUCCESS object requires the emoji itself.
    submitted = st.button('Submit')
    if submitted:
        #writes updates to screen
        #st.write("Edited dataframe:", editable_df)
        #writes updates to db
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                , [when_matched().update({
                    'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                )
            st.success('Someone clicked the button', icon = '👍')
        except:
            st.write('Something went wrong.')
else:
    st.write('There are no pending orders right now', icon = '👍')




