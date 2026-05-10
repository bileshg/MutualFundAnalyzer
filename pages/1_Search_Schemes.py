from typing import Any

import requests
import streamlit as st
from pydantic import ValidationError

from src.core.state import init_state
from src.mfapi.client import MFAPIClient
from src.mfapi.model import NAVHistoryResponse, NAVHistoryStatus, SchemeSearchResult
from src.ui.layout import analyze_scheme, create_chart_button, sidebar_watchlist

TITLE = "Mutual Fund Analyzer - Search"
DATA_ERROR_TYPES = (requests.RequestException, ValidationError)

st.set_page_config(page_title=TITLE)


@st.cache_data(ttl=3600)
def cached_search_schemes(query: str) -> list[SchemeSearchResult]:
    return MFAPIClient().search_schemes(query)


@st.cache_data(ttl=3600)
def cached_get_latest_nav(scheme_code: str) -> NAVHistoryResponse:
    return MFAPIClient().get_latest_nav(scheme_code)


def create_watchlist_button(scheme_code: str) -> bool:
    return st.button(
        "",
        icon=":material/bookmark_add:",
        key=f"watchlist_{scheme_code}",
        help="Add this scheme to your watchlist for easy access later.",
    )


def render_scheme_details(
    scheme_details: NAVHistoryResponse, expanded: bool = False
) -> None:
    scheme_code_str = str(scheme_details.meta.scheme_code)

    with st.expander(
        f'Details for :yellow[**"{scheme_details.meta.scheme_name}"**]',
        expanded=expanded,
    ):
        label_column, value_column = st.columns([0.3, 0.7], gap="small")
        with label_column:
            st.markdown("**Fund House:**")
            st.markdown("**Scheme Type:**")
            st.markdown("**Scheme Category:**")
            st.markdown("**Latest NAV Date:**")
            st.markdown("**Latest NAV Value:**")
        with value_column:
            latest_nav = scheme_details.data[0] if scheme_details.data else None
            st.markdown(scheme_details.meta.fund_house or "N/A")
            st.markdown(scheme_details.meta.scheme_type or "N/A")
            st.markdown(scheme_details.meta.scheme_category or "N/A")
            st.markdown(latest_nav.date if latest_nav else "N/A")
            st.markdown(latest_nav.nav if latest_nav else "N/A")

        if scheme_details.status != NAVHistoryStatus.SUCCESS or not scheme_details.data:
            st.warning("Latest NAV is not available for this scheme right now.")

        with st.container(
            horizontal=True,
            horizontal_alignment="right",
            vertical_alignment="center",
            gap="small",
        ):
            watchlist_button = create_watchlist_button(scheme_code_str)
            chart_button = create_chart_button("search", scheme_code_str)

    if watchlist_button:
        if scheme_code_str not in st.session_state["watchlist"]:
            st.session_state["watchlist"][scheme_code_str] = scheme_details
            st.success(
                f'Scheme ":green[**{scheme_details.meta.scheme_name}**]" added to watchlist.'
            )
            st.rerun()
        else:
            st.info(
                f'Scheme ":green[**{scheme_details.meta.scheme_name}**]" is already in the watchlist.'
            )

    if chart_button:
        analyze_scheme(scheme_code_str)


def render_schemes(schemes: list[SchemeSearchResult]) -> None:
    def create_row() -> list[Any]:
        return st.columns([0.15, 0.85], gap="small", vertical_alignment="center")

    header_code_column, header_name_column = create_row()

    with header_code_column:
        st.markdown("**Scheme Code**")
    with header_name_column:
        st.markdown("**Scheme Name**")

    buttons = []
    for index, scheme in enumerate(schemes):
        code_column, name_column = create_row()
        with code_column:
            buttons.append(
                st.button(
                    f":green[**{scheme.scheme_code}**]",
                    key=f"search_{scheme.scheme_code}",
                    help=f'Click to view details for "{scheme.scheme_name}"',
                )
            )
        with name_column:
            st.markdown(scheme.scheme_name)

        session_state_key = str(scheme.scheme_code)
        if session_state_key in st.session_state:
            render_scheme_details(st.session_state[session_state_key], expanded=False)
            buttons[index] = False  # Reset button to avoid re-fetching

        if buttons[index]:
            try:
                scheme_details = cached_get_latest_nav(str(scheme.scheme_code))
            except DATA_ERROR_TYPES:
                st.error(
                    "Unable to load scheme details right now. Please try again later."
                )
                continue
            st.session_state[session_state_key] = scheme_details
            render_scheme_details(scheme_details, expanded=True)


def render_results(query: str) -> None:
    if query:
        try:
            result = cached_search_schemes(query)
        except DATA_ERROR_TYPES:
            st.error("Unable to search schemes right now. Please try again later.")
            return

        if result:
            render_schemes(result)
        else:
            st.warning("No mutual fund schemes found for the given query.")
    else:
        st.error("Please enter a search query to find mutual fund schemes.")


def main():
    init_state()

    sidebar_watchlist()

    st.title(TITLE)
    st.write("This is the search page for the Mutual Fund Analyzer application.")

    input_column, search_column = st.columns(
        [0.8, 0.2], gap="small", vertical_alignment="bottom"
    )
    with input_column:
        query = st.text_input(
            label="Search Mutual Fund Schemes",
            placeholder="Enter query to search mutual fund schemes",
        )
    with search_column:
        search_button = st.button("Search", width="stretch", type="primary")

    st.divider()

    if query or search_button:
        render_results(query)


if __name__ == "__main__":
    main()
