"""
Application Streamlit pour la collecte et l'analyse descriptive de données sportives.
Auteur : Généré avec Claude (Anthropic)
Description : Application complète permettant la collecte, l'analyse,
              la visualisation et l'export de données sportives.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import io
import os
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION GLOBALE DE LA PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SportAnalytics Pro",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS PERSONNALISÉ — thème sombre "stade"
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Importation des polices */
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* Palette */
    :root {
        --bg-dark:      #0a0d12;
        --bg-card:      #111620;
        --bg-sidebar:   #0d1018;
        --accent:       #00e5a0;
        --accent2:      #0af;
        --warning:      #ffb347;
        --danger:       #ff4f64;
        --text-primary: #e8edf5;
        --text-muted:   #7a8499;
        --border:       #1e2535;
    }

    /* Fond global */
    .stApp { background-color: var(--bg-dark); color: var(--text-primary); }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border);
    }

    /* Titres */
    h1, h2, h3, h4 {
        font-family: 'Barlow Condensed', sans-serif !important;
        letter-spacing: 0.04em;
        color: var(--text-primary) !important;
    }
    h1 { font-size: 2.6rem !important; font-weight: 800 !important; }

    /* Accent sur les métriques */
    [data-testid="stMetricValue"] {
        font-family: 'IBM Plex Mono', monospace !important;
        color: var(--accent) !important;
        font-size: 1.6rem !important;
    }
    [data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 0.75rem !important; }

    /* Cartes / expanders */
    [data-testid="stExpander"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
        color: #000 !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.4rem !important;
        text-transform: uppercase !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    /* Onglets */
    .stTabs [data-baseweb="tab"] {
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.05em !important;
        color: var(--text-muted) !important;
    }
    .stTabs [aria-selected="true"] { color: var(--accent) !important; }

    /* DataFrames */
    [data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 8px !important; }

    /* Inputs */
    input, select, textarea {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-color: var(--border) !important;
    }

    /* Séparateur stylisé */
    hr { border-color: var(--border) !important; }

    /* Badge accent */
    .badge-accent {
        display: inline-block;
        background: var(--accent);
        color: #000;
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700;
        font-size: 0.7rem;
        letter-spacing: 0.1em;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
    }

    /* Alerte personnalisée */
    .custom-warning {
        background: rgba(255,179,71,0.12);
        border-left: 3px solid var(--warning);
        padding: 0.75rem 1rem;
        border-radius: 0 6px 6px 0;
        color: var(--warning);
        font-size: 0.9rem;
    }
    .custom-danger {
        background: rgba(255,79,100,0.12);
        border-left: 3px solid var(--danger);
        padding: 0.75rem 1rem;
        border-radius: 0 6px 6px 0;
        color: var(--danger);
        font-size: 0.9rem;
    }
    .custom-success {
        background: rgba(0,229,160,0.1);
        border-left: 3px solid var(--accent);
        padding: 0.75rem 1rem;
        border-radius: 0 6px 6px 0;
        color: var(--accent);
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# THÈME MATPLOTLIB (graphiques cohérents)
# ─────────────────────────────────────────────
PLOT_BG     = "#111620"
PLOT_FG     = "#e8edf5"
ACCENT_CLR  = "#00e5a0"
ACCENT2_CLR = "#00aaff"
PALETTE     = ["#00e5a0", "#00aaff", "#ffb347", "#ff4f64", "#bf7fff", "#ff6eb4",
               "#7fffd4", "#ffd700", "#f08080", "#87ceeb"]

def appliquer_theme_matplotlib():
    """Applique le thème sombre personnalisé à tous les graphiques Matplotlib."""
    plt.rcParams.update({
        "figure.facecolor":  PLOT_BG,
        "axes.facecolor":    PLOT_BG,
        "axes.edgecolor":    "#1e2535",
        "axes.labelcolor":   PLOT_FG,
        "axes.titlecolor":   PLOT_FG,
        "axes.titlesize":    13,
        "axes.labelsize":    11,
        "axes.grid":         True,
        "grid.color":        "#1e2535",
        "grid.linewidth":    0.6,
        "text.color":        PLOT_FG,
        "xtick.color":       "#7a8499",
        "ytick.color":       "#7a8499",
        "xtick.labelsize":   9,
        "ytick.labelsize":   9,
        "legend.facecolor":  "#0d1018",
        "legend.edgecolor":  "#1e2535",
        "legend.labelcolor": PLOT_FG,
        "figure.dpi":        120,
    })

appliquer_theme_matplotlib()

# ─────────────────────────────────────────────
# ÉTAT DE SESSION — initialisation
# ─────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

# ─────────────────────────────────────────────
# FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────

def fig_vers_bytes(fig) -> bytes:
    """Convertit une figure Matplotlib en bytes PNG pour le téléchargement."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight",
                facecolor=fig.get_facecolor(), dpi=150)
    buf.seek(0)
    return buf.getvalue()


