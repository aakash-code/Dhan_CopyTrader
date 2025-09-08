import streamlit as st

def sidebar():
    with st.sidebar:
        st.title("Dhan Copy Trader")
        
        # Navigation
        selected = st.radio(
            "Navigation",
            ["Home", "Dashboard"],
            index=0 if not st.session_state.login_status else 1
        )
        
        st.divider()
        
        # Account status
        if st.session_state.login_status:
            st.success("Connected to Dhan")
            
            # Show account details
            st.markdown("### Account Details")
            if st.session_state.master_client:
                st.info(f"Master Account: {st.session_state.master_client}")
            if st.session_state.child_client:
                st.info(f"Child Account: {st.session_state.child_client}")
            
            # Logout button
            if st.button("Logout"):
                st.session_state.login_status = False
                st.session_state.master_client = None
                st.session_state.child_client = None
                st.experimental_rerun()
        
        st.markdown("---")
        
        # Copy trading status
        st.markdown("### Copy Trading Status")
        status = "🟢 Active" if st.session_state.login_status else "🔴 Inactive"
        st.markdown(f"Status: {status}")
        
        # Version info
        st.markdown("---")
        st.markdown("v1.0.0")
        
    return selected