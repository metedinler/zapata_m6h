import os
import re
import ast
import argparse
import hashlib
import tkinter as tk
import yaml
from functools import lru_cache
from multiprocessing import Pool, cpu_count
from tkinter import filedialog, messagebox
from typing import Dict, List, Tuple, Set
from pathlib import Path

# Yapılandırma dosyası yolu
CONFIG_FILE = "scanner_config.yaml"

class EnhancedEnvironmentScanner:
    def __init__(self):
        self.cache = {}
        self.load_config()
        self.setup_patterns()

    def load_config(self):
        """Yapılandırma dosyasını yükler"""
        try:
            with open(CONFIG_FILE, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.config = {
                'enable_regex': True,
                'enable_ast': True,
                'cache_size': 100,
                'active_db_patterns': ['SQL*', 'MongoDB']
            }

    def setup_patterns(self):
        """Desenleri yapılandırmadan yükler"""
        self.env_patterns = [
            (r'\bos\.getenv\(["\']([^"\']+)["\']\)', 'os.getenv'),
            (r'\bos\.environ(?:\[["\']([^"\']+)["\']\]|\.get\(["\']([^"\']+)["\']\))', 'os.environ'),
            (r'\bconfig\.([A-Z_]+)\b', 'config_module'),
            (r'\bcfg\.([A-Z_]+)\b', 'cfg_alias'),
            (r'\bload_dotenv\(([^)]*)\)', 'load_dotenv'),
            (r'\bdotenv_values\(["\']([^"\']+)["\']\)', 'dotenv_values'),
            (r'\b(?:json|yaml)\.(?:load|safe_load)\(open\(["\']([^"\']+)["\']\)', 'file_load'),
            (r'\bwith\s+open\(["\']([^"\']+)["\']\).+\.(?:load|safe_load)\(', 'with_file_load'),
            (r'\bargparse\.ArgumentParser\(.*?add_argument\(["\']--([a-zA-Z0-9_]+)["\']', 'argparse'),
            (r'\bsys\.argv\[(\d+)\]', 'sys_argv'),
            (r'\b([A-Z_]{4,})\s*=\s*["\'][^"\']*["\']', 'direct_assignment'),
            (r'#.*alternatif(?:ler)?\s*:\s*([^\n]+)', 'comment_alternatives'),
            (r'\b(?:settings|conf)\[["\']([^"\']+)["\']\]', 'dict_access'),
            (r'\bclass\s+\w+\(BaseSettings\):.*?([A-Z_]+)\s*:\s*\w+\s*=?\s*Field\(', 'pydantic_field'),
            (r'\b(?:os|config)\.environ\s*=\s*([^\)]+)\)', 'dynamic_assignment'),
            (r'\b(?:dynaconf|python_decouple)\.(?:settings|config)\(["\']([^"\']+)["\']\)', 'third_party_libs')
        ] if self.config.get('enable_regex', True) else []

        self.db_patterns = [
            (r'sqlite3\.connect\(["\']([^"\']+)["\']\)', 'SQLite'),
            (r'mysql\.connector\.connect\([^)]*', 'MySQL'),
            (r'psycopg2\.connect\([^)]*', 'PostgreSQL'),
            (r'oracledb\.connect\(["\']([^"\']+)["\']\)', 'OracleDB'),
            (r'snowflake\.connector\.connect\([^)]*', 'Snowflake'),
            (r'cockroachdb\.connect\(["\']([^"\']+)["\']\)', 'CockroachDB'),
            (r'tidb\.connect\(["\']([^"\']+)["\']\)', 'TiDB'),
            (r'yugabyte\.connect\(["\']([^"\']+)["\']\)', 'YugabyteDB'),
            (r'timescaledb\.connect\(["\']([^"\']+)["\']\)', 'TimescaleDB'),
            (r'memgraph\.connect\(["\']([^"\']+)["\']\)', 'Memgraph'),
            (r'duckdb\.connect\(["\']([^"\']+)["\']\)', 'DuckDB'),
            (r'couchbase\.connect\(["\']([^"\']+)["\']\)', 'Couchbase'),
            (r'sqlalchemy\.create_engine\(["\']([^"\']+)["\']\)', 'SQLAlchemy'),
            (r'pymongo\.MongoClient\(["\']([^"\']+)["\']\)', 'MongoDB'),
            (r'cassandra\.cluster\.Cluster\([^)]*', 'Cassandra'),
            (r'boto3\.resource\(["\']dynamodb["\']\)', 'DynamoDB'),
            (r'elasticsearch\.Elasticsearch\(["\']([^"\']+)["\']\)', 'Elasticsearch'),
            (r'neo4j\.GraphDatabase\.driver\(["\']([^"\']+)["\']\)', 'Neo4j'),
            (r'clickhouse_driver\.connect\(["\']([^"\']+)["\']\)', 'ClickHouse'),
            (r'pymemcache\.Client\(["\']([^"\']+)["\']\)', 'Memcached'),
            (r'couchdb\.Server\(["\']([^"\']+)["\']\)', 'CouchDB'),
            (r'pyArango\.connection\.Connection\(["\']([^"\']+)["\']\)', 'ArangoDB'),
            (r'influxdb\.InfluxDBClient\(["\']([^"\']+)["\']\)', 'InfluxDB'),
            (r'firebase_admin\.db\.reference\(["\']([^"\']+)["\']\)', 'Firebase'),
            (r'supabase\.Client\(["\']([^"\']+)["\']\)', 'Supabase'),
            (r'orientdb\.connect\(["\']([^"\']+)["\']\)', 'OrientDB'),
            (r'scylladb\.connect\(["\']([^"\']+)["\']\)', 'ScyllaDB'),
            (r'foundationdb\.open\(["\']([^"\']+)["\']\)', 'FoundationDB'),
            (r'rethinkdb\.connect\(["\']([^"\']+)["\']\)', 'RethinkDB'),
            (r'aerospike\.Client\(["\']([^"\']+)["\']\)', 'Aerospike'),
            (r'riak\.RiakClient\(["\']([^"\']+)["\']\)', 'Riak'),
            (r'msrestazure\.AzureConfigurable\(["\']([^"\']+)["\']\)', 'Azure SQL'),
            (r'google\.cloud\.bigquery\.Client\(["\']([^"\']+)["\']\)', 'Google BigQuery'),
            (r'redshift_connector\.connect\(["\']([^"\']+)["\']\)', 'Amazon Redshift'),
            (r'ibm_db\.connect\(["\']([^"\']+)["\']\)', 'IBM DB2'),
            (r'interbase\.connect\(["\']([^"\']+)["\']\)', 'InterBase'),
            (r'greenplum\.connect\(["\']([^"\']+)["\']\)', 'Greenplum'),
            (r'opentsdb\.connect\(["\']([^"\']+)["\']\)', 'OpenTSDB'),
            (r'sap_hana\.connect\(["\']([^"\']+)["\']\)', 'SAP HANA'),
            (r'delta\.connect\(["\']([^"\']+)["\']\)', 'Databricks Delta Lake'),
            (r'pydruid\.connect\(["\']([^"\']+)["\']\)', 'Druid'),
            (r'presto\.connect\(["\']([^"\']+)["\']\)', 'PrestoDB'),
            (r'trino\.connect\(["\']([^"\']+)["\']\)', 'Trino'),
            (r'pyhive\.connect\(["\']([^"\']+)["\']\)', 'Apache Hive'),
            (r'impala\.connect\(["\']([^"\']+)["\']\)', 'Apache Impala'),
            (r'kudu\.connect\(["\']([^"\']+)["\']\)', 'Kudu'),
            (r'voltdb\.connect\(["\']([^"\']+)["\']\)', 'VoltDB'),
            (r'exasol\.connect\(["\']([^"\']+)["\']\)', 'Exasol'),
            (r'google\.cloud\.firestore\.Client\(["\']([^"\']+)["\']\)', 'Google Firestore'),
            (r'harperdb\.connect\(["\']([^"\']+)["\']\)', 'HarperDB'),
            (r'singlestoredb\.connect\(["\']([^"\']+)["\']\)', 'SingleStoreDB'),
            (r'datomic\.connect\(["\']([^"\']+)["\']\)', 'Datomic'),
            (r'actian\.connect\(["\']([^"\']+)["\']\)', 'Actian Vector'),
            (r'sap_ase\.connect\(["\']([^"\']+)["\']\)', 'SAP ASE (Sybase)'),
            (r'faiss\.IndexFlatL2\(["\']([^"\']+)["\']\)', 'FAISS'),
            (r'chromadb\.PersistentClient\(["\']([^"\']+)["\']\)', 'ChromaDB'),
            (r'milvus\.Collection\(["\']([^"\']+)["\']\)', 'Milvus'),
            (r'weaviate\.Client\(["\']([^"\']+)["\']\)', 'Weaviate'),
            (r'pinecone\.Index\(["\']([^"\']+)["\']\)', 'Pinecone'),
            (r'annoy\.AnnoyIndex\(["\']([^"\']+)["\']\)', 'Annoy'),
            (r'nmslib\.init\(["\']([^"\']+)["\']\)', 'NMSLib'),
            (r'hnswlib\.Index\(["\']([^"\']+)["\']\)', 'HNSWlib'),
            (r'pgvector\.connect\(["\']([^"\']+)["\']\)', 'PGVector'),
            (r'vespa\.Application\(["\']([^"\']+)["\']\)', 'Vespa'),
            (r'vald\.Client\(["\']([^"\']+)["\']\)', 'Vald'),
            (r'sptag\.AnnIndex\(["\']([^"\']+)["\']\)', 'SPTAG'),
            (r'qdrant_client\.QdrantClient\(["\']([^"\']+)["\']\)', 'Qdrant'),
            (r'redisearch\.Client\(["\']([^"\']+)["\']\)', 'RediSearch Vector Index'),
            (r'solr\.SolrClient\(["\']([^"\']+)["\']\)', 'Apache Solr Vector'),
            (r'opensearchpy\.OpenSearch\(["\']([^"\']+)["\']\)', 'OpenSearch Vector Index'),
            (r'deeplake\.VectorStore\(["\']([^"\']+)["\']\)', 'DeepLake'),
            (r'vectordb\.Client\(["\']([^"\']+)["\']\)', 'VectorDB.ai'),
            (r'tiledb\.connect\(["\']([^"\']+)["\']\)', 'TileDB'),
            (r'edgedb\.connect\(["\']([^"\']+)["\']\)', 'EdgeDB'),
            (r'surrealdb\.connect\(["\']([^"\']+)["\']\)', 'SurrealDB'),
            (r'warp10\.connect\(["\']([^"\']+)["\']\)', 'Warp 10'),
            (r'terminusdb\.connect\(["\']([^"\']+)["\']\)', 'TerminusDB'),
            (r'actian_zen\.connect\(["\']([^"\']+)["\']\)', 'Actian Zen'),
            (r'ravendb\.connect\(["\']([^"\']+)["\']\)', 'RavenDB'),
            (r'dolt\.connect\(["\']([^"\']+)["\']\)', 'Dolt'),
            (r'quasardb\.connect\(["\']([^"\']+)["\']\)', 'Quasardb'),
            (r'hyperdb\.connect\(["\']([^"\']+)["\']\)', 'HyperDB'),
            (r'immudb\.connect\(["\']([^"\']+)["\']\)', 'Immudb'),
            (r'xtdb\.connect\(["\']([^"\']+)["\']\)', 'XTDB'),
            (r'ejdb\.connect\(["\']([^"\']+)["\']\)', 'EJDB'),
            (r'lokijs\.connect\(["\']([^"\']+)["\']\)', 'LokiJS'),
            (r'zodb\.connect\(["\']([^"\']+)["\']\)', 'ZODB'),
            (r'flatbuffers\.connect\(["\']([^"\']+)["\']\)', 'Flatbuffers'),
            (r'unqlite\.connect\(["\']([^"\']+)["\']\)', 'UnQLite'),
            (r'btrieve\.connect\(["\']([^"\']+)["\']\)', 'Btrieve'),
        ]

        self.file_patterns = [
            (r'(?:open|with open)\(["\']([^"\']+)["\']', 'open'),
            (r'os\.fdopen\(["\']([^"\']+)["\']\)', 'os.fdopen'),
            (r'io\.open\(["\']([^"\']+)["\']\)', 'io.open'),
            (r'file\(["\']([^"\']+)["\']\)', 'file'),
            (r'read\(["\']([^"\']+)["\']\)', 'read'),
            (r'write\(["\']([^"\']+)["\']\)', 'write'),
            (r'shutil\.copy\(["\']([^"\']+)["\']', 'shutil.copy'),
            (r'shutil\.copy2\(["\']([^"\']+)["\']', 'shutil.copy2'),
            (r'shutil\.copyfile\(["\']([^"\']+)["\']', 'shutil.copyfile'),
            (r'shutil\.move\(["\']([^"\']+)["\']', 'shutil.move'),
            (r'os\.remove\(["\']([^"\']+)["\']\)', 'os.remove'),
            (r'os\.unlink\(["\']([^"\']+)["\']\)', 'os.unlink'),
            (r'shutil\.rmtree\(["\']([^"\']+)["\']\)', 'shutil.rmtree'),
            (r'os\.mkdir\(["\']([^"\']+)["\']\)', 'os.mkdir'),
            (r'os\.makedirs\(["\']([^"\']+)["\']\)', 'os.makedirs'),
            (r'os\.rmdir\(["\']([^"\']+)["\']\)', 'os.rmdir'),
            (r'os\.removedirs\(["\']([^"\']+)["\']\)', 'os.removedirs'),
            (r'os\.stat\(["\']([^"\']+)["\']\)', 'os.stat'),
            (r'os\.path\.exists\(["\']([^"\']+)["\']\)', 'os.path.exists'),
            (r'os\.path\.isfile\(["\']([^"\']+)["\']\)', 'os.path.isfile'),
            (r'os\.path\.isdir\(["\']([^"\']+)["\']\)', 'os.path.isdir'),
            (r'os\.path\.join\(["\']([^"\']+)["\']', 'os.path.join'),
            (r'os\.path\.abspath\(["\']([^"\']+)["\']\)', 'os.path.abspath'),
            (r'os\.path\.dirname\(["\']([^"\']+)["\']\)', 'os.path.dirname'),
            (r'os\.path\.basename\(["\']([^"\']+)["\']\)', 'os.path.basename'),
            (r'os\.rename\(["\']([^"\']+)["\']\)', 'os.rename'),
            (r'os\.replace\(["\']([^"\']+)["\']\)', 'os.replace'),
            (r'os\.chmod\(["\']([^"\']+)["\']\)', 'os.chmod'),
            (r'os\.chown\(["\']([^"\']+)["\']\)', 'os.chown'),
            (r'os\.link\(["\']([^"\']+)["\']\)', 'os.link'),
            (r'os\.symlink\(["\']([^"\']+)["\']\)', 'os.symlink'),
            (r'os\.readlink\(["\']([^"\']+)["\']\)', 'os.readlink'),
        ]

        self.ast_targets = {
            'os.getenv': ast.Call,
            'direct_assignment': ast.Assign
        } if self.config.get('enable_ast', True) else {}

    @lru_cache(maxsize=100)
    def get_file_hash(self, file_path: str) -> str:
        """Dosya hash'ini hesaplar"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def _cached_ast_parse(self, file_path: str) -> ast.AST:
        """AST ağacını önbelleğe alır"""
        current_hash = self.get_file_hash(file_path)
        if file_path not in self.cache or self.cache[file_path]['hash'] != current_hash:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                self.cache[file_path] = {'hash': current_hash, 'tree': tree}
        return self.cache[file_path]['tree']

    def _parallel_scan(self, file_list: List[str]) -> List[Dict]:
        """Paralel tarama işlemi"""
        with Pool(cpu_count()) as pool:
            return pool.map(self._process_file, file_list)

    def _process_file(self, file_path: str) -> Dict:
        """Geliştirilmiş dosya işleme metodu"""
        results = {
            'env_vars': {},
            'db_connections': set(),
            'file_ops': set(),
            'errors': []
        }
        
        try:
            # AST Analizi
            if self.config.get('enable_ast'):
                tree = self._cached_ast_parse(file_path)
                self._ast_analysis(tree, results, file_path)

            # Regex Analizi
            if self.config.get('enable_regex'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self._regex_analysis(content, results, file_path)

        except Exception as e:
            results['errors'].append(f"Kritik hata: {str(e)}")
        
        return results

    def _ast_analysis(self, tree: ast.AST, results: Dict, file_path: str):
        """AST tabanlı analiz"""
        class AdvancedVisitor(ast.NodeVisitor):
            def __init__(self, results, file_path):
                self.results = results
                self.file_path = file_path

            def visit_Call(self, node):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'getenv' and isinstance(node.func.value, ast.Name) and node.func.value.id == 'os':
                        if node.args and isinstance(node.args[0], ast.Str):
                            env_var = node.args[0].s
                            self.results['env_vars'][env_var] = self.file_path
                self.generic_visit(node)
        
        AdvancedVisitor(results, file_path).visit(tree)

    def _regex_analysis(self, content: str, results: Dict, file_path: str):
        """Gelişmiş regex analizi"""
        # Çevresel değişkenler
        for pattern, ptype in self.env_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                if ptype == 'os.getenv' or ptype == 'os.environ':
                    var_name = match.group(1)
                    results['env_vars'][var_name] = {
                        'value': '',  # Değer bilinmiyorsa boş bırak
                        'sources': [f"{file_path}:{match.start()}"],
                        'alternatives': []
                    }
                elif ptype == 'direct_assignment':
                    var_name = match.group(1)
                    var_value = match.group(0).split('=')[1].strip(" '\"")
                    results['env_vars'][var_name] = {
                        'value': var_value,
                        'sources': [f"{file_path}:{match.start()}"],
                        'alternatives': []
                    }
                elif ptype == 'comment_alternatives':
                    alternatives = [a.strip() for a in match.group(1).split(',')]
                    for var in results['env_vars']:
                        results['env_vars'][var]['alternatives'].extend(alternatives)

        # Dosya işlemleri
        for pattern, ptype in self.file_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                results['file_ops'].add((
                    match.group(1),
                    ptype,
                    f"{file_path}:{match.start()}"
                ))

        # Veritabanı bağlantıları
        for pattern, db_type in self.db_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                results['db_connections'].add((
                    db_type,
                    file_path,
                    f"{file_path}:{match.start()}"
                ))

    def _get_file_list(self, path: str, recursive: bool = False) -> List[str]:
        """Verilen yoldaki dosya listesini alır"""
        file_list = []
        if os.path.isfile(path):
            file_list.append(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(('.py', '.txt')) or '.' not in file:
                        file_list.append(os.path.join(root, file))
                if not recursive:
                    break
        return file_list

    def _merge_results(self, results: List[Dict]) -> Dict:
        """Paralel tarama sonuçlarını birleştirir"""
        merged_results = {
            'env_vars': {},
            'db_connections': set(),
            'file_ops': set(),
            'errors': []
        }
        for result in results:
            # Çevresel değişkenler
            for var, data in result['env_vars'].items():
                if var in merged_results['env_vars']:
                    if isinstance(data, dict):
                        merged_results['env_vars'][var]['sources'].extend(data['sources'])
                        merged_results['env_vars'][var]['alternatives'].extend(data['alternatives'])
                    else:
                        merged_results['env_vars'][var]['sources'].append(data)
                else:
                    merged_results['env_vars'][var] = data if isinstance(data, dict) else {'value': data, 'sources': [], 'alternatives': []}
            
            # Diğer veriler
            merged_results['db_connections'].update(result['db_connections'])
            merged_results['file_ops'].update(result['file_ops'])
            merged_results['errors'].extend(result['errors'])
        return merged_results

    def scan(self, path: str, recursive: bool = False) -> Dict:
        """Geliştirilmiş tarama metodu"""
        file_list = self._get_file_list(path, recursive)
        results = self._parallel_scan(file_list)
        return self._merge_results(results)

    def generate_report(self, results: Dict, output_file: str):
        """Rapor oluşturur"""
        with open(output_file, 'w', encoding='utf-8') as f:
            # Çevresel Değişkenler
            f.write("### ÇEVRESEL DEĞİŞKENLER ###\n")
            for var, data in results['env_vars'].items():
                # Eğer data bir string ise, bunu sözlük yapısına dönüştür
                if isinstance(data, str):
                    data = {'value': data, 'sources': [], 'alternatives': []}
                
                f.write(f"{var}={data.get('value', '')}")
                if data.get('alternatives'):
                    f.write(f"  # Alternatifler: {', '.join(data['alternatives'])}")
                f.write(f"\n# Kaynak: {', '.join(data.get('sources', []))}\n\n")
            
            # Veritabanları
            f.write("\n### VERİTABANI BAĞLANTILARI ###\n")
            for db in results['db_connections']:
                f.write(f"{db[0]} -> {db[1]}\n")
            
            # Dosya İşlemleri
            f.write("\n### DOSYA İŞLEMLERİ ###\n")
            for op in results['file_ops']:
                f.write(f"{op[1].upper()}: {op[0]} @ {op[2]}\n")
            
            # Hatalar
            if results['errors']:
                f.write("\n### HATALAR ###\n")
                for error in results['errors']:
                    f.write(f"! {error}\n")

    def _extract_env_vars(self, content: str) -> Dict[str, str]:
        """Kod içeriğinden çevresel değişkenleri ve dosya yollarını çıkarır"""
        env_vars = {}
        pattern = re.compile(r'(\w+)\s*=\s*os\.path\.join\(([^)]+)\)')
        matches = pattern.findall(content)
        for var_name, join_args in matches:
            parts = [part.strip().strip('"\'') for part in join_args.split(',')]
            if len(parts) > 1:
                base_var = parts[0].split('.')[-1]
                sub_dir = parts[1]
                env_var_name = f"{var_name.upper()}"
                env_vars[env_var_name] = os.path.join(parts[0], sub_dir)
        return env_vars

    def generate_env_file(self, results: Dict, output_file: str):
        """Çevresel değişkenleri .env dosyasına yazar"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for var, data in results['env_vars'].items():
                if isinstance(data, dict):
                    f.write(f"{var}={data.get('value', '')}\n")
                else:
                    f.write(f"{var}={data}\n")

            # Ekstra dizinleri belirle ve yaz
            for file_path in results['env_vars'].values():
                if isinstance(file_path, dict):
                    file_path = file_path.get('sources', [])[0].split(':')[0]
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        extra_vars = self._extract_env_vars(content)
                        for var, path in extra_vars.items():
                            f.write(f"{var}={path}\n")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Çevresel Tarayıcı v2.0")
        self.scanner = EnhancedEnvironmentScanner()
        self._create_widgets()
    
    def _create_widgets(self):
        # GUI düzeni
        tk.Label(self, text="Tarama Dizini:").grid(row=0, column=0, padx=5, pady=5)
        self.dir_entry = tk.Entry(self, width=50)
        self.dir_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Gözat", command=self.browse_directory).grid(row=0, column=2, padx=5, pady=5)

        self.recursive_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Alt Klasörleri Tara", variable=self.recursive_var).grid(row=1, column=1, sticky='w')

        tk.Button(self, text="Taramayı Başlat", command=self.run_scan, bg='green', fg='white').grid(row=2, column=1, pady=10)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(0, directory)

    def run_scan(self):
        target_dir = self.dir_entry.get() or os.getcwd()
        results = self.scanner.scan(target_dir, self.recursive_var.get())
        output_file = os.path.join(target_dir, 'çevresel.txt')
        self.scanner.generate_report(results, output_file)
        self.scanner.generate_env_file(results, os.path.join(target_dir, '.env'))
        messagebox.showinfo("Tamamlandı", f"Tarama başarıyla tamamlandı!\nSonuçlar: {output_file}\n{len(results['env_vars'])} değişken bulundu.")
        self.quit()
        self.destroy()

def main_cli():
    import os  # Eksik olan os modülü import edildi
    parser = argparse.ArgumentParser(description='Çevresel Değişken Tarayıcı')
    parser.add_argument('-d', '--directory', help='Tarama dizini (varsayılan: .)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Alt klasörleri tara')
    args = parser.parse_args()

    scanner = EnhancedEnvironmentScanner()
    results = scanner.scan(args.directory or os.getcwd(), args.recursive)
    scanner.generate_report(results, 'çevresel.txt')
    scanner.generate_env_file(results, '.env')
    print(f"Tarama tamamlandı. {len(results['env_vars'])} değişken bulundu.")

if __name__ == "__main__":
    if len(os.sys.argv) > 1:
        main_cli()
    else:
        app = Application()
        app.mainloop()
