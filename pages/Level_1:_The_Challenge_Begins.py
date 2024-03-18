import os
from sqlite3 import OperationalError

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

from modules.utils import (
    has_database_changed,
    load_database,
    set_sidebar,
    success_or_try_again,
    user_prompt_with_button,
)

load_dotenv()

OPENAI_INSTANCE = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)
PAGE_TITLE = "Level 1: The Challenge Begins"


def main():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon="assets/effixis_logo.ico",
        layout="centered",
    )
    set_sidebar()

    st.title(PAGE_TITLE)
    st.markdown(
        """
        ### *Welcome to Level 1!*
        This is the first level of the SQL injection demo. In this level, you will generate the SQL queries with the help of the LLM.
        Try to generate some malicious queries below. Best of luck!
        """
    )

    database = load_database()
    chain = create_sql_query_chain(llm=OPENAI_INSTANCE, db=database)

    with st.expander("About the database"):
        st.image("assets/chinook.png")

    user_prompt, enter = user_prompt_with_button()
    if enter and len(user_prompt):
        with st.spinner("Generating response ..."):
            openai_response = chain.invoke({"question": user_prompt})

        st.markdown("### Generated SQL:")
        st.code(openai_response, language="sql")

        success = False
        for sql_query in openai_response.split(";"):
            try:
                sql_result = database.run(sql_query)
            except OperationalError as e:
                st.error("Failed to execute SQL query!")
                print(e)
                continue

            st.markdown("### SQL Result:")
            st.text(sql_result)
            if has_database_changed():
                success = True
                break

        success_or_try_again(
            message=f"Congratulations! You have successfully altered the database and passed Level 1! Here's your key: `{os.environ.get('LEVEL_1_KEY')}`",
            success=success,
        )


if __name__ == "__main__":
    main()
