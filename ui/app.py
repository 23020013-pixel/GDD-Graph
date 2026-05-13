import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Hetionet Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look
st.markdown("""
<style>
    /* Background and main container */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* Global text color */
    p, span, label, div, h1, h2, h3, h4, h5, h6, code, pre {
        color: #000000 !important;
    }

    /* JSON and Code blocks */
    [data-testid="stJson"] span {
        color: #000000 !important;
    }
    .stCodeBlock code {
        color: #000000 !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #dee2e6;
    }
    
    /* Sidebar text */
    [data-testid="stSidebarNav"] span {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1 {
        color: #000000 !important;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] div {
        color: #000000 !important;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Links and other elements */
    a {
        color: #007bff !important;
    }
</style>
""", unsafe_allow_html=True)

# API Health Check
def check_api_health():
    try:
        response = requests.get("http://localhost:8000/health", timeout=1)
        if response.status_code == 200:
            return response.json().get("neo4j") == "connected"
    except:
        return False
    return False

# Sidebar
with st.sidebar:
    st.title("🧬 Hetionet Explorer")
    st.caption("v1.0.0")
    st.divider()
    
    health = check_api_health()
    if health:
        st.success("API: Online | Neo4j: Connected")
    else:
        st.error("API: Offline or Neo4j Disconnected")
    
    st.divider()
    st.info("Biological knowledge graph exploration tool.")

# Navigation
pages = [
    st.Page("pages/1_entity_search.py", title="Entity Search", icon="🔍"),
    st.Page("pages/2_relationship_explorer.py", title="Relationship Explorer", icon="🕸️"),
    st.Page("pages/3_drug_recommendation.py", title="Drug Recommendation", icon="💊"),
    st.Page("pages/4_pipeline_dashboard.py", title="Pipeline Dashboard", icon="📊"),
]

pg = st.navigation(pages)
pg.run()
