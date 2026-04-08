# app.py
import streamlit as st
import subprocess
import time
from airflow_client import trigger_dag, get_dag_status, get_dag_progress
from db import load_table
from dashboards import plot_indicator
from auth import require_auth

require_auth()

st.set_page_config(layout="wide")

# ========================
# HEADER AVEC 2 LOGOS
# ========================
header_left, header_center, header_right = st.columns([2, 6, 2])

with header_left:
    st.image("C:/Users/DELL/Documents/assets/drs.png", width=160)

with header_right:
    st.image("C:/Users/DELL/Documents/assets/drs2.png", width=160)

st.markdown(
    "<h1 style='text-align: center; color: #1F4BD8;'>📊 Plateforme d'automatisation SAP – DRS</h1>",
    unsafe_allow_html=True
)

# ========================
# SIDEBAR : Session + Statut des données
# ========================
st.sidebar.markdown("### 👤 Session")

if st.sidebar.button("🚪 Déconnexion"):
    st.session_state.authenticated = False
    st.session_state.dag_running = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Statut des données")

try:
    df_check = load_table("recap_trim")
    
    if df_check is not None and not df_check.empty:
        st.sidebar.success("✅ Données disponibles")
        
        # Afficher la dernière période disponible
        periodes = [c for c in df_check.columns if "_" in c]
        if periodes:
            derniere_periode = periodes[-1]
            st.sidebar.info(f"📅 Dernière période : {derniere_periode}")
    else:
        st.sidebar.warning("⚠️ Aucune donnée disponible")
        st.sidebar.info("💡 Lancez un traitement via Airflow")
        
except Exception:
    st.sidebar.warning("⚠️ Aucune donnée disponible")
    st.sidebar.info("💡 Lancez un traitement via Airflow")

# ========================
# Upload RATIOS
# ========================
st.header("1️⃣ Charger votre fichier RATIOS")

file = st.file_uploader("Uploader ratios.xlsx", type="xlsx")

