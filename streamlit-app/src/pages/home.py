import streamlit as st
from utils.dhan_helper import validate_credentials

def show_home():
    st.title("Welcome to Dhan Copy Trader 📈")
    
    # Hero section
    st.markdown("""
    ### Automate Your Trading Journey
    Copy trades automatically between master and child accounts with secure, 
    reliable execution and real-time monitoring.
    """)
    
    # Features section
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Key Features
            - ✅ Real-time trade copying
            - 📊 Live portfolio tracking
            - 🔒 Secure authentication
            - ⚡ Low latency execution
            """)
        
        with col2:
            st.markdown("""
            #### Benefits
            - 💼 Manage multiple accounts
            - 📈 Track performance
            - ⚙️ Customize trading parameters
            - 🎯 Risk management
            """)
    
    # Login form
    with st.form("login_form"):
        st.subheader("Login")
        
        account_type = st.radio("Account Type", ["Master", "Child"])
        client_id = st.text_input("Client ID")
        access_token = st.text_input("Access Token", type="password")
        
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if validate_credentials(client_id, access_token):
                st.session_state.login_status = True
                if account_type == "Master":
                    st.session_state.master_client = client_id
                else:
                    st.session_state.child_client = client_id
                st.success(f"Successfully logged in as {account_type} account!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials!")