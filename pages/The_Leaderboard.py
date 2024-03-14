import os

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

from modules.utils import set_sidebar

load_dotenv()

PAGE_TITLE = "The Leaderboard"

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="assets/effixis_logo.ico",
    layout="centered",
)
set_sidebar()

st.title(PAGE_TITLE)

st.markdown(
    """
    ### *Welcome to the leaderboard!*
    Here you can submit your keys and see how you compare to others!
    """
)

# Display leaderboard
url = f"https://getpantry.cloud/apiv1/pantry/{os.environ.get('PANTRY_ID')}/basket/{os.environ.get('PANTRY_BASKET')}"
leaderboard_response = requests.get(url)
if leaderboard_response.status_code == 200:
    leaderboard_json = leaderboard_response.json()
    leaderboard_data = (
        pd.DataFrame(leaderboard_json)
        .T[["level 0", "level 1", "level 2"]]
        .applymap(lambda x: "✅" if x else "❌")
    )
    leaderboard_data = leaderboard_data.rename(
        columns={"level 0": "Level 0", "level 1": "Level 1", "level 2": "Level 2"}
    )
    leaderboard_data["Score"] = leaderboard_data.apply(
        lambda x: x.value_counts().get("✅", 0) * 100, axis=1
    )
    leaderboard_data = leaderboard_data.sort_values(by="Score", ascending=False)
    leaderboard_data = leaderboard_data.reset_index()
    leaderboard_data = leaderboard_data.rename(columns={"index": "Name"})
    leaderboard_data.index += 1
    st.dataframe(leaderboard_data)
else:
    st.error("An error occurred while fetching the leaderboard.")


# Submit keys
with st.form("leaderboard"):
    key = st.text_input("Enter your key here:")
    email = st.text_input("Enter your email here:")
    display_name = st.text_input("Enter your leaderboard display name here:")
    st.markdown(
        "*Note: Your email will not be displayed on the leaderboard, it is only used to contact you if you win!*"
    )
    submit = st.form_submit_button("Submit")

    if submit and key and email and display_name:
        if (
            display_name in leaderboard_json.keys()
            and email != leaderboard_json[display_name]["email"]
        ):
            st.error("This display name is already taken, please choose another one.")
        else:
            try:
                if display_name not in leaderboard_json.keys():
                    data = {
                        display_name: {
                            "email": email,
                            "level 0": key == os.environ.get("LEVEL_0_KEY"),
                            "level 1": key == os.environ.get("LEVEL_1_KEY"),
                            "level 2": key == os.environ.get("LEVEL_2_KEY"),
                        }
                    }
                else:
                    data = {
                        display_name: {
                            "email": email,
                            "level 0": key == os.environ.get("LEVEL_0_KEY")
                            or leaderboard_data[
                                leaderboard_data["Name"] == display_name
                            ]["Level 0"].values[0]
                            == "✅",
                            "level 1": key == os.environ.get("LEVEL_1_KEY")
                            or leaderboard_data[
                                leaderboard_data["Name"] == display_name
                            ]["Level 1"].values[0]
                            == "✅",
                            "level 2": key == os.environ.get("LEVEL_2_KEY")
                            or leaderboard_data[
                                leaderboard_data["Name"] == display_name
                            ]["Level 2"].values[0]
                            == "✅",
                        }
                    }
                updated_data = leaderboard_json
                updated_data.update(data)
                response = requests.post(url, json=updated_data)

                st.success(
                    "You should soon be able to see your name and your scores on the leaderboard! 🎉"
                )
            except Exception as e:
                st.error(f"An error occurred while submitting your key: {e}")
