from sqlalchemy.ext.asyncio import AsyncSession
from core.models.paper import Paper
from .citation_graph import CitationGraphBuilder
import logging

logger = logging.getLogger("rm_research.maps.engine")

class MapEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.graph_builder = CitationGraphBuilder()

    async def generate_citation_map(self, seed_doi: str) -> dict:
        """
        Coordinates graph building and prepares JSON payload specifically 
        optimized for WebGL/D3.js frontend rendering.
        """
        logger.info(f"Generating map for seed: {seed_doi}")
        
        # 1. Build the raw relational graph
        raw_graph = await self.graph_builder.build_local_graph(seed_doi)
        
        # 2. Format for D3.js / Sigma.js
        # Sigma.js requires specific 'x', 'y', 'size', and 'color' attributes
        formatted_nodes = []
        for i, node in enumerate(raw_graph["nodes"]):
            formatted_nodes.append({
                "id": node["id"],
                "label": node["title"][:50] + "..." if len(node["title"]) > 50 else node["title"],
                "size": max(3, min(20, node["citations"] / 10)), # Scale node by citations
                "color": "#3b82f6" if node["year"] and node["year"] > 2020 else "#94a3b8",
                "x": 0, # Frontend force-layout will calculate actual positions
                "y": 0,
                "data": node
            })
            
        return {
            "seed": seed_doi,
            "nodes": formatted_nodes,
            "edges": raw_graph["edges"]
        }
