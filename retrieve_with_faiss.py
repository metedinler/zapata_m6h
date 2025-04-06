import faiss
import numpy as np
import logging
from sentence_transformers import SentenceTransformer

sentence_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def faiss_search(query_text, top_k=3):
    """
    FAISS kullanarak vektör araması yapar.
    """
    try:
        query_embedding = sentence_model.encode(query_text).reshape(1, -1)
        distances, indices = index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            doc_data = redis_client.get(f"faiss_doc:{idx}")
            if doc_data:
                results.append(json.loads(doc_data))
        
        return results

    except Exception as e:
        logging.error(f"❌ FAISS araması başarısız oldu: {str(e)}")
        return []
