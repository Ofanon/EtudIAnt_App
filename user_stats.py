import streamlit as st
import user_manager
from streamlit_echarts import st_echarts

st.title("🚀 Ma progression")

if "stats_subject" not in st.session_state:
    st.session_state.stats_subject = None

st.info("Données prises en compte depuis le 11/02/2025.")

with st.container(border=True, key="stats_1"):
    st.subheader("🎯 Les chiffres importants :")
    st.write(f"🎯 Tu as complété {user_manager.get_total_quiz_count(user_id=st.session_state.user_id)} quizs interactifs !")
    st.write(f"📈 Ta moyenne est de {user_manager.get_average_quiz_score(user_id=st.session_state.user_id)} bonnes réponses par quiz interactifs !")

with st.container(border=True, key="stats_2"):
    st.subheader("📈 Données des quizs :")
    st.session_state.stats_subject = st.selectbox(
        "Matière du quiz :",
        user_manager.get_stats(user_id=st.session_state.user_id, column="subject")
    )

    if st.session_state.stats_subject:
        with st.spinner("Chargement des données..."):
            progression_df = user_manager.progression_user(
                user_id=st.session_state.user_id, 
                subject=st.session_state.stats_subject
            )
    else:
        progression_df = None
        
    if progression_df is not None and not progression_df.empty:
        dates = progression_df["Date"].astype(str).tolist()
        bonnes_reponses = progression_df["Bonnes Réponses"].tolist()
        mauvaises_reponses = progression_df["Mauvaises Réponses"].tolist()
        notes = progression_df["Note sur 20"].tolist()

        options = {
            "title": {"text": "Évolution de tes performances"},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": ["Bonnes Réponses", "Mauvaises Réponses", "Note sur 20"]},
            "xAxis": {"type": "category", "data": dates},
            "yAxis": {"type": "value"},
            "series": [
                {
                    "name": "Bonnes Réponses",
                    "type": "line",
                    "data": bonnes_reponses,
                    "smooth": True,
                    "areaStyle": {},
                    "lineStyle": {"width": 3},
                    "symbolSize": 8,
                },
                {
                    "name": "Mauvaises Réponses",
                    "type": "line",
                    "data": mauvaises_reponses,
                    "smooth": True,
                    "areaStyle": {},
                    "lineStyle": {"width": 3, "type": "dashed"},  # Style différent
                    "symbolSize": 8,
                },
                {
                    "name": "Note sur 20",
                    "type": "line",
                    "data": notes,
                    "smooth": True,
                    "areaStyle": {},
                    "lineStyle": {"width": 2, "color": "#ff7f0e"},  # Couleur spécifique
                    "symbolSize": 8,
                }
            ],
        }

        st_echarts(options=options, height="500px")
    else:
        st.info("Pas de données pour l'instant.")