def detecter_aberrantes_iqr(serie: pd.Series):
    """
    Détecte les valeurs aberrantes via la méthode IQR.
    Retourne le masque booléen des outliers.
    """
    Q1, Q3 = serie.quantile(0.25), serie.quantile(0.75)
    IQR = Q3 - Q1
    borne_basse  = Q1 - 1.5 * IQR
    borne_haute  = Q3 + 1.5 * IQR
    return (serie < borne_basse) | (serie > borne_haute)


def colonnes_numeriques(df: pd.DataFrame) -> list:
    """Retourne la liste des colonnes numériques du DataFrame."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def colonnes_categorielles(df: pd.DataFrame) -> list:
    """Retourne la liste des colonnes catégorielles du DataFrame."""
    return df.select_dtypes(include=["object", "category"]).columns.tolist()

# ─────────────────────────────────────────────
# EN-TÊTE PRINCIPAL
# ─────────────────────────────────────────────
st.markdown("""
<div style='padding: 1.2rem 0 0.5rem 0;'>
    <span class='badge-accent'>v1.0</span>
    <h1 style='margin: 0.3rem 0 0.1rem 0;'>🏆 SportAnalytics Pro</h1>
    <p style='color:#7a8499; font-size:0.95rem; margin:0;'>
        Collecte · Analyse descriptive · Visualisation de données sportives
    </p>
</div>
<hr>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR — FILTRES INTERACTIFS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filtres")
    st.markdown("---")

    df_global = st.session_state.df.copy()

    if df_global.empty:
        st.info("Chargez des données pour activer les filtres.")
        df_filtre = df_global
    else:
        # ── Recherche par nom ──────────────────
        recherche_nom = st.text_input("🔍 Rechercher un joueur", "")

        # ── Filtre Sport ───────────────────────
        sports_dispo = ["Tous"]
        if "sport" in df_global.columns:
            sports_dispo += sorted(df_global["sport"].dropna().unique().tolist())
        sport_sel = st.selectbox("⚽ Sport", sports_dispo)

        # ── Filtre Équipe ──────────────────────
        equipes_dispo = ["Toutes"]
        if "equipe" in df_global.columns:
            equipes_dispo += sorted(df_global["equipe"].dropna().unique().tolist())
        equipe_sel = st.selectbox("🏟️ Équipe", equipes_dispo)

        # ── Filtre Poste ───────────────────────
        postes_dispo = ["Tous"]
        if "poste" in df_global.columns:
            postes_dispo += sorted(df_global["poste"].dropna().unique().tolist())
        poste_sel = st.selectbox("👕 Poste", postes_dispo)

        # ── Filtre Âge ─────────────────────────
        if "age" in df_global.columns and df_global["age"].notna().any():
            age_min = int(df_global["age"].min())
            age_max = int(df_global["age"].max())
            if age_min < age_max:
                age_range = st.slider("🎂 Tranche d'âge",
                                      age_min, age_max, (age_min, age_max))
            else:
                age_range = (age_min, age_max)
                st.write(f"Âge unique : {age_min}")
        else:
            age_range = None

        # ── Application des filtres ────────────
        df_filtre = df_global.copy()

        if recherche_nom and "nom" in df_filtre.columns:
            df_filtre = df_filtre[
                df_filtre["nom"].str.contains(recherche_nom, case=False, na=False)
            ]

        if sport_sel != "Tous" and "sport" in df_filtre.columns:
            df_filtre = df_filtre[df_filtre["sport"] == sport_sel]

        if equipe_sel != "Toutes" and "equipe" in df_filtre.columns:
            df_filtre = df_filtre[df_filtre["equipe"] == equipe_sel]

        if poste_sel != "Tous" and "poste" in df_filtre.columns:
            df_filtre = df_filtre[df_filtre["poste"] == poste_sel]

        if age_range and "age" in df_filtre.columns:
            df_filtre = df_filtre[
                df_filtre["age"].between(age_range[0], age_range[1])
            ]

        st.markdown("---")
        st.metric("Joueurs filtrés", len(df_filtre))
        st.metric("Total joueurs",   len(df_global))

