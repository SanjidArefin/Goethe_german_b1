const CHAPTERS = Array.from({ length: 12 }, (_, index) => index + 1);
const SEPARATOR = " \u2014 ";

const state = {
  entries: [],
  chapter: "all",
  query: "",
  selectedId: null,
};

const elements = {
  chapterTabs: document.querySelector("#chapter-tabs"),
  allChapterButton: document.querySelector('[data-chapter="all"]'),
  allCount: document.querySelector("#all-count"),
  totalCount: document.querySelector("#total-count"),
  chapterLabel: document.querySelector("#chapter-label"),
  pageTitle: document.querySelector("#page-title"),
  searchInput: document.querySelector("#search-input"),
  clearSearch: document.querySelector("#clear-search"),
  resultCount: document.querySelector("#result-count"),
  wordList: document.querySelector("#word-list"),
  wordDetail: document.querySelector("#word-detail"),
  detailPosition: document.querySelector("#detail-position"),
  previousWord: document.querySelector("#previous-word"),
  nextWord: document.querySelector("#next-word"),
  loadStatus: document.querySelector("#load-status"),
};

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  }[character]));
}

function normalizeForSearch(value) {
  return value
    .toLocaleLowerCase("de-DE")
    .replaceAll("\u00e4", "ae")
    .replaceAll("\u00f6", "oe")
    .replaceAll("\u00fc", "ue")
    .replaceAll("\u00df", "ss");
}

function chapterName(chapter) {
  return `Kapitel ${chapter}`;
}

function parseGlossary(text, chapter) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const divider = line.indexOf(SEPARATOR);

      if (divider === -1) {
        return null;
      }

      const word = line.slice(0, divider).trim();
      const meaning = line.slice(divider + SEPARATOR.length).trim();

      if (!word || !meaning) {
        return null;
      }

      return {
        id: `${chapter}-${word}`,
        chapter,
        word,
        meaning,
        searchText: normalizeForSearch(`${word} ${meaning}`),
      };
    })
    .filter(Boolean);
}

function sortedEntries(entries) {
  return [...entries].sort((left, right) => (
    left.word.localeCompare(right.word, "de-DE", { sensitivity: "base" })
    || left.chapter - right.chapter
  ));
}

function entriesForCurrentView() {
  const query = normalizeForSearch(state.query.trim());

  return sortedEntries(
    state.entries.filter((entry) => (
      (state.chapter === "all" || entry.chapter === state.chapter)
      && (!query || entry.searchText.includes(query))
    )),
  );
}

function renderChapterTabs() {
  elements.chapterTabs.innerHTML = CHAPTERS.map((chapter) => {
    const count = state.entries.filter((entry) => entry.chapter === chapter).length;
    const isActive = state.chapter === chapter;

    return `
      <button class="chapter-tab${isActive ? " is-active" : ""}" type="button"
        data-chapter="${chapter}" aria-pressed="${isActive}">
        <span>${chapterName(chapter)}</span>
        <span class="tab-count">${count || "..."}</span>
      </button>
    `;
  }).join("");

  const allActive = state.chapter === "all";
  elements.allChapterButton.classList.toggle("is-active", allActive);
  elements.allChapterButton.setAttribute("aria-pressed", String(allActive));
  elements.allCount.textContent = state.entries.length || "...";
  elements.totalCount.textContent = state.entries.length ? `${state.entries.length}` : "...";
}

function renderHeader(visibleEntries) {
  const scope = state.chapter === "all" ? "Alle Kapitel" : chapterName(state.chapter);
  elements.chapterLabel.textContent = scope;
  elements.pageTitle.textContent = state.query.trim() ? "Suchergebnisse" : "Wortschatz";
  elements.resultCount.textContent = `${visibleEntries.length} ${visibleEntries.length === 1 ? "entry" : "entries"}`;
  elements.clearSearch.hidden = !state.query;
}

function ensureSelected(visibleEntries) {
  if (!visibleEntries.some((entry) => entry.id === state.selectedId)) {
    state.selectedId = visibleEntries[0]?.id ?? null;
  }
}

function renderWordList(visibleEntries) {
  if (!visibleEntries.length) {
    elements.wordList.innerHTML = '<div class="empty-state">No matching words found.</div>';
    return;
  }

  let lastLetter = "";
  const rows = [];

  for (const entry of visibleEntries) {
    const letter = entry.word.slice(0, 1).toLocaleUpperCase("de-DE");

    if (letter !== lastLetter) {
      rows.push(`<div class="letter-heading" aria-hidden="true">${escapeHtml(letter)}</div>`);
      lastLetter = letter;
    }

    rows.push(`
      <button class="word-row${entry.id === state.selectedId ? " is-selected" : ""}"
        type="button" role="option" aria-selected="${entry.id === state.selectedId}"
        data-entry-id="${escapeHtml(entry.id)}">
        <span class="word-name">${escapeHtml(entry.word)}</span>
        <span class="word-meaning">${escapeHtml(entry.meaning)}</span>
        <span class="chapter-tag">${chapterName(entry.chapter)}</span>
      </button>
    `);
  }

  elements.wordList.innerHTML = rows.join("");
}

