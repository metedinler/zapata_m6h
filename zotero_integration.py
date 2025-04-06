import os
import json
import requests
import sqlite3
import redis
from configmodule import config

class ZoteroIntegration:
    def __init__(self):
        self.api_key = config.ZOTERO_API_KEY
        self.user_id = config.ZOTERO_USER_ID
        self.api_url = config.ZOTERO_API_URL
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

        # Redis bağlantısı
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

        # SQLite bağlantısı
        self.sqlite_db = config.SQLITE_DB_PATH
        self.ensure_tables()

    def ensure_tables(self):
        """SQLite içinde kaynakça verilerini saklamak için gerekli tabloları oluşturur."""
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS references (
                id TEXT PRIMARY KEY,
                title TEXT,
                authors TEXT,
                year TEXT,
                journal TEXT,
                doi TEXT,
                file_path TEXT
            )
        """)
        conn.commit()
        conn.close()

    def fetch_references_from_zotero(self):
        """Zotero’dan tüm kaynakça verilerini çeker ve JSON formatında kaydeder."""
        response = requests.get(f"{self.api_url}/items", headers=self.headers)
        if response.status_code == 200:
            references = response.json()
            with open(os.path.join(config.TEMIZ_KAYNAKCA_DIZIN, "zotero_references.json"), "w", encoding="utf-8") as f:
                json.dump(references, f, indent=4)
            print("✅ Zotero'dan kaynakça verileri alındı ve kaydedildi.")
            return references
        else:
            print(f"❌ Zotero'dan veri alınamadı: {response.status_code}")
            return None

    def save_references_to_sqlite(self, references):
        """Kaynakçaları SQLite veritabanına kaydeder."""
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        for ref in references:
            item_id = ref["key"]
            title = ref["data"].get("title", "Bilinmiyor")
            authors = ", ".join([creator["lastName"] for creator in ref["data"].get("creators", [])])
            year = ref["data"].get("date", "Bilinmiyor")
            journal = ref["data"].get("publicationTitle", "Bilinmiyor")
            doi = ref["data"].get("DOI", None)
            file_path = ref["data"].get("filePath", None)

            cursor.execute("""
                INSERT OR REPLACE INTO references (id, title, authors, year, journal, doi, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (item_id, title, authors, year, journal, doi, file_path))
        
        conn.commit()
        conn.close()
        print("✅ Zotero kaynakçaları SQLite veritabanına kaydedildi.")

    def fetch_pdf_from_scihub(self, doi):
        """DOI’ye göre Sci-Hub üzerinden makale PDF dosyasını indirir."""
        sci_hub_url = f"https://sci-hub.se/{doi}"
        response = requests.get(sci_hub_url, stream=True)
        if response.status_code == 200:
            pdf_path = os.path.join(config.PDF_DIR, f"{doi}.pdf")
            with open(pdf_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"✅ PDF indirildi: {pdf_path}")
            return pdf_path
        else:
            print(f"❌ Sci-Hub'tan PDF indirilemedi: {response.status_code}")
            return None

    def cache_references_to_redis(self, references):
        """Kaynakça verilerini Redis önbelleğine kaydeder."""
        for ref in references:
            item_id = ref["key"]
            ref_data = json.dumps(ref["data"])
            self.redis_client.set(f"reference:{item_id}", ref_data)
        print("✅ Kaynakçalar Redis’e kaydedildi.")

    def load_cached_references(self):
        """Redis'ten kaynakça verilerini yükler."""
        keys = self.redis_client.keys("reference:*")
        references = [json.loads(self.redis_client.get(key)) for key in keys]
        return references

    def export_references(self, format="ris"):
        """Kaynakçaları farklı formatlarda dışa aktarır (RIS, BibTeX, CSV, Pajek, VOSviewer)."""
        references = self.load_cached_references()
        export_path = os.path.join(config.TEMIZ_KAYNAKCA_DIZIN, f"references.{format}")

        if format == "ris":
            with open(export_path, "w", encoding="utf-8") as f:
                for ref in references:
                    f.write(f"TY  - JOUR\nTI  - {ref.get('title', '')}\nAU  - {ref.get('authors', '')}\nPY  - {ref.get('year', '')}\nJO  - {ref.get('journal', '')}\nDO  - {ref.get('doi', '')}\nER  -\n\n")
        elif format == "bib":
            with open(export_path, "w", encoding="utf-8") as f:
                for ref in references:
                    f.write(f"@article{{{ref.get('doi', '')},\ntitle = {{{ref.get('title', '')}}},\nauthor = {{{ref.get('authors', '')}}},\nyear = {{{ref.get('year', '')}}},\njournal = {{{ref.get('journal', '')}}},\ndoi = {{{ref.get('doi', '')}}}\n}}\n\n")
        elif format == "csv":
            with open(export_path, "w", encoding="utf-8") as f:
                f.write("Title,Authors,Year,Journal,DOI\n")
                for ref in references:
                    f.write(f"{ref.get('title', '')},{ref.get('authors', '')},{ref.get('year', '')},{ref.get('journal', '')},{ref.get('doi', '')}\n")
        
        print(f"✅ Kaynakçalar {format.upper()} formatında dışa aktarıldı: {export_path}")

# **Örnek Kullanım**
if __name__ == "__main__":
    zotero = ZoteroIntegration()
    references = zotero.fetch_references_from_zotero()
    if references:
        zotero.save_references_to_sqlite(references)
        zotero.cache_references_to_redis(references)
        zotero.export_references(format="ris")  # RIS formatında dışa aktar
