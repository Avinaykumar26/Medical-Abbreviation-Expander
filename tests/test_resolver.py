from models.resolver import AbbreviationResolver
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CSV_PATH = os.path.join(DATA_DIR, 'abbreviations.csv')


def test_lookup_unambiguous():
    resolver = AbbreviationResolver(csv_path=CSV_PATH)
    assert resolver.lookup('BP') == ['Blood Pressure']
    chosen, conf = resolver.resolve('BP')
    assert chosen == 'Blood Pressure'
    assert conf > 0.9


def test_lookup_ambiguous():
    resolver = AbbreviationResolver(csv_path=CSV_PATH)
    # RA has two expansions per CSV separated by '|'
    candidates = resolver.lookup('RA')
    assert isinstance(candidates, list)
    assert len(candidates) == 2
    assert 'Rheumatoid Arthritis' in candidates
    assert 'Right Atrium' in candidates
    
    chosen, conf = resolver.resolve('RA')
    # Default resolve returns the first one with lower confidence
    assert chosen == candidates[0]
    assert conf == 0.6
