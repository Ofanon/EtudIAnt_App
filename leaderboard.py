import streamlit as st
import user_manager

st.title("🏆 Top 3 Leaderboard")

# Récupérer le top 5
leaderboard_answers = user_manager.get_leaderboard_answers(limit=3)
leaderboard_xp = user_manager.get_leaderboard_xp(limit=3)
tab1, tab2 = st.tabs(tabs=["Classement par nombre de bonnes réponses", "Classement par nombre de Points d'Experience 🔥"])

if tab1:
    if leaderboard_answers:
        st.subheader("Classements des joueurs(euses) qui ont le plus de bonnes réponse :")

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

elif tab1:
    if leaderboard_xp:

        st.subheader("Classements des joueurs(euses) qui ont le plus de Points d'Experience 🔥 :")

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