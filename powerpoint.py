import streamlit as st
import google.generativeai as genai
import io
import os
import re
from pptx import Presentation

# Configuration de l'API Gemini
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel(model_name="gemini-pro")

st.title("Générateur de Code PowerPoint IA")

user_prompt = st.text_area("Décris le contenu du PowerPoint (ex: Titre et idées clés)")

if st.button("Générer le Code"):
    with st.spinner("Génération du code..."):
        prompt_ai = f"""
        Génère un script Python utilisant python-pptx qui crée un fichier PowerPoint avec le contenu suivant :
        {user_prompt}
        """
        response = model.generate_content(prompt_ai)
        match = re.search(r'\[.*\]', response.text, re.DOTALL)
        if match:
                text = match.group(0)

        if "import" not in text or "Presentation()" not in text:
            st.error("Le code généré ne semble pas valide. Réessayez.")
        else:
            with open("generated_pptx.py", "w") as f:
                f.write(text)

            st.code(text, language="python")
            st.success("Code généré avec succès ! Vous pouvez maintenant l'exécuter.")

if os.path.exists("generated_pptx.py") and st.button("Exécuter le Code et Générer le PowerPoint"):
    try:
        with open("generated_pptx.py", "r") as f:
            code_content = f.read()

        exec(code_content, {})

        if os.path.exists("presentation.pptx"):
            st.success("Le PowerPoint a été généré avec succès !")

            with open("presentation.pptx", "rb") as f:
                pptx_bytes = io.BytesIO(f.read())

            st.download_button(
                label="Télécharger le PowerPoint",
                data=pptx_bytes,
                file_name="presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        else:
            st.error("Le script a été exécuté, mais le fichier PowerPoint n'a pas été trouvé.")

    except Exception as e:
        st.error(f"Erreur lors de l'exécution : {e}")
