import streamlit as st
import user_manager
import sqlite3

main_pages = [st.Page("main.py", title="🏠 Accueil"), st.Page("shop.py", title="🛒 Boutique"), st.Page("quiz.py", title="🎯 Quiz Interactif"), st.Page("quiz_user.py", title="Quiz des points faibles"), st.Page("revision_sheet.py", title="📝 Créateur de fiche de révision"), st.Page("leaderboard.py", title="🏆 Leaderboard")]
if "started_questions" not in st.session_state:
    st.session_state.started_questions = True
    st.session_state.questions_user_count = 0
    st.session_state.responses_user = {}
    st.session_state.questions_user = [
        {
            "question_number": 1,
            "question": "Dans quelle classe es-tu ?",
            "type": "level",
            "choices": ["6ème", "5ème", "4ème", "3ème", "Seconde", "Premiere", "Terminale"]
        },
        {
            "question_number": 2,
            "question": "Quelle est ta matière préférée ?",
            "type": "subject",
            "choices": ["Français", "Mathématiques", "Histoire", "Géographie", "EMC", 
                        "Sciences et Vie de la Terre", "Physique Chimie", "Technologie", 
                        "Anglais", "Allemand", "Espagnol"]
        },
        {
            "question_number": 3,
            "question": "Quelle est la matière que tu trouves la plus difficile ?",
            "type": "subject",
            "choices": ["Français", "Mathématiques", "Histoire", "Géographie", "EMC", 
                        "Sciences et Vie de la Terre", "Physique Chimie", "Technologie", 
                        "Anglais", "Allemand", "Espagnol"]
        }
    ]

st.progress(st.session_state.questions_user_count/2)

current_question = st.session_state.questions_user[st.session_state.questions_user_count]

st.subheader(current_question["question"])

response_key = f"response_q{st.session_state.questions_user_count}"
st.session_state.responses_user[response_key] = st.radio(
    "Fais ton choix :", current_question["choices"], 
    index=current_question["choices"].index(st.session_state.responses_user.get(response_key, current_question["choices"][0])) if response_key in st.session_state.responses_user else 0
)


if st.session_state.questions_user_count < len(st.session_state.questions_user) - 1:
    if st.button("Continuer"):
        st.session_state.questions_user_count += 1
        st.rerun()
else:
    if st.button("Terminer"):
        conn = sqlite3.connect(user_manager.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET class_level = ?, favorite_subject = ?, least_favorite_subject = ? WHERE user_id = ?", (st.session_state.responses_user["response_q0"], st.session_state.responses_user["response_q1"], st.session_state.responses_user["response_q2"], st.session_state.user_id))
        conn.commit()
        st.success(f"✅ C'est bon ! L'EtudIAnt est entrainé {st.session_state.user_id} !")
        st.balloons()
        conn.close()
        st.session_state.user_connected = True
        st.session_state.pages = main_pages
        st.session_state.connect_questions_user = False
        st.session_state.questions_user_count = 0
        st.rerun()
        
if st.session_state.questions_user_count > 0:
    if st.button("Revenir en arrière", type="tertiary"):
        st.session_state.questions_user_count -= 1
        st.rerun()
