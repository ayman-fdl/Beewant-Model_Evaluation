import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Rapport d'Évaluation Qwen 3 - Search Web",
    page_icon="📊",
    layout="wide"
)

# Titre de l'application
st.title("Rapport d'Évaluation Qwen 3 - Search Web")
st.markdown("""
Cette application présente une analyse détaillée des performances de Qwen 3 dans différents domaines thématiques.
Les évaluations sont basées sur des critères précis pour les sources et les réponses.
""")

# Chargement des données
@st.cache_data
def load_evaluation_data():
    data = []
    for file in os.listdir("evaluation_web"):
        if file.endswith(".json"):
            with open(os.path.join("evaluation_web", file), "r") as f:
                eval_data = json.load(f)
                thematic = file.replace("Evaluation_", "").replace(".json", "")
                
                # Calcul des moyennes des sources
                source_relevance = np.mean([source["relevance"] for source in eval_data["sources"]])
                source_credibility = np.mean([source["credibility"] for source in eval_data["sources"]])
                source_freshness = np.mean([source["freshness"] for source in eval_data["sources"]])
                
                for response in eval_data["response"]:
                    data.append({
                        "thematic": thematic,
                        "model": response["model"],
                        "source_relevance": source_relevance,
                        "source_credibility": source_credibility,
                        "source_freshness": source_freshness,
                        "relevance": response["Relevance"],
                        "correctness": response["Correctness"],
                        "completeness": response["Completeness"],
                        "clarity": response["Clarity"],
                        "depth": response["Depth"],
                        "comment": response["Comment"]
                    })
    return pd.DataFrame(data)

# Chargement des données
df = load_evaluation_data()

# Section des critères d'évaluation
st.header("Critères d'Évaluation")

with st.expander("Critères d'Évaluation des Sources", expanded=False):
    st.markdown("""
    ### Pertinence (1-5)
    Évalue dans quelle mesure le titre et le snippet de la source indiquent clairement qu'elle contient des informations pertinentes pour la question. La pertinence est jugée sur la base de la correspondance entre les mots-clés de la question et ceux présents dans le titre et le snippet.

    ### Crédibilité (1-5)
    Évalue la fiabilité apparente de la source basée sur le domaine du lien (par exemple, .edu, .gov, .org), le nom du site web, et la formulation du titre et du snippet. Les sources provenant de domaines institutionnels, de médias reconnus ou d'organisations établies sont considérées comme plus crédibles.

    ### Actualité (1-5)
    Mesure la fraîcheur apparente de l'information basée sur les indices temporels présents dans le titre et le snippet (dates, références à des événements récents). L'évaluation se fait sur la base des mentions explicites de dates ou d'événements récents dans le snippet.
    """)

with st.expander("Critères d'Évaluation des Réponses", expanded=False):
    st.markdown("""
    ### Pertinence (1-5)
    Évalue dans quelle mesure la réponse répond directement et précisément à la question posée, sans digression ni information superflue. Une réponse pertinente doit rester focalisée sur le sujet demandé.

    ### Exactitude (1-5)
    Mesure la précision et la fiabilité des informations fournies. Une réponse exacte doit être basée sur des faits vérifiables et des sources fiables, sans erreurs factuelles ou interprétations incorrectes.

    ### Exhaustivité (1-5)
    Évalue la couverture complète du sujet, en incluant tous les aspects importants de la question. Une réponse exhaustive doit aborder tous les points essentiels sans omissions significatives.

    ### Clarté (1-5)
    Mesure la qualité de la structure et de la présentation de la réponse. Une réponse claire doit être bien organisée, facile à comprendre et utiliser un langage approprié pour le sujet.

    ### Profondeur (1-5)
    Évalue le niveau d'analyse et de détail fourni dans la réponse. Une réponse profonde doit aller au-delà des informations de base, fournissant des analyses pertinentes et des détails significatifs.
    """)

# Section 1: Vue d'ensemble
st.header("Vue d'Ensemble")

# Création de deux colonnes pour les graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader("Évaluation des Sources")
    # Calcul des moyennes globales pour les sources
    source_metrics = {
        "Pertinence": df["source_relevance"].mean(),
        "Crédibilité": df["source_credibility"].mean(),
        "Actualité": df["source_freshness"].mean()
    }
    
    # Création du graphique pour les sources
    source_fig = go.Figure()
    source_fig.add_trace(go.Bar(
        x=list(source_metrics.keys()),
        y=list(source_metrics.values()),
        text=[f"{val:.2f}" for val in source_metrics.values()],
        textposition='auto',
    ))
    
    source_fig.update_layout(
        title="Moyennes Globales des Sources",
        yaxis=dict(range=[0, 5]),
        showlegend=False
    )
    st.plotly_chart(source_fig, use_container_width=True)

