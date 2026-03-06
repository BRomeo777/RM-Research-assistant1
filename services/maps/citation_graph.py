import asyncio
from typing import List, Dict, Any, Set
import logging
from services.search.openalex import OpenAlexClient
from config.settings import settings

logger = logging.getLogger("rm_research.maps.citation_graph")

class CitationGraphBuilder:
    def __init__(self):
        self.client = OpenAlexClient()
        self.max_depth = settings.MAX_CITATION_DEPTH

    async def build_local_graph(self, seed_doi: str) -> Dict[str, Any]:
        """
        Builds a 2-generation citation network around a seed paper.
        Returns a dictionary formatted for frontend graph visualization.
        """
        if not seed_doi:
            return {"nodes": [], "edges": []}

        nodes: Dict[str, dict] = {}
        edges: List[dict] = []
        visited_dois: Set[str] = set()

        # Helper function for recursive fetching
        async def fetch_generation(doi: str, current_depth: int, direction: str):
            if current_depth > self.max_depth or doi in visited_dois:
                return
                
            visited_dois.add(doi)
            
            # OpenAlex syntax: 'cites:DOI' gets papers citing this one (forward)
            # 'cited_by:DOI' gets papers this one references (backward)
            query_prefix = "cites:" if direction == "forward" else "cited_by:"
            raw_results = await self.client.search_works(f"{query_prefix}{doi}", limit=15)
            
            for work in raw_results:
                work_doi = work.get("doi")
                if not work_doi:
                    continue
                    
                # Add node if it doesn't exist
                if work_doi not limitations not in nodes:
                    nodes[work_doi] = {
                        "id": work_doi,
                        "title": work.get("title", "Unknown"),
                        "citations": work.get("cited_by_count", 0),
                        "year": work.get("publication_year")
                    }
                
                # Add edge
                source = doi if direction == "forward" else work_doi
                target = work_doi if direction == "forward" else doi
                
                edges.append({"source": source, "target": target})
                
                # Recursively fetch next generation
                await fetch_generation(work_doi, current_depth + 1, direction)

        # Start the snowball process concurrently
        logger.info(f"Initiating citation snowball for seed: {seed_doi}")
        await asyncio.gather(
            fetch_generation(seed_doi, 1, "forward"),
            fetch_generation(seed_doi, 1, "backward")
        )

        return {
            "nodes": list(nodes.values()),
            "edges": edges
        }
