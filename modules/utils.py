import hashlib
import shutil

import streamlit as st
from langchain_community.utilities import SQLDatabase

WORKING_DB = "data/chinook_working.db"
BACKUP_DB = "data/chinook_backup.db"


def set_sidebar() -> None:
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
    return SQLDatabase.from_uri(f"sqlite:///{WORKING_DB}")


def _reset_database() -> SQLDatabase:
    """Copy original database to working database"""
    shutil.copyfile(f"./{BACKUP_DB}", f"./{WORKING_DB}")
    return SQLDatabase.from_uri(f"sqlite:///{WORKING_DB}")


def _calculate_file_checksum(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def has_database_changed() -> bool:
    """Check if the working database has been changed"""
    original_checksum = _calculate_file_checksum(BACKUP_DB)
    current_checksum = _calculate_file_checksum(WORKING_DB)
    return original_checksum != current_checksum


def user_prompt_with_button() -> tuple[str, bool]:
    user_request = st.text_input("Prompt:", placeholder="Enter your prompt here ...")
    enter = st.button("Enter", use_container_width=True)
    return user_request, enter


def success_or_try_again(message: str, success: bool) -> None:
    if success:
        st.balloons()
        st.success(message)
        _reset_database()
        st.stop()
    else:
        st.warning("The database was not altered.")
        st.info("Please try again.")
