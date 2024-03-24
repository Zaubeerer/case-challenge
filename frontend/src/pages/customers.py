import pandas as pd
import requests
import streamlit as st
from st_utils.menu import APP_TITLE, ICON_PATH, URL, menu_with_redirect

st.set_page_config(page_title=APP_TITLE, page_icon=str(ICON_PATH))

menu_with_redirect()

st.write("Create a Customer")
cols = st.columns(2)
with cols[0]:
    customer_name = st.text_input("Enter the name for the new customer")
with cols[1]:
    st.container(height=12, border=False)
    create_button = st.button("Create customer")

    if create_button:
        response = requests.post(f"{URL}/customers/", json={"name": customer_name})

st.write("Delete a Customer")
cols = st.columns(2)
with cols[0]:
    customers = requests.get(f"{URL}/customers/")
    customer = st.selectbox(
        "Select a customer",
        options=[(customer["name"], customer["id"]) for customer in customers.json()],
    )
with cols[1]:
    st.container(height=12, border=False)
    delete_button = st.button("Delete customer", key="delete_customer_button")

    if delete_button:
        customer_id = customer[1]
        response = requests.delete(f"{URL}/customers/{customer_id}")

st.write("Customers")
response = requests.get(f"{URL}/customers")
st.table(pd.DataFrame(response.json()))
