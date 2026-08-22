const state = {
  entries: [],
  chapters: [],
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

function chapterName(chapter) {
  return `Kapitel ${chapter}`;
}

function entriesForCurrentView() {
  return GlossaryModel.filterEntries(state.entries, {
    chapter: state.chapter,
    query: state.query,
  });
}

function renderChapterTabs() {
  elements.chapterTabs.innerHTML = state.chapters.map((chapter) => {
    const isActive = state.chapter === chapter.number;

    return `
      <button class="chapter-tab${isActive ? " is-active" : ""}" type="button"
        data-chapter="${chapter.number}" aria-pressed="${isActive}">
        <span>${chapter.title}</span>
        <span class="tab-count">${chapter.entries.length}</span>
      </button>
    `;
  }).join("");

  const allActive = state.chapter === "all";
  elements.allChapterButton.classList.toggle("is-active", allActive);
  elements.allChapterButton.setAttribute("aria-pressed", String(allActive));
  elements.allCount.textContent = state.entries.length;
  elements.totalCount.textContent = state.entries.length;
}

function renderHeader(visibleEntries) {
  elements.chapterLabel.textContent = state.chapter === "all"
    ? "Alle Kapitel"
    : chapterName(state.chapter);
  elements.pageTitle.textContent = state.query.trim() ? "Suchergebnisse" : "Wortschatz";
  elements.resultCount.textContent = `${visibleEntries.length} ${visibleEntries.length === 1 ? "Eintrag" : "Eintraege"}`;
  elements.clearSearch.hidden = !state.query;
}

function ensureSelected(visibleEntries) {
  if (!visibleEntries.some((entry) => entry.id === state.selectedId)) {
    state.selectedId = visibleEntries[0]?.id ?? null;
  }
}

function renderWordList(visibleEntries) {
  if (!visibleEntries.length) {
    elements.wordList.innerHTML = '<div class="empty-state">Keine passenden Woerter gefunden.</div>';
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
    elements.wordDetail.innerHTML = '<p class="empty-detail">Kein Wort ausgewaehlt</p>';
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
    const glossary = await window.glossaryApi.loadGlossary();

    state.chapters = glossary.chapters;
    state.entries = glossary.chapters.flatMap((chapter) => (
      chapter.entries.map((entry) => ({
        ...entry,
        id: `${chapter.number}-${entry.word}`,
        chapter: chapter.number,
        searchText: GlossaryModel.normalizeForSearch(`${entry.word} ${entry.meaning}`),
      }))
    ));

    elements.loadStatus.textContent = `${glossary.totalEntries} Woerter`;
    render();
  } catch (error) {
    console.error(error);
    elements.loadStatus.textContent = "Glossar konnte nicht geladen werden";
    elements.wordList.innerHTML = '<div class="empty-state">Die Glossardaten konnten nicht geladen werden.</div>';
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
  const isTyping = ["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName);

  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    elements.searchInput.focus();
    return;
  }

  if (!isTyping && event.key === "ArrowDown") {
    event.preventDefault();
    changeSelectedWord(1);
  }

  if (!isTyping && event.key === "ArrowUp") {
    event.preventDefault();
    changeSelectedWord(-1);
  }
});

loadGlossary();
