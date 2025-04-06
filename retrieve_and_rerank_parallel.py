import concurrent.futures
import logging
from retrieve_with_faiss import faiss_search
from retrieve_with_chromadb import chroma_search
from reranking import rerank_results

def retrieve_and_rerank_parallel(query, source="faiss", method="bert", top_k=5, top_n=3):
    """
    Retrieve edilen verileri çoklu işlem desteğiyle re-rank eder.
    """
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_retrieve = executor.submit(retrieve_from_source, query, source, top_k)
            documents = future_retrieve.result()
            
            future_rerank = executor.submit(rerank_results, query, documents, method, top_n)
            ranked_documents = future_rerank.result()
        
        return ranked_documents

    except Exception as e:
        logging.error(f"❌ Paralel Retrieve + Re-Ranking başarısız oldu: {str(e)}")
        return []