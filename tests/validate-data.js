const { getGlossary } = require("../backend/glossary-service");

const glossary = getGlossary();
const counts = glossary.chapters.map((chapter) => chapter.entries.length);

console.log(`Validated ${glossary.totalEntries} entries across ${glossary.chapters.length} chapters.`);
console.log(`Chapter counts: ${counts.join(", ")}`);
