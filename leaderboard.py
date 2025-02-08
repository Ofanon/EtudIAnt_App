import streamlit as st
import user_manager

st.title("🏆 Top 5 Leaderboard")

# Récupérer le top 5
leaderboard_answers = user_manager.get_leaderboard_answers(limit=3)
leaderboard_xp = user_manager.get_leaderboard_xp(limit=3)

if leaderboard_answers:
    st.write("Voici le classement des 3 joueurs avec le meilleur nombre de bonne réponses :")

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

if leaderboard_xp:
    st.write("Voici le classement des 3 joueurs avec le plus de Points d'Experience :")

    for i, (user_id, corrects_answers) in enumerate(leaderboard_xp, start=1):
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