# ─────────────────────────────────────────────
# ONGLETS PRINCIPAUX
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Collecte",
    "📊 Analyse",
    "📈 Visualisations",
    "🔎 Données",
    "💾 Export"
])

# ══════════════════════════════════════════════
# ONGLET 1 — COLLECTE DES DONNÉES
# ══════════════════════════════════════════════
with tab1:
    st.subheader("Importer un fichier")

    col_upload, col_info = st.columns([2, 1])

    with col_upload:
        fichier = st.file_uploader(
            "Déposer un fichier CSV ou Excel",
            type=["csv", "xlsx", "xls"],
            help="Formats supportés : .csv, .xlsx, .xls"
        )

        if fichier is not None:
            try:
                # Détermination du type de fichier
                nom_fichier = fichier.name.lower()
                if nom_fichier.endswith(".csv"):
                    # Tentative auto-détection du séparateur
                    contenu = fichier.read()
                    fichier.seek(0)
                    separateur = ";" if contenu.count(b";") > contenu.count(b",") else ","
                    df_import = pd.read_csv(fichier, sep=separateur)
                elif nom_fichier.endswith((".xlsx", ".xls")):
                    df_import = pd.read_excel(fichier, engine="openpyxl")
                else:
                    st.error("Format de fichier non reconnu.")
                    df_import = None

                if df_import is not None:
                    if df_import.empty:
                        st.markdown('<div class="custom-danger">⚠️ Le fichier importé est vide.</div>',
                                    unsafe_allow_html=True)
                    else:
                        # Nettoyage minimal des noms de colonnes
                        df_import.columns = (
                            df_import.columns.str.strip()
                                             .str.lower()
                                             .str.replace(" ", "_")
                                             .str.replace(r"[^a-z0-9_]", "", regex=True)
                        )
                        st.session_state.df = df_import
                        st.markdown(
                            f'<div class="custom-success">✅ Fichier chargé : '
                            f'{len(df_import)} lignes × {len(df_import.columns)} colonnes</div>',
                            unsafe_allow_html=True
                        )
                        st.dataframe(df_import.head(5), use_container_width=True)

            except Exception as e:
                st.markdown(
                    f'<div class="custom-danger">❌ Erreur lors de l\'import : {e}</div>',
                    unsafe_allow_html=True
                )

    with col_info:
        st.markdown("##### Format attendu")
        exemple = pd.DataFrame({
            "nom":            ["Dupont L.", "Martin R."],
            "sport":          ["Football", "Basketball"],
            "equipe":         ["PSG", "Asvel"],
            "age":            [24, 29],
            "poste":          ["Milieu", "Pivot"],
            "buts_passes":    [12, 0],
            "passes":         [45, 32],
            "matchs_joues":   [30, 28],
            "note_moyenne":   [7.8, 6.9],
        })
        st.dataframe(exemple, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Saisie manuelle d'un joueur")

    with st.expander("➕ Ajouter un joueur manuellement", expanded=False):
        with st.form("formulaire_joueur", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                nom     = st.text_input("Nom du joueur *")
                sport   = st.selectbox("Sport *",
                    ["Football", "Basketball", "Tennis", "Rugby",
                     "Handball", "Volleyball", "Natation", "Athlétisme", "Autre"])
                equipe  = st.text_input("Équipe")
            with c2:
                age     = st.number_input("Âge", 10, 60, 22)
                poste   = st.text_input("Poste")
                matchs  = st.number_input("Matchs joués", 0, 100, 0)
            with c3:
                buts    = st.number_input("Buts / Points", 0, 500, 0)
                passes  = st.number_input("Passes / Assists", 0, 300, 0)
                note    = st.number_input("Note moyenne (0-10)", 0.0, 10.0, 5.0, step=0.1)

            soumis = st.form_submit_button("✅ Ajouter le joueur")

            if soumis:
                if not nom.strip():
                    st.error("Le nom du joueur est obligatoire.")
                else:
                    nouvelle_ligne = {
                        "nom":           nom.strip(),
                        "sport":         sport,
                        "equipe":        equipe.strip() or "Non définie",
                        "age":           age,
                        "poste":         poste.strip() or "Non défini",
                        "buts_passes":   buts,
                        "passes":        passes,
                        "matchs_joues":  matchs,
                        "note_moyenne":  note,
                    }
                    nouvelle_df = pd.DataFrame([nouvelle_ligne])

                    if st.session_state.df.empty:
                        st.session_state.df = nouvelle_df
                    else:
                        # Fusion intelligente : aligner les colonnes
                        st.session_state.df = pd.concat(
                            [st.session_state.df, nouvelle_df],
                            ignore_index=True
                        )
                    st.success(f"✅ Joueur « {nom} » ajouté avec succès !")

    # ── Sauvegarde rapide en CSV ────────────────
    if not st.session_state.df.empty:
        st.markdown("---")
        st.subheader("Sauvegarde locale")
        csv_bytes = st.session_state.df.to_csv(index=False, sep=";",
                                                 encoding="utf-8-sig").encode("utf-8-sig")
        nom_fichier_export = f"donnees_sport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        st.download_button(
            label="💾 Télécharger les données brutes (CSV)",
            data=csv_bytes,
            file_name=nom_fichier_export,
            mime="text/csv"
        )

# ══════════════════════════════════════════════
# ONGLET 2 — ANALYSE DESCRIPTIVE
# ══════════════════════════════════════════════
with tab2:
    if df_filtre.empty:
        st.info("Aucune donnée à analyser. Chargez un fichier ou ajoutez des joueurs.")
    else:
        num_cols  = colonnes_numeriques(df_filtre)
        cat_cols  = colonnes_categorielles(df_filtre)

        # ── KPIs rapides ────────────────────────────
        st.subheader("Vue d'ensemble")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Joueurs",    len(df_filtre))
        k2.metric("Variables",  len(df_filtre.columns))
        k3.metric("Numériques", len(num_cols))
        k4.metric("Catégorielles", len(cat_cols))

        st.markdown("---")

        # ── Statistiques descriptives ───────────────
        st.subheader("📐 Statistiques descriptives — Variables numériques")
        if num_cols:
            stats = df_filtre[num_cols].agg(
                ["mean", "median", "std", "min", "max", "count"]
            ).T.rename(columns={
                "mean":   "Moyenne",
                "median": "Médiane",
                "std":    "Écart-type",
                "min":    "Min",
                "max":    "Max",
                "count":  "Effectif",
            })
            stats = stats.round(3)
            st.dataframe(stats, use_container_width=True)
        else:
            st.info("Aucune colonne numérique détectée.")

        st.markdown("---")

        # ── Tableaux de fréquence ───────────────────
        st.subheader("📋 Tableaux de fréquence — Variables catégorielles")
        if cat_cols:
            col_sel = st.selectbox("Sélectionner une variable", cat_cols)
            freq = (df_filtre[col_sel]
                    .value_counts()
                    .reset_index()
                    .rename(columns={"index": col_sel, "count": "Effectif"}))
            freq.columns = [col_sel, "Effectif"]
            freq["Fréquence (%)"] = (freq["Effectif"] / freq["Effectif"].sum() * 100).round(2)
            freq["Fréq. cumulée (%)"] = freq["Fréquence (%)"].cumsum().round(2)
            st.dataframe(freq, use_container_width=True, hide_index=True)
        else:
            st.info("Aucune colonne catégorielle détectée.")

        st.markdown("---")

        # ── Valeurs manquantes ──────────────────────
        st.subheader("🔍 Détection des valeurs manquantes")
        manquantes = df_filtre.isnull().sum().reset_index()
        manquantes.columns = ["Variable", "Nb manquants"]
        manquantes["% manquants"] = (
            manquantes["Nb manquants"] / len(df_filtre) * 100
        ).round(2)
        manquantes = manquantes[manquantes["Nb manquants"] > 0]

        if manquantes.empty:
            st.markdown('<div class="custom-success">✅ Aucune valeur manquante détectée.</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="custom-warning">⚠️ {len(manquantes)} variable(s) contiennent des valeurs manquantes.</div>',
                unsafe_allow_html=True
            )
            st.dataframe(manquantes, use_container_width=True, hide_index=True)

        st.markdown("---")

        # ── Valeurs aberrantes (IQR) ────────────────
        st.subheader("⚠️ Détection des valeurs aberrantes (méthode IQR)")
        if num_cols:
            rapport_aberrantes = []
            for col in num_cols:
                serie = df_filtre[col].dropna()
                if len(serie) >= 4:
                    masque = detecter_aberrantes_iqr(serie)
                    nb = masque.sum()
                    if nb > 0:
                        Q1, Q3 = serie.quantile(0.25), serie.quantile(0.75)
                        IQR = Q3 - Q1
                        rapport_aberrantes.append({
                            "Variable":     col,
                            "Nb outliers":  nb,
                            "% outliers":   round(nb / len(serie) * 100, 2),
                            "Borne basse":  round(Q1 - 1.5 * IQR, 3),
                            "Borne haute":  round(Q3 + 1.5 * IQR, 3),
                        })

            if rapport_aberrantes:
                df_aberrantes = pd.DataFrame(rapport_aberrantes)
                st.markdown(
                    f'<div class="custom-warning">⚠️ Valeurs aberrantes détectées dans '
                    f'{len(rapport_aberrantes)} variable(s).</div>',
                    unsafe_allow_html=True
                )
                st.dataframe(df_aberrantes, use_container_width=True, hide_index=True)
            else:
                st.markdown('<div class="custom-success">✅ Aucune valeur aberrante détectée.</div>',
                            unsafe_allow_html=True)
        else:
            st.info("Aucune colonne numérique disponible pour l'analyse.")

# ══════════════════════════════════════════════
# ONGLET 3 — VISUALISATIONS
# ══════════════════════════════════════════════
with tab3:
    if df_filtre.empty:
        st.info("Aucune donnée à visualiser.")
    else:
        num_cols = colonnes_numeriques(df_filtre)
        cat_cols = colonnes_categorielles(df_filtre)

        if not num_cols:
            st.warning("Aucune colonne numérique disponible pour les graphiques.")
        else:
            # ── HISTOGRAMME ─────────────────────────────
            st.subheader("📊 Histogramme des performances")
            col_hist = st.selectbox("Variable pour l'histogramme", num_cols, key="hist_var")
            bins_hist = st.slider("Nombre de classes", 5, 50, 15, key="hist_bins")

            fig_hist, ax = plt.subplots(figsize=(10, 4))
            ax.hist(df_filtre[col_hist].dropna(), bins=bins_hist,
                    color=ACCENT_CLR, edgecolor=PLOT_BG, alpha=0.85)
            # Ligne de moyenne
            moy = df_filtre[col_hist].mean()
            ax.axvline(moy, color=ACCENT2_CLR, lw=1.5, linestyle="--",
                       label=f"Moyenne = {moy:.2f}")
            ax.set_title(f"Distribution de « {col_hist} »")
            ax.set_xlabel(col_hist)
            ax.set_ylabel("Fréquence")
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig_hist)

            dl_hist = st.download_button(
                "⬇️ Télécharger l'histogramme",
                data=fig_vers_bytes(fig_hist),
                file_name="histogramme.png",
                mime="image/png",
                key="dl_hist"
            )
            plt.close(fig_hist)

            st.markdown("---")

            # ── BOXPLOT ──────────────────────────────────
            st.subheader("📦 Boxplot par groupe")
            col_box_y  = st.selectbox("Variable numérique (Y)", num_cols, key="box_y")
            col_box_x_opts = [c for c in cat_cols if df_filtre[c].nunique() <= 20]
            if col_box_x_opts:
                col_box_x = st.selectbox("Grouper par", col_box_x_opts, key="box_x")
                groupes = sorted(df_filtre[col_box_x].dropna().unique())
                donnees_box = [
                    df_filtre.loc[df_filtre[col_box_x] == g, col_box_y].dropna().values
                    for g in groupes
                ]
                fig_box, ax = plt.subplots(figsize=(max(8, len(groupes) * 1.2), 5))
                bp = ax.boxplot(donnees_box, patch_artist=True, notch=False,
                                medianprops=dict(color=ACCENT2_CLR, lw=2))
                for patch, couleur in zip(bp["boxes"],
                                          [PALETTE[i % len(PALETTE)] for i in range(len(groupes))]):
                    patch.set_facecolor(couleur)
                    patch.set_alpha(0.75)
                ax.set_xticklabels(groupes, rotation=25, ha="right")
                ax.set_title(f"Boxplot de « {col_box_y} » par « {col_box_x} »")
                ax.set_ylabel(col_box_y)
                plt.tight_layout()
                st.pyplot(fig_box)
                st.download_button(
                    "⬇️ Télécharger le boxplot",
                    data=fig_vers_bytes(fig_box),
                    file_name="boxplot.png",
                    mime="image/png",
                    key="dl_box"
                )
                plt.close(fig_box)
            else:
                st.info("Aucune colonne catégorielle avec ≤ 20 modalités pour le groupage.")

            st.markdown("---")

            # ── HEATMAP DE CORRÉLATION ───────────────────
            st.subheader("🔥 Heatmap des corrélations")
            if len(num_cols) >= 2:
                corr = df_filtre[num_cols].corr()
                fig_hm, ax = plt.subplots(
                    figsize=(max(6, len(num_cols)), max(5, len(num_cols) * 0.85))
                )
                cmap = sns.diverging_palette(220, 20, as_cmap=True)
                sns.heatmap(corr, ax=ax, cmap=cmap, annot=True, fmt=".2f",
                            linewidths=0.4, linecolor=PLOT_BG,
                            square=True, annot_kws={"size": 8},
                            cbar_kws={"shrink": 0.8})
                ax.set_title("Matrice de corrélation (Pearson)")
                plt.xticks(rotation=30, ha="right")
                plt.tight_layout()
                st.pyplot(fig_hm)
                st.download_button(
                    "⬇️ Télécharger la heatmap",
                    data=fig_vers_bytes(fig_hm),
                    file_name="heatmap_correlations.png",
                    mime="image/png",
                    key="dl_hm"
                )
                plt.close(fig_hm)
            else:
                st.info("Au moins 2 variables numériques requises pour la heatmap.")

            st.markdown("---")

            # ── GRAPHIQUE EN BARRES COMPARATIF ───────────
            st.subheader("📊 Comparaison entre joueurs")
            col_bar_y   = st.selectbox("Statistique à comparer", num_cols, key="bar_y")
            col_nom_opts = [c for c in df_filtre.columns
                            if df_filtre[c].dtype == object and df_filtre[c].nunique() <= 40]

            if col_nom_opts:
                col_nom   = st.selectbox("Colonne identifiant le joueur/groupe", col_nom_opts, key="bar_nom")
                nb_joueurs = st.slider("Nombre de joueurs à afficher", 5, 30, 10, key="bar_nb")

                df_bar = (df_filtre.groupby(col_nom)[col_bar_y]
                          .mean()
                          .sort_values(ascending=False)
                          .head(nb_joueurs)
                          .reset_index())

                fig_bar, ax = plt.subplots(figsize=(10, max(4, nb_joueurs * 0.45)))
                colors = [PALETTE[i % len(PALETTE)] for i in range(len(df_bar))]
                bars = ax.barh(df_bar[col_nom], df_bar[col_bar_y],
                               color=colors, edgecolor=PLOT_BG, alpha=0.88)

                # Valeurs sur les barres
                for bar, val in zip(bars, df_bar[col_bar_y]):
                    ax.text(val + 0.01 * df_bar[col_bar_y].max(),
                            bar.get_y() + bar.get_height() / 2,
                            f"{val:.2f}", va="center", color=PLOT_FG, fontsize=8)

                ax.set_title(f"Top {nb_joueurs} — « {col_bar_y} » (moyenne)")
                ax.set_xlabel(col_bar_y)
                ax.invert_yaxis()
                plt.tight_layout()
                st.pyplot(fig_bar)
                st.download_button(
                    "⬇️ Télécharger le graphique en barres",
                    data=fig_vers_bytes(fig_bar),
                    file_name="barres_comparatif.png",
                    mime="image/png",
                    key="dl_bar"
                )
                plt.close(fig_bar)
            else:
                st.info("Aucune colonne de texte disponible pour l'axe des joueurs/groupes.")

