import streamlit as st
from streamlit_lottie import st_lottie
import json

if "robot_main" not in st.session_state:
    with open("robot_main.json","r") as f:
        st.session_state.robot_main = json.load(f)

st.title("📚 Bienvenue dans **l'EtudIAnt** ! 🤖")

col1, col2 = st.columns(2)

with col2:
    st.subheader("🎯 Comment ça marche ?")
    st.markdown("""
    - **L'EtudIAnt** est une **Intelligence Artificielle** basée sur le modèle d'IA de Google.
    - **Gagne des Points d'Expérience** 🔥 en utilisant les services et achète des **Étoiles** ⭐.
    - **Les Étoiles** ⭐ te permettent d'utiliser l'IA plus longtemps !
    - 🎁 **Chaque jour, tu reçois 3 Étoiles gratuitement dans la 🛒 Boutique !**
    - 🏆 **Classement** : Fais partie des meilleurs en accumulant des points d'expérience !
    """)

    st.success("Bon apprentissage et amuse-toi bien ! 🎉")

with col1:
    st_lottie(st.session_state.robot_main, height=400, key="robot_main", loop=True)
