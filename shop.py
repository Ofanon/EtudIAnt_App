import streamlit as st
import user_manager
import json
from streamlit_lottie import st_lottie

if "robot_star" not in st.session_state:
    with open("robot_star.json", "r") as f:
        st.session_state.robot_star = json.load(f)

header_col1, header_col2 = st.columns([4, 3])

with header_col1:
    st.title("🛒 Boutique")
    st.subheader(f"Que veux-tu acheter {st.session_state.user_id} ?")
    st.write(f"**🔥 Points d'Experience : {user_manager.get_any_user_data(user_id=st.session_state.user_id, column="xp")}**")
    st.write(f"**⭐ Etoiles : {user_manager.get_any_user_data(user_id=st.session_state.user_id, column="credits")}**")

with header_col2:
    st_lottie(st.session_state.robot_star, height=200, key="robot", loop=True)

st.markdown(" ")

st.subheader("⭐ Etoiles")
with st.container():
    col1, col2, col3 = st.columns(3, border=True, vertical_alignment="bottom")

    with col1:
        st.image(image="5_Stars.png", width=140)
        st.write("Prix : **1000 🔥**")
        if st.button("Acheter **5 ⭐**"):
            if user_manager.add_credits(user_id=st.session_state.user_id, xp_used=1000, amount=5):
                st.success("Tu as 5 nouvelles Etoiles !")
                st.rerun()
            else:
                st.error("Pas assez de Points d'Experience 🔥.")
    with col2:
        st.image(image="10_Stars.png", width=140)
        st.write("Prix : **2000 🔥**")
        if st.button("Acheter **10 ⭐**"):
            if user_manager.add_credits(user_id=st.session_state.user_id, xp_used=2000, amount=10):
                st.success("Tu as 20 nouvelles Etoiles !")
                st.rerun()
            else:
                st.error("Pas assez de Points d'Experience 🔥.")
    with col3:
        st.image(image="20_Stars.png", width=140)
        st.write("Prix : **4000 🔥**")
        if st.button("Acheter **20 ⭐**"):
            if user_manager.add_credits(user_id=st.session_state.user_id, xp_used=4000, amount=20):
                st.success("Tu as 20 nouvelles Etoiles !")
                st.rerun()
            else:
                st.error("Pas assez de Points d'Experience 🔥.")

st.markdown(" ")

st.subheader("🎁 Cadeau quotidien")
with st.container(key="gift", border=True):
    st.write("Récupère **3 ⭐ gratuitement** chaque jour ici !")
    if st.button("🎁 Récuperer 3 ⭐ gratuitement", disabled=not user_manager.can_get_gift(user_id=st.session_state.user_id)):
        user_manager.update_gift_date(user_id=st.session_state.user_id)
        user_manager.reset_daily_credits(user_id=st.session_state.user_id)
        st.success("Les 3 Etoiles quotidiennes ont bien été ajoutées !")
        st.rerun()

