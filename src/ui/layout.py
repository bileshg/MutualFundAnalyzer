from pathlib import Path
from tkinter.constants import PAGES

import streamlit as st

PATH_ROOT = Path(__file__).parent.parent.parent
PAGES_DIR = PATH_ROOT / "pages"


def sidebar_watchlist() -> None:
    st.sidebar.subheader("Watchlist")

    watchlist = st.session_state.get("watchlist", {})
    if not watchlist:
        st.sidebar.info("No schemes added yet.")
        return None

    for scheme_code, scheme_details in watchlist.items():
        label_column, chart_column, remove_column = st.sidebar.columns(
            [0.8, 0.1, 0.1], gap="xsmall"
        )
        with label_column:
            st.markdown(scheme_details.meta.scheme_name)
        with chart_column:
            chart_button = st.button(
                "",
                icon=":material/show_chart:",
                key=f"chart_{scheme_code}",
            )
        with remove_column:
            remove_button = st.button(
                "", icon=":material/close:", type="primary", key=f"remove_{scheme_code}"
            )

        if chart_button:
            st.session_state["selected_scheme"] = scheme_code
            st.switch_page(PAGES_DIR / "2_Analyze_Scheme.py")

        if remove_button:
            del st.session_state["watchlist"][scheme_code]
            st.rerun()
