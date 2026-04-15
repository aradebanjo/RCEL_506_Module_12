import streamlit as st

# Basic page configuration
st.set_page_config(
    page_title="Ecobici Hello World",
    page_icon="🚲",
    layout="centered"
)

# Title and Header
st.title("🚲 Hello, Mexico City!")
st.header("Ecobici Data Dashboard")

# A simple interactive element
name = st.text_input("Enter your name to start the tour:", "Cyclist")

st.write(f"Welcome, **{name}**! This is a starter app for analyzing Ecobici data.")

# A placeholder for future data
st.info("Coming soon: Interactive maps and trip duration statistics!")

# Adding a button just for fun
if st.button('Click for a random CDMX fact'):
    st.success("Did you know? The Ecobici system is one of the largest bike-sharing programs in Latin America!")
