import pandas as pd
import streamlit as st

from recommendation_engine_streamlit.post_request import post_request


def app():
    st.title("Recommendation Engine")

    with st.form("my_form"):
        token = st.text_input(
            "WF-USER-TOKEN",
            help="Your WF-USER-TOKEN. Update this info button to show people where they can find their token.",
        )

        number_recommendations = st.slider(
            label="Number of recommendations",
            min_value=1,
            value=3,
            max_value=5,
        )
        max_availability = (
            st.slider(
                "Available time (min)",
                min_value=0,
                value=60,
                max_value=180,
            )
            * 60
        )
        motivation_score = st.slider(
            label="Motivation score",
            min_value=0,
            value=5,
            max_value=10,
        )
        fatigue_score = st.slider(
            "Fatigue score",
            min_value=0,
            value=5,
            max_value=10,
        )

        workout_type_family_id = 0
        # workout_type_family_id = st.radio(
        # "workout_type_family_id", [0, 1], index=0, horizontal=True
        # )

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            response = post_request(
                token,
                number_recommendations,
                max_availability,
                motivation_score,
                fatigue_score,
                workout_type_family_id,
            )
            recommendations = response.json()

            for i, recommendation in enumerate(recommendations):
                with st.container(border=True):
                    st.header(f"""#{i+1} {recommendation["plan"]["name"]}""")
                    st.subheader("Why we think you will love this")
                    st.write(" and ".join(recommendation["reasons"]))
                    st.subheader("What's the workout")
                    st.write(recommendation["plan"]["description"])
                    # st.write(recommendation["plan"]["file"]["url"])
                    st.subheader("Give me the stats")
                    df = pd.DataFrame(
                        recommendation["plan"]["plan_metric"],
                        index=[0],
                    )[
                        [
                            "nm",
                            "map",
                            "ac",
                            "ftp",
                            "duration",
                            "tss",
                            "intensity_factor",
                        ]
                    ].rename(
                        columns={
                            "intensity_factor": "if",
                            "duration": "minutes",
                        }
                    )
                    df["minutes"] = (df["minutes"] / 60) // 1
                    st.dataframe(df)

            with st.expander("Inspect JSON"):
                st.write(recommendations)


if __name__ == "__main__":
    app()
