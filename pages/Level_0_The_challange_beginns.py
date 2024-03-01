import os
import streamlit as st
import sqlite3
from dotenv import load_dotenv
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from modules.utils import (
    set_sidebar,
    load_database,
    reset_database,
    has_database_changed,
)

load_dotenv()
openai_instance = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)

st.set_page_config(
    page_title="Level 0: The challange beginns",
    page_icon="assets/effixis_logo.ico",
    layout="centered",
)

set_sidebar()

st.title("Level 0: SQL Injections via LLM\:s")

st.markdown(
    """
    ### *Welcome to level 0!*
    This is the first level of the SQL injection demo. In this level, you will generate the SQL queries with the help of the LLM. 
    Try to generate some malicius queries below. Best of luck!
    """
)

if st.button("Reset database"):
    database = reset_database()
else:
    database = load_database()
chain = create_sql_query_chain(llm=openai_instance, db=database)
success = False

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
                if has_database_changed():
                    success = True
                    st.balloons()
            except sqlite3.OperationalError as e:
                st.error(e)
        if success:
            st.success(
                f"Congratulations! You have successfully altered the database and passed level 0! Here's your key: `{os.environ.get('LEVEL_0_KEY')}`"
            )
