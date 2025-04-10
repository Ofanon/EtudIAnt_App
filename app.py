import streamlit as st
import user_manager

if "pages" not in st.session_state:
    st.session_state.pages = {}
    st.session_state.user_connected = False

st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.logo(image="etudiant_logo_title.png", icon_image="etudiant_icon_logoV2.png", size='large')
if st.session_state.user_connected is True:
    with st.sidebar:
        with st.container(border=True):
            st.markdown(f"**🔥 Points d'Experience : {user_manager.get_any_user_data(user_id=st.session_state.user_id, column="xp")}**")
            st.markdown(f"**💎 Points de Classement : {user_manager.get_any_user_data(user_id=st.session_state.user_id, column="corrects_answers")*10}**")
            st.markdown(f"**⭐ Etoiles : {user_manager.get_any_user_data(user_id=st.session_state.user_id, column="credits")}**")

    with st.sidebar:
        if st.button("🚪 Se deconnecter", type="primary"):
            st.session_state.user_id = None
            st.session_state.pages = {}
            st.session_state.user_connected = False
            st.rerun()
    with st.sidebar:
        st.info("**Attention** ! L'EtudIAnt est en version bêta. Il est possible que tu tombes sur certains bugs, n'hésite pas à changer de page sur le site pour résoudre le problème.")

if len(st.session_state.pages) > 0:
    pg = st.navigation(pages=st.session_state.pages)
else:
    pg = st.navigation([st.Page("welcome.py", title="login")])

pg.run()