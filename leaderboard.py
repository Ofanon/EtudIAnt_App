import streamlit as st
import user_manager

st.title("🏆 Top 5 Leaderboard")

# Récupérer le top 5
leaderboard = user_manager.get_leaderboard()

if leaderboard:
    st.write("Voici le classement des 5 meilleurs joueurs :")

    for i, (user_id, xp) in enumerate(leaderboard, start=1):
        if i == 1:
            st.write(f"🥇 **{i}. {user_id}** - {xp} XP")  # Or met un style spécial pour le 1er
        elif i == 2:
            st.write(f"🥈 **{i}. {user_id}** - {xp} XP")
        elif i == 3:
            st.write(f"🥉 **{i}. {user_id}** - {xp} XP")
        else:
            st.write(f"✨ {i}. {user_id} - {xp} XP")
else:
    st.write("Personne n'a encore gagné de points ! 🚀")