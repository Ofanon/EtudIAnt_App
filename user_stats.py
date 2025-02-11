import streamlit as st
import user_manager
from streamlit_echarts import st_echarts

st.title("🚀 Ma progression")

if "stats_subject" not in st.session_state:
    st.session_state.stats_subject = None

st.info("Données prises en compte depuis le 11/02/2025.")

with st.container(border=True, key="stats_1"):
    st.subheader(f"🎯 Tu as complété {user_manager.get_total_quiz_count(user_id=st.session_state.user_id)} quizs interactifs !")
    st.subheader(f"📈 Ta moyenne en quiz est de {user_manager.get_average_quiz_score(user_id="oscar")} bonnes réponses !")

with st.container(border=True, key="stats_2"):
    st.session_state.stats_subject = st.selectbox("Mes matières de quizs", user_manager.get_stats(user_id=st.session_state.user_id, column="subject"))
    if st.session_state.stats_subject:
        progression_df = user_manager.progression_user(user_id=st.session_state.user_id, subject=st.session_state.stats_subject)

    if not progression_df.empty:
        dates = progression_df["Date"].astype(str).tolist()
        scores = progression_df["Bonnes Réponses"].tolist()

        options = {
            "title": {"text": "Évolution de tes bonnes réponses"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": dates},
            "yAxis": {"type": "value"},
            "series": [
                {
                    "name": "Bonnes Réponses",
                    "type": "line",
                    "data": scores,
                    "smooth": True,
                    "areaStyle": {},
                    "lineStyle": {"width": 3},
                    "symbolSize": 8,
                }
            ],
        }

        st_echarts(options=options, height="500px")
    else:
        st.info("Pas de données pour l'instant.")