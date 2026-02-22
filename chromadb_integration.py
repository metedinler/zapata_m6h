from configmodule import config

try:
    import chromadb
except Exception:
    chromadb = None


def search_chromadb(query, top_k=5):
    """REST API uyumluluğu için ChromaDB arama yardımcı fonksiyonu."""
    try:
        if chromadb is None:
            return {"ids": [], "documents": [], "metadatas": [], "distances": [], "error": "chromadb paketi yüklü değil"}
        client = chromadb.PersistentClient(path=str(config.CHROMA_DB_PATH))
        collection = client.get_or_create_collection(name="embeddings")
        results = collection.query(query_texts=[str(query)], n_results=top_k)

        return {
            "ids": results.get("ids", []),
            "documents": results.get("documents", []),
            "metadatas": results.get("metadatas", []),
            "distances": results.get("distances", []),
        }
    except Exception as error:
        return {"ids": [], "documents": [], "metadatas": [], "distances": [], "error": str(error)}
