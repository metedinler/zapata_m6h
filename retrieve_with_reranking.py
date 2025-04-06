import numpy as np
import logging
from retrieve_with_faiss import faiss_search
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from retrieve_with_chromadb import chroma_search

# BERT modeli yükleme
bert_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve_from_source(query, source="faiss", top_k=5):
    """
    FAISS veya ChromaDB üzerinden veri retrieve eder.
    :param query: Kullanıcının sorgusu
    :param source: "faiss" veya "chroma" (veri kaynağı)
    :param top_k: Döndürülecek sonuç sayısı
    :return: Retrieve edilen belgeler listesi
    """
    try:
        if source == "faiss":
            return faiss_search(query, top_k=top_k)
        elif source == "chroma":
            return chroma_search(query, top_k=top_k)
        else:
            logging.error(f"❌ Geçersiz veri kaynağı: {source}")
            return []
    except Exception as e:
        logging.error(f"❌ Retrieve işlemi başarısız oldu: {str(e)}")
        return []

def rerank_results(query, documents, method="bert", top_n=3):
    """
    Retrieve edilen metinleri re-rank eder.
    :param query: Kullanıcının sorgusu
    :param documents: Retrieve edilen metinler
    :param method: "bert" veya "tfidf" (re-ranking yöntemi)
    :param top_n: En iyi kaç sonuç döndürülecek
    :return: En iyi sıralanmış metinler
    """
    try:
        if method == "bert":
            query_embedding = bert_model.encode(query, convert_to_tensor=True)
            doc_embeddings = bert_model.encode([doc["text"] for doc in documents], convert_to_tensor=True)
            cosine_scores = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]
            ranked_indices = cosine_scores.argsort(descending=True)[:top_n]
        
        elif method == "tfidf":
            vectorizer = TfidfVectorizer()
            all_texts = [query] + [doc["text"] for doc in documents]
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            query_vec = tfidf_matrix[0]
            doc_vectors = tfidf_matrix[1:]
            scores = np.dot(doc_vectors, query_vec.T).toarray().flatten()
            ranked_indices = np.argsort(scores)[::-1][:top_n]

        else:
            logging.error(f"❌ Geçersiz re-ranking yöntemi: {method}")
            return documents[:top_n]

        return [documents[i] for i in ranked_indices]
    
    except Exception as e:
        logging.error(f"❌ Re-ranking işlemi başarısız oldu: {str(e)}")
        return documents[:top_n]


def retrieve_and_rerank(query, source="faiss", method="bert", top_k=5, top_n=3):
    """
    Retrieve edilen verileri alır, re-rank eder ve en iyi sonuçları döndürür.
    :param query: Kullanıcının sorgusu
    :param source: FAISS veya ChromaDB
    :param method: Re-ranking yöntemi ("bert" veya "tfidf")
    :param top_k: Retrieve edilecek toplam sonuç sayısı
    :param top_n: En iyi döndürülecek sonuç sayısı
    :return: En iyi sıralanmış metinler
    """
    try:
        documents = retrieve_from_source(query, source, top_k)
        return rerank_results(query, documents, method, top_n)
    
    except Exception as e:
        logging.error(f"❌ Retrieve + Re-Ranking başarısız oldu: {str(e)}")
        return []

