import json
import requests
import os
from pyzotero import zotero
from configmodule import config

class ZoteroExtension:
    def __init__(self):
        """Zotero ile bağlantıyı kurar."""
        self.api_key = config.ZOTERO_API_KEY
        self.user_id = config.ZOTERO_USER_ID
        self.library_type = "user"
        self.zot = zotero.Zotero(self.user_id, self.library_type, self.api_key)
        self.zapata_api_url = config.ZAPATA_REST_API_URL  # Zapata Rest API ile iletişim
        self.output_folder = config.ZOTERO_OUTPUT_FOLDER  # Zapata'ya gönderilecek dosyalar için dizin

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def fetch_all_references(self):
        """
        Zotero'dan tüm referansları getirir.
        """
        try:
            references = self.zot.items()
            return references
        except Exception as e:
            print(f"❌ Zotero referanslarını çekerken hata oluştu: {e}")
            return []

    def fetch_pdf_files(self):
        """
        Zotero'daki tüm PDF dosyalarını çeker.
        """
        try:
            pdf_files = []
            items = self.zot.items()
            for item in items:
                if "data" in item and "attachments" in item["data"]:
                    for attachment in item["data"]["attachments"]:
                        if attachment["contentType"] == "application/pdf":
                            pdf_files.append(attachment["path"])
            return pdf_files
        except Exception as e:
            print(f"❌ Zotero PDF dosyalarını çekerken hata oluştu: {e}")
            return []

    def send_to_zapata(self, item_id):
        """
        Zotero'dan belirli bir makaleyi alıp Zapata'ya gönderir.
        """
        try:
            item = self.zot.item(item_id)
            data = {
                "title": item["data"]["title"],
                "abstract": item["data"].get("abstractNote", ""),
                "authors": item["data"].get("creators", []),
                "publication": item["data"].get("publicationTitle", ""),
                "year": item["data"].get("date", ""),
                "doi": item["data"].get("DOI", ""),
                "pdf_path": item["data"].get("attachments", [])
            }

            response = requests.post(f"{self.zapata_api_url}/analyze", json=data)
            if response.status_code == 200:
                print(f"✅ {item['data']['title']} başarıyla Zapata'ya gönderildi.")
            else:
                print(f"❌ Zapata'ya gönderirken hata oluştu: {response.text}")
        except Exception as e:
            print(f"❌ Zotero'dan Zapata'ya veri gönderirken hata oluştu: {e}")

    def fetch_results_from_zapata(self, query):
        """
        Zapata M6H'dan Zotero'ya sorgu yaparak sonuçları getirir.
        """
        try:
            response = requests.get(f"{self.zapata_api_url}/search", params={"query": query})
            if response.status_code == 200:
                results = response.json()
                return results
            else:
                print(f"❌ Zapata'dan veri alırken hata oluştu: {response.text}")
                return []
        except Exception as e:
            print(f"❌ Zapata'dan veri alırken hata oluştu: {e}")
            return []

    def highlight_references(self, query):
        """
        Zotero'da bir sorguya uygun referansları işaretler.
        """
        try:
            results = self.fetch_results_from_zapata(query)
            for result in results:
                item_id = result["id"]
                self.zot.update_item(item_id, {"tags": ["Zapata Highlight"]})
                print(f"✅ {result['title']} işaretlendi.")
        except Exception as e:
            print(f"❌ Zotero'da referans işaretleme hatası: {e}")

    def extract_notes(self, item_id):
        """
        Zotero'daki belirli bir öğeye ait notları çeker.
        """
        try:
            notes = self.zot.item(item_id, "notes")
            return notes
        except Exception as e:
            print(f"❌ Zotero notlarını çekerken hata oluştu: {e}")
            return []

    def sync_with_zapata(self):
        """
        Zotero'daki tüm referansları Zapata ile senkronize eder.
        """
        try:
            references = self.fetch_all_references()
            for ref in references:
                self.send_to_zapata(ref["key"])
        except Exception as e:
            print(f"❌ Zotero senkronizasyonunda hata oluştu: {e}")

# Modülü çalıştırmak için nesne oluştur
if __name__ == "__main__":
    zotero_ext = ZoteroExtension()
    zotero_ext.sync_with_zapata()
