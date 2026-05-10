import pandas as pd
import requests
import streamlit as st
from pydantic import ValidationError

from src.core.state import init_state
from src.data.transform import (
    NAV_ANALYSIS_COLUMNS,
    convert_to_csv_data,
    process_nav_data,
)
from src.mfapi.client import MFAPIClient
from src.mfapi.model import NAVHistoryResponse, NAVHistoryStatus
from src.ui.layout import sidebar_watchlist
from src.utils.string_utils import pascal_case

TITLE = "Mutual Fund Analyzer - Chart"
DATA_ERROR_TYPES = (requests.RequestException, ValidationError)

st.set_page_config(page_title=TITLE)


@st.cache_data(ttl=3600)
def cached_get_nav_data(scheme_code: str) -> NAVHistoryResponse:
    return MFAPIClient().get_nav_data(scheme_code)


def create_csv_export_button(df: pd.DataFrame, filename: str = "analysis.csv"):
    csv_bytes = convert_to_csv_data(df)
    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name=filename,
        mime="text/csv",
        icon=":material/download:",
        help="Download the NAV data as a CSV file for offline analysis.",
    )


def render_chart() -> None:
    scheme_code = st.session_state.get("selected_scheme")

    if not scheme_code:
        st.info("Please select a scheme from the watchlist to view its chart.")
        return

    try:
        nav_history = cached_get_nav_data(scheme_code)
    except DATA_ERROR_TYPES:
        st.error("Unable to load NAV history right now. Please try again later.")
        return

    if nav_history.status != NAVHistoryStatus.SUCCESS or not nav_history.data:
        st.warning("NAV history is not available for this scheme right now.")
        return

    st.write(f"### {nav_history.meta.scheme_name}")
    nav_data_df = process_nav_data(nav_history.data)

    if nav_data_df.empty or not set(NAV_ANALYSIS_COLUMNS).issubset(nav_data_df.columns):
        st.warning("There is not enough valid NAV history to build a chart.")
        return

    st.line_chart(
        nav_data_df,
        x="Date",
        y=["NAV", "50_DMA", "200_DMA"],
        color=["#0055AA", "#BB3300", "#AA5500"],
    )

    with st.container(
        horizontal=True,
        horizontal_alignment="right",
        vertical_alignment="center",
        gap="small",
    ):
        filename = f"{pascal_case(nav_history.meta.scheme_name)}_analysis.csv"
        create_csv_export_button(nav_data_df, filename=filename)


def main() -> None:
    init_state()

    sidebar_watchlist()

    st.title(TITLE)
    st.write("This is the chart page for the Mutual Fund Analyzer application.")

    render_chart()


if __name__ == "__main__":
    main()
