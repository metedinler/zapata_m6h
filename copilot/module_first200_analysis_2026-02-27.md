# Zapata Modül İlk 200 Satır Analizi

- Tarih: 2026-02-27 04:44:50

- Kapsam: Kök dizindeki 59 Python modülü

- Yöntem: Her dosyanın ilk 200 satırı + basit AST sembol çıkarımı + kök dizin referans taraması

## alternativeembeddingmodule.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: AlternativeEmbeddingProcessor

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, numpy, chromadb, redis, logging, colorlog, sentence_transformers, configmodule

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 117 satır

## chromadb_integration.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: search_chromadb

- İlk200 satırda importlar: configmodule, chromadb

- Kök modül referansları: rest_api.py, test_suite(ilk kod).py

- İlk200 satır uzunluğu: 25 satır

## citation_mapping.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: process_citations

- İlk200 satırda importlar: citationmappingmodule

- Kök modül referansları: rest_api.py, test_suite(ilk kod).py

- İlk200 satır uzunluğu: 19 satır

## citationmappingmodule.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: re, sqlite3, chromadb, redis, json, logging, colorlog, concurrent.futures, configmodule

- Kök modül referansları: citation_mapping.py, test_suite.py

- İlk200 satır uzunluğu: 200 satır

## clustering_module.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: ClusteringProcessor

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: numpy, sqlite3, chromadb, logging, colorlog, sklearn.cluster, configmodule

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 147 satır

## configmodule.py

- Rol: konfigürasyon katmanı

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, logging, colorlog, pathlib, dotenv, chromadb, redis, sqlite3

- Kök modül referansları: FineTuning.py, Mind_Map_Visualizer.py, alternativeembeddingmodule.py, chromadb_integration.py, citationmappingmodule.py, clustering_module.py, d3js_visualizer.py, document_parser.py, embeddingmodule.py, error_logging.py, faiss_integration.py, filesavemodule.py

- İlk200 satır uzunluğu: 200 satır

## d3js_visualizer.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: D3Visualizer

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, json, webbrowser, configmodule

- Kök modül referansları: Mind_Map_Visualizer.py

- İlk200 satır uzunluğu: 116 satır

## document_parser.py

- Rol: PDF/doküman işleme katmanı

- İlk200 satırda sınıflar: DocumentParser

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, logging, colorlog, fitz, json, pathlib, configmodule, redisqueue, sqlite_storage, layout_analysis, scientific_mapping

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 189 satır

## embeddingmodule.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: EmbeddingProcessor

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, logging, colorlog, openai, chromadb, redis, numpy, configmodule, ollama_client

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 145 satır

## env_bulucu3.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, re, ast, argparse, hashlib, tkinter, yaml, functools, multiprocessing, threading, typing, pathlib, concurrent.futures

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 200 satır

## envbulucu.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, re, ast, argparse, hashlib, tkinter, yaml, functools, multiprocessing, typing, pathlib

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 200 satır

## envbulucuy.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: EnhancedEnvironmentScanner

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, re, ast, argparse, hashlib, tkinter, yaml, functools, multiprocessing, typing, pathlib

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 200 satır

## error_logging.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: ErrorLogger

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, json, sqlite3, logging, datetime, configmodule

- Kök modül referansları: test_suite(ilk kod).py, test_suite.py

- İlk200 satır uzunluğu: 151 satır

## evaluation_metrics.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: logging, colorlog, numpy, sklearn.metrics

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 166 satır

## faiss_integration.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: FAISSIntegration

- İlk200 satırda fonksiyonlar: search_faiss

- İlk200 satırda importlar: faiss, numpy, json, logging, colorlog, sqlite3, configmodule, rediscache

- Kök modül referansları: guimodule.py, main.py, rag_pipeline.py, reranking_module.py, rest_api.py, retrieval_reranker.py, test_suite(ilk kod).py

- İlk200 satır uzunluğu: 178 satır

## fetch_top_k_results.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: FetchTopKResults

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: logging, colorlog, json, datetime, multi_source_search, reranking

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 136 satır

## filesavemodule.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, json, sqlite3, csv, chromadb, logging, colorlog, configmodule

- Kök modül referansları: test_suite.py

- İlk200 satır uzunluğu: 148 satır

## FineTuning.py

- Rol: eğitim/fine-tuning katmanı

- İlk200 satırda sınıflar: FineTuningDataset, FineTuner

- İlk200 satırda fonksiyonlar: parallel_finetune, train_selected_models

- İlk200 satırda importlar: json, redis, sqlite3, torch, logging, multiprocessing, concurrent.futures, torch.utils.data, transformers, configmodule

- Kök modül referansları: rest_api.py

- İlk200 satır uzunluğu: 126 satır

## guimindmap.py

- Rol: GUI katmanı

- İlk200 satırda sınıflar: MindMapGUI

- İlk200 satırda fonksiyonlar: run_gui

- İlk200 satırda importlar: json, os, sqlite3, redis, tkinter, webbrowser, http.server, configmodule, zotero_integration, zapata_restapi

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 66 satır

