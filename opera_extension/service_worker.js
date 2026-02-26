const API_URL = "http://127.0.0.1:5000/browser/ingest";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "zapata-send-selection",
    title: "Zapata'ya gönder (seçili metin)",
    contexts: ["selection"]
  });

  chrome.contextMenus.create({
    id: "zapata-send-page",
    title: "Zapata'ya gönder (sayfayı oku)",
    contexts: ["page"]
  });
});

async function sendToZapata(payload) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`API hata: ${response.status} ${errText}`);
  }
  return response.json();
}

async function getPageText(tabId) {
  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => (document.body?.innerText || "").slice(0, 20000)
  });

  if (!results || !results.length) {
    return "";
  }
  return results[0].result || "";
}

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  try {
    if (!tab || !tab.id) {
      return;
    }

    if (info.menuItemId === "zapata-send-selection") {
      const payload = {
        selectedText: info.selectionText || "",
        title: tab.title || "",
        url: tab.url || ""
      };
      const result = await sendToZapata(payload);
      console.log("Zapata yanıtı:", result);
      return;
    }

    if (info.menuItemId === "zapata-send-page") {
      const pageText = await getPageText(tab.id);
      const payload = {
        pageText,
        title: tab.title || "",
        url: tab.url || ""
      };
      const result = await sendToZapata(payload);
      console.log("Zapata yanıtı:", result);
    }
  } catch (error) {
    console.error("Zapata gönderim hatası:", error);
  }
});
