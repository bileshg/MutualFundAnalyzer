import streamlit as st


def init_state():
    st.session_state.setdefault("watchlist", {})
    st.session_state.setdefault("selected_scheme", None)
