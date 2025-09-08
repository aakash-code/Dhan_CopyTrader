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
        
        # ... rest of the sidebar code ...
        
    return selected

# Make sure the function is available for import
__all__ = ['sidebar']