from fastapi import APIRouter, Query, HTTPException
from ..db import db
from typing import List, Dict, Any

router = APIRouter()

@router.get("/explore")
async def explore_graph(
    source_id: str,
    target_id: str,
    max_hops: int = Query(2, ge=1, le=3)
):
    # Tìm đường đi ngắn nhất giữa 2 node
    cypher = f"""
    MATCH p = shortestPath((s {{id: $source_id}})-[*..{max_hops}]-(t {{id: $target_id}}))
    RETURN p
    """
    records = await db.run_query(cypher, {"source_id": source_id, "target_id": target_id})
    
    nodes = []
    edges = []
    seen_nodes = set()
    
    if not records:
        return {"nodes": [], "edges": []}
        
    for record in records:
        path = record["p"]
        for node in path.nodes:
            if node.id not in seen_nodes:
                labels = list(node.labels)
                kind = node.get("kind", "")
                
                # Xác định màu dựa trên label hoặc thuộc tính 'kind'
                if "Gene" in labels or kind == "Gene":
                    color = "#00ff00" # Green
                elif "Disease" in labels or kind == "Disease":
                    color = "#ff0000" # Red
                elif "Compound" in labels or kind == "Compound":
                    color = "#ffff00" # Yellow
                elif kind == "Biological Process":
                    color = "#00ffff" # Cyan
                else:
                    color = "#cccccc" # Gray
                
                nodes.append({
                    "id": node["id"],
                    "label": node.get("name", node["id"]),
                    "color": color
                })
                seen_nodes.add(node.id)
        
        for rel in path.relationships:
            edges.append({
                "source": rel.start_node["id"],
                "target": rel.end_node["id"],
                "label": rel.get("type", "RELATION")
            })
            
    return {"nodes": nodes, "edges": edges}
