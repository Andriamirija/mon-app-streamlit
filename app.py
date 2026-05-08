import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd


df = pd.read_csv("users.csv", sep=";")
df.columns = ["name", "password", "email", "failed_login_attempts", "logged_in", "role"]

# Nos données utilisateurs doivent respecter ce format
lesDonneesDesComptes = {
    'usernames': {
        'utilisateur': {
            'name': 'utilisateur',
            'password': 'utilisateurMDP',
            'email': 'utilisateur@gmail.com',
            'failed_login_attempts': 0,  # Sera géré automatiquement
            'logged_in': False,          # Sera géré automatiquement
            'role': 'utilisateur'
        },
        'root': {
            'name': 'RIJA',
            'password': '10031982',
            'email': 'mirijavali@yahoo.fr',
            'failed_login_attempts': 0,  # Sera géré automatiquement
            'logged_in': False,          # Sera géré automatiquement
            'role': 'administrateur'
        }
    }
}

for _, row in df.iterrows():
    lesDonneesDesComptes["usernames"][row["name"]] = {
        "name": row["name"],
        "password": str(row["password"]),
        "email": row["email"],
        "failed_login_attempts": int(row["failed_login_attempts"]),
        "logged_in": bool(row["logged_in"]),
        "role": row["role"]
    }

authenticator = stauth.Authenticate(
    lesDonneesDesComptes,  # Les données des comptes
    "cookie name",         # Le nom du cookie, un str quelconque
    "cookie key",          # La clé du cookie, un str quelconque
    30,                    # Le nombre de jours avant que le cookie expire
)
authenticator.login()

# Gestion des états 
if st.session_state.get("authentication_status") is False:
    st.error("Les champs username et mot de passe doivent être remplie")

elif st.session_state.get("authentication_status") is None:
    st.warning("Les champs username et mot de passe doivent être remplie")

elif st.session_state.get("authentication_status"):

    # Sidebar 
    with st.sidebar:
        authenticator.logout("Déconnexion")
        st.markdown(f"Bienvenue *{st.session_state['name']}*")
        st.markdown("---")
        page = st.selectbox("", [" Accueil", " Les photos de mes chiens"])

          # Page Accueil 
    if page == " Accueil":
        st.title("Bienvenue sur ma page")
        st.image(
            "images/photo1.png",
            use_container_width=False,
            width=500
        )

    # Album photo 
    elif page == " Les photos de mes chiens":
        st.title("Bienvenue dans l'album de mes chiens ")

        images = [
            "images/chien1.png",
            "images/chien2.png",
            "images/chien3.png",
            "images/chien4.png",
            "images/chien5.png",
            "images/chien6.png",
        ]

        # images par ligne
        for i in range(0, len(images), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(images):
                    col.image(images[i + j], use_container_width=True)