function renderDetail(visibleEntries) {
  const currentIndex = visibleEntries.findIndex((entry) => entry.id === state.selectedId);
  const entry = visibleEntries[currentIndex];

  if (!entry) {
    elements.wordDetail.innerHTML = '<p class="empty-detail">No word selected</p>';
    elements.detailPosition.textContent = "0 / 0";
    elements.previousWord.disabled = true;
    elements.nextWord.disabled = true;
    return;
  }

  elements.wordDetail.innerHTML = `
    <p class="detail-chapter">${chapterName(entry.chapter)}</p>
    <h3 class="detail-word">${escapeHtml(entry.word)}</h3>
    <div class="meaning-block">
      <p class="meaning-label">English</p>
      <p class="detail-meaning">${escapeHtml(entry.meaning)}</p>
    </div>
  `;
  elements.detailPosition.textContent = `${currentIndex + 1} / ${visibleEntries.length}`;
  elements.previousWord.disabled = currentIndex <= 0;
  elements.nextWord.disabled = currentIndex >= visibleEntries.length - 1;
}

function render() {
  const visibleEntries = entriesForCurrentView();
  ensureSelected(visibleEntries);
  renderChapterTabs();
  renderHeader(visibleEntries);
  renderWordList(visibleEntries);
  renderDetail(visibleEntries);
}

function selectEntry(entryId, focus = false) {
  state.selectedId = entryId;
  render();

  if (focus) {
    const selected = elements.wordList.querySelector(`[data-entry-id="${CSS.escape(entryId)}"]`);
    selected?.focus({ preventScroll: true });
    selected?.scrollIntoView({ block: "nearest" });
  }
}

function changeSelectedWord(offset) {
  const visibleEntries = entriesForCurrentView();
  const currentIndex = visibleEntries.findIndex((entry) => entry.id === state.selectedId);
  const nextEntry = visibleEntries[currentIndex + offset];

  if (nextEntry) {
    selectEntry(nextEntry.id, true);
  }
}

function selectChapter(chapter) {
  state.chapter = chapter === "all" ? "all" : Number(chapter);
  state.selectedId = null;
  render();
}

async function loadGlossary() {
  elements.loadStatus.textContent = "Glossar wird geladen";

  try {
    const chapterData = await Promise.all(CHAPTERS.map(async (chapter) => {
      const fileName = `Kapitel_${String(chapter).padStart(2, "0")}_glossary_corrected.txt`;
      const response = await fetch(`../${fileName}`);

      if (!response.ok) {
        throw new Error(`Could not load ${fileName}`);
      }

      return parseGlossary(await response.text(), chapter);
    }));

    state.entries = chapterData.flat();
    elements.loadStatus.textContent = `${state.entries.length} Woerter`;
    render();
  } catch (error) {
    console.error(error);
    elements.loadStatus.textContent = "Glossar konnte nicht geladen werden";
    elements.wordList.innerHTML = '<div class="empty-state">The glossary files could not be loaded.</div>';
  }
}

elements.chapterTabs.addEventListener("click", (event) => {
  const button = event.target.closest("[data-chapter]");

  if (button) {
    selectChapter(button.dataset.chapter);
  }
});

elements.allChapterButton.addEventListener("click", () => selectChapter("all"));

elements.searchInput.addEventListener("input", (event) => {
  state.query = event.target.value;
  state.selectedId = null;
  render();
});

elements.clearSearch.addEventListener("click", () => {
  elements.searchInput.value = "";
  state.query = "";
  state.selectedId = null;
  elements.searchInput.focus();
  render();
});

elements.wordList.addEventListener("click", (event) => {
  const row = event.target.closest("[data-entry-id]");

  if (row) {
    selectEntry(row.dataset.entryId);
  }
});

elements.previousWord.addEventListener("click", () => changeSelectedWord(-1));
elements.nextWord.addEventListener("click", () => changeSelectedWord(1));

document.addEventListener("keydown", (event) => {
  const typing = ["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName);

  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    elements.searchInput.focus();
    return;
  }

  if (!typing && event.key === "ArrowDown") {
    event.preventDefault();
    changeSelectedWord(1);
  }

  if (!typing && event.key === "ArrowUp") {
    event.preventDefault();
    changeSelectedWord(-1);
  }
});

loadGlossary();
