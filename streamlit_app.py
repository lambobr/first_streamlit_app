import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


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


def get_fruityvice_details(fruit_input):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_input)
  # streamlit.text(fruityvice_response.json())
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) # json_normalize converts json to table
  return  fruityvice_normalized 
 

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_input = streamlit.text_input('What fruit would like information about?','Kiwi') # Kiwi is optionally included to show Kiwi when the page loads first
  if not fruit_input:
    streamlit.error("Please select a fruit to get information.")
  else:
    streamlit.write('The user entered', fruit_input)
    function_output = get_fruityvice_details(fruit_input)
    streamlit.dataframe(function_output) # show the table on page
except URLError as e:
  streamlit.error()

streamlit.stop()

# connect to snowflake


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  # secrets is made inside streamlit app settings. secrets also contain default settings to use like username, password, database, schema
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
# my_data_row = my_cur.fetchone() -- to only fetch one row
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

fruit_to_add = streamlit.text_input('What fruit would you like to add?') 
if fruit_to_add:
  streamlit.write('Thanks for adding',fruit_to_add)

my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('from streamlit')")
  
