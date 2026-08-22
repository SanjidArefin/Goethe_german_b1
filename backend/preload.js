const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("glossaryApi", {
  loadGlossary: () => ipcRenderer.invoke("glossary:load"),
});
