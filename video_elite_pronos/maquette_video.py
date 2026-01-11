<<<<<<< HEAD
import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Elite Pronos - Maquette Vidéo", layout="centered")

# CSS PERSONNALISÉ POUR LE LOOK "DARK / PREMIUM"
st.markdown("""
    <style>
    .stApp {
        background-color: #0B132B;
        color: white;
    }
    h1, h2, h3 {
        color: #D4AF37 !important; /* DORE */
        font-family: 'Impact', sans-serif;
    }
    .stButton>button {
        background-color: #D4AF37;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }
    .metric-card {
        background-color: #1C2541;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #D4AF37;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATÉRAL POUR CHOISIR L'ÉCRAN À AFFICHER ---
ecran = st.sidebar.radio("Choisir l'écran pour la capture :", 
                         ["1. Accueil/Inscription", "2. Gameplay/Mise", "3. Jokers", "4. Classement Gala"])

# --- ÉCRAN 1 : INSCRIPTION ---
if ecran == "1. Accueil/Inscription":
    st.title("PRÊT À DÉTRÔNER TES POTES ?")
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://api.dicebear.com/9.x/avataaars/svg?seed=King", caption="Ton Avatar")
        st.button("CHANGER AVATAR")
    
    with col2:
        st.text_input("TON PSEUDO DE GUERRIER", value="Sniper_92")
        st.text_input("CODE PIN SECRET", value="****", type="password")
        st.text_input("EMAIL", value="champion@elite.com")
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("ENTRER DANS L'ARÈNE ⚽")

# --- ÉCRAN 2 : GAMEPLAY ---
elif ecran == "2. Gameplay/Mise":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("GRILLE SEMAINE 12")
    with col2:
        st.metric("BUDGET RESTANT", "100 pts")

    st.info("💡 GRAND CHELEM : Trouve les 4 scores -> Budget 140 pts la semaine prochaine !")

    with st.container():
        st.markdown("### PSG vs MARSEILLE")
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.write("Ton Prono (Score Exact)")
            st.markdown("## 2 - 1")
        with c2:
            st.slider("Ta Mise", 10, 60, 40, key="slider1")
        with c3:
            st.markdown("### Gain Potentiel: 125 pts")
    st.markdown("---")
    with st.container():
        st.markdown("### LIVERPOOL vs MAN CITY")
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.write("Ton Prono")
            st.markdown("## 3 - 3")
        with c2:
            st.slider("Ta Mise", 10, 60, 20, key="slider2")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("VALIDER MES PRONOS (TOTAL 60/100)")

# --- ÉCRAN 3 : JOKERS ---
elif ecran == "3. Jokers":
    st.title("CHOISIS TON ARME")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h1>👑 x2</h1>
            <h3>POINTS DOUBLES</h3>
            <p>Tu es sûr de toi ? Double tes gains.</p>
        </div>
        """, unsafe_allow_html=True)
        st.checkbox("Activer Points Doubles")

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h1>✋🕵️</h1>
            <h3>POINTS VOLÉS</h3>
            <p>Copie les pronos du meilleur joueur.</p>
        </div>
        """, unsafe_allow_html=True)
        vole = st.checkbox("Activer Points Volés")
        
        if vole:
            st.warning("⚠️ CIBLE VERROUILLÉE : @Nico_The_Boss (1er)")
            st.dataframe(pd.DataFrame({
                "Cible": ["Nico_The_Boss", "Alex_Pro", "Sam_Foot"],
                "Forme": ["✅✅✅", "✅❌✅", "❌✅✅"],
                "Points": [450, 410, 390]
            }), hide_index=True)

# --- ÉCRAN 4 : CLASSEMENT GALA ---
elif ecran == "4. Classement Gala":
    st.balloons() # Animation Streamlit
    st.title("🏆 RÉSULTATS SEMAINE 12")
    
    # Podiums
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("https://api.dicebear.com/9.x/avataaars/svg?seed=Winner", width=150)
        st.markdown("<h3 style='text-align: center; color: gold;'>1. SNIPER_92</h3>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>520 PTS</h1>", unsafe_allow_html=True)
    
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 2. Lucas_Bet")
        st.markdown("#### 480 PTS")
        
    with col3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 3. Tom_R")
        st.markdown("#### 465 PTS")

    st.markdown("---")
=======
import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Elite Pronos - Maquette Vidéo", layout="centered")

# CSS PERSONNALISÉ POUR LE LOOK "DARK / PREMIUM"
st.markdown("""
    <style>
    .stApp {
        background-color: #0B132B;
        color: white;
    }
    h1, h2, h3 {
        color: #D4AF37 !important; /* DORE */
        font-family: 'Impact', sans-serif;
    }
    .stButton>button {
        background-color: #D4AF37;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }
    .metric-card {
        background-color: #1C2541;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #D4AF37;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATÉRAL POUR CHOISIR L'ÉCRAN À AFFICHER ---
ecran = st.sidebar.radio("Choisir l'écran pour la capture :", 
                         ["1. Accueil/Inscription", "2. Gameplay/Mise", "3. Jokers", "4. Classement Gala"])

# --- ÉCRAN 1 : INSCRIPTION ---
if ecran == "1. Accueil/Inscription":
    st.title("PRÊT À DÉTRÔNER TES POTES ?")
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://api.dicebear.com/9.x/avataaars/svg?seed=King", caption="Ton Avatar")
        st.button("CHANGER AVATAR")
    
    with col2:
        st.text_input("TON PSEUDO DE GUERRIER", value="Sniper_92")
        st.text_input("CODE PIN SECRET", value="****", type="password")
        st.text_input("EMAIL", value="champion@elite.com")
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("ENTRER DANS L'ARÈNE ⚽")

# --- ÉCRAN 2 : GAMEPLAY ---
elif ecran == "2. Gameplay/Mise":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("GRILLE SEMAINE 12")
    with col2:
        st.metric("BUDGET RESTANT", "100 pts")

    st.info("💡 GRAND CHELEM : Trouve les 4 scores -> Budget 140 pts la semaine prochaine !")

    with st.container():
        st.markdown("### PSG vs MARSEILLE")
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.write("Ton Prono (Score Exact)")
            st.markdown("## 2 - 1")
        with c2:
            st.slider("Ta Mise", 10, 60, 40, key="slider1")
        with c3:
            st.markdown("### Gain Potentiel: 125 pts")
    st.markdown("---")
    with st.container():
        st.markdown("### LIVERPOOL vs MAN CITY")
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.write("Ton Prono")
            st.markdown("## 3 - 3")
        with c2:
            st.slider("Ta Mise", 10, 60, 20, key="slider2")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("VALIDER MES PRONOS (TOTAL 60/100)")

# --- ÉCRAN 3 : JOKERS ---
elif ecran == "3. Jokers":
    st.title("CHOISIS TON ARME")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h1>👑 x2</h1>
            <h3>POINTS DOUBLES</h3>
            <p>Tu es sûr de toi ? Double tes gains.</p>
        </div>
        """, unsafe_allow_html=True)
        st.checkbox("Activer Points Doubles")

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h1>✋🕵️</h1>
            <h3>POINTS VOLÉS</h3>
            <p>Copie les pronos du meilleur joueur.</p>
        </div>
        """, unsafe_allow_html=True)
        vole = st.checkbox("Activer Points Volés")
        
        if vole:
            st.warning("⚠️ CIBLE VERROUILLÉE : @Nico_The_Boss (1er)")
            st.dataframe(pd.DataFrame({
                "Cible": ["Nico_The_Boss", "Alex_Pro", "Sam_Foot"],
                "Forme": ["✅✅✅", "✅❌✅", "❌✅✅"],
                "Points": [450, 410, 390]
            }), hide_index=True)

# --- ÉCRAN 4 : CLASSEMENT GALA ---
elif ecran == "4. Classement Gala":
    st.balloons() # Animation Streamlit
    st.title("🏆 RÉSULTATS SEMAINE 12")
    
    # Podiums
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("https://api.dicebear.com/9.x/avataaars/svg?seed=Winner", width=150)
        st.markdown("<h3 style='text-align: center; color: gold;'>1. SNIPER_92</h3>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>520 PTS</h1>", unsafe_allow_html=True)
    
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 2. Lucas_Bet")
        st.markdown("#### 480 PTS")
        
    with col3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 3. Tom_R")
        st.markdown("#### 465 PTS")

    st.markdown("---")
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    st.success("💰 GRAND CHELEM DÉCROCHÉ PAR : SNIPER_92 (+40 PTS BONUS)")