## guimodule.py

- Rol: GUI katmanı

- İlk200 satırda sınıflar: ZapataGUI

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: customtkinter, threading, logging, colorlog, configmodule, retriever_integration, faiss_integration, rag_pipeline

- Kök modül referansları: main.py

- İlk200 satır uzunluğu: 113 satır

## helpermodule.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: HelperFunctions

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, re, logging, colorlog, gc, json, configmodule, nltk.corpus, nltk

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 140 satır

## layout_analysis.py

- Rol: PDF/doküman işleme katmanı

- İlk200 satırda sınıflar: LayoutAnalyzer

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: re, json, logging, colorlog, sqlite3, configmodule, rediscache

- Kök modül referansları: document_parser.py

- İlk200 satır uzunluğu: 146 satır

## main.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: ZapataM6H

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, logging, colorlog, argparse, configmodule, guimodule, retriever_integration, faiss_integration, rag_pipeline, reranking_module, training_monitor, customtkinter

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 130 satır

## Mind_Map_Visualizer.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: MindMapVisualizer

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: json, tkinter, configmodule, d3js_visualizer

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 37 satır

## mindmap_visualizer.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: MindMapVisualizer

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, json, networkx, matplotlib.pyplot, pyzotero, configmodule

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 91 satır

## multi_source_search.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: MultiSourceSearch

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: logging, colorlog, faiss, json, numpy, multiprocessing, concurrent.futures, chromadb, sqlite_storage, redisqueue, query_expansion, reranking, retriever_integration, configmodule, sentence_transformers

- Kök modül referansları: fetch_top_k_results.py

- İlk200 satır uzunluğu: 192 satır

## ollama_client.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: OllamaClient

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: requests, configmodule

- Kök modül referansları: embeddingmodule.py, rag_pipeline.py

- İlk200 satır uzunluğu: 45 satır

## openclaw_client.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: OpenClawClient

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: requests, configmodule

- Kök modül referansları: rag_pipeline.py

- İlk200 satır uzunluğu: 42 satır

## pdfkutuphane.py

- Rol: PDF/doküman işleme katmanı

- İlk200 satırda sınıflar: AdvancedPDFProcessor

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: pdfplumber, fitz, pdfminer, layoutparser, detectron2, tabula, borb, tika, pdfquery, camelot, pytesseract, re, pandas, numpy, typing

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 200 satır

## pdfprocessing.py

- Rol: PDF/doküman işleme katmanı

- İlk200 satırda sınıflar: PDFProcessor

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, fitz, pdfplumber, logging, colorlog, pathlib, dotenv, configmodule

- Kök modül referansları: test_suite.py

- İlk200 satır uzunluğu: 132 satır

## process_manager.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: ProcessManager

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, time, logging, multiprocessing, redis, queue, concurrent.futures, configmodule

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 104 satır

## query_expansion.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: QueryExpansion

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: logging, colorlog, nltk, nltk.corpus, configmodule, nltk.stem

- Kök modül referansları: multi_source_search.py, search_engine.py

- İlk200 satır uzunluğu: 120 satır

## rag_pipeline.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: RAGPipeline

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: logging, colorlog, retriever_integration, faiss_integration, configmodule, ollama_client, openclaw_client

- Kök modül referansları: guimodule.py, main.py, rest_api.py, retrieval_reranker.py

- İlk200 satır uzunluğu: 132 satır

## rediscache.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: redis, json, pickle, logging, colorlog, configmodule

- Kök modül referansları: faiss_integration.py, layout_analysis.py, scientific_mapping.py, veri_isleme.py

- İlk200 satır uzunluğu: 200 satır

## redisqueue.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: RedisQueue

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: redis, json, time, logging, colorlog, configmodule, threading

- Kök modül referansları: document_parser.py, multi_source_search.py, search_engine.py, sync_faiss_chromadb.py, test_suite.py

- İlk200 satır uzunluğu: 200 satır

## reranking_module.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: RerankingModule

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: logging, colorlog, numpy, faiss_integration, retriever_integration, configmodule

- Kök modül referansları: main.py

- İlk200 satır uzunluğu: 108 satır

## rest_api.py

- Rol: API/servis katmanı

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: get_db_connection, get_rag_pipeline, home, start_training, get_training_status, get_training_results, process_citation_data, retrieve_documents_api, query_alias_api, search_in_chromadb, search_in_faiss, stop_training

- İlk200 satırda importlar: flask, logging, redis, sqlite3, threading, configmodule, FineTuning, yapay_zeka_finetuning, retriever_integration, citation_mapping, chromadb_integration, faiss_integration, rag_pipeline

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 187 satır

## retrieval_reranker.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: RetrievalReranker

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: logging, colorlog, numpy, sentence_transformers, retriever_integration, faiss_integration, rag_pipeline

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 117 satır

## retrieve_and_rerank_parallel.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: retrieve_and_rerank_parallel

- İlk200 satırda importlar: concurrent.futures, logging, retrieve_with_faiss, retrieve_with_chromadb, reranking

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 23 satır

