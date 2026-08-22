const fs = require("node:fs");
const path = require("node:path");

const DATA_FILE = path.join(__dirname, "data", "glossary.json");
let cachedGlossary;

function isSorted(entries) {
  const collator = new Intl.Collator("de-DE", { sensitivity: "base" });

  return entries.every((entry, index) => (
    index === 0 || collator.compare(entries[index - 1].word, entry.word) <= 0
  ));
}

function validateGlossary(glossary) {
  if (!glossary || !Array.isArray(glossary.chapters)) {
    throw new Error("Glossary data does not contain chapters.");
  }

  const entries = [];

  for (const chapter of glossary.chapters) {
    if (!Number.isInteger(chapter.number) || !Array.isArray(chapter.entries)) {
      throw new Error("Glossary chapter data is invalid.");
    }

    if (!isSorted(chapter.entries)) {
      throw new Error(`Kapitel ${chapter.number} is not alphabetically sorted.`);
    }

    const seenWords = new Set();

    for (const entry of chapter.entries) {
      if (!entry.word || !entry.meaning || /[,;/]/.test(entry.meaning)) {
        throw new Error(`Kapitel ${chapter.number} contains an invalid glossary entry.`);
      }

      if (seenWords.has(entry.word)) {
        throw new Error(`Kapitel ${chapter.number} contains a duplicate word.`);
      }

      seenWords.add(entry.word);
      entries.push(entry);
    }
  }

  if (glossary.chapters.length !== 12 || entries.length !== glossary.totalEntries) {
    throw new Error("Glossary totals do not match the bundled data.");
  }

  return glossary;
}

function getGlossary() {
  if (!cachedGlossary) {
    const data = fs.readFileSync(DATA_FILE, "utf8");
    cachedGlossary = validateGlossary(JSON.parse(data));
  }

  return cachedGlossary;
}

module.exports = {
  getGlossary,
  validateGlossary,
};
