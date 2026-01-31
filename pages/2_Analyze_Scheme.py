import streamlit as st

from src.core.state import init_state
from src.data.transform import process_nav_data
from src.mfapi.client import MFAPIClient
from src.ui.layout import sidebar_watchlist


def render_chart() -> None:
    client = MFAPIClient()

    scheme_code = st.session_state.get("selected_scheme")

    if not scheme_code:
        st.info("Please select a scheme from the watchlist to view its chart.")
        return

    nav_history = client.get_nav_data(scheme_code)

    st.write(f"### {nav_history.meta.scheme_name}")
    nav_data_df = process_nav_data(nav_history.data)
    st.line_chart(
        nav_data_df,
        x="Date",
        y=["NAV", "50_DMA", "200_DMA"],
        color=["#0055AA", "#BB3300", "#AA5500"],
    )


def main() -> None:
    init_state()

    sidebar_watchlist()

    title = "Mutual Fund Analyzer - Chart"

    st.title(title)
    st.write("This is the chart page for the Mutual Fund Analyzer application.")

    render_chart()


if __name__ == "__main__":
    main()
