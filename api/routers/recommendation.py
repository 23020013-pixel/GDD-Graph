from fastapi import APIRouter, Query
from ..db import db
from typing import List, Dict, Any

router = APIRouter()

@router.get("/drugs")
async def recommend_drugs(
    disease_id: str,
    top_k: int = Query(10, ge=1, le=50)
):
    cypher = """
    MATCH (d:Disease {id: $disease_id})-[:RELATION {type: 'DaG'}]-(g:Gene)-[:RELATION {type: 'GiG'}]-(g2:Gene)-[r:RELATION]-(c:Compound)
    WHERE r.type IN ['CbG', 'CuG', 'CdG']
    RETURN c.name as drug, count(DISTINCT g2) as score, collect(DISTINCT g2.name) as target_genes
    ORDER BY score DESC
    LIMIT $top_k
    """
    records = await db.run_query(cypher, {"disease_id": disease_id, "top_k": top_k})
    
    results = []
    for record in records:
        results.append({
            "Drug": record["drug"],
            "Score": record["score"],
            "Target Genes": ", ".join(record["target_genes"][:3]) 
        })
        
    return results
