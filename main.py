import streamlit as st

st.title("📚 Bienvenue dans **l'EtudIAnt** ! 🤖")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Comment ça marche ?")
    st.markdown("""
    - **L'EtudIAnt** est une **Intelligence Artificielle** basée sur le modèle d'IA de Google.
    - **Gagne des Points d'Expérience** 🔥 en utilisant les services et achète des **Étoiles** ⭐.
    - **Les Étoiles** ⭐ te permettent d'utiliser l'IA plus longtemps !
    - 🎁 **Chaque jour, tu reçois 2 Étoiles gratuitement dans la 🛒 Boutique!**
    - 🏆 **Classement** : Fais partie des meilleurs en accumulant des points d'expérience !
    """)

st.success("Bon apprentissage et amuse-toi bien ! 🎉")
