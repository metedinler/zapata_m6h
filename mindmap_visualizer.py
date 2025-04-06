# ilk verilen kod
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from pyzotero import zotero
from configmodule import config

class MindMapVisualizer:
    def __init__(self):
        """Zotero ile bağlantıyı kurar ve görselleştirme için gerekli dizinleri oluşturur."""
        self.api_key = config.ZOTERO_API_KEY
        self.user_id = config.ZOTERO_USER_ID
        self.library_type = "user"
        self.zot = zotero.Zotero(self.user_id, self.library_type, self.api_key)
        self.output_folder = config.MINDMAP_OUTPUT_FOLDER  # Görsellerin kaydedileceği klasör

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def fetch_references(self):
        """
        Zotero'dan tüm referansları çeker.
        """
        try:
            references = self.zot.items()
            return references
        except Exception as e:
            print(f"❌ Zotero referanslarını çekerken hata oluştu: {e}")
            return []

    def extract_citation_network(self):
        """
        Zotero’daki atıf ilişkilerini çıkararak bir network grafiği oluşturur.
        """
        references = self.fetch_references()
        citation_graph = nx.DiGraph()

        for ref in references:
            ref_id = ref["key"]
            title = ref["data"]["title"]
            citation_graph.add_node(ref_id, label=title)

            if "relations" in ref["data"] and "dc:relation" in ref["data"]["relations"]:
                cited_refs = ref["data"]["relations"]["dc:relation"]
                for cited in cited_refs:
                    cited_id = cited.split("/")[-1]
                    citation_graph.add_edge(ref_id, cited_id)

        return citation_graph

    def visualize_citation_network(self):
        """
        Zotero’daki atıf ilişkilerini bir zihin haritası olarak görselleştirir.
        """
        graph = self.extract_citation_network()
        plt.figure(figsize=(12, 8))

        pos = nx.spring_layout(graph, seed=42)
        labels = {node: data["label"] for node, data in graph.nodes(data=True)}

        nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="lightblue", edge_color="gray", font_size=10)
        nx.draw_networkx_labels(graph, pos, labels, font_size=8, font_weight="bold")

        output_path = os.path.join(self.output_folder, "citation_network.png")
        plt.savefig(output_path)
        plt.show()

        print(f"✅ Zihin haritası oluşturuldu: {output_path}")

    def export_graph_json(self):
        """
        Zotero atıf ağını D3.js uyumlu bir JSON formatında dışa aktarır.
        """
        graph = self.extract_citation_network()
        nodes = [{"id": node, "label": data["label"]} for node, data in graph.nodes(data=True)]
        links = [{"source": u, "target": v} for u, v in graph.edges()]

        graph_data = {"nodes": nodes, "links": links}
        output_path = os.path.join(self.output_folder, "citation_network.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=4)

        print(f"✅ Zihin haritası JSON olarak kaydedildi: {output_path}")

# Modülü çalıştırmak için nesne oluştur
if __name__ == "__main__":
    visualizer = MindMapVisualizer()
    visualizer.visualize_citation_network()
    visualizer.export_graph_json()
