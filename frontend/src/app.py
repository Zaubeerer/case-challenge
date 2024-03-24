import streamlit as st
from st_utils.menu import APP_TITLE, ICON_PATH, menu

st.set_page_config(page_title=APP_TITLE, page_icon=str(ICON_PATH))

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = "user"

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role


def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role


menu()  # Render the dynamic menu!

if "password_correct" in st.session_state:
    st.switch_page("pages/customers.py")
