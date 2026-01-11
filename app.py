import streamlit as st
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.database_manager import DatabaseManager
from migrate import migrate_database

# Migration de la base de données au démarrage
migrate_database()

st.set_page_config(
    page_title="Elite Pronos 2",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {background-color: #0A1628; color: white;}
    .stApp {background-color: #0A1628;}
    h1, h2, h3 {color: #FFD700 !important;}
    p, div, span, label {color: white !important;}
    .stButton>button {background-color: #FFD700; color: black; font-weight: bold; width: 100%;}
    .stMetric {background-color: #1A1A1A; padding: 15px; border-radius: 10px; border: 2px solid #FFD700;}
    .stMetric label {color: #FFD700 !important; font-size: 16px !important;}
    .stMetric [data-testid="stMetricValue"] {color: white !important; font-size: 24px !important;}
    [data-testid="stSidebar"] {background-color: #0A1628;}
    .stRadio > label {color: white !important;}
    .stMarkdown {color: white !important;}
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.pseudo = None
    st.session_state.prenom = None

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🏆 Elite Pronos 2</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #FFD700;'>Que le meilleur gagne !</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        with st.form("login_form"):
            st.subheader("🔐 Connexion")
            pseudo = st.text_input("Pseudo", placeholder="Entre ton pseudo")
            password = st.text_input("PIN", type="password", placeholder="••••")
            submit = st.form_submit_button("🚀 SE CONNECTER")
            
            if submit:
                if not pseudo or not password:
                    st.error("❌ Remplis tous les champs !")
                else:
                    db = DatabaseManager()
                    conn = db.create_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        SELECT id, pseudo, prenom FROM utilisateurs
                        WHERE pseudo = ? AND pin = ? AND statut = 'actif'
                    """, (pseudo, password))
                    
                    user = cursor.fetchone()
                    conn.close()
                    
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user[0]
                        st.session_state.pseudo = user[1]
                        st.session_state.prenom = user[2]
                        st.rerun()
                    else:
                        st.error("❌ Identifiants incorrects")

def dashboard_page():
    st.title(f"🏠 Bienvenue {st.session_state.prenom or st.session_state.pseudo} !")
    
    db = DatabaseManager()
    conn = db.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COALESCE(SUM(points_totaux), 0) FROM historique
        WHERE utilisateur_id = ?
    """, (st.session_state.user_id,))
    points_totaux = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) + 1 FROM (
            SELECT utilisateur_id, SUM(points_totaux) as total
            FROM historique
            GROUP BY utilisateur_id
            HAVING total > ?
        )
    """, (points_totaux,))
    classement = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT jokers_doubles_disponibles, jokers_voles_disponibles
        FROM stock_jokers
        WHERE utilisateur_id = ?
    """, (st.session_state.user_id,))
    jokers = cursor.fetchone()
    jokers_doubles = jokers[0] if jokers else 0
    jokers_voles = jokers[1] if jokers else 0
    
    conn.close()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Points totaux", f"{points_totaux:.1f}")
    
    with col2:
        st.metric("🏆 Classement", f"#{classement}")
    
    with col3:
        st.metric("🎴 Jokers ×2", jokers_doubles)
    
    with col4:
        st.metric("🦹 Jokers Vol", jokers_voles)
    
    st.markdown("---")
    
    cursor = db.create_connection().cursor()
    cursor.execute("""
        SELECT semaine, date_premier_match, date_cloture_pronos
        FROM journees_calendrier
        WHERE statut = 'a_venir'
        ORDER BY semaine
        LIMIT 1
    """)
    
    prochaine = cursor.fetchone()
    
    if prochaine:
        semaine, date_match, date_cloture = prochaine
        
        st.info(f"📅 **Prochaine journée : Semaine {semaine}**  \n"
               f"⚽ 1er match : {date_match}  \n"
               f"🔒 Clôture : {date_cloture}")
        
        cursor.execute("""
            SELECT COUNT(DISTINCT p.match_id) 
            FROM pronostics p
            JOIN matchs m ON p.match_id = m.id
            WHERE p.utilisateur_id = ? AND m.semaine = ?
        """, (st.session_state.user_id, semaine))
        
        nb_pronos = cursor.fetchone()[0]
        
        if nb_pronos == 0:
            st.warning("⚠️ Tu n'as pas encore fait tes pronos !")
        else:
            st.success(f"✅ Pronos validés ({nb_pronos} matchs)")
    else:
        st.info("ℹ️ Aucune journée en cours")
    
    cursor.connection.close()

def pronos_page():
    st.title("📝 Mes Pronos")
    
    db = DatabaseManager()
    conn = db.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT semaine, date_cloture_pronos, statut
        FROM journees_calendrier
        WHERE statut = 'a_venir'
        ORDER BY semaine
        LIMIT 1
    """)
    
    journee = cursor.fetchone()
    
    if not journee:
        st.warning("⚠️ Aucune journée disponible pour pronostiquer")
        conn.close()
        return
    
    semaine, date_cloture, statut = journee
    
    st.subheader(f"Journée {semaine}")
    st.info(f"🔒 Clôture : {date_cloture}")
    
    cursor.execute("""
        SELECT id, equipe_domicile, equipe_exterieur, cote_domicile, cote_nul, cote_exterieur
        FROM matchs
        WHERE semaine = ?
        ORDER BY id
    """, (semaine,))
    
    matchs = cursor.fetchall()
    
    if not matchs:
        st.warning("⚠️ Aucun match disponible pour cette journée")
        conn.close()
        return
    
    cursor.execute("""
        SELECT match_id, pronostic FROM pronostics
        WHERE utilisateur_id = ? AND match_id IN (SELECT id FROM matchs WHERE semaine = ?)
    """, (st.session_state.user_id, semaine))
    
    pronos_existants = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    
    with st.form("pronos_form"):
        pronos = {}
        
        for match in matchs:
            match_id, dom, ext, cote_d, cote_n, cote_e = match
            
            st.markdown(f"### ⚽ {dom} vs {ext}")
            
            prono_actuel = pronos_existants.get(match_id, None)
            
            options = [
                f"1 - {dom} ({cote_d})",
                f"N - Nul ({cote_n})",
                f"2 - {ext} ({cote_e})"
            ]
            
            index = 0
            if prono_actuel == '1':
                index = 0
            elif prono_actuel == 'N':
                index = 1
            elif prono_actuel == '2':
                index = 2
            
            choix = st.radio(
                "Ton prono",
                options,
                index=index,
                key=f"prono_{match_id}",
                horizontal=True
            )
            
            if choix.startswith("1"):
                pronos[match_id] = '1'
            elif choix.startswith("N"):
                pronos[match_id] = 'N'
            else:
                pronos[match_id] = '2'
            
            st.markdown("---")
        
        submitted = st.form_submit_button("💾 VALIDER MES PRONOS")
        
        if submitted:
            db = DatabaseManager()
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM pronostics
                WHERE utilisateur_id = ? AND match_id IN (SELECT id FROM matchs WHERE semaine = ?)
            """, (st.session_state.user_id, semaine))
            
            for match_id, prono in pronos.items():
                cursor.execute("""
                    INSERT INTO pronostics (utilisateur_id, match_id, pronostic)
                    VALUES (?, ?, ?)
                """, (st.session_state.user_id, match_id, prono))
            
            conn.commit()
            conn.close()
            
            st.success("✅ Pronos enregistrés avec succès !")
            st.balloons()

def classement_page():
    st.title("🏆 Classement")
    
    tab1, tab2, tab3 = st.tabs(["📊 Général", "🎯 Précision", "📅 Historique"])
    
    db = DatabaseManager()
    conn = db.create_connection()
    cursor = conn.cursor()
    
    with tab1:
        st.subheader("Classement Général")
        
        cursor.execute("""
            SELECT u.pseudo, SUM(h.points_totaux) as total
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            GROUP BY u.id
            ORDER BY total DESC
        """)
        
        classement = cursor.fetchall()
        
        if classement:
            for idx, (pseudo, points) in enumerate(classement, 1):
                medaille = ""
                if idx == 1:
                    medaille = "🥇"
                elif idx == 2:
                    medaille = "🥈"
                elif idx == 3:
                    medaille = "🥉"
                
                couleur = "#FFD700" if pseudo == st.session_state.pseudo else "#FFFFFF"
                
                st.markdown(f"<p style='font-size: 18px; color: {couleur};'>"
                          f"{medaille} <strong>#{idx}</strong> - {pseudo} : <strong>{points:.1f} pts</strong>"
                          f"</p>", unsafe_allow_html=True)
        else:
            st.info("Aucune donnée disponible")
    
    with tab2:
        st.subheader("Classement Précision")
        
        cursor.execute("""
            SELECT u.pseudo, 
                   COUNT(h.id) as nb_semaines,
                   AVG(h.points_totaux) as moyenne
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            GROUP BY u.id
            HAVING nb_semaines > 0
            ORDER BY moyenne DESC
        """)
        
        classement_precision = cursor.fetchall()
        
        if classement_precision:
            for idx, (pseudo, nb_semaines, moyenne) in enumerate(classement_precision, 1):
                medaille = ""
                if idx == 1:
                    medaille = "🥇"
                elif idx == 2:
                    medaille = "🥈"
                elif idx == 3:
                    medaille = "🥉"
                
                couleur = "#FFD700" if pseudo == st.session_state.pseudo else "#FFFFFF"
                
                st.markdown(f"<p style='font-size: 18px; color: {couleur};'>"
                          f"{medaille} <strong>#{idx}</strong> - {pseudo} : <strong>{moyenne:.2f} pts/semaine</strong> ({nb_semaines} semaines)"
                          f"</p>", unsafe_allow_html=True)
        else:
            st.info("Aucune donnée disponible")
    
    with tab3:
        st.subheader("Historique par semaine")
        
        cursor.execute("""
            SELECT DISTINCT semaine FROM historique ORDER BY semaine DESC
        """)
        
        semaines = [row[0] for row in cursor.fetchall()]
        
        if semaines:
            semaine_selectionnee = st.selectbox("Sélectionne une semaine", semaines)
            
            cursor.execute("""
                SELECT u.pseudo, h.points_totaux
                FROM historique h
                JOIN utilisateurs u ON h.utilisateur_id = u.id
                WHERE h.semaine = ?
                ORDER BY h.points_totaux DESC
            """, (semaine_selectionnee,))
            
            resultats = cursor.fetchall()
            
            st.markdown(f"### Semaine {semaine_selectionnee}")
            
            for idx, (pseudo, points) in enumerate(resultats, 1):
                medaille = ""
                if idx == 1:
                    medaille = "🥇"
                elif idx == 2:
                    medaille = "🥈"
                elif idx == 3:
                    medaille = "🥉"
                
                couleur = "#FFD700" if pseudo == st.session_state.pseudo else "#FFFFFF"
                
                st.markdown(f"<p style='font-size: 18px; color: {couleur};'>"
                          f"{medaille} <strong>#{idx}</strong> - {pseudo} : <strong>{points:.1f} pts</strong>"
                          f"</p>", unsafe_allow_html=True)
        else:
            st.info("Aucun historique disponible")
    
    conn.close()

def recap_page():
    st.title("🎪 Récapitulatif")
    
    db = DatabaseManager()
    conn = db.create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT semaine FROM journees_calendrier
        WHERE statut = 'terminee'
        ORDER BY semaine DESC
        LIMIT 1
    """)
    
    semaine_row = cursor.fetchone()
    
    if not semaine_row:
        st.info("ℹ️ Aucune semaine terminée")
        conn.close()
        return
    
    semaine = semaine_row[0]
    
    st.subheader(f"Semaine {semaine}")
    
    cursor.execute("""
        SELECT u.pseudo, h.points_totaux
        FROM historique h
        JOIN utilisateurs u ON h.utilisateur_id = u.id
        WHERE h.semaine = ?
        ORDER BY h.points_totaux DESC
        LIMIT 3
    """, (semaine,))
    
    top3 = cursor.fetchall()
    
    st.markdown("### 🏆 Podium de la semaine")
    
    if top3:
        medailles = ["🥇", "🥈", "🥉"]
        for idx, (pseudo, points) in enumerate(top3):
            st.markdown(f"<h3>{medailles[idx]} {pseudo} - {points:.1f} pts</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🏅 Trophées de la semaine")
    
    cursor.execute("""
        SELECT t.categorie, u.pseudo, t.valeur, t.description
        FROM trophees t
        JOIN utilisateurs u ON t.utilisateur_id = u.id
        WHERE t.semaine = ?
        ORDER BY 
            CASE t.categorie
                WHEN 'roi' THEN 1
                WHEN 'sniper' THEN 2
                WHEN 'banquier' THEN 3
                WHEN 'cactus' THEN 4
                WHEN 'grand_chelem' THEN 5
                WHEN 'joker_double' THEN 6
            END
    """, (semaine,))
    
    trophees = cursor.fetchall()
    
    if trophees:
        for categorie, pseudo, valeur, description in trophees:
            icone = {
                'roi': '👑',
                'sniper': '🎯',
                'banquier': '🎰',
                'cactus': '🌵',
                'grand_chelem': '💎',
                'joker_double': '🃏'
            }.get(categorie, '🏆')
            
            st.markdown(f"**{icone} {description}** : {pseudo} ({valeur:.1f} pts)")
    else:
        st.info("Aucun trophée attribué")
    
    conn.close()

if st.session_state.logged_in:
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.pseudo}")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "📝 Mes Pronos", "🏆 Classement", "🎪 Récap"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Déconnexion"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.pseudo = None
            st.session_state.prenom = None
            st.rerun()
    
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "📝 Mes Pronos":
        pronos_page()
    elif page == "🏆 Classement":
        classement_page()
    elif page == "🎪 Récap":
        recap_page()
else:
    login_page()