with col2:
    st.subheader("Évaluation des Réponses")
    # Calcul des moyennes globales pour les réponses
    response_metrics = {
        "Pertinence": df["relevance"].mean(),
        "Exactitude": df["correctness"].mean(),
        "Exhaustivité": df["completeness"].mean(),
        "Clarté": df["clarity"].mean(),
        "Profondeur": df["depth"].mean()
    }
    
    # Création du graphique pour les réponses
    response_fig = go.Figure()
    response_fig.add_trace(go.Bar(
        x=list(response_metrics.keys()),
        y=list(response_metrics.values()),
        text=[f"{val:.2f}" for val in response_metrics.values()],
        textposition='auto',
    ))
    
    response_fig.update_layout(
        title="Moyennes Globales des Réponses",
        yaxis=dict(range=[0, 5]),
        showlegend=False
    )
    st.plotly_chart(response_fig, use_container_width=True)

# Affichage des statistiques détaillées
st.subheader("Statistiques Détaillées")

# Création de deux colonnes pour les statistiques
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sources")
    source_stats = pd.DataFrame({
        "Critère": ["Pertinence", "Crédibilité", "Actualité"],
        "Moyenne": [df["source_relevance"].mean(), df["source_credibility"].mean(), df["source_freshness"].mean()],
        "Min": [df["source_relevance"].min(), df["source_credibility"].min(), df["source_freshness"].min()],
        "Max": [df["source_relevance"].max(), df["source_credibility"].max(), df["source_freshness"].max()]
    })
    # Formatage des colonnes numériques uniquement
    numeric_cols = source_stats.columns.difference(['Critère'])
    st.dataframe(source_stats.style.format({col: "{:.2f}" for col in numeric_cols}))

with col2:
    st.markdown("### Réponses")
    response_stats = pd.DataFrame({
        "Critère": ["Pertinence", "Exactitude", "Exhaustivité", "Clarté", "Profondeur"],
        "Moyenne": [df["relevance"].mean(), df["correctness"].mean(), df["completeness"].mean(), df["clarity"].mean(), df["depth"].mean()],
        "Min": [df["relevance"].min(), df["correctness"].min(), df["completeness"].min(), df["clarity"].min(), df["depth"].min()],
        "Max": [df["relevance"].max(), df["correctness"].max(), df["completeness"].max(), df["clarity"].max(), df["depth"].max()]
    })
    # Formatage des colonnes numériques uniquement
    numeric_cols = response_stats.columns.difference(['Critère'])
    st.dataframe(response_stats.style.format({col: "{:.2f}" for col in numeric_cols}))

# Section 2: Analyse par Thématique
st.header("Analyse par Thématique")

# Sélection de la thématique
selected_thematic = st.selectbox(
    "Sélectionnez une thématique",
    options=sorted(df['thematic'].unique())
)

# Filtrage des données pour la thématique sélectionnée
thematic_data = df[df['thematic'] == selected_thematic]

# Création de deux colonnes pour les graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader("Évaluation des Sources")
    # Création du graphique pour les sources
    source_fig = go.Figure()
    
    # Utilisation des données du premier modèle uniquement
    model_data = thematic_data.iloc[0]
    source_fig.add_trace(go.Bar(
        x=["Pertinence", "Crédibilité", "Actualité"],
        y=[model_data["source_relevance"],
           model_data["source_credibility"],
           model_data["source_freshness"]],
        text=[f"{val:.2f}" for val in [model_data["source_relevance"],
                                      model_data["source_credibility"],
                                      model_data["source_freshness"]]],
        textposition='auto',
    ))
    
    source_fig.update_layout(
        title="Évaluation des Sources",
        yaxis=dict(range=[0, 5]),
        showlegend=False
    )
    st.plotly_chart(source_fig, use_container_width=True)

with col2:
    st.subheader("Évaluation des Réponses")
    # Création du graphique pour les réponses
    response_fig = go.Figure()
    
    for model in thematic_data['model'].unique():
        model_data = thematic_data[thematic_data['model'] == model]
        response_fig.add_trace(go.Bar(
            name=model,
            x=["Pertinence", "Exactitude", "Exhaustivité", "Clarté", "Profondeur"],
            y=[model_data["relevance"].iloc[0],
               model_data["correctness"].iloc[0],
               model_data["completeness"].iloc[0],
               model_data["clarity"].iloc[0],
               model_data["depth"].iloc[0]],
            text=[f"{val:.2f}" for val in [model_data["relevance"].iloc[0],
                                          model_data["correctness"].iloc[0],
                                          model_data["completeness"].iloc[0],
                                          model_data["clarity"].iloc[0],
                                          model_data["depth"].iloc[0]]],
            textposition='auto',
        ))
    
    response_fig.update_layout(
        title="Évaluation des Réponses",
        barmode='group',
        yaxis=dict(range=[0, 5]),
        showlegend=True
    )
    st.plotly_chart(response_fig, use_container_width=True)

# Section 3: Données Brutes
st.header("Données Brutes")
st.dataframe(df)