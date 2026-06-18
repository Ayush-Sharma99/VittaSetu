# rag/gst_rules.py
import os

CORPUS_PATH = os.path.join(os.path.dirname(__file__), "gst_rules_corpus.txt")

def load_rules():
    if not os.path.exists(CORPUS_PATH):
        return []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    rules = [rule.strip() for rule in content.split("---RULE---") if rule.strip()]
    return rules
