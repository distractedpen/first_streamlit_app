
import streamlit as st
import pandas as pd
import requests
import snowflake.connector


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
fruit_choice = st.text_input('What fruit would you like information about?', "Kiwi")
st.write('The user entered', fruit_choice)
# get the data from fruityvice
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# convert from json to pd dataframe
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# display pd dataframe
st.dataframe(fruityvice_normalized)


conn = snowflake.connector.connect(**st.secrets["snowflake"])
cur = conn.cursor()
cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
data = cur.fetchone()
st.text("Hello from Snowflake:")
st.text(data)
