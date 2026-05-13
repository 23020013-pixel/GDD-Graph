from neo4j import AsyncGraphDatabase
from .config import settings
import logging

logger = logging.getLogger(__name__)

class Neo4jDB:
    def __init__(self):
        self.driver = None

    async def connect(self):
        self.driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD),
            max_connection_pool_size=50
        )
        logger.info("Connected to Neo4j")

    async def close(self):
        if self.driver:
            await self.driver.close()
            logger.info("Closed Neo4j connection")

    async def run_query(self, cypher, params=None):
        if not self.driver:
            raise Exception("Neo4j driver not initialized")
        
        async with self.driver.session() as session:
            result = await session.run(cypher, params or {})
            return [record async for record in result]

db = Neo4jDB()
