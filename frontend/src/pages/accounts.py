import pandas as pd
import requests
import streamlit as st
from st_utils.menu import APP_TITLE, ICON_PATH, URL, menu_with_redirect

st.set_page_config(page_title=APP_TITLE, page_icon=str(ICON_PATH))

menu_with_redirect()

customers = requests.get(f"{URL}/customers/")

if len(customers.json()) == 0:
    create_customer = st.button("Create a customer first")

    if create_customer:
        st.switch_page("pages/customers.py")

else:
    st.write("Create an Account")
    cols = st.columns(2)
    with cols[0]:
        customer = st.selectbox(
            "Select a customer",
            options=[
                (customer["name"], customer["id"]) for customer in customers.json()
            ],
        )
        balance = st.number_input("Enter the balance", value=0, step=10)
    with cols[1]:
        st.container(height=12, border=False)
        create_button = st.button("Create an account for the customer")

        if create_button:
            response = requests.post(
                f"{URL}/accounts/",
                json={"customer_id": customer[1], "balance": balance},
            )

    accounts = requests.get(f"{URL}/accounts/").json()

    if len(accounts) > 0:
        st.write("Delete an Account")
        account_id = int(
            st.selectbox(
                "Select an account",
                options=[account["id"] for account in accounts],
            )
        )
        delete_button = st.button("Delete an account")

        if delete_button:
            response = requests.delete(f"{URL}/accounts/{account_id}")

    st.write("Accounts")
    response = requests.get(f"{URL}/accounts/")
    st.table(pd.DataFrame(response.json()))
