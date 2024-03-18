import os

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

from modules.utils import set_sidebar

load_dotenv()

PANTRY_ID = os.environ.get("PANTRY_ID")
PANTRY_BASKET = os.environ.get("PANTRY_BASKET")
assert (
    PANTRY_ID is not None and PANTRY_BASKET is not None
), "Pantry ID and basket name must be set in .env file."


PAGE_TITLE = "The Leaderboard"

pd.set_option("future.no_silent_downcasting", True)


def _user_passed_level(df: pd.DataFrame, name: str, level: str) -> bool:
    return df.loc[df["Name"] == name, level].values[0] == "✅"


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
        ### *Welcome to the leaderboard!*
        Here you can submit your keys and see how you compare to others!
        """
    )

    # Display leaderboard
    leaderboard_url = (
        f"https://getpantry.cloud/apiv1/pantry/{PANTRY_ID}/basket/{PANTRY_BASKET}"
    )
    leaderboard_response = requests.get(leaderboard_url)
    if leaderboard_response.status_code == 200:
        leaderboard_json = leaderboard_response.json()
        print(f"Leaderboard data: {leaderboard_json}")
        leaderboard_data = (
            pd.DataFrame(leaderboard_json)
            .transpose()
            .rename(
                columns={
                    "level 0": "Level 1",
                    "level 1": "Level 2",
                    "level 2": "Level 3",
                },
            )[["Level 1", "Level 2", "Level 3"]]
            .fillna(False)
            .map(lambda x: "✅" if x else "❌")
            .assign(
                # Weighted sum of the levels
                Score=lambda df: df.apply(
                    lambda x: sum(
                        [int(passing == "✅") * (i + 1) for i, passing in enumerate(x)]
                    ),
                    axis=1,
                )
            )
            .sort_values(by="Score", ascending=False)
            .reset_index()
            .rename(columns={"index": "Name"})
        )
        st.dataframe(leaderboard_data)
    else:
        st.error("An error occurred while fetching the leaderboard.")
        st.stop()

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
                st.error(
                    "This display name is already taken, please choose another one."
                )
            else:
                if key not in {
                    os.environ.get("LEVEL_1_KEY"),
                    os.environ.get("LEVEL_2_KEY"),
                    os.environ.get("LEVEL_3_KEY"),
                }:
                    st.error("Invalid key!")
                    st.stop()

                if display_name not in leaderboard_json.keys():
                    data = {
                        display_name: {
                            "email": email,
                            "level 0": key == os.environ.get("LEVEL_1_KEY"),
                            "level 1": key == os.environ.get("LEVEL_2_KEY"),
                            "level 2": key == os.environ.get("LEVEL_3_KEY"),
                        }
                    }
                else:
                    data = {
                        display_name: {
                            "email": email,
                            "level 0": (
                                key == os.environ.get("LEVEL_1_KEY")
                                or _user_passed_level(
                                    leaderboard_data, display_name, "Level 1"
                                )
                            ),
                            "level 1": (
                                key == os.environ.get("LEVEL_2_KEY")
                                or _user_passed_level(
                                    leaderboard_data, display_name, "Level 2"
                                )
                            ),
                            "level 2": (
                                key == os.environ.get("LEVEL_3_KEY")
                                or _user_passed_level(
                                    leaderboard_data, display_name, "Level 3"
                                )
                            ),
                        }
                    }

                try:
                    updated_data = leaderboard_json | data
                    print(f"Updated data: {updated_data}")
                    _ = requests.post(leaderboard_url, json=leaderboard_json | data)

                    st.success(
                        "You should soon be able to see your name and your scores on the leaderboard! 🎉"
                    )
                except Exception as e:
                    st.error(f"An error occurred while submitting your key: {e}")


if __name__ == "__main__":
    main()
