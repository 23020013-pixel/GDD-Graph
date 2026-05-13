import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title("📊 Pipeline Dashboard")

try:
    response = requests.get("http://localhost:8000/stats")
    if response.status_code == 200:
        stats = response.json()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Nodes", f"{stats['nodes']:,}")
        col2.metric("Edges", f"{stats['edges']:,}")
        col3.metric("Avg Degree", f"{stats['avg_degree']:.1f}")
        col4.metric("Status", "Online", delta="Connected")
    else:
        st.error("Could not fetch stats from API.")
except Exception as e:
    st.error(f"Error: {e}")

st.divider()

st.subheader("Data Processing Timeline (Placeholder)")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Ingestion', 'Validation', 'Indexing']
)

st.line_chart(chart_data)
