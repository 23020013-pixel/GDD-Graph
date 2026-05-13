from fastapi import APIRouter, Query
from ..db import db
from ..models.entities import PaginatedResponse
from typing import Optional

router = APIRouter()

@router.get("/{disease_id}/genes", response_model=PaginatedResponse)
async def get_disease_genes(
    disease_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    # Query for items
    query_items = """
    MATCH (d:Disease {id: $id})-[r:RELATION {type: 'DaG'}]-(g:Gene)
    RETURN g
    SKIP $offset LIMIT $limit
    """
    items_records = await db.run_query(query_items, {"id": disease_id, "offset": offset, "limit": limit})
    items = [dict(record["g"]) for record in items_records]
    
    # Query for total count
    query_count = """
    MATCH (d:Disease {id: $id})-[r:RELATION {type: 'DaG'}]-(g:Gene)
    RETURN count(g) as total
    """
    count_records = await db.run_query(query_count, {"id": disease_id})
    total_count = count_records[0]["total"] if count_records else 0
    
    has_next = offset + limit < total_count
    
    return PaginatedResponse(
        total_count=total_count,
        items=items,
        has_next=has_next,
        offset=offset,
        limit=limit
    )

@router.get("/all")
async def get_all_diseases():
    cypher = """
    MATCH (d:Disease)
    RETURN d.name as name, d.id as id
    ORDER BY d.name
    """
    records = await db.run_query(cypher)
    return {record["name"]: record["id"] for record in records if record["name"]}
