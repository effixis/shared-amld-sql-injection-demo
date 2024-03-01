import shutil
import streamlit as st
import hashlib
from langchain_community.utilities import SQLDatabase


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


@st.cache_resource(show_spinner="Loading database ...")
def load_database() -> SQLDatabase:
    st.session_state["original_checksum"] = calculate_file_checksum(
        "./data/chinook_working.db"
    )
    return SQLDatabase.from_uri("sqlite:///data/chinook_working.db")


def reset_database():
    """Copy original database to working database"""
    shutil.copyfile("./data/chinook_backup.db", "./data/chinook_working.db")
    return SQLDatabase.from_uri("sqlite:///data/chinook_working.db")


def calculate_file_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def has_database_changed() -> bool:
    """Check if the working database has been changed"""
    current_checksum = calculate_file_checksum("./data/chinook_working.db")
    return current_checksum != st.session_state["original_checksum"]
