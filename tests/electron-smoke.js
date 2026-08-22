const assert = require("node:assert/strict");
const path = require("node:path");
const { app, BrowserWindow, ipcMain } = require("electron");
const { getGlossary } = require("../backend/glossary-service");

app.commandLine.appendSwitch("disable-gpu");
ipcMain.handle("glossary:load", () => getGlossary());

async function run() {
  await app.whenReady();

  const window = new BrowserWindow({
    show: false,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      preload: path.join(__dirname, "..", "backend", "preload.js"),
    },
  });

  try {
    await window.loadFile(path.join(__dirname, "..", "frontend", "index.html"));

    const result = await window.webContents.executeJavaScript([
      "new Promise((resolve, reject) => {",
      "  const readState = () => {",
      "    const rows = [...document.querySelectorAll('.word-row')];",
      "    if (rows.length === 0) {",
      "      reject(new Error('Glossary UI did not render any word rows.'));",
      "      return;",
      "    }",
      "    const input = document.querySelector('#search-input');",
      "    input.value = 'abhaengen';",
      "    input.dispatchEvent(new Event('input', { bubbles: true }));",
      "    setTimeout(() => {",
      "      const foundTransliterated = [...document.querySelectorAll('.word-name')].some((element) => element.textContent === 'abhängen');",
      "      input.value = '';",
      "      input.dispatchEvent(new Event('input', { bubbles: true }));",
      "      document.querySelector('[data-chapter=\\\"3\\\"]').click();",
      "      setTimeout(() => {",
      "        const chapterRows = [...document.querySelectorAll('.word-row')];",
      "        const before = document.querySelector('.word-row.is-selected')?.dataset.entryId;",
      "        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));",
      "        setTimeout(() => resolve({",
      "          totalEntries: Number(document.querySelector('#all-count').textContent),",
      "          chapterRows: chapterRows.length,",
      "          foundTransliterated,",
      "          movedSelection: before !== document.querySelector('.word-row.is-selected')?.dataset.entryId,",
      "          nodeExposed: typeof window.require !== 'undefined',",
      "        }), 0);",
      "      }, 0);",
      "    }, 0);",
      "  };",
      "  const poll = (attemptsLeft) => {",
      "    if (document.querySelectorAll('.word-row').length > 0) { readState(); return; }",
      "    if (attemptsLeft === 0) { reject(new Error('Glossary UI timed out.')); return; }",
      "    setTimeout(() => poll(attemptsLeft - 1), 25);",
      "  };",
      "  poll(40);",
      "})",
    ].join("\n"));

    assert.equal(result.totalEntries, 9435);
    assert.equal(result.chapterRows, 892);
    assert.equal(result.foundTransliterated, true);
    assert.equal(result.movedSelection, true);
    assert.equal(result.nodeExposed, false);
    console.log("Electron smoke test passed: local glossary UI loaded without a web server.");
  } finally {
    window.destroy();
    app.quit();
  }
}

run().catch((error) => {
  console.error(error);
  app.exit(1);
});
