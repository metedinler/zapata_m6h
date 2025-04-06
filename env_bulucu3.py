import os
import re
import ast
import argparse
import hashlib
import tkinter as tk
import yaml
from functools import lru_cache
from multiprocessing import Pool, cpu_count, Manager
from threading import Thread
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Tuple, Set
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Yapılandırma dosyası yolu
CONFIG_FILE = "scanner_config.yaml"
PATTERNS_FILE = "patterns.yaml"
#DOSYA_YOLU = "C:/Users/mete/Zotero/zotasistan/zapata_m6h/"

class EnhancedEnvironmentScanner:
    def __init__(self):
        self.cache = {}
        self.load_config()
        self.load_patterns()
        self.compile_patterns()

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

    def load_patterns(self):
        """Harici YAML dosyasından desenleri yükler"""
        try:
            with open(PATTERNS_FILE, "r") as f:
                patterns = yaml.safe_load(f)
                if patterns is None:
                    raise ValueError("patterns.yaml içeriği geçersiz.")
                self.env_patterns = patterns.get("env_patterns", [])
                self.db_patterns = patterns.get("db_patterns", [])
                self.file_patterns = patterns.get("file_patterns", [])
        except (FileNotFoundError, ValueError) as e:
            print(f"patterns.yaml yüklenemedi: {e}. Varsayılan desenler kullanılacak.")
            self.setup_default_patterns()

    def setup_default_patterns(self):
        """Varsayılan desenleri tanımlar"""
        self.env_patterns = [
            (r'\bos\.getenv\(["\']([^"\']+)["\']\s*,\s*["\']([^"\']*)["\']\)',
             'os.getenv_default'),
            (r'\bPath\(os\.path\.join\(([^)]+)\)\)', 'path_join'),
            (r'\bos\.getenv\(["\']([^"\']+)["\']\)', 'os.getenv'),
            (
                r'\bos\.environ(?:\[["\']([^"\']+)["\']\]|\.get\(["\']([^"\']+)["\']\))',
                'os.environ'),
        ]
        self.db_patterns = [
            (r'sqlite3\.connect\(["\']([^"\']+)["\']\)', 'SQLite'),
            (r'mysql\.connector\.connect\([^)]*', 'MySQL'),
        ]
        self.file_patterns = [
            (r'(?:open|with open)\(["\']([^"\']+)["\']', 'open'),
            (r'os\.fdopen\(["\']([^"\']+)["\']\)', 'os.fdopen'),
        ]

    def compile_patterns(self):
        """Desenleri derle ve önbelleğe al"""
        self.compiled_env_patterns = [
            (re.compile(pattern),
             ptype) for pattern,
            ptype in self.env_patterns]
        self.compiled_db_patterns = [
            (re.compile(pattern),
             ptype) for pattern,
            ptype in self.db_patterns]
        self.compiled_file_patterns = [
            (re.compile(pattern),
             ptype) for pattern,
            ptype in self.file_patterns]

    @lru_cache(maxsize=100)
    def get_file_hash(self, file_path: str) -> str:
        """Dosya hash'ini hesaplar"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"Hata (get_file_hash): {e}")
            return ""

    def _cached_ast_parse(self, file_path: str) -> ast.AST:
        """AST ağacını önbelleğe alır"""
        try:
            current_hash = self.get_file_hash(file_path)
            if file_path not in self.cache or self.cache[file_path]['hash'] != current_hash:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    self.cache[file_path] = {
                        'hash': current_hash, 'tree': tree}
            return self.cache[file_path]['tree']
        except Exception as e:
            print(f"Hata (_cached_ast_parse): {e}")
            return None

    def _parallel_scan(
            self, file_list: List[str], progress_callback=None) -> List[Dict]:
        """Paralel tarama işlemi"""
        try:
            results = []
            with Pool(cpu_count()) as pool:
                for i, result in enumerate(
                        pool.imap_unordered(self._process_file, file_list)):
                    results.append(result)
                    if progress_callback:
                        progress_callback(i + 1, len(file_list))
            return results
        except Exception as e:
            print(f"Hata (_parallel_scan): {e}")
            return []

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
        """AST ile os.getenv ve Path/join kullanımlarını yakala"""
        class EnvVisitor(ast.NodeVisitor):
            def __init__(self, results, file_path):
                self.results = results
                self.file_path = file_path

            def visit_Assign(self, node):
                try:
                    # os.getenv ile atamaları yakala
                    if isinstance(node.value, ast.Call) and isinstance(
                            node.value.func, ast.Attribute):
                        if node.value.func.attr == 'getenv' and isinstance(
                                node.value.func.value, ast.Name) and node.value.func.value.id == 'os':
                            # Constant node için .value
                            var_name = node.value.args[0].value
                            default_value = node.value.args[1].value if len(
                                node.value.args) > 1 else ""
                            self.results['env_vars'][var_name] = {
                                'value': default_value,
                                'sources': [f"{self.file_path}:{node.lineno}"]
                            }
                    # Path ve os.path.join ile oluşturulan yolları yakala
                    if isinstance(node.value, ast.Call) and (isinstance(
                            node.value.func, ast.Attribute) or isinstance(node.value.func, ast.Name)):
                        func_name = node.value.func.attr if isinstance(
                            node.value.func, ast.Attribute) else node.value.func.id
                        if func_name in ['join', 'Path']:
                            path_parts = [arg.value for arg in node.value.args]
                            full_path = os.path.join(
                                *path_parts).replace('\\', '/')
                            var_name = node.targets[0].attr if isinstance(
                                node.targets[0], ast.Attribute) else node.targets[0].id
                            self.results['env_vars'][var_name] = {
                                'value': full_path,
                                'sources': [f"{self.file_path}:{node.lineno}"]
                            }
                except Exception as e:
                    print(f"Hata (visit_Assign): {e}")

        EnvVisitor(results, file_path).visit(tree)

    def _regex_analysis(self, content: str, results: Dict, file_path: str):
        """Gelişmiş regex analizi"""
        # Çevresel değişkenler
        for compiled_pattern, ptype in self.compiled_env_patterns:
            matches = compiled_pattern.finditer(content)
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
        # Diğer desenler burada devam eder...

    def _merge_results(self, results: List[Dict]) -> Dict:
        """Paralel tarama sonuçlarını birleştirir"""
        merged_results = {
            'env_vars': {},
            'db_connections': set(),
            'file_ops': set(),
            'errors': []
        }
        try:
            for result in results:
                # Çevresel değişkenler
                for var, data in result['env_vars'].items():
                    if var in merged_results['env_vars']:
                        merged_results['env_vars'][var]['sources'].extend(
                            data['sources'])
                        merged_results['env_vars'][var]['alternatives'].extend(
                            data['alternatives'])
                    else:
                        merged_results['env_vars'][var] = data
                # Diğer veriler
                merged_results['db_connections'].update(
                    result['db_connections'])
                merged_results['file_ops'].update(result['file_ops'])
                merged_results['errors'].extend(result['errors'])
        except Exception as e:
            print(f"Hata (_merge_results): {e}")
        return merged_results

    def scan(self, path: str, recursive: bool = False,
             progress_callback=None) -> Dict:
        """Geliştirilmiş tarama metodu"""
        try:
            file_list = self._get_file_list(path, recursive)
            results = self._parallel_scan(file_list, progress_callback)
            return self._merge_results(results)
        except Exception as e:
            print(f"Hata (scan): {e}")
            return {}

    def _get_file_list(self, path: str, recursive: bool = False) -> List[str]:
        """Verilen yoldaki dosya listesini alır"""
        try:
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
        except Exception as e:
            print(f"Hata (_get_file_list): {e}")
            return []

    def generate_report(self, results: Dict, output_file: str):
        """Rapor oluşturur"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Çevresel değişkenler
                f.write("### ÇEVRESEL DEĞİŞKENLER ###\n")
                for var, data in results['env_vars'].items():
                    f.write(f"{var}={data.get('value', '')}\n")
                    if data.get('alternatives'):
                        f.write(
                            f"  # Alternatifler: {
                                ', '.join(
                                    data['alternatives'])}\n")
                    f.write(
                        f"# Kaynak: {
                            ', '.join(
                                data.get(
                                    'sources',
                                    []))}\n")
                # Diğer raporlama işlemleri burada devam eder...
        except Exception as e:
            print(f"Hata (generate_report): {e}")

    def generate_env_file(self, results: Dict, output_file: str):
        """Çevresel değişkenleri .env dosyasına yazar"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for var, data in results['env_vars'].items():
                    f.write(f"{var}={data.get('value', '')}\n")
        except Exception as e:
            print(f"Hata (generate_env_file): {e}")


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Çevresel Tarayıcı v2.0")
        self.scanner = EnhancedEnvironmentScanner()
        self._create_widgets()

    def _create_widgets(self):
        """GUI düzenini oluşturur"""
        tk.Label(
            self,
            text="Tarama Dizini:").grid(
            row=0,
            column=0,
            padx=5,
            pady=5)
        self.dir_entry = tk.Entry(self, width=50)
        self.dir_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(
            self,
            text="Gözat",
            command=self.browse_directory).grid(
            row=0,
            column=2,
            padx=5,
            pady=5)

        self.recursive_var = tk.BooleanVar()
        tk.Checkbutton(
            self,
            text="Alt Klasörleri Tara",
            variable=self.recursive_var).grid(
            row=1,
            column=1,
            sticky='w')

        self.multithread_var = tk.BooleanVar()
        tk.Checkbutton(
            self,
            text="Threading Kullan",
            variable=self.multithread_var).grid(
            row=2,
            column=1,
            sticky='w')

        self.multiprocessing_var = tk.BooleanVar()
        tk.Checkbutton(
            self,
            text="Çok İşlemcili Çalış",
            variable=self.multiprocessing_var).grid(
            row=3,
            column=1,
            sticky='w')

        tk.Button(
            self,
            text="Taramayı Başlat",
            command=self.run_scan,
            bg='green',
            fg='white').grid(
            row=4,
            column=1,
            pady=10)

        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=5, column=1, pady=10)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(0, directory)

    def update_progress(self, current, total):
        """İlerleme çubuğunu günceller"""
        self.progress['value'] = (current / total) * 100
        self.update_idletasks()

    def run_scan(self):
        target_dir = self.dir_entry.get() or os.getcwd()
        recursive = self.recursive_var.get()
        use_multithreading = self.multithread_var.get()
        use_multiprocessing = self.multiprocessing_var.get()

        def scan_task():
            try:
                results = self.scanner.scan(
                    target_dir, recursive, progress_callback=self.update_progress)
                output_file = os.path.join(target_dir, 'çevresel.txt')
                self.scanner.generate_report(results, output_file)
                self.scanner.generate_env_file(
                    results, os.path.join(target_dir, '.env'))
                messagebox.showinfo("Tamamlandı", f"Tarama başarıyla tamamlandı!\nSonuçlar: {
                                    output_file}\n{len(results['env_vars'])} değişken bulundu.")
            except Exception as e:
                messagebox.showerror(
                    "Hata", f"Tarama sırasında bir hata oluştu: {e}")

        if use_multithreading:
            thread = Thread(target=scan_task)
            thread.start()
        else:
            scan_task()


def main_cli():
    parser = argparse.ArgumentParser(description='Çevresel Değişken Tarayıcı')
    parser.add_argument(
        '-d',
        '--directory',
        help='Tarama dizini (varsayılan: .)')
    parser.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        help='Alt klasörleri tara')
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
