import streamlit as st
from streamlit_lottie import st_lottie
import json
import user_manager

if "robot_main" not in st.session_state:
    with open("robot_main.json","r") as f:
        st.session_state.robot_main = json.load(f)
    st.session_state.kaimana_gift = True

st.title(f"🤖 Bienvenue sur l'EtudIAnt !")

col1, col2 = st.columns(2)
with col2:
    st.subheader("🎯 Comment ça marche ?")
    st.markdown("""
    - **L'EtudIAnt** est une **Intelligence Artificielle** qui vous permet d'étudier et d'apprendre !
                   
    - **Gagne des Points d'Expérience** 🔥 en utilisant les services (quizs, fiches de révision) pour acheter des **Étoiles** ⭐ !
                
    - **Les Étoiles** ⭐ te permettent d'utiliser l'IA plus longtemps !
                
    - 🎁 **Chaque jour, tu reçois 3 Étoiles gratuitement dans la 🛒 Boutique (n'oublie pas de les récupérer) !**
                
    - 🏆 **Classement** : Fais partie du **Top 3** en accumulant des points d'expérience !
    """)

    st.success("Bon apprentissage et amuse-toi bien ! 🎉")

with col1:
    st_lottie(st.session_state.robot_main, height=400, key="robot_main", loop=True)

st.subheader(f"🤩 Vous êtes {user_manager.get_users_number()+1} personnes à utiliser l'EtudIAnt ! Merci de me faire confiance !")
