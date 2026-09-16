import streamlit as st
import pandas as pd

from database import (
    initialize_database,
    add_observation,
    get_observations,
)

from ai_engine import (
    analyze_observation,
    generate_trend_summary,
    generate_session_brief,
)

from analytics import build_analytics_data


st.set_page_config(
    page_title="AutiTrack AI",
    page_icon="🧩",
    layout="wide",
)


initialize_database()


st.title("🧩 AutiTrack AI")

st.caption(
    "AI-assisted developmental observation tracking "
    "and longitudinal pattern summarization."
)

st.warning(
    "AutiTrack AI is an observation-support tool. "
    "It does not diagnose autism or any medical condition."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Add Observation",
        "Dashboard",
        "AI Session Brief",
    ]
)


# --------------------------------------------------
# ADD OBSERVATION
# --------------------------------------------------

if page == "Add Observation":

    st.header("Add Observation")

    date = st.date_input(
        "Observation Date"
    )

    observation = st.text_area(
        "Observation",
        placeholder=(
            "Example: During playtime, the child "
            "joined another child and participated "
            "in the game."
        ),
        height=150,
    )

    context = st.selectbox(
        "Context",
        [
            "Home",
            "School",
            "Playground",
            "Therapy Session",
            "Community",
            "Other",
        ]
    )

    activity = st.text_input(
        "Activity",
        placeholder="Example: Group play"
    )

    if st.button(
        "Analyze Observation",
        type="primary"
    ):

        if not observation.strip():

            st.error(
                "Please enter an observation."
            )

        else:

            with st.spinner(
                "Analyzing observation..."
            ):

                result = analyze_observation(
                    observation_text=observation,
                    context=context,
                    activity=activity,
                )

            if "error" in result:

                st.error(
                    result["error"]
                )

                if "raw_response" in result:
                    st.code(
                        result["raw_response"]
                    )

            else:

                st.success(
                    "Observation analyzed successfully."
                )

                st.subheader(
                    "AI Analysis"
                )

                st.write(
                    "**Domains:**"
                )

                st.write(
                    ", ".join(
                        result.get(
                            "domains",
                            []
                        )
                    )
                )

                st.write(
                    "**Observed Behavior:**"
                )

                for behavior in result.get(
                    "observed_behavior",
                    []
                ):
                    st.write(
                        f"- {behavior}"
                    )

                st.write(
                    "**Trigger / Context:**"
                )

                st.write(
                    result.get(
                        "trigger"
                    ) or "Not specified"
                )

                st.write(
                    "**Summary:**"
                )

                st.info(
                    result.get(
                        "summary",
                        ""
                    )
                )

                if st.button(
                    "Save Observation"
                ):

                    add_observation(
                        date=str(date),
                        observation=observation,
                        context=context,
                        activity=activity,
                        domains=result.get(
                            "domains",
                            []
                        ),
                        observed_behavior=result.get(
                            "observed_behavior",
                            []
                        ),
                        trigger=result.get(
                            "trigger"
                        ),
                        summary=result.get(
                            "summary",
                            ""
                        ),
                    )

                    st.success(
                        "Observation saved."
                    )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

elif page == "Dashboard":

    st.header(
        "Observation Dashboard"
    )

    rows, columns = get_observations()

    df = pd.DataFrame(
        rows,
        columns=columns
    )

    if df.empty:

        st.info(
            "No observations recorded yet."
        )

    else:

        st.subheader(
            "Recorded Observations"
        )

        display_columns = [
            "date",
            "context",
            "activity",
            "domains",
            "summary",
        ]

        st.dataframe(
            df[display_columns],
            use_container_width=True,
        )

        st.divider()

        st.subheader(
            "Personal Baseline"
        )

        analytics_data = build_analytics_data(
            df
        )

        baseline = analytics_data[
            "baseline"
        ]

        recent = analytics_data[
            "recent"
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "Historical Observation Counts"
            )

            st.bar_chart(
                pd.Series(baseline)
            )

        with col2:

            st.write(
                "Recent Observation Counts"
            )

            st.bar_chart(
                pd.Series(recent)
            )

        st.subheader(
            "Context Patterns"
        )

        patterns = analytics_data[
            "context_patterns"
        ]

        if patterns:

            pattern_df = pd.DataFrame(
                patterns
            )

            st.dataframe(
                pattern_df,
                use_container_width=True,
            )

        else:

            st.info(
                "No context patterns available."
            )

        st.divider()

        st.subheader(
            "AI Trend Summary"
        )

        if st.button(
            "Generate Trend Summary"
        ):

            with st.spinner(
                "Generating summary..."
            ):

                result = generate_trend_summary(
                    analytics_data
                )

            if "error" in result:

                st.error(
                    result["error"]
                )

            else:

                st.write(
                    result.get(
                        "summary",
                        ""
                    )
                )

                if result.get(
                    "notable_changes"
                ):

                    st.write(
                        "**Notable Changes**"
                    )

                    for item in result[
                        "notable_changes"
                    ]:

                        st.write(
                            f"- {item}"
                        )

                if result.get(
                    "context_patterns"
                ):

                    st.write(
                        "**Context Patterns**"
                    )

                    for item in result[
                        "context_patterns"
                    ]:

                        st.write(
                            f"- {item}"
                        )

                if result.get(
                    "discussion_topics"
                ):

                    st.write(
                        "**Discussion Topics**"
                    )

                    for item in result[
                        "discussion_topics"
                    ]:

                        st.write(
                            f"- {item}"
                        )


# --------------------------------------------------
# SESSION BRIEF
# --------------------------------------------------

elif page == "AI Session Brief":

    st.header(
        "AI Professional Session Brief"
    )

    rows, columns = get_observations()

    df = pd.DataFrame(
        rows,
        columns=columns
    )

    if df.empty:

        st.info(
            "Add observations first."
        )

    else:

        analytics_data = build_analytics_data(
            df
        )

        session_data = {
            "observations": df[
                [
                    "date",
                    "context",
                    "activity",
                    "domains",
                    "observed_behavior",
                    "summary",
                ]
            ].to_dict(
                orient="records"
            ),
            "analytics": analytics_data,
        }

        if st.button(
            "Generate Session Brief",
            type="primary"
        ):

            with st.spinner(
                "Generating session brief..."
            ):

                result = generate_session_brief(
                    session_data
                )

            if "error" in result:

                st.error(
                    result["error"]
                )

            else:

                st.subheader(
                    "Observation Overview"
                )

                st.write(
                    result.get(
                        "observation_overview",
                        ""
                    )
                )

                st.subheader(
                    "Recent Changes"
                )

                for item in result.get(
                    "recent_changes",
                    []
                ):

                    st.write(
                        f"- {item}"
                    )

                st.subheader(
                    "Contextual Patterns"
                )

                for item in result.get(
                    "contextual_patterns",
                    []
                ):

                    st.write(
                        f"- {item}"
                    )

                st.subheader(
                    "Notable Observations"
                )

                for item in result.get(
                    "notable_observations",
                    []
                ):

                    st.write(
                        f"- {item}"
                    )

                st.subheader(
                    "Discussion Points"
                )

                for item in result.get(
                    "discussion_points",
                    []
                ):

                    st.write(
                        f"- {item}"
                    )

                st.divider()

                st.caption(
                    "This brief summarizes recorded observations "
                    "for discussion with a qualified professional. "
                    "It is not a diagnosis."
                )
