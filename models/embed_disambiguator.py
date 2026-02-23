# models/embed_disambiguator.py
from sentence_transformers import SentenceTransformer, util
import numpy as np
from typing import List, Tuple

class EmbedDisambiguator:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def choose_candidate(self, candidates: List[str], context_sentence: str) -> Tuple[str, float]:
        """
        Given candidate expansions and the sentence context where abbr appears,
        pick best candidate via cosine similarity.
        Returns (best_candidate, confidence)
        """
        # encode
        texts = candidates + [context_sentence]
        embeddings = self.model.encode(texts, convert_to_tensor=True)
        candidate_embs = embeddings[:-1]
        context_emb = embeddings[-1]
        sims = util.cos_sim(candidate_embs, context_emb).cpu().numpy().flatten()
        best_idx = int(np.argmax(sims))
        return candidates[best_idx], float(sims[best_idx])
