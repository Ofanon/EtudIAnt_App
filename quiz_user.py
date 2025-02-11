import streamlit as st
import google.generativeai as genai
import json
import re
import user_manager
import random

genai.configure(api_key=st.secrets[random.choice(["API_KEY1", "API_KEY2"])])
model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

st.title("🤯 Quiz des points faibles")

def create_questions(level, subject):
    with st.spinner("La création du quiz des points faibles est en cours..."):
        response_ai = model.generate_content(f"Crée un QCM de 7 questions de niveau {level} en {subject}. Le quiz doit porter sur des chapitres de l'année. L'utilisateur a a des difficultés dans cette matière donc rend le quiz fun (avec des emojis par exemple). Toutes les réponses doivent être dans un container JSON avec : question_number , question , choices , correct_answer , explanation.")
    match = re.search(r'\[.*\]', response_ai.text, re.DOTALL)
    if match:
            json_text = match.group(0)
            data = json.loads(json_text)
            return data
    else:
        st.error("Erreur lors de la création des questions.")
        return []

with st.spinner("La page est en cours de chargement..."):
    if "started_user" not in st.session_state:
        st.session_state.xp_updated_user = False
        st.session_state.current_question_user = None
        st.session_state.question_count_user = 0
        st.session_state.started_user = False
        st.session_state.data_user = None
        st.session_state.question_user = None
        st.session_state.choices_user = None
        st.session_state.correct_answer_user = 0
        st.session_state.correct_answers_user = 0
        st.session_state.verified_user = False
        st.session_state.explanation_user = None
        st.session_state.note_user = None
        st.session_state.points_user = None
        st.toast(f"Bienvenue dans le quiz des points faibles {st.session_state.user_id} ! Tu vas y arriver !")

if not st.session_state.started_user:
    st.subheader("Es-tu prêt(e) à commencer le quiz des points faibles ?")
    st.write("Ce quiz va te permettre de **t'entrainer sur la matière que tu aimes le moins** !")
    st.success("**Bientôt disponible : Quiz des réponses que tu as raté.**")

disable_buttons = False
if "started_user" in st.session_state:

    if not st.session_state.started_user:
        st.session_state.can_start_user = False
        st.write(f"**Prix : 1 ⭐**")
        if st.button("🚀 Commencer le quiz", disabled=st.session_state.can_start_user):
            if user_manager.use_credit(user_id=st.session_state.user_id, credits_to_use=1):
                disable_buttons = True
                st.session_state.can_start_user = True
                st.session_state.data_user = create_questions(level=user_manager.get_any_user_data(user_id=st.session_state.user_id, column="class_level"), subject=user_manager.get_any_user_data(user_id=st.session_state.user_id, column="least_favorite_subject"))
            else:
                st.error("Tu as utilisé toutes tes Etoiles, reviens demain pour utiliser l'EtudIAnt.")
        
        if "data_user" in st.session_state and st.session_state.data_user:
            st.session_state.current_question_user = st.session_state.data_user[st.session_state.question_count_user]
            st.session_state.question_user = st.session_state.current_question_user['question']
            st.session_state.choices_user = st.session_state.current_question_user['choices']
            st.session_state.correct_answer_user = st.session_state.current_question_user['correct_answer']
            st.session_state.explanation_user = st.session_state.current_question_user['explanation']
            st.session_state.started_user = True
            st.rerun()

    if st.session_state.started_user:
        if not st.session_state.question_count_user > 9:
            st.progress(st.session_state.question_count_user/7)
            disable_radio = st.session_state.verified_user
            disable_verify = st.session_state.verified_user
            st.subheader(st.session_state.question_user)
            user_repsponse = st.radio("Sélectionne ta réponse :", st.session_state.choices_user, disabled=disable_radio)

            if st.button("Verifier", disabled=disable_verify):
                st.session_state.verified_user = True
                st.rerun()

            if st.session_state.verified_user and not st.session_state.xp_updated_user:
                if user_repsponse == st.session_state.correct_answer_user:
                    st.success("Bien joué, tu as trouvé la bonne réponse !")
                    st.session_state.correct_answers_user += 1
                    st.session_state.xp_updated_user = True

                else:
                    st.error(f"Raté, la bonne réponse était : {st.session_state.correct_answer_user}")
                st.info(st.session_state.explanation_user)

            if st.session_state.verified_user == True:
                if st.button("Continuer"):
                    st.session_state.verified_user = False
                    st.session_state.question_count_user += 1
                    if not st.session_state.question_count_user > 9:
                        st.session_state.current_question_user = st.session_state.data_user[st.session_state.question_count_user] 
                        st.session_state.question_user = st.session_state.current_question_user['question']
                        st.session_state.choices_user = st.session_state.current_question_user['choices']
                        st.session_state.correct_answer_user = st.session_state.current_question_user['correct_answer']
                        st.session_state.explanation_user = st.session_state.current_question_user['explanation']
                        st.session_state.xp_updated_user = False
                        st.rerun()
                    else:
                        st.rerun()
        else:
            st.session_state.note_user = round((st.session_state.correct_answers_user / 7) * 20)
            st.subheader(f"Bravo ! Le quiz est terminé !")
            st.subheader(f"Ta note est de {st.session_state.note_user}/20 !")
            st.balloons()
            if st.button("Refaire un autre quiz"):
                if st.session_state.xp_updated_user is not True:
                    user_manager.add_xp(user_id=st.session_state.user_id, points=st.session_state.correct_answers_user*30)
                    st.session_state.xp_updated_user = True
                del st.session_state.started_user
                st.session_state.can_start_user = False
                st.rerun()