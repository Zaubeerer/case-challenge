import os
import pathlib

import streamlit as st

from .auth import check_password

CFD = pathlib.Path(__file__).parent
LOGO_PATH = CFD / "logo.png"
ICON_PATH = CFD / "logo.png"

APP_TITLE = "Banking App"
DEBUG = os.getenv("DEBUG", False)
URL = "http://localhost:8000" if DEBUG else "https://banking-api.fly.dev"

print(f"DEBUG: {DEBUG}")


def sidebar_header():
    st.sidebar.image(str(LOGO_PATH), use_column_width=True)
    st.sidebar.container(height=10, border=False)
    st.sidebar.title("Banking App")


def authenticated_menu():
    # Show a navigation menu for authenticated users
    sidebar_header()

    st.sidebar.page_link("pages/customers.py", label="Customers")
    st.sidebar.page_link("pages/accounts.py", label="Accounts")
    st.sidebar.page_link("pages/transfers.py", label="Transfers")

    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Manage users")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Manage admin access",
            disabled=st.session_state.role != "super-admin",
        )

    if st.sidebar.button("Logout"):
        del st.session_state["password_correct"]
        st.rerun()


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    sidebar_header()
    st.sidebar.title("Administration")
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu

    if not check_password():
        unauthenticated_menu()
        return
    else:
        authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu

    if not check_password():
        st.switch_page("app.py")
    else:
        menu()
