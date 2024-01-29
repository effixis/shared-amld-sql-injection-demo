import streamlit as st

def set_sidebar():
    with st.sidebar:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.header("Effixis")
            st.markdown(
                """***Take your Artificial Intelligence projects to the next level.***"""
            )
        with col2:
            st.image("assets/effixis_logo.ico", use_column_width=True)
        st.markdown(
            """
            #### About Effixis
            *Effixis was founded in 2017, in close proximity to the Swiss Institute of Technology in Lausanne (EPFL), with the goal of making data analytics and machine learning accessible to private companies and public institutions.
            Since then, we have expanded our reach and opened offices in Brussels in 2022.
            Our company specializes in Natural Language Processing (NLP), Large Language Models (LLMs), and proprietary technologies, allowing us to offer top-tier services and products to our clients and partners.
            We are dedicated to fostering long-term and reliable partnerships with our clients through our innovative approaches, and unwavering commitment.*
            """
        )
        st.markdown("#### Learn more about us at: https://effixis.ch/")
        st.markdown("---")