import streamlit as st
from pages.home import show_home
from pages.dashboard import show_dashboard
from components import sidebar  # Changed import statement

def init_session_state():
    if 'login_status' not in st.session_state:
        st.session_state.login_status = False
    if 'master_client' not in st.session_state:
        st.session_state.master_client = None
    if 'child_client' not in st.session_state:
        st.session_state.child_client = None

st.set_page_config(
    page_title="Dhan Copy Trader",
    page_icon="📈",
    layout="wide"
)

def main():
    init_session_state()
    selected_page = sidebar()
    
    if selected_page == "Home":
        show_home()
    elif selected_page == "Dashboard":
        show_dashboard()

if __name__ == "__main__":
    main()