import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Rapport d'Évaluation Qwen 3",
    page_icon="📊",
    layout="wide"
)

# Titre et introduction
st.title("📊 Rapport d'Évaluation de Qwen 3 - Capacités de Recherche Web")
st.markdown("""
Cette application présente une analyse détaillée des performances de Qwen 3 dans différentes thématiques,
basée sur l'évaluation de ses capacités de recherche web.
""")

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

# Fonction pour charger les données
def load_evaluation_data():
    data = []
    evaluation_dir = "evaluation_web"
    
    for filename in os.listdir(evaluation_dir):
        if filename.endswith(".json"):
            thematic = filename.replace("Evaluation_", "").replace(".json", "")
            with open(os.path.join(evaluation_dir, filename), 'r') as f:
                eval_data = json.load(f)
                for response in eval_data.get("response", []):
                    data.append({
                        "thematic": thematic,
                        "model": response["model"],
                        "relevance": response["Relevance"],
                        "correctness": response["Correctness"],
                        "completeness": response["Completeness"],
                        "clarity": response["Clarity"],
                        "depth": response["Depth"]
                    })
    return pd.DataFrame(data)

# Chargement des données
df = load_evaluation_data()

# Calcul des moyennes
averages = df.groupby("model")[["relevance", "correctness", "completeness", "clarity", "depth"]].mean().reset_index()

# Section 1: Vue d'ensemble
st.header("Vue d'Ensemble des Performances")

# Graphique des moyennes
fig = go.Figure()
for model in averages["model"].unique():
    model_data = averages[averages["model"] == model]
    fig.add_trace(go.Bar(
        name=model,
        x=["Pertinence", "Exactitude", "Exhaustivité", "Clarté", "Profondeur"],
        y=[model_data["relevance"].iloc[0], 
           model_data["correctness"].iloc[0],
           model_data["completeness"].iloc[0],
           model_data["clarity"].iloc[0],
           model_data["depth"].iloc[0]],
        text=[f"{val:.1f}" for val in [model_data["relevance"].iloc[0],
                                      model_data["correctness"].iloc[0],
                                      model_data["completeness"].iloc[0],
                                      model_data["clarity"].iloc[0],
                                      model_data["depth"].iloc[0]]],
        textposition='auto',
    ))

fig.update_layout(
    title="Moyennes des Critères par Modèle",
    barmode='group',
    yaxis=dict(range=[0, 5]),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# Section 2: Analyse par Thématique
st.header("Analyse par Thématique")

# Sélection de la thématique
selected_thematic = st.selectbox(
    "Sélectionnez une thématique",
    sorted(df["thematic"].unique())
)

# Filtrage des données pour la thématique sélectionnée
thematic_data = df[df["thematic"] == selected_thematic]

# Graphique pour la thématique sélectionnée
fig_thematic = go.Figure()
for model in thematic_data["model"].unique():
    model_data = thematic_data[thematic_data["model"] == model]
    fig_thematic.add_trace(go.Bar(
        name=model,
        x=["Pertinence", "Exactitude", "Exhaustivité", "Clarté", "Profondeur"],
        y = [
            model_data["relevance"].iloc[0],
            model_data["correctness"].iloc[0],
            model_data["completeness"].iloc[0],
            model_data["clarity"].iloc[0],
            model_data["depth"].iloc[0]
        ],
        text=[f"{val:.1f}" for val in [model_data["relevance"].iloc[0],
                                        model_data["correctness"].iloc[0],
                                        model_data["completeness"].iloc[0],
                                        model_data["clarity"].iloc[0],
                                        model_data["depth"].iloc[0]]],
        textposition='auto',
    ))

fig_thematic.update_layout(
    title=f"Évaluation pour la thématique: {selected_thematic}",
    barmode='group',
    yaxis=dict(range=[0, 5]),
    showlegend=True
)

st.plotly_chart(fig_thematic, use_container_width=True)

# Section 3: Tableau détaillé
st.header("Données Détaillées")
st.dataframe(df, use_container_width=True)

# Section 4: Statistiques globales
st.header("Statistiques Globales")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Moyennes par Modèle")
    st.dataframe(averages, use_container_width=True)

with col2:
    st.subheader("Moyennes par Critère")
    criterion_means = df[["relevance", "correctness", "completeness", "clarity", "depth"]].mean()
    st.dataframe(criterion_means.to_frame("Moyenne"), use_container_width=True)

# Section 5: Conclusion
st.header("Conclusion")
st.markdown("""
### Points Forts
- Performance exceptionnelle en termes de pertinence et de clarté
- Excellente cohérence entre les évaluateurs
- Couverture complète des sujets
""")