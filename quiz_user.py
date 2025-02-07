import streamlit as st
import google.generativeai as genai
import json
import re
import user_manager
import random

genai.configure(api_key=st.secrets[random.choice(["API_KEY1", "API_KEY2","API_KEY3", "API_KEY4"])])
model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

st.title("🤯 Quiz des points faibles")

def create_questions(level, subject):
    with st.spinner("La création du quiz des points faibles est en cours...") :
        response_ai = model.generate_content(f"Crée un QCM de 10 questions de niveau {level} en {subject}. Le quiz doit porter sur des chapitres compliqués de l'année. Toutes les réponses doivent être dans un container JSON avec : question_number , question , choices , correct_answer , explanation.")
    match = re.search(r'\[.*\]', response_ai.text, re.DOTALL)
    if match:
            json_text = match.group(0)
            data = json.loads(json_text)
            return data
    else:
        st.error("Erreur lors de la création des questions.")
        return []

with st.spinner("La page est en cours de chargement..."):
    if "started" not in st.session_state:
        st.session_state.xp_updated_user = False
        st.session_state.current_question_user = None
        st.session_state.question_count_user_user = 0
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

if not st.session_state.started:
    st.subheader("Es-tu prêt(e) à commencer le quiz des points faibles ?")
    st.write("Ce quiz va te permettre de **t'entrainer sur la matière que tu aimes le moins** !")
    st.success("**Bientôt disponible : Quiz des réponses que tu as raté.**")

disable_buttons = False
if "started" in st.session_state:

    if not st.session_state.started:
        st.session_state.can_start = False
        st.write(f"**Prix : 1 ⭐**")
        if st.button("🚀 Commencer le quiz", disabled=st.session_state.can_start):
            if user_manager.use_credit(user_id=st.session_state.user_id, credits_to_use=1):
                disable_buttons = True
                st.session_state.can_start = True
                st.session_state.data = create_questions(level=user_manager.get_any_user_data(user_id=st.session_state.user_id, column="class_level"), subject=user_manager.get_any_user_data(user_id=st.session_state.user_id, column="least_favorite_subject"))
            else:
                st.error("Tu as utilisé toutes tes Etoiles, reviens demain pour utiliser l'EtudIAnt.")
        
        if "data" in st.session_state and st.session_state.data:
            st.session_state.current_question = st.session_state.data[st.session_state.question_count]
            st.session_state.question = st.session_state.current_question['question']
            st.session_state.choices = st.session_state.current_question['choices']
            st.session_state.correct_answer = st.session_state.current_question['correct_answer']
            st.session_state.explanation = st.session_state.current_question['explanation']
            st.session_state.started = True
            st.rerun()

    if st.session_state.started:
        if not st.session_state.question_count > 9:
            st.progress(st.session_state.question_count/st.session_state.questions_number)
            disable_radio = st.session_state.verified
            disable_verify = st.session_state.verified
            st.subheader(st.session_state.question)
            user_repsponse = st.radio("Sélectionne ta réponse :", st.session_state.choices, disabled=disable_radio)

            if st.button("Verifier", disabled=disable_verify):
                st.session_state.verified = True
                st.rerun()

            if st.session_state.verified and not st.session_state.xp_updated:
                if user_repsponse == st.session_state.correct_answer:
                    user_manager.add_xp(user_id=st.session_state.user_id, points=30)
                    st.success("Bien joué, tu as trouvé la bonne réponse !")
                    st.session_state.correct_answers += 1
                    st.session_state.xp_updated = True

                else:

                    st.error(f"Raté, la bonne réponse était : {st.session_state.correct_answer}")
                st.write(st.session_state.explanation)

            if st.session_state.verified == True:
                if st.button("Continuer"):
                    st.session_state.verified = False
                    st.session_state.question_count += 1
                    if not st.session_state.question_count > 9:
                        st.session_state.current_question = st.session_state.data[st.session_state.question_count] 
                        st.session_state.question = st.session_state.current_question['question']
                        st.session_state.choices = st.session_state.current_question['choices']
                        st.session_state.correct_answer = st.session_state.current_question['correct_answer']
                        st.session_state.explanation = st.session_state.current_question['explanation']
                        st.session_state.xp_updated = False
                        st.rerun()
                    else:
                        st.rerun()
        else:
            st.session_state.note = round((st.session_state.correct_answers / st.session_state.questions_number) * 20)
            st.subheader(f"Bravo ! Le quiz est terminé !")
            st.subheader(f"Ta note est de {st.session_state.note}/20 !")
            st.balloons()
            if st.button("Refaire un autre quiz"):
                user_manager.add_xp(user_id=st.session_state.user_id, points=150)
                del st.session_state.started
                st.session_state.can_start = False
                st.rerun()