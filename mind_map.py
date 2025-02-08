import streamlit as st
import google.generativeai as genai
import networkx as nx
import matplotlib.pyplot as plt
import json

genai.configure(api_key="AIzaSyC7gtsgXWwLHAdudPwNBAfUCPy_evWvwO4")
st.title("Générateur de Carte Mentale")

subject = st.text_input("Le sujet de la Carte Mentale :")

if st.button("📌 Générer la carte mentale"):
    if subject:
        with st.spinner("L'IA réfléchit..."):
            model = genai.GenerativeModel("gemini-1.5-flash-002")
            prompt = f"Génère une carte mentale en JSON pour le sujet '{subject}', avec des concepts et sous-concepts."
            response = model.generate_content(prompt)

            try:
                json_start = response.text.find("[")
                json_end = response.text.rfind("]") + 1
                json_text = response.text[json_start:json_end]
                relations = json.loads(json_text)
            except Exception as e:
                st.error("Erreur dans la génération des concepts.")
                st.stop()

        G = nx.Graph()
        G.add_node(subject, size=2000, color="red")

        for concept, sous_concepts in relations.items():
            G.add_node(concept, size=1000, color="blue")
            G.add_edge(subject, concept)

            for sous_concept in sous_concepts:
                G.add_node(sous_concept, size=500, color="green")
                G.add_edge(concept, sous_concept)

        fig, ax = plt.subplots(figsize=(10, 7))
        pos = nx.spring_layout(G)
        node_sizes = [nx.get_node_attributes(G, "size").get(n, 500) for n in G.nodes()]
        node_colors = [nx.get_node_attributes(G, "color").get(n, "gray") for n in G.nodes()]

        nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, edge_color="gray", font_size=10, font_weight="bold", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("❗ Veuillez entrer un sujet.")