import pandas as pd
import requests
import streamlit as st
from st_utils.menu import APP_TITLE, ICON_PATH, menu_with_redirect

st.set_page_config(page_title=APP_TITLE, page_icon=str(ICON_PATH))

menu_with_redirect()

st.write("Create an Account")
cols = st.columns(2)
with cols[0]:
    customers = requests.get("https://banking-api.fly.dev/customers/")
    customer = st.selectbox(
        "Select a customer",
        options=[(customer["name"], customer["id"]) for customer in customers.json()],
    )
    balance = st.number_input("Enter the balance", value=0, step=10)
with cols[1]:
    st.container(height=12, border=False)
    create_button = st.button("Create an account for the customer")

    if create_button:
        response = requests.post(
            "https://banking-api.fly.dev/accounts/",
            json={"customer_id": customer[1], "balance": balance},
        )

st.write("Accounts")
response = requests.get("https://banking-api.fly.dev/accounts/")
st.table(pd.DataFrame(response.json()))
