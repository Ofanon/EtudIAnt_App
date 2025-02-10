import streamlit as st
import user_manager
import json
from streamlit_lottie import st_lottie

col1, col2 = st.columns(2)
with col1:
    st.title("🏆 Top 3 Leaderboard")

leaderboard_answers = user_manager.get_leaderboard_answers(limit=3)
leaderboard_xp = user_manager.get_leaderboard_xp(limit=3)
tab1, tab2 = st.tabs(tabs=["Classement par nombre de bonnes réponses", "Classement par nombre de Points d'Experience 🔥"])

if "robot_leaderboard" not in st.session_state:
    with open("robot_leaderboard.json","r") as f:
        st.session_state.robot_leaderboard = json.load(f)

with col2:
    st_lottie(st.session_state.robot_leaderboard, height=400, key="robot_leaderboard", loop=True)

with tab1:
    if leaderboard_answers:
        st.subheader("Classement des joueurs(euses) qui ont le plus de bonnes réponses :")

        for i, (user_id, corrects_answers) in enumerate(leaderboard_answers, start=1):
            if i == 1:
                st.write(f"🥇 **{i}. {user_id}** - {corrects_answers} bonnes réponses")
            elif i == 2:
                st.write(f"🥈 **{i}. {user_id}** - {corrects_answers} bonnes réponses")
            elif i == 3:
                st.write(f"🥉 **{i}. {user_id}** - {corrects_answers} bonnes réponses")
            else:
                st.write(f"✨ {i}. {user_id} - {corrects_answers} bonnes réponses")
    else:
        st.write("Personne n'a encore gagné de points ! 🚀")

with tab2:
    if leaderboard_xp:

        st.subheader("Classement des joueurs(euses) qui ont le plus de Points d'Experience 🔥 :")

        for i, (user_id, corrects_answers) in enumerate(leaderboard_xp, start=1):
            if i == 1:
                    st.write(f"🥇 **{i}. {user_id}** - {corrects_answers} 🔥")
            elif i == 2:
                    st.write(f"🥈 **{i}. {user_id}** - {corrects_answers} 🔥")
            elif i == 3:
                    st.write(f"🥉 **{i}. {user_id}** - {corrects_answers} 🔥")
            else:
                    st.write(f"✨ {i}. {user_id} - {corrects_answers} 🔥")
    else:
        st.write("Personne n'a encore gagné de points ! 🚀")
