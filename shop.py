import streamlit as st
import user_manager

st.title("🛒 Boutique")
st.subheader(f"Que veux-tu acheter {st.session_state.user_id} ?")

st.write(f"**🔥 Points d'Experience : {user_manager.get_any_user_data(user_id=st.session_state.user_id, column="xp")}**")
st.write(f"**⭐ Etoiles : {user_manager.get_any_user_data(user_id=st.session_state.user_id, column="credits")}**")

col1, col2, col3 = st.columns(3)

with col1:
    st.image(image="5_stars.png", width=140)
    st.write("Prix : **800 🔥**")
    if st.button("Acheter **5 ⭐**"):
        if user_manager.add_credits(user_id=st.session_state.user_id, xp_used=800, amount=5):
            st.success("Tu as 5 nouvelles Etoiles !")
            st.rerun()
        else:
            st.error("Pas assez de Points d'Experience 🔥.")
with col2:
    st.image(image="10_stars.png", width=140)
    st.write("Prix : **1580 🔥**")
    if st.button("Acheter **10 ⭐**"):
        if user_manager.add_credits(user_id=st.session_state.user_id, xp_used=1580, amount=10):
            st.success("Tu as 20 nouvelles Etoiles !")
            st.rerun()
        else:
            st.error("Pas assez de Points d'Experience 🔥.")
with col3:
    st.image(image="20_stars.png", width=140)
    st.write("Prix : **3000 🔥**")
    if st.button("Acheter **20 ⭐**"):
        if user_manager.add_credits(user_id=st.session_state.user_id, xp_used=3000, amount=20):
            st.success("Tu as 20 nouvelles Etoiles !")
            st.rerun()
        else:
            st.error("Pas assez de Points d'Experience 🔥.")

st.subheader("🎁 Cadeau quotidient")
st.write("Récupère **5 ⭐ gratuitement** chaque jour ici !")

if st.button("🎁 Récuperer 5 Etoiles gratuites", disabled=not user_manager.can_spin_wheel(user_id=st.session_state.user_id)):
    user_manager.update_date_spin_wheel(user_id=st.session_state.user_id)
    user_manager.reset_daily_credits(user_id=st.session_state.user_id)
    st.success("Les 5 Etoiles quotidiennes ont bien été ajoutées !")
    st.rerun()

