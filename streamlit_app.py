import streamlit
import pandas
import response

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥣 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt", index_col='Fruit') # set column Fruit as row index

# Let's put a pick list here so they can pick the fruit they want to include
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index)) # the list is the values of index which is values from column "Fruit"
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries']) # adding default picks Avocado and Strawberries
fruits_to_show = my_fruit_list.loc[fruits_selected] # loc is used to access the rows based on selected indices

# Display the table on the page
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())