# ══════════════════════════════════════════════
# ONGLET 4 — TABLEAU DE DONNÉES
# ══════════════════════════════════════════════
with tab4:
    if df_filtre.empty:
        st.info("Aucune donnée disponible.")
    else:
        st.subheader(f"Tableau filtré — {len(df_filtre)} enregistrement(s)")
        st.dataframe(df_filtre, use_container_width=True)

        # Aperçu rapide des types
        with st.expander("🔬 Types de données et infos colonnes"):
            info_df = pd.DataFrame({
                "Type":           df_filtre.dtypes.astype(str),
                "Nb non-nuls":    df_filtre.count(),
                "% rempli":       (df_filtre.count() / len(df_filtre) * 100).round(1),
                "Nb uniques":     df_filtre.nunique(),
            })
            st.dataframe(info_df, use_container_width=True)

# ══════════════════════════════════════════════
# ONGLET 5 — EXPORT
# ══════════════════════════════════════════════
with tab5:
    if df_filtre.empty:
        st.info("Aucune donnée à exporter.")
    else:
        st.subheader("💾 Export du rapport d'analyse")

        # ── Construction du rapport CSV ─────────────
        rapport_lignes = []

        # En-tête
        rapport_lignes.append(["=== RAPPORT D'ANALYSE SPORTIVE ==="])
        rapport_lignes.append([f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"])
        rapport_lignes.append([f"Joueurs analysés : {len(df_filtre)}"])
        rapport_lignes.append([])

        # Statistiques descriptives
        num_cols = colonnes_numeriques(df_filtre)
        if num_cols:
            rapport_lignes.append(["--- STATISTIQUES DESCRIPTIVES ---"])
            stats = df_filtre[num_cols].agg(
                ["mean", "median", "std", "min", "max", "count"]
            ).T.rename(columns={
                "mean":   "Moyenne",
                "median": "Médiane",
                "std":    "Écart-type",
                "min":    "Min",
                "max":    "Max",
                "count":  "Effectif",
            }).round(3)
            rapport_lignes.append(["Variable"] + stats.columns.tolist())
            for idx, row in stats.iterrows():
                rapport_lignes.append([idx] + row.tolist())
            rapport_lignes.append([])

        # Valeurs manquantes
        rapport_lignes.append(["--- VALEURS MANQUANTES ---"])
        manquantes = df_filtre.isnull().sum()
        for col, nb in manquantes.items():
            pct = round(nb / len(df_filtre) * 100, 2)
            rapport_lignes.append([col, f"{nb} manquant(s)", f"{pct}%"])
        rapport_lignes.append([])

        # Valeurs aberrantes
        rapport_lignes.append(["--- VALEURS ABERRANTES (IQR) ---"])
        for col in num_cols:
            serie = df_filtre[col].dropna()
            if len(serie) >= 4:
                masque = detecter_aberrantes_iqr(serie)
                nb = masque.sum()
                rapport_lignes.append([col, f"{nb} outlier(s)",
                                        f"{round(nb/len(serie)*100,2)}%"])
        rapport_lignes.append([])

        # Données filtrées
        rapport_lignes.append(["--- DONNÉES FILTRÉES ---"])
        rapport_lignes.append(df_filtre.columns.tolist())
        for _, row in df_filtre.iterrows():
            rapport_lignes.append(row.tolist())

        # Conversion en CSV
        buf_rapport = io.StringIO()
        import csv
        writer = csv.writer(buf_rapport, delimiter=";")
        writer.writerows(rapport_lignes)
        rapport_bytes = buf_rapport.getvalue().encode("utf-8-sig")

        st.download_button(
            label="📄 Télécharger le rapport complet (CSV)",
            data=rapport_bytes,
            file_name=f"rapport_sport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.subheader("📸 Export groupé des graphiques")
        st.info(
            "Rendez-vous dans l'onglet **Visualisations** pour télécharger "
            "chaque graphique individuellement en PNG haute résolution."
        )

        # Récapitulatif en bas
        st.markdown("---")
        st.markdown("#### Récapitulatif du jeu de données filtré")
        kp1, kp2, kp3, kp4 = st.columns(4)
        kp1.metric("Lignes",        len(df_filtre))
        kp2.metric("Colonnes",      len(df_filtre.columns))
        kp3.metric("Numériques",    len(num_cols))
        kp4.metric("% complet",
                   f"{round((df_filtre.notna().sum().sum() / df_filtre.size) * 100, 1)}%")

# ─────────────────────────────────────────────
# PIED DE PAGE
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#7a8499; font-size:0.8rem;'>"
    "SportAnalytics Pro · Propulsé par Streamlit · "
    f"Session du {datetime.now().strftime('%d/%m/%Y')}"
    "</p>",
    unsafe_allow_html=True
)