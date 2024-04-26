# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(""" Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#Add multiselect option called ingredient_list
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
    )

# Use st.write() and st.text() to take a closer look at the ingredient_list LIST that a person selected
if ingredients_list: # Adding the if ingredient list command will only show the LIST if an ingredient is selected
    ingredients_string = '' # This will convert the LIST to a string

    for fruit_chosen in ingredients_list: # Creating a FOR LOOP
        ingredients_string += fruit_chosen + ' ' # += operator means "add this to what is already in the variable". Here, we are adding a space between fruit names
   
    #st.write(ingredients_string)

    # Build a SQL Insert Statement & Test It in worksheets
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order') # Create Submit button so that selections are only recorded when final
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
