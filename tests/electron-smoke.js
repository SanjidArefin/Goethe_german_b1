const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { app, BrowserWindow, ipcMain } = require("electron");
const { getGlossary } = require("../backend/glossary-service");

app.commandLine.appendSwitch("disable-gpu");
const testProfile = path.join(os.tmpdir(), `b1-glossar-smoke-${process.pid}`);
fs.rmSync(testProfile, { force: true, recursive: true });
app.setPath("userData", testProfile);
ipcMain.handle("glossary:load", () => getGlossary());

function removeTestProfile() {
  try {
    fs.rmSync(testProfile, { force: true, maxRetries: 3, recursive: true, retryDelay: 100 });
  } catch {
    // Chromium can briefly retain a profile handle on Windows after shutdown.
  }
}

async function run() {
  await app.whenReady();

  const window = new BrowserWindow({
    show: false,
    width: 1920,
    height: 1080,
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
      "    const initialTheme = document.documentElement.dataset.theme;",
      "    const themeToggle = document.querySelector('#theme-toggle');",
      "    themeToggle.click();",
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
      "        const kButton = document.querySelector('.alphabet-button[data-letter=\\\"K\\\"]');",
      "        const kHeading = document.querySelector('.letter-heading[data-letter=\\\"K\\\"]');",
      "        const wordListPanel = document.querySelector('.word-list-panel');",
      "        const appShell = document.querySelector('.app-shell').getBoundingClientRect();",
      "        const stickyBarsOpaque = ['.list-header', '.alphabet-jump'].every((selector) => (",
      "          getComputedStyle(document.querySelector(selector)).backgroundColor !== 'rgba(0, 0, 0, 0)'",
      "        ));",
      "        const headerCells = [...document.querySelector('.list-header').children];",
      "        const rowCells = [...document.querySelector('.word-row').children];",
      "        const headerBounds = headerCells.map((cell) => cell.getBoundingClientRect());",
      "        const rowBounds = rowCells.map((cell) => cell.getBoundingClientRect());",
      "        const columnsAligned = Math.abs(headerBounds[0].left - rowBounds[0].left) <= 1",
      "          && Math.abs(headerBounds[1].left - rowBounds[1].left) <= 1",
      "          && Math.abs(headerBounds[2].right - rowBounds[2].right) <= 1;",
      "        kButton.click();",
      "        const before = document.querySelector('.word-row.is-selected')?.dataset.entryId;",
      "        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));",
      "        setTimeout(() => resolve({",
      "          totalEntries: Number(document.querySelector('#all-count').textContent),",
      "          chapterRows: chapterRows.length,",
      "          alphabetJumpWorks: !kButton.disabled && kHeading !== null,",
      "          alphabetJumpMoved: wordListPanel.scrollTop > 0,",
      "          columnsAligned,",
      "          fillsViewport: Math.abs(appShell.width - window.innerWidth) <= 1",
      "            && Math.abs(appShell.height - window.innerHeight) <= 1,",
      "          stickyBarsOpaque,",
      "          foundTransliterated,",
      "          movedSelection: before !== document.querySelector('.word-row.is-selected')?.dataset.entryId,",
      "          initialTheme,",
      "          toggledTheme: document.documentElement.dataset.theme,",
      "          storedTheme: localStorage.getItem('b1-glossar-theme'),",
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
    assert.equal(result.alphabetJumpWorks, true);
    assert.equal(result.alphabetJumpMoved, true);
    assert.equal(result.columnsAligned, true);
    assert.equal(result.fillsViewport, true);
    assert.equal(result.stickyBarsOpaque, true);
    assert.equal(result.foundTransliterated, true);
    assert.equal(result.movedSelection, true);
    assert.equal(result.initialTheme, "dark");
    assert.equal(result.toggledTheme, "light");
    assert.equal(result.storedTheme, "light");
    assert.equal(result.nodeExposed, false);
    console.log("Electron smoke test passed: offline glossary UI, dark default, and saved theme toggle.");
  } finally {
    window.destroy();
    app.quit();
    removeTestProfile();
  }
}

run().catch((error) => {
  console.error(error);
  app.exit(1);
});
