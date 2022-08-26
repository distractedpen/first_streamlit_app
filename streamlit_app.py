
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import urllib.error import URLError


st.title('My Parents New Healthy Diner')

st.header('Breakfast Favorites')   
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# pick list for user to choose fruits to include
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits: ", list(my_fruit_list.index), default=['Avocado', 'Strawberries'])
# display the full table on page
fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)


st.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    st.dataframe(fruityvice_normalized)
except URLError as e:
  st.error()

conn = snowflake.connector.connect(**st.secrets["snowflake"])
cur = conn.cursor()
cur.execute("select * from fruit_load_list")
data_rows = cur.fetchall()
st.text("The fruit load list contains:")
st.dataframe(data_rows)

new_fruit = st.text_input("What fruit would you like to add?")
st.text("Thanks for adding " + new_fruit)
if new_fruit:
  cur.execute("insert into fruit_load_list values ?", new_fruit)
