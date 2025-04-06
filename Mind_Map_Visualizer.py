import json
import tkinter as tk
from tkinter import ttk
from configmodule import config
import d3js_visualizer

class MindMapVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Zihin Haritası - Zapata M6H")
        self.create_ui()

    def create_ui(self):
        """
        Kullanıcı arayüzünü oluşturur.
        """
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill="both", expand=True)

        self.load_button = ttk.Button(self.root, text="Haritayı Yükle", command=self.load_mind_map)
        self.load_button.pack()

    def load_mind_map(self):
        """
        JSON formatında saklanan zihin haritasını yükler ve görüntüler.
        """
        try:
            with open(config.MINDMAP_JSON_PATH, "r", encoding="utf-8") as f:
                mind_map_data = json.load(f)
            d3js_visualizer.display_mind_map(mind_map_data)
        except Exception as e:
            print(f"❌ Hata: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MindMapVisualizer(root)
    root.mainloop()
