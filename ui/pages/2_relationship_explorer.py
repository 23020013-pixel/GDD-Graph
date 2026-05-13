import streamlit as st
import requests
from streamlit_agraph import agraph, Node, Edge, Config

st.title("🕸️ Relationship Explorer")

col1, col2 = st.columns([1, 3])

with col1:
    source = st.text_input("Source ID", value="Gene::6441")
    target = st.text_input("Target ID", value="Biological Process::GO:0050868")
    max_hop = st.slider("Max Hops", 1, 3, 2)
    explore = st.button("Explore Path")

with col2:
    st.subheader("Graph Visualization")
    
    if explore:
        try:
            response = requests.get(
                f"http://localhost:8000/api/graph/explore",
                params={"source_id": source, "target_id": target, "max_hops": max_hop}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if not data["nodes"]:
                    st.warning("No path found between these entities.")
                else:
                    nodes = [Node(id=n["id"], label=n["label"], size=25, color=n["color"]) for n in data["nodes"]]
                    edges = [Edge(source=e["source"], target=e["target"], label=e["label"]) for e in data["edges"]]

                    config = Config(width=800, 
                                    height=600, 
                                    directed=True, 
                                    nodeHighlightBehavior=True, 
                                    highlightColor="#F7A7A6", 
                                    collapsible=True,
                                    node={'labelProperty': 'label'},
                                    link={'labelProperty': 'label', 'renderConfiguration': (True, 'straight')}
                                   )

                    return_value = agraph(nodes=nodes, 
                                          edges=edges, 
                                          config=config)

                    if return_value:
                        st.write(f"Selected Node: {return_value}")
            else:
                st.error("Failed to fetch graph data.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Enter source and target IDs and click 'Explore Path' to see the relationship.")
