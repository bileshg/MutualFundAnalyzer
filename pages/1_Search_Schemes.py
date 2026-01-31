from typing import Any

import streamlit as st

from src.core.state import init_state
from src.mfapi.client import MFAPIClient
from src.mfapi.model import NAVHistoryResponse, SchemeSearchResult
from src.ui.layout import sidebar_watchlist


def render_scheme_details(
    scheme_details: NAVHistoryResponse, expanded: bool = False
) -> None:
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
            st.markdown(scheme_details.meta.fund_house or "N/A")
            st.markdown(scheme_details.meta.scheme_type or "N/A")
            st.markdown(scheme_details.meta.scheme_category or "N/A")
            st.markdown(scheme_details.data[0].date)
            st.markdown(scheme_details.data[0].nav)

        watchlist_button = st.button(
            ":green[Add to Watchlist]",
            key=f"watchlist_{scheme_details.meta.scheme_code}",
        )

    if watchlist_button:
        watchlist_key = str(scheme_details.meta.scheme_code)
        if watchlist_key not in st.session_state["watchlist"]:
            st.session_state["watchlist"][watchlist_key] = scheme_details
            st.success(
                f'Scheme ":green[**{scheme_details.meta.scheme_name}**]" added to watchlist.'
            )
            st.rerun()
        else:
            st.info(
                f'Scheme ":green[**{scheme_details.meta.scheme_name}**]" is already in the watchlist.'
            )


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
                )
            )
        with name_column:
            st.markdown(scheme.scheme_name)

        session_state_key = str(scheme.scheme_code)
        if session_state_key in st.session_state:
            render_scheme_details(st.session_state[session_state_key], expanded=False)
            buttons[index] = False  # Reset button to avoid re-fetching

        if buttons[index]:
            scheme_details = MFAPIClient().get_latest_nav(scheme.scheme_code)
            st.session_state[session_state_key] = scheme_details
            render_scheme_details(scheme_details, expanded=True)


def render_results(query: str) -> None:
    if query:
        result = MFAPIClient().search_schemes(query)
        if result:
            render_schemes(result)
        else:
            st.warning("No mutual fund schemes found for the given query.")
    else:
        st.error("Please enter a search query to find mutual fund schemes.")


def main():
    init_state()

    sidebar_watchlist()

    title = "Mutual Fund Analyzer - Search"

    st.set_page_config(page_title=title)

    st.title(title)
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
