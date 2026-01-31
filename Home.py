import streamlit as st
from src.core.state import init_state
from src.ui.layout import sidebar_watchlist

def main():
    init_state()

    st.set_page_config(
        page_title="Mutual Fund Analyzer"
    )

    st.write("# Mutual Fund Analyzer")

    sidebar_watchlist()

    st.markdown(
        """
        This application allows you to analyze mutual funds using data from the MFAPI.

        ## Features
        - Search for mutual fund schemes
        - View latest NAVs
        - Analyze NAV history
        - User-friendly interface built with Streamlit
        - Powered by MFAPI for reliable mutual fund data

        ## Get Started
        - Use the sidebar to navigate through different features of the app.
        - Explore the various functionalities and make informed investment decisions!

        ### Happy Investing!
    """
    )


if __name__ == "__main__":
    main()
