import os
import json
import webbrowser
from configmodule import config

class D3Visualizer:
    def __init__(self):
        self.html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                .node circle {
                    fill: steelblue;
                    stroke: white;
                    stroke-width: 2px;
                }
                .node text {
                    font-size: 14px;
                    fill: black;
                }
                .link {
                    fill: none;
                    stroke: #ccc;
                    stroke-width: 2px;
                }
            </style>
        </head>
        <body>
            <svg width="960" height="600"></svg>
            <script>
                var treeData = JSON.parse('%DATA%');

                var margin = {{top: 20, right: 90, bottom: 30, left: 90}},
                    width = 960 - margin.left - margin.right,
                    height = 600 - margin.top - margin.bottom;

                var svg = d3.select("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                var treeLayout = d3.tree().size([height, width]);

                var root = d3.hierarchy(treeData);
                treeLayout(root);

                var link = svg.selectAll(".link")
                    .data(root.links())
                    .enter().append("path")
                    .attr("class", "link")
                    .attr("d", d3.linkHorizontal()
                        .x(function(d) { return d.y; })
                        .y(function(d) { return d.x; }));

                var node = svg.selectAll(".node")
                    .data(root.descendants())
                    .enter().append("g")
                    .attr("class", "node")
                    .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

                node.append("circle")
                    .attr("r", 10);

                node.append("text")
                    .attr("dy", ".35em")
                    .attr("x", function(d) { return d.children ? -13 : 13; })
                    .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
                    .text(function(d) { return d.data.name; });
            </script>
        </body>
        </html>
        """

    def generate_html(self, json_data):
        """
        JSON verisini D3.js kullanarak interaktif bir HTML dosyası oluşturur.
        """
        json_string = json.dumps(json_data).replace("'", "&#39;")
        html_content = self.html_template.replace("%DATA%", json_string)

        html_path = os.path.join(config.OUTPUT_DIR, "mindmap.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return html_path

    def show_mindmap(self, json_data):
        """
        Zihin haritasını oluşturup varsayılan tarayıcıda açar.
        """
        html_file = self.generate_html(json_data)
        webbrowser.open("file://" + html_file)

# Örnek kullanım
if __name__ == "__main__":
    example_data = {
        "name": "Makale Başlığı",
        "children": [
            {"name": "Özet"},
            {"name": "Giriş"},
            {
                "name": "Kaynakça",
                "children": [
                    {"name": "Referans 1"},
                    {"name": "Referans 2"}
                ]
            }
        ]
    }

    visualizer = D3Visualizer()
    visualizer.show_mindmap(example_data)
