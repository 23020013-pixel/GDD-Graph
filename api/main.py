from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import db
from .cache import limiter
from .errors import (
    APIError, api_error_handler, 
    Neo4jError, neo4j_error_handler,
    ValidationError, validation_error_handler,
    general_exception_handler
)
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .routers import entity, disease, graph, recommendation

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await db.connect()
    except Exception as e:
        print(f"Failed to connect to Neo4j: {e}")
    yield
    # Shutdown
    await db.close()

app = FastAPI(title="Hetionet Explorer API", lifespan=lifespan)

# Add rate limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add custom exception handlers
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(Neo4jError, neo4j_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Health endpoint
@app.get("/health")
async def health():
    neo4j_status = "connected" if db.driver else "disconnected"
    return {"status": "ok", "neo4j": neo4j_status}

@app.get("/stats")
async def get_stats():
    node_count_query = "MATCH (n) RETURN count(n) as count"
    rel_count_query = "MATCH ()-[r]->() RETURN count(r) as count"
    
    node_records = await db.run_query(node_count_query)
    rel_records = await db.run_query(rel_count_query)
    
    return {
        "nodes": node_records[0]["count"] if node_records else 0,
        "edges": rel_records[0]["count"] if rel_records else 0,
        "avg_degree": (rel_records[0]["count"] / node_records[0]["count"]) if node_records and node_records[0]["count"] > 0 else 0
    }

@app.get("/")
async def root():
    return {
        "message": "Hetionet Explorer API is running",
        "docs": "/docs",
        "health": "/health"
    }

# Include routers
app.include_router(entity.router, prefix="/api/entity", tags=["entity"])
app.include_router(disease.router, prefix="/api/disease", tags=["disease"])
app.include_router(graph.router, prefix="/api/graph", tags=["graph"])
app.include_router(recommendation.router, prefix="/api/recommend", tags=["recommendation"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
