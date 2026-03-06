# Caching & Search Limits
HOT_CACHE_LIMIT = 400_000 
MAX_SEARCH_RESULTS = 100

# Extraction Tiers (Phase 3: TrialSieve)
PICO_FIELDS = ["Population", "Intervention", "Comparator", "Outcome"]
ROB_DOMAINS = [
    "Randomization", 
    "Deviations from intended interventions", 
    "Missing outcome data", 
    "Measurement of the outcome", 
    "Selection of the reported result"
]

# Integrity Engine (Phase 5: Veritas)
VECTOR_DIMENSION = 384  # Standard size for semantic fingerprinting models
SHIELD_LEVELS = ["Semantic", "Structural", "Attribution"]