if file:
    # Sauvegarder le fichier dans WSL
    try:
        temp_path = "temp_ratios.xlsx"
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        
        # Copier vers WSL
        subprocess.run(
            ["wsl", "cp", temp_path, "/home/bolade/airflow-docker/data/input/ratios.xlsx"],
            check=True
        )
        
        st.success("✅ Fichier chargé dans Airflow")
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement: {e}")

    # ========================
    # Boutons actions
    # ========================
    st.markdown("---")
    st.subheader("2️⃣ Lancer le traitement")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Lien vers Airflow
        airflow_url = "http://localhost:8080/dags/pca_pipeline_complet/"  
        
        st.markdown(
            f"""
            <a href="{airflow_url}" target="_blank">
                <button style="
                    background-color: #1F4BD8;
                    color: white;
                    padding: 0.75rem 1.5rem;
                    border: none;
                    border-radius: 0.5rem;
                    cursor: pointer;
                    font-size: 1rem;
                    font-weight: bold;
                    width: 100%;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                ">
                    🌐 Ouvrir Airflow pour lancer le traitement
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )
        
        st.info("💡 Cliquez sur le bouton **Play ▶️** en haut à droite du DAG dans Airflow pour lancer l'exécution")
    
    with col2:
        if st.button("🔄 Actualiser les données", use_container_width=True):
            st.rerun()

# ========================
# Téléchargement des fichiers générés
# ========================
st.markdown("---")
st.header("3️⃣ Télécharger les fichiers générés")

# Vérifier si des fichiers sont disponibles
files_available = False
try:
    result = subprocess.run(
        ["wsl", "test", "-f", "/home/bolade/airflow-docker/data/output/scores.xlsx"],
        capture_output=True,
        timeout=5
    )
    files_available = (result.returncode == 0)
except:
    pass

if not files_available:
    st.info("📂 Aucun fichier disponible. Lancez d'abord un traitement via Airflow.")
else:
    col1, col2, col3 = st.columns(3)

    # ========================
    # scores.xlsx
    # ========================
    with col1:
        try:
            result = subprocess.run(
                ["wsl", "cat", "/home/bolade/airflow-docker/data/output/scores.xlsx"],
                capture_output=True,
                timeout=10
            )

            if result.returncode == 0:
                st.download_button(
                    label="📥 Télécharger scores.xlsx",
                    data=result.stdout,
                    file_name="scores.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            else:
                st.info("📄 scores.xlsx non disponible")

        except Exception:
            st.info("📄 scores.xlsx non disponible")

    # ========================
    # recap_trim.xlsx
    # ========================
    with col2:
        try:
            result = subprocess.run(
                ["wsl", "cat", "/home/bolade/airflow-docker/data/output/recap_trim.xlsx"],
                capture_output=True,
                timeout=10
            )

            if result.returncode == 0:
                st.download_button(
                    label="📥 Télécharger recap_trim.xlsx",
                    data=result.stdout,
                    file_name="recap_trim.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            else:
                st.info("📄 recap_trim.xlsx non disponible")

        except Exception:
            st.info("📄 recap_trim.xlsx non disponible")

    # ========================
    # ZIP global
    # ========================
    with col3:
        try:
            import zipfile
            import io

            zip_buffer = io.BytesIO()

            files_to_zip = [
                "scores.xlsx",
                "sap.xlsx",
                "recap_scores.xlsx",
                "situation.xlsx",
                "recap_trim.xlsx"
            ]

            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for filename in files_to_zip:
                    try:
                        result = subprocess.run(
                            ["wsl", "cat", f"/home/bolade/airflow-docker/data/output/{filename}"],
                            capture_output=True,
                            timeout=10
                        )

                        if result.returncode == 0:
                            zip_file.writestr(filename, result.stdout)

                    except Exception:
                        pass  # fichier absent → ignoré

            zip_buffer.seek(0)

            if zip_buffer.getbuffer().nbytes > 0:
                st.download_button(
                    label="📦 Télécharger tous les fichiers (ZIP)",
                    data=zip_buffer,
                    file_name="airflow_resultats.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            else:
                st.info("📦 Aucun fichier disponible")

        except Exception as e:
            st.error(f"❌ Erreur ZIP : {e}")


# ========================
# Dashboards avec auto-refresh
# ========================
st.markdown("---")
st.header("4️⃣ Tableaux de bord")

try:
    df = load_table("recap_trim")
    
    if df is None or df.empty:
        st.info("⏳ En attente des résultats du traitement...")
        st.info("💡 Les dashboards apparaîtront automatiquement une fois le traitement terminé")
        
        # Auto-refresh toutes les 30 secondes
        with st.spinner("Actualisation automatique dans 30 secondes..."):
            time.sleep(30)
        st.rerun()
    else:
        periodes = [c for c in df.columns if "_" in c]
        
        if not periodes:
            st.warning("⚠️ Aucune période trouvée dans les données")
        else:
            default_periodes = periodes[-4:] if len(periodes) >= 4 else periodes

            selected = st.multiselect(
                "Sélectionner les périodes à afficher",
                periodes,
                default=default_periodes
            )

            if selected:
                for indic in df["Indicateur"].unique():
                    fig = plot_indicator(df, indic, selected)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 Sélectionnez au moins une période pour afficher les graphiques")
                
except Exception as e:
    st.error(f"❌ Erreur lors du chargement des dashboards : {e}")
    st.info("💡 Vérifiez que le traitement Airflow s'est bien terminé et que les données sont chargées dans PostgreSQL")




import pandas as pd
from datetime import datetime

# ========================
# MODULE : FILTRAGE PAR SITUATION
# ========================

st.markdown("---")
st.header("5️⃣ Filtrage des SFD par situation prudentielle")

# Charger les données
@st.cache_data
def load_situation_data():
    """Charge les données de la table situation"""
    df = load_table("situation")
    return df

df_situation = load_situation_data()

# Vérifier que les données existent
if df_situation is None or df_situation.empty:
    st.warning("⚠️ Aucune donnée disponible dans la table 'situation'")
    st.stop()

# ========================
# SÉLECTION DES FILTRES
# ========================

st.subheader("🔍 Critères de filtrage")

col1, col2, col3 = st.columns(3)

# ========================
# 1. SÉLECTION DE L'ANNÉE
# ========================
with col1:
    # Obtenir toutes les années disponibles
    annees_disponibles = sorted(df_situation['Année'].unique(), reverse=True)
    
    # Année en cours par défaut
    annee_en_cours = datetime.now().year
    default_annee = annee_en_cours if annee_en_cours in annees_disponibles else annees_disponibles[0]
    
    annee_selectionnee = st.selectbox(
        "📅 Sélectionner l'année",
        options=annees_disponibles,
        index=annees_disponibles.index(default_annee) if default_annee in annees_disponibles else 0
    )

# Filtrer par année
df_annee = df_situation[df_situation['Année'] == annee_selectionnee]

# ========================
# 2. SÉLECTION DES PÉRIODES
# ========================
with col2:
    # Obtenir toutes les périodes disponibles pour l'année sélectionnée
    periodes_disponibles = sorted(df_annee['Période'].unique(), reverse=True)
    
    # Sélectionner les 4 dernières périodes par défaut
    quatre_dernieres = periodes_disponibles[:4] if len(periodes_disponibles) >= 4 else periodes_disponibles
    
    periodes_selectionnees = st.multiselect(
        "📊 Sélectionner les périodes",
        options=periodes_disponibles,
        default=quatre_dernieres,
        help="Par défaut, les 4 dernières périodes sont sélectionnées"
    )

# Vérifier qu'au moins une période est sélectionnée
if not periodes_selectionnees:
    st.warning("⚠️ Veuillez sélectionner au moins une période")
    st.stop()

# Filtrer par périodes
df_filtered = df_annee[df_annee['Période'].isin(periodes_selectionnees)]

# ========================
# 3. SÉLECTION DE L'INDICATEUR
# ========================
with col3:
    indicateur = st.selectbox(
        "📈 Sélectionner l'indicateur",
        options=["SG", "RP", "QP", "EF/PRO", "RENT", "BIL"],
        format_func=lambda x: {
            "SG": "Situation Globale (SG)",
            "RP": "Ratio Prudentiel (RP)",
            "QP": "Qualité Portefeuille (QP)",
            "EF/PRO": "Efficacité/Productivité (EF/PRO)",
            "RENT": "Rentabilité (RENT)",
            "BIL": "Bilan (BIL)"
        }.get(x, x)
    )

# ========================
# 4. SÉLECTION DE LA SITUATION
# ========================

col_sit1, col_sit2, col_sit3 = st.columns([1, 1, 2])

with col_sit1:
    situation = st.selectbox(
        "🎯 Sélectionner la situation",
        options=["bonne", "satisfaisante", "difficile"]
    )

# Message récapitulatif
st.info(
    f"📊 Filtrage : **{indicateur}** = **{situation}** | "
    f"Année **{annee_selectionnee}** | "
    f"{len(periodes_selectionnees)} période(s) : {', '.join(periodes_selectionnees)}"
)

# ========================
# FILTRAGE DES DONNÉES
# ========================

# Filtrer selon l'indicateur et la situation sélectionnés
df_resultats = df_filtered[df_filtered[indicateur] == situation]

# ========================
# AFFICHAGE DES RÉSULTATS
# ========================

st.markdown("---")
st.subheader(f"📋 Liste des SFD")

if df_resultats.empty:
    st.warning(
        f"❌ Aucun SFD trouvé avec **{indicateur} = {situation}** "
        f"pour l'année **{annee_selectionnee}** sur les périodes sélectionnées"
    )
else:
    # Compter les occurrences par SFD
    compte_par_sfd = df_resultats.groupby(['AGREMENT', 'STRUCTURE']).size().reset_index(name='nb_periodes')
    compte_par_sfd = compte_par_sfd.sort_values('nb_periodes', ascending=False)
    
    st.success(f"✅ **{len(compte_par_sfd)} SFD** trouvé(s) avec {indicateur} = {situation}")
    
    # Afficher le tableau
    st.dataframe(
        compte_par_sfd.rename(columns={
            'AGREMENT': 'Agrément',
            'STRUCTURE': 'Structure',
            'nb_periodes': f'Nombre de périodes en situation {situation}'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # ========================
    # DÉTAILS PAR PÉRIODE
    # ========================
    
    with st.expander("📅 Voir le détail par période"):
        # Pivot pour voir toutes les périodes
        pivot_data = df_resultats.pivot_table(
            index=['AGREMENT', 'STRUCTURE'],
            columns='Période',
            values=indicateur,
            aggfunc='first'
        ).reset_index()
        
        st.dataframe(pivot_data, use_container_width=True, hide_index=True)
    
    # ========================
    # BOUTON DE TÉLÉCHARGEMENT
    # ========================
    
    # Convertir en CSV pour téléchargement
    csv = compte_par_sfd.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label=f"📥 Télécharger la liste ({len(compte_par_sfd)} SFD)",
        data=csv,
        file_name=f"SFD_{indicateur}_{situation}_{annee_selectionnee}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ========================
# STATISTIQUES GLOBALES
# ========================

st.markdown("---")
st.subheader(f"📊 Statistiques globales pour {indicateur}")

col1, col2, col3 = st.columns(3)

with col1:
    nb_bonne = len(df_filtered[df_filtered[indicateur] == "bonne"].groupby(['AGREMENT']).size())
    st.metric("Situation BONNE", nb_bonne, delta=None)

with col2:
    nb_satisfaisante = len(df_filtered[df_filtered[indicateur] == "satisfaisante"].groupby(['AGREMENT']).size())
    st.metric("Situation SATISFAISANTE", nb_satisfaisante, delta=None)

with col3:
    nb_difficile = len(df_filtered[df_filtered[indicateur] == "difficile"].groupby(['AGREMENT']).size())
    st.metric("Situation DIFFICILE", nb_difficile, delta=None)

