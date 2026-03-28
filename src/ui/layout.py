from pathlib import Path

import streamlit as st

PATH_ROOT = Path(__file__).parent.parent.parent
PAGES_DIR = PATH_ROOT / "pages"


def create_chart_button(location: str, scheme_code: str) -> bool:
    return st.button(
        "",
        icon=":material/show_chart:",
        key=f"{location}_chart_{scheme_code}",
        help="View the historical NAV chart for this scheme.",
    )


def create_remove_button(scheme_code: str) -> bool:
    return st.button(
        "", icon=":material/close:", type="primary", key=f"remove_{scheme_code}"
    )


def analyze_scheme(scheme_code: str) -> None:
    st.session_state["selected_scheme"] = scheme_code
    st.switch_page(PAGES_DIR / "2_Analyze_Scheme.py")


def remove_scheme(scheme_code: str) -> None:
    del st.session_state["watchlist"][scheme_code]
    st.rerun()


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
            chart_button = create_chart_button("watchlist", scheme_code)

        with remove_column:
            remove_button = create_remove_button(scheme_code)

        if chart_button:
            analyze_scheme(scheme_code)

        if remove_button:
            remove_scheme(scheme_code)
