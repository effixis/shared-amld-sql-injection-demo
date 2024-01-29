import shutil
import streamlit as st
import sqlite3
from dotenv import load_dotenv
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from modules.utils import set_sidebar


@st.cache_resource(show_spinner="Loading database ...")
def load_database() -> SQLDatabase:
    return SQLDatabase.from_uri("sqlite:///data/chinook_working.db")


def reset_database():
    """Copy original database to working database"""
    shutil.copyfile("./data/chinook_backup.db", "./data/chinook_working.db")
    return SQLDatabase.from_uri("sqlite:///data/chinook_working.db")


load_dotenv()
openai_instance = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)


def main():
    st.set_page_config(
        page_title="AMLD SQL injection demo", page_icon="assets/effixis_logo.ico", layout="centered"
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
    st.markdown("#### **Try to generate some malicius queries below!**")

    if st.button("Reset database"):
        database = reset_database()
    else:
        database = load_database()
    chain = create_sql_query_chain(llm=openai_instance, db=database)

    if user_request := st.text_input("Enter your request here:"):
        with st.spinner("Generating response ..."):
            openai_response = chain.invoke({"question": user_request})
            st.markdown("## Result:")
            st.markdown(f"**SQL Response:** {openai_response}")
            st.markdown("## SQL Result:")
            for sql_query in openai_response.split(";"):
                try:
                    sql_result = database.run(sql_query)
                    if sql_result:
                        st.code(sql_result)
                except sqlite3.OperationalError as e:
                    st.error(e)


if __name__ == "__main__":
    main()
