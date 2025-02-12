import streamlit as st
import user_manager
import json
from streamlit_lottie import st_lottie

col1, col2 = st.columns(2)
with col1:
    st.title("🏆 Top 3 Leaderboard")

leaderboard_xp = user_manager.get_leaderboard_answers(limit=3)

if "robot_leaderboard" not in st.session_state:
    with open("robot_leaderboard.json","r") as f:
        st.session_state.robot_leaderboard = json.load(f)

with col2:
    st_lottie(st.session_state.robot_leaderboard, height=400, key="robot_leaderboard", loop=True)

if leaderboard_xp:

    st.subheader("Classement des joueurs(euses) de l'EtudIAnt :")
    st.info("Rentre dans le classement en ayant le maximum de bonnes réponses dans les quizs !")

    for i, (user_id, corrects_answers) in enumerate(leaderboard_xp, start=1):
        if i == 1:
            st.write(f"🥇 **{i}. {user_id}** - {corrects_answers*10} points")
        elif i == 2:
            st.write(f"🥈 **{i}. {user_id}** - {corrects_answers*10} points")
        elif i == 3:
            st.write(f"🥉 **{i}. {user_id}** - {corrects_answers*10} points")
        else:
            st.write(f"✨ {i}. {user_id} - {corrects_answers*10} points")
else:
    st.write("Personne n'a encore gagné de points ! 🚀")
