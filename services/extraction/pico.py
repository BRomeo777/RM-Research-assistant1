import os
from typing import Optional
from pydantic import BaseModel
from groq import AsyncGroq
import logging
from config.settings import settings

logger = logging.getLogger("rm_research.extraction.pico")

class PICOData(BaseModel):
    population: str
    intervention: str
    comparator: str
    outcome: str

class PICOExtractor:
    def __init__(self):
        # We only initialize the client if the key exists to prevent crashes during basic testing
        self.api_key = settings.GROQ_API_KEY
        self.client = AsyncGroq(api_key=self.api_key) if self.api_key else None
        self.model = "llama3-8b-8192" # Fast, efficient model for structured extraction

    async def extract_pico(self, abstract: str) -> Optional[PICOData]:
        """Extracts PICO elements from an abstract using LLM inference."""
        if not self.client:
            logger.warning("GROQ_API_KEY not set. Skipping PICO extraction.")
            return None
            
        if not abstract or len(abstract.strip()) < 50:
            return None

        system_prompt = """
        You are a highly precise medical researcher. Extract the PICO elements 
        (Population, Intervention, Comparator, Outcome) from the provided abstract.
        Return ONLY a valid JSON object with the keys: 'population', 'intervention', 
        'comparator', 'outcome'. If an element is missing, return 'Not specified' for that key.
        """

        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": abstract}
                ],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.0 # Strict determinism for data extraction
            )
            
            # Parse the JSON response into our Pydantic model
            import json
            result_dict = json.loads(chat_completion.choices[0].message.content)
            return PICOData(**result_dict)
            
        except Exception as e:
            logger.error(f"LLM Extraction failed: {str(e)}")
            return None
