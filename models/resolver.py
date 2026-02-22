# models/resolver.py
import pandas as pd
from typing import Dict, Tuple, List
import sqlite3
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CSV_PATH = os.path.join(DATA_DIR, 'abbreviations.csv')

class AbbreviationResolver:
    def __init__(self, csv_path=CSV_PATH, db_url=None):
        self.abbr_map = {}
        if os.path.exists(csv_path):
            try:
                self.df = pd.read_csv(csv_path)
                # normalize abbr -> list of expansions
                for _, row in self.df.iterrows():
                    abbr = str(row['abbr']).strip().upper()
                    expansions = str(row['expansion']).split('|') if pd.notna(row['expansion']) else []
                    expansions = [e.strip() for e in expansions if e.strip()]
                    self.abbr_map[abbr] = expansions
            except Exception as e:
                print(f"Error loading CSV {csv_path}: {e}")
        else:
            print(f"Warning: CSV file not found at {csv_path}")
        
        # optional DB for user-saved mappings (simple sqlite)
        self.db_url = db_url

    def lookup(self, abbr: str) -> List[str]:
        return self.abbr_map.get(abbr.upper(), [])

    def resolve(self, abbr: str, context: str = None) -> Tuple[str, float]:
        """
        Return chosen expansion and confidence.
        Default: if only one candidate, return it with high confidence.
        If multiple, return first with lower confidence (or call disambiguator).
        """
        candidates = self.lookup(abbr)
        if not candidates:
            return (abbr, 0.0)  # unknown
        if len(candidates) == 1:
            return (candidates[0], 0.95)
        # ambiguous: naive fallback
        return (candidates[0], 0.6)
