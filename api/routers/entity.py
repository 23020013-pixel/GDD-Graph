from fastapi import APIRouter, HTTPException, Depends
from ..db import db
from ..models.entities import EntityResponse, Gene, Disease, Drug
from typing import List

router = APIRouter()

@router.get("/{entity_id}", response_model=EntityResponse)
async def get_entity(entity_id: str):
    cypher = """
    MATCH (n {id: $id})
    RETURN n, labels(n) as labels
    """
    records = await db.run_query(cypher, {"id": entity_id})
    
    if not records:
        raise HTTPException(status_code=404, detail=f"Entity with ID {entity_id} not found")
    
    record = records[0]
    node = record["n"]
    labels = record["labels"]
    
    properties = dict(node)
    
    if "Gene" in labels:
        entity = Gene(**properties)
    elif "Disease" in labels:
        entity = Disease(**properties)
    elif "Compound" in labels:
        entity = Drug(**properties)
    else:
        from ..models.entities import BaseEntity
        entity = BaseEntity(**properties)
        
    return EntityResponse(entity=entity, labels=labels)
