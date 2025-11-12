import streamlit as st
import user_manager
import requests
from streamlit_lottie import st_lottie

st.title("🤖 Connexion à l'EtudIAnt")

if "connexion_type" not in st.session_state:
    st.session_state.connexion_type = "connect"
    st.session_state.user_id = None
    st.session_state.connect_questions_user = False

main_pages = [st.Page("main.py", title="🏠 Accueil"), st.Page("shop.py", title="🛒 Boutique"), st.Page("quiz.py", title="🎯 Quiz Interactif"), st.Page("quiz_user.py", title="🤯 Quiz des points faibles"), st.Page("revision_sheet.py", title="📝 Créateur de fiche de révision"), st.Page("leaderboard.py", title="🏆 Leaderboard"), st.Page("user_stats.py",title="🚀 Ma progression")]
questions_page = [st.Page("questions_user.py", title="Questions")]

if not st.session_state.connect_questions_user:
    if st.session_state.connexion_type == "connect":
        with st.form("connect_form"):
            id = st.text_input("Ton identifiant :", placeholder="Ex : etudIAnt123")
            password = st.text_input("Ton mot de passe :", type="password")
            if st.form_submit_button("🔑 Se connecter"):
                if id and password:
                    if user_manager.authenticate_user(user_id=id, password=password):
                        st.success(f"Tu es bien connecté !")
                        st.session_state.user_id = id
                        if user_manager.is_user_profile_complete(user_id=st.session_state.user_id):
                            st.balloons()
                            st.session_state.user_connected = True
                            st.session_state.pages = main_pages
                            st.rerun()
                        else:
                            st.session_state.pages = questions_page
                            st.rerun()
                    else:
                        st.error("L'identifiant ou le mot de passe est incorrect.")
                else:
                    st.error("Remplis tous les champs.")
            if st.form_submit_button("❓ Pas de compte ? En créer un", type="tertiary"):
                st.session_state.connexion_type = "create_account"
                st.rerun()

    elif st.session_state.connexion_type == "create_account":
        with st.form("create_account_form"):
            id = st.text_input("Crée ton identifiant :", placeholder="Ex : etudIAnt123")
            password = st.text_input("Crée ton mot de passe :", type="password")
            if st.form_submit_button("➕ Créer un compte"):
                if id and password:
                    if user_manager.register_user(user_id=id, password=password):
                        st.session_state.user_id = id
                        st.session_state.connect_questions_user = False
                        st.session_state.pages = questions_page
                        st.rerun()
                    else:
                        st.error("Cet identifiant existe déjà.")
                else:
                    st.error("Remplis tous les champs.")
            if st.form_submit_button("❓ Déjà un compte ? Se connecter", type="tertiary"):
                st.session_state.connexion_type = "connect"
                st.rerun()