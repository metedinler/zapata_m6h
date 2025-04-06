import pdfplumber
import fitz  # PyMuPDF
import pdfminer
import layoutparser as lp
import detectron2
import tabula
import borb
import tika
import pdfquery
import camelot
import pytesseract
import re
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from concurrent.futures import ProcessPoolExecutor
from transformers import pipeline
from PIL import Image

class AdvancedPDFProcessor:
    def __init__(self, 
                 text_method='multi', 
                 table_method='multi', 
                 reference_method='advanced',
                 debug_mode=False):
        self.text_methods = ['pdfplumber', 'pymupdf', 'pdfminer', 'borb', 'tika']
        self.table_methods = ['pymupdf', 'pdfplumber', 'tabula', 'camelot']
        self.reference_methods = ['regex', 'ml', 'section_based']
        
        self.text_method = text_method
        self.table_method = table_method
        self.reference_method = reference_method
        self.debug_mode = debug_mode
        
        # ML Modelleri
        self.reference_model = self._load_reference_model()
        self.layout_model = self._load_layout_model()

    def _load_reference_model(self):
        """Referans çıkarma için ML modeli"""
        return pipeline("token-classification", model="dslim/bert-base-NER")

    def _load_layout_model(self):
        """Layout tespiti için model"""
        return lp.Detectron2LayoutModel(
            "lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config"
        )

    def extract_text(self, pdf_path) -> str:
        """Çoklu kütüphane ile metin çıkarma"""
        texts = []
        
        # PDFPlumber
        if 'pdfplumber' in self.text_method or self.text_method == 'multi':
            with pdfplumber.open(pdf_path) as pdf:
                texts.append(" ".join([page.extract_text() for page in pdf.pages]))
        
        # PyMuPDF
        if 'pymupdf' in self.text_method or self.text_method == 'multi':
            doc = fitz.open(pdf_path)
            texts.append(" ".join([page.get_text() for page in doc]))
        
        # Borb
        if 'borb' in self.text_method or self.text_method == 'multi':
            with open(pdf_path, 'rb') as file:
                doc = borb.pdf.DocumentFromBytes(file.read())
                borb_text = " ".join([page.extract_text() for page in doc.pages])
                texts.append(borb_text)
        
        # Tika
        if 'tika' in self.text_method or self.text_method == 'multi':
            raw = tika.parser.from_file(pdf_path)
            texts.append(raw.get('content', ''))
        
        # PDFMiner
        if 'pdfminer' in self.text_method or self.text_method == 'multi':
            from pdfminer.high_level import extract_text
            pdfminer_text = extract_text(pdf_path)
            texts.append(pdfminer_text)
        
        # En uzun metni seç veya birleştir
        return max(texts, key=len) if texts else ""

    def extract_tables(self, pdf_path) -> List[pd.DataFrame]:
        """Çoklu kütüphane ile tablo çıkarma"""
        all_tables = []
        
        # PyMuPDF
        if 'pymupdf' in self.table_method or self.table_method == 'multi':
            doc = fitz.open(pdf_path)
            for page in doc:
                pymupdf_tables = page.find_tables()
                all_tables.extend(pymupdf_tables)
        
        # PDFPlumber
        if 'pdfplumber' in self.table_method or self.table_method == 'multi':
            with pdfplumber.open(pdf_path) as pdf:
                pdfplumber_tables = [
                    pd.DataFrame(page.extract_table()) 
                    for page in pdf.pages if page.extract_table()
                ]
                all_tables.extend(pdfplumber_tables)
        
        # Tabula
        if 'tabula' in self.table_method or self.table_method == 'multi':
            tabula_tables = tabula.read_pdf(pdf_path, pages='all')
            all_tables.extend(tabula_tables)
        
        # Camelot
        if 'camelot' in self.table_method or self.table_method == 'multi':
            camelot_tables = camelot.read_pdf(pdf_path)
            all_tables.extend([table.df for table in camelot_tables])
        
        return all_tables

    def extract_references(self, pdf_path) -> List[str]:
        """Gelişmiş referans çıkarma"""
        text = self.extract_text(pdf_path)
        references = []
        
        # Regex Tabanlı
        if self.reference_method in ['regex', 'multi']:
            regex_patterns = [
                r'\[(\d+)\]\s*(.+?)(?=\[|\n\n|$)',  # Sayısal referans
                r'([A-Z][a-z]+ et al\., \d{4})',     # Yazar stili
                r'(\w+,\s\d{4}[a-z]?)'               # APA stili
            ]
            for pattern in regex_patterns:
                references.extend(re.findall(pattern, text, re.DOTALL))
        
        # ML Tabanlı
        if self.reference_method in ['ml', 'multi']:
            ml_references = self.reference_model(text)
            references.extend([
                entity['word'] for entity in ml_references 
                if entity['entity'] == 'B-MISC'
            ])
        
        # Bölüm Bazlı
        if self.reference_method in ['section_based', 'multi']:
            section_references = self._extract_references_by_section(text)
            references.extend(section_references)
        
        return list(set(references))

    def _extract_references_by_section(self, text):
        """Bölüm bazlı referans çıkarma"""
        sections = ['References', 'Bibliography', 'Works Cited']
        references = []
        
        for section in sections:
            section_match = re.search(
                f"{section}(.*?)(\n\n|\Z)", 
                text, 
                re.IGNORECASE | re.DOTALL
            )
            if section_match:
                section_text = section_match.group(1)
                references.extend(
                    re.findall(r'\[(\d+)\]\s*(.+?)(?=\[|\n\n|$)', section_text, re.DOTALL)
                )
        
        return references

    def detect_page_layout(self, pdf_path):
        """Gelişmiş sayfa düzeni tespiti"""
        doc = fitz.open(pdf_path)
        layouts = []
        
        # Layout Parser
        model = lp.Detectron2LayoutModel(
            "lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config"
        )
        
        for page_num, page in enumerate(doc):
            # Sayfa görüntüsü
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Layout tespiti
            detected_layout = model.detect(img)
            
            page_layout = {
                'page_number': page_num + 1,
                'elements': {
                    'text_blocks': [],
                    'titles': [],
                    'figures': [],
                    'tables': [],
                    'headers': [],
                    'footers': []
                }
            }
            
            for block in detected_layout:
                block_type = self._classify_block(block)
                page_layout['elements'][f'{block_type}s'].append(block)
            
            layouts.append(page_layout)
        
        return layouts

    def _classify_block(self, block):
        """Blok sınıflandırma"""
        block_type_map = {
            'Title': 'title',
            'Text': 'text',
            'Figure': 'figure', 
            'Table': 'table',
            'Header': 'header',
            'Footer': 'footer'
        }
        
        return block_type_map.get(block.type, 'text')

    def process_pdf(self, pdf_path):
        """Tüm özellikleri birleştirilmiş PDF işleme"""
        return {
            'text': self.extract_text(pdf_path),
            'tables': self.extract_tables(pdf_path),
            'references': self.extract_references(pdf_path),
            'layout': self.detect_page_layout(pdf_path)
        }

# Kullanım örneği
pdf_processor = AdvancedPDFProcessor(
    text_method='multi', 
    table_method='multi', 
    reference_method='advanced',
    debug_mode=True
)

# PDF işleme
result = pdf_processor.process_pdf('akademik_makale.pdf')