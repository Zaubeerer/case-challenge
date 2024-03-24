import pandas as pd
import requests
import streamlit as st
from st_utils.menu import APP_TITLE, ICON_PATH, menu_with_redirect

st.set_page_config(page_title=APP_TITLE, page_icon=str(ICON_PATH))

menu_with_redirect()

cols = st.columns(2)
with cols[0]:
    accounts = requests.get("https://banking-api.fly.dev/accounts/")
    sender = st.selectbox(
        "Select an account to send money from",
        options=[account["id"] for account in accounts.json()],
    )
    receiver = st.selectbox(
        "Select an account to send money to",
        options=[account["id"] for account in accounts.json()],
    )
    amount = st.number_input("Enter the amount to be sent", value=0, step=10)
with cols[1]:
    st.container(height=12, border=False)
    create_button = st.button("Transfer money")

    if create_button:
        response = requests.post(
            "https://banking-api.fly.dev/transfers/",
            json={"id_sender": sender, "id_receiver": receiver, "amount": amount},
        )
        st.write(response)


st.write("Transfers")
response = requests.get("https://banking-api.fly.dev/transfers/history")
st.table(pd.DataFrame(response.json()))
