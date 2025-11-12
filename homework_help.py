import PIL.Image
import streamlit as st
import google.generativeai as genai
import PIL
import random

genai.configure(api_key=st.secrets[random.choice(["API_KEY1", "API_KEY2","API_KEY3", "API_KEY4"])])
model = genai.GenerativeModel(model_name="gemini-pro")

st.title("Aide aux devoirs")

st.subheader("Sur quel exercice veux-tu que je t'aides ?")

if "phone" not in st.session_state:
    st.session_state.phone = True
    st.session_state.analyze_image = False
    st.session_state.image_homework = None

if not st.session_state.analyze_image:
    if st.session_state.phone:
        if st.button("**Tu es sur ordinateur ? Clique ici pour importer la photo de ton devoir !**", type="tertiary"):
            st.session_state.phone = False
            st.rerun()
        enable = st.checkbox("Activer la caméra", help="Active la caméra pour photographier ton devoir.", value=False)
        image = st.camera_input("Clique sur **Take a photo** pour prendre une photo de ton devoir : ", disabled=not enable)
        if image:
            st.session_state.image_homework = image
            st.write("La photo de ton exercice")
            st.image(image=image)
            if st.button("Analyser le devoir", type="primary"):
                st.session_state.analyze_image = True
                st.rerun()
    elif not st.session_state.phone:
        if st.button("**Tu es sur portable ? Clique ici pour prendre en photo ton devoir !**", type="tertiary"):
            st.session_state.phone = True
            st.rerun()
        image = st.file_uploader("Importe l'image de ton devoir ici : ")
        if image:
            st.session_state.image_homework = image
            st.write("La photo de ton exercice")
            st.image(image=image)
            if st.button("Analyser le devoir", type="primary"):
                st.session_state.analyze_image = True
                st.rerun()

if st.session_state.analyze_image:
    st.image(st.session_state.image_homework)
    image = PIL.Image.open(st.session_state.image_homework)
    newsize = (300, 300)
    final_image = image.resize(newsize)
    prompt = "Aide l'utilisateur dans ce devoir en lui expliquant étape par étape comment le résoudre."
    with st.spinner("L'EtudIAnt réléchit..."):
        response_ai = model.generate_content([prompt, final_image])
    st.chat_message(response_ai.text, avatar="assistant")