## retrieve_api.py

- Rol: API/servis katmanı

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: _get_connection, _discover_text_columns, _search_sqlite, status, query, retrieve

- İlk200 satırda importlar: sqlite3, flask, configmodule

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 86 satır

## retrieve_with_faiss.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: faiss_search

- İlk200 satırda importlar: faiss, numpy, logging, sentence_transformers

- Kök modül referansları: retrieve_and_rerank_parallel.py, retrieve_with_reranking.py

- İlk200 satır uzunluğu: 26 satır

## retrieve_with_reranking.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: retrieve_from_source, rerank_results, retrieve_and_rerank

- İlk200 satırda importlar: numpy, logging, retrieve_with_faiss, sentence_transformers, sklearn.feature_extraction.text, retrieve_with_chromadb

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 84 satır

## retriever_integration.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: RetrieverIntegration

- İlk200 satırda fonksiyonlar: retrieve_documents

- İlk200 satırda importlar: requests, logging, colorlog, configmodule

- Kök modül referansları: guimodule.py, main.py, multi_source_search.py, rag_pipeline.py, reranking_module.py, rest_api.py, retrieval_reranker.py, test_suite(ilk kod).py

- İlk200 satır uzunluğu: 105 satır

## robustembeddingmodule.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: RobustEmbeddingProcessor

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, numpy, openai, chromadb, redis, logging, colorlog, sentence_transformers, configmodule

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 142 satır

## scientific_mapping.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: ScientificMapper

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: re, json, logging, colorlog, sqlite3, configmodule, rediscache

- Kök modül referansları: document_parser.py

- İlk200 satır uzunluğu: 170 satır

## search_engine.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: SearchEngine

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: logging, colorlog, faiss, json, chromadb, sqlite_storage, redisqueue, query_expansion, sentence_transformers

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 166 satır

## sqlite_storage.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: SQLiteStorage

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: sqlite3, json, logging, colorlog, configmodule

- Kök modül referansları: document_parser.py, multi_source_search.py, search_engine.py

- İlk200 satır uzunluğu: 200 satır

## sync_faiss_chromadb.py

- Rol: RAG/IR katmanı

- İlk200 satırda sınıflar: SyncFAISSChromaDB

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, logging, colorlog, faiss, numpy, chromadb, redisqueue, configmodule

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 137 satır

## test_env_bulucu3.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: validate_yaml

- İlk200 satırda importlar: yaml

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 15 satır

## test_suite(ilk kod).py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: TestZapataM6H

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: unittest, os, redis, sqlite3, configmodule, yapay_zeka_finetuning, retriever_integration, citation_mapping, chromadb_integration, faiss_integration, error_logging

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 92 satır

## test_suite.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: TestZapataModules

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: unittest, os, json, sqlite3, logging, datetime, configmodule, error_logging, redisqueue, yapay_zeka_finetuning, pdfprocessing, filesavemodule, citationmappingmodule

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 170 satır

## text_processing.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: TextProcessor

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, re, json, sqlite3, redis, nltk, nltk.corpus, nltk.tokenize, configmodule, nltk.stem

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 105 satır

## training_monitor.py

- Rol: eğitim/fine-tuning katmanı

- İlk200 satırda sınıflar: TrainingMonitor

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: customtkinter, threading, time, logging, colorlog

- Kök modül referansları: main.py

- İlk200 satır uzunluğu: 108 satır

## veri_gorsellestirme.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: DataVisualizer

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: json, logging, colorlog, sqlite3, networkx, matplotlib.pyplot, seaborn, configmodule, numpy

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 142 satır

## veri_isleme.py

- Rol: genel yardımcı modül

- İlk200 satırda sınıflar: CitationAnalyzer

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: json, logging, colorlog, sqlite3, configmodule, chromadb, rediscache

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 160 satır

## yapay_zeka_finetuning.py

- Rol: eğitim/fine-tuning katmanı

- İlk200 satırda sınıflar: -

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, json, sqlite3, redis, torch, multiprocessing, concurrent.futures, transformers, configmodule, logging_module, datasets

- Kök modül referansları: rest_api.py, test_suite(ilk kod).py, test_suite.py

- İlk200 satır uzunluğu: 200 satır

## zotero_extension.py

- Rol: Zotero entegrasyon katmanı

- İlk200 satırda sınıflar: ZoteroExtension

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: json, requests, os, pyzotero, configmodule

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 126 satır

## zotero_integration.py

- Rol: Zotero entegrasyon katmanı

- İlk200 satırda sınıflar: ZoteroIntegration

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, json, requests, sqlite3, redis, configmodule

- Kök modül referansları: guimindmap.py

- İlk200 satır uzunluğu: 132 satır

## zoteromodule.py

- Rol: Zotero entegrasyon katmanı

- İlk200 satırda sınıflar: ZoteroManager

- İlk200 satırda fonksiyonlar: -

- İlk200 satırda importlar: os, requests, logging, colorlog, configmodule, json

- Kök modül referansları: tespit edilmedi

- İlk200 satır uzunluğu: 125 satır
