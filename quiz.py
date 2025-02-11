import streamlit as st
import google.generativeai as genai
import json
import re
import user_manager
import random

genai.configure(api_key=st.secrets[random.choice(["API_KEY1", "API_KEY2"])])
model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

st.title("🎯 Quiz interactif")

def create_questions(level, subject, questions, prompt):
    with st.spinner("La création du quiz est en cours...") :
        response_ai = model.generate_content(f"Crée un QCM de {questions} questions de niveau {level} en {subject} et de sujet : {prompt}. Toutes les réponses doivent être dans un container JSON avec : question_number , question , choices , correct_answer , explanation.")
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
        st.session_state.level = None
        st.session_state.subject = None
        st.session_state.difficulty = None
        st.session_state.user_prompt = None
        st.session_state.xp_updated = False
        st.session_state.current_question = None
        st.session_state.question_count = 0
        st.session_state.started = False
        st.session_state.data = None
        st.session_state.question = None
        st.session_state.choices = None
        st.session_state.correct_answer = 0
        st.session_state.wrong_answers= 0
        st.session_state.correct_answers = 0
        st.session_state.verified = False
        st.session_state.explanation = None
        st.session_state.note = None
        st.session_state.points = None
        st.toast(f"Bienvenue dans le quiz interactif {st.session_state.user_id} ! Apprends bien !")

disable_buttons = False
if "started" in st.session_state:

    if not st.session_state.started:
        st.session_state.can_start = False
        st.subheader("Sur quoi veux-tu créer ton quiz ?")
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.subject = st.selectbox("📚 **Sélectionne la matière du quiz :** ", ["Français", "Mathématiques", "Histoire","Géographie","EMC", "Sciences et Vie de la Terre", "Physique Chimie","Technologie", "Anglais","Allemand", "Espagnol"], )
                st.session_state.user_prompt = st.text_input("📝 **Le sujet du quiz :**", placeholder="Ex : sur la révolution", disabled=disable_buttons)
            with col2:
                st.session_state.questions_number = st.slider("🎚 **Sélectionne le nombre de questions :**", 10, 15)
                st.write(f"**Prix : {round(st.session_state.questions_number/8.5)} ⭐**")
            if st.button("🚀 Créer le quiz", disabled=st.session_state.can_start):
                if st.session_state.user_prompt != "":
                    if user_manager.use_credit(user_id=st.session_state.user_id, credits_to_use=round(st.session_state.questions_number/8.5)):
                        disable_buttons = True
                        st.session_state.can_start = True
                        st.session_state.data = create_questions(level=user_manager.get_any_user_data(user_id=st.session_state.user_id, column="class_level"), subject=st.session_state.subject,questions=st.session_state.questions_number, prompt=st.session_state.user_prompt)
                    else:
                        st.error("Tu as utilisé toutes tes Etoiles, reviens demain pour utiliser l'EtudIAnt.")
                else:
                    st.error("Remplis le 'sujet du quiz' pour créer le quiz interactif.")
        
        if "data" in st.session_state and st.session_state.data:
            st.session_state.current_question = st.session_state.data[st.session_state.question_count]
            st.session_state.question = st.session_state.current_question['question']
            st.session_state.choices = st.session_state.current_question['choices']
            st.session_state.correct_answer = st.session_state.current_question['correct_answer']
            st.session_state.explanation = st.session_state.current_question['explanation']
            st.session_state.started = True
            st.rerun()

    if st.session_state.started:
        if not st.session_state.question_count > st.session_state.questions_number - 1:
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
                    st.success("Bien joué, tu as trouvé la bonne réponse !")
                    st.session_state.correct_answers += 1
                    st.session_state.xp_updated = True

                else:

                    st.error(f"Raté, la bonne réponse était : {st.session_state.correct_answer}")
                    st.session_state.wrong_answers += 1
                st.write(st.session_state.explanation)

            if st.session_state.verified == True:
                if st.button("Continuer"):
                    st.session_state.verified = False
                    st.session_state.question_count += 1
                    if not st.session_state.question_count > st.session_state.questions_number - 1:
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
            user_manager.add_xp(user_id=st.session_state.user_id, points=st.session_state.correct_answers * 30)
            st.balloons()
            with st.spinner("Le quiz est en cours d'enregistrement..."):
                if user_manager.insert_quiz(user_id=st.session_state.user_id, subject=subject, correct_answers=st.session_state.correct_answers, wrong_answers=st.session_state.wrong_answers):
                    st.success("Le quiz a été enregistré avec succès !")
            st.info("Conseil : Ne quitte pas le quiz avant que l'enregistrement soit fini.")
            if st.button("Refaire un autre quiz"):
                user_manager.add_xp(user_id=st.session_state.user_id, points=50)
                del st.session_state.started
                st.session_state.can_start = False
                st.rerun()