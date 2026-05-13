import streamlit as st
import requests

st.title("🔍 Entity Search")
st.write("Search for Genes, Diseases, or Drugs in the Hetionet knowledge graph.")

search_query = st.text_input("Enter Entity ID (e.g., Gene::5243, Disease::DOID:1612, Compound::DB00945)")

if search_query:
    try:
        response = requests.get(f"http://localhost:8000/api/entity/{search_query}")
        if response.status_code == 200:
            data = response.json()
            entity = data["entity"]
            labels = data["labels"]
            
            st.success(f"Found {labels[0]}: {entity.get('name', 'N/A')}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Kind:** {entity.get('kind', 'N/A')}")
                st.json(entity)
            with col2:
                st.write("**Labels:**")
                for label in labels:
                    st.code(label)
        elif response.status_code == 404:
            st.warning("Entity not found.")
        else:
            st.error(f"Error: {response.json().get('message', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
else:
    st.info("Try searching for: Gene::5243")
