# rag/knowledge_base.py
import os
import chromadb
from.rag.gst_rules import load_rules

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

# Simple mock vector store or ChromaDB helper
class GSTKnowledgeBase:
    def __init__(self):
        # We can implement a clean in-memory fallback for local environments if chromadb setup fails,
        # or use standard chromadb since it's required.
        try:
            self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
            self.collection = self.client.get_or_create_collection("gst_rules")
            self._seed_rules()
            self.chroma_available = True
        except Exception as e:
            print(f"ChromaDB initialization failed: {e}. Falling back to simple memory/keyword matching.")
            self.chroma_available = False
            self.rules = load_rules()

    def _seed_rules(self):
        # Only seed if collection is empty
        if self.collection.count() == 0:
            rules = load_rules()
            documents = []
            ids = []
            for idx, rule in enumerate(rules):
                documents.append(rule)
                ids.append(f"rule_{idx}")
            if documents:
                # We can use a default embedding function or add documents directly (chroma uses default sentence_transformers if not specified)
                self.collection.add(
                    documents=documents,
                    ids=ids
                )

    def query(self, text: str, n_results: int = 3) -> list:
        if not self.chroma_available:
            # Fallback keyword ranking / substring match
            matched = []
            for r in self.rules:
                score = sum(1 for word in text.split() if word.lower() in r.lower())
                matched.append((score, r))
            matched.sort(reverse=True, key=lambda x: x[0])
            return [item[1] for item in matched[:n_results]]
        
        try:
            results = self.collection.query(
                query_texts=[text],
                n_results=n_results
            )
            if results and results.get("documents"):
                return results["documents"][0]
        except Exception as e:
            print(f"Query error: {e}")
        
        # Fallback to loading directly
        return load_rules()[:n_results]

# Single instance
kb = GSTKnowledgeBase()
