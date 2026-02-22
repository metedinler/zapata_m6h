import json
import re
import sqlite3

import requests

from configmodule import config

headers = {
    "Zotero-API-Key": config.ZOTERO_API_KEY,
    "Zotero-API-Version": "3",
}
url = f"https://api.zotero.org/users/{config.ZOTERO_USER_ID}/items"
resp = requests.get(url, headers=headers, params={"limit": 1}, timeout=20)
resp.raise_for_status()
item = resp.json()[0]

title = item.get("data", {}).get("title", "")
doc_id = item.get("key", "zotero_doc")

conn = sqlite3.connect(str(config.SQLITE_DB_PATH))
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS retrieve_docs (doc_id TEXT PRIMARY KEY, text TEXT)")
cur.execute("INSERT OR REPLACE INTO retrieve_docs (doc_id, text) VALUES (?, ?)", (doc_id, title))
conn.commit()
conn.close()

query = (re.findall(r"[A-Za-z]{4,}", title) or ["test"])[0]
payload = {"query": query, "top_k": 3}
ret = requests.post("http://127.0.0.1:8000/query", json=payload, timeout=20)

print("Q", query)
print("RET", ret.status_code, ret.text[:300])
