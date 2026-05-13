import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Drug Recommendation", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stTitle {
        color: #000000;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: none;
        -webkit-text-fill-color: initial;
        margin-bottom: 1rem;
    }
    p, span, label, div, h1, h2, h3 {
        color: #000000 !important;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        border-color: #1b5e20;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 Drug Recommendation")

# Fetch list of diseases from API
@st.cache_data
def get_diseases():
    try:
        response = requests.get("http://localhost:8000/api/disease/all")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return {"Error fetching diseases": ""}

disease_options = get_diseases()
disease_name = st.selectbox("Select Disease", list(disease_options.keys()))
disease_id = disease_options[disease_name]
top_k = st.slider("Top-K recommendations", 5, 20, 10)

st.divider()

if st.button("Get Recommendations"):
    try:
        response = requests.get(
            f"http://localhost:8000/api/recommend/drugs",
            params={"disease_id": disease_id, "top_k": top_k}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                
                # Enhanced Dataframe display
                st.subheader("Results")
                st.dataframe(
                    df,
                    width="stretch",
                    column_config={
                        "Drug": st.column_config.TextColumn(
                            "💊 Recommended Drug",
                            width="medium",
                        ),
                        "Score": st.column_config.ProgressColumn(
                            "🎯 Relevance Score",
                            help="Number of target genes found",
                            format="%d",
                            min_value=0,
                            max_value=int(df["Score"].max()) if not df.empty else 10,
                        ),
                        "Target Genes": st.column_config.TextColumn(
                            "🧬 Associated Genes",
                            help="Top gene associations",
                        )
                    },
                    hide_index=True,
                )
            else:
                st.warning("No recommendations found for this disease.")
        else:
            st.error("Failed to fetch recommendations.")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("💡 Select a disease and click 'Get Recommendations' to see potential drug treatments.")
