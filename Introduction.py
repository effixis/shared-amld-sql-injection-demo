import streamlit as st
from modules.utils import set_sidebar


def main():
    st.set_page_config(
        page_title="AMLD SQL injection demo",
        page_icon="assets/effixis_logo.ico",
        layout="centered",
    )
    set_sidebar()
    st.title("SQL Injections via LLM\:s")
    st.markdown("### *Welcome to Effixis' demo for AMLD EPFL 2024!* 🎉")

    st.markdown(
        """
        #### What is this demo about?
        This demo is about risk associated with the use of LLM\:s, in this case illustrated by SQL injections.
        SQL injections are a common vulnerability in web applications.
        They allow an attacker to execute arbitrary SQL code on the database server.
        This a very dangerous vulnerability as it can lead to data leaks, data corruption, and even data loss.

        #### The SQL database used in this demo
        The database used in this demo is the Chinook database.
        It is a sample database that represents a digital media store, including tables for artists, albums, media tracks, invoices and customers.

        You can see the shema below:
        """
    )
    st.image("assets/chinook.png")

    st.markdown(
        """
        #### What does LLM\:s have to do with this?
        A large usecase for large language models (LLM\:s) is to generate SQL queries.
        This is a very useful feature, as it allows users to interact with databases without having to know SQL.
        But this is also prone to SQL injections, as the users and by extension the LLM\:s, can generate malicious SQL queries.
        """
    )

    st.divider()
    st.markdown(
        """
        #### The levels
        Try to inject malicoius SQL code to alter the SQL table, each level is more difficult than the previous one!

        - **Level 0**: You generate the SQL queries with the help of the LLM.
        - **Level 1**: The SQL queries are first checked by an LLM Safeguard, which detects and removes malicious SQL queries.

        Are you happy with your results? Submit the keys on the leaderboard to see how you compare to others!
        """
    )


if __name__ == "__main__":
    main()
