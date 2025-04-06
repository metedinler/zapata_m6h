import json
import os
import sqlite3
import redis
import tkinter as tk
from tkinter import ttk
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
from configmodule import config
from zotero_integration import fetch_zotero_data
from zapata_restapi import fetch_mindmap_data

class MindMapGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Zotero & Zapata Zihin Haritası")
        self.create_widgets()
        self.server = None

    def create_widgets(self):
        """GUI bileşenlerini oluşturur."""
        self.label = ttk.Label(self.master, text="Zihin Haritası Görselleştirme", font=("Arial", 14))
        self.label.pack(pady=10)

        self.load_button = ttk.Button(self.master, text="Veri Yükle", command=self.load_mindmap_data)
        self.load_button.pack(pady=5)

        self.open_map_button = ttk.Button(self.master, text="Haritayı Görüntüle", command=self.open_mindmap)
        self.open_map_button.pack(pady=5)

    def load_mindmap_data(self):
        """Zotero ve Zapata’dan verileri çekerek JSON formatında kaydeder."""
        zotero_data = fetch_zotero_data()
        zapata_data = fetch_mindmap_data()

        mindmap_data = {"nodes": [], "links": []}

        # Zotero’dan gelen kaynakça verileri
        for item in zotero_data:
            mindmap_data["nodes"].append({"id": item["title"], "group": "zotero"})
        
        # Zapata’dan gelen atıf ve bağlantılar
        for link in zapata_data["links"]:
            mindmap_data["links"].append({"source": link["source"], "target": link["target"], "type": "citation"})

        with open("mindmap_data.json", "w", encoding="utf-8") as f:
            json.dump(mindmap_data, f, indent=4)
        print("✅ Zihin haritası verileri başarıyla yüklendi!")

    def open_mindmap(self):
        """Zihin haritasını görüntülemek için yerel bir HTML sunucusu başlatır."""
        file_path = os.path.abspath("mindmap.html")
        webbrowser.open("file://" + file_path)

        if self.server is None:
            self.server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
            print("🌍 Mind Map Server başlatıldı: http://localhost:8080")
            self.server.serve_forever()

def run_gui():
    root = tk.Tk()
    app = MindMapGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
