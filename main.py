import streamlit as st
from streamlit_lottie import st_lottie
import json
import user_manager

if "robot_main" not in st.session_state:
    with open("robot_main.json","r") as f:
        st.session_state.robot_main = json.load(f)

st.title(f"🤖 Bienvenue sur l'EtudIAnt !")
with st.container(border=True):
    st.subheader("**Kaimana part déjà !**")
    st.write("**Donne-lui des Points d'Experience !**")
    xp = st.slider("Combien de Points d'Experience veux-tu lui donner ?", 10, 60)
    if st.button(f"Donner {xp} Points d'Experience à Kaimana", type="primary"):
        with st.spinner("Les Points d'Experience sont en chemin..."):
            user_manager.gift_to_kaimana(user_id=st.session_state.user_id, xp=xp)
            st.balloons()
    st.write("Les Points d'Experience donnés seront déduits de ton compte.")

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
