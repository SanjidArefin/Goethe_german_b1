from pathlib import Path

INPUT = Path("Kapitel_01_glossary_final.txt")
OUTPUT = Path("Kapitel_01_glossary_corrected.txt")

# One simple, flashcard-friendly English meaning.
# These corrections override bad machine translations.
CORRECTIONS = {
    "abend": "evening",
    "abends": "in the evening",
    "achten": "to pay attention to",
    "achtet": "pays attention",
    "adjektive": "adjectives",
    "adjektiven": "adjectives",
    "affin": "related",
    "alle": "all",
    "alte": "old",
    "alten": "old",
    "andere": "other",
    "anderen": "other",
    "anzurufen": "to call",
    "arbeit": "work",
    "arbeiten": "to work",
    "aufgestanden": "got up",
    "aufhören": "to stop",
    "ausdrücken": "to express",
    "aussagen": "to state",
    "bade": "bathe",
    "bahn": "railway",
    "bedanken": "to thank",
    "beginn": "beginning",
    "bekannt": "known",
    "berichten": "to report",
    "beruflich": "professional",
    "besucht": "visited",
    "bock": "desire",
    "dabei": "with it",
    "darauf": "on it",
    "diese": "this",
    "diesem": "this",
    "diesen": "this",
    "dieser": "this",
    "dir": "you",
    "dorthin": "there",
    "drüben": "over there",
    "einfach": "simple",
    "einhalten": "to comply with",
    "erfahre": "experience",
    "erholt": "recovered",
    "erklärt": "explained",
    "erkältet": "having a cold",
    "erwartet": "expected",
    "erzählt": "told",
    "euer": "your",
    "fahren": "to drive",
    "fahrt": "journey",
    "falsch": "wrong",
    "fast": "almost",
    "feierabend": "end of work",
    "finde": "find",
    "folgende": "following",
    "frühen": "early",
    "ganz": "whole",
    "ganze": "whole",
    "ganzen": "whole",
    "gibt": "gives",
    "gleich": "same",
    "gleichen": "same",
    "große": "large",
    "großer": "large",
    "guter": "good",
    "gutes": "good",
    "hab": "have",
    "hause": "home",
    "heim": "home",
    "heißen": "to be called",
    "hierher": "here",
    "hätte": "would have",
    "ihn": "him",
    "ihnen": "them",
    "ins": "into the",
    "interessante": "interesting",
    "interessanter": "more interesting",
    "jede": "every",
    "jedem": "each",
    "jeden": "every",
    "jeder": "everyone",
    "kann": "can",
    "keine": "no",
    "keinen": "no",
    "kleine": "small",
    "kleinere": "smaller",
    "koche": "cook",
    "krank": "sick",
    "kranke": "sick",
    "können": "can",
    "könnten": "could",
    "letzte": "last",
    "liebe": "love",
    "liebsten": "favorite",
    "liegt": "lies",
    "lässt": "lets",
    "mag": "likes",
    "meldet": "reports",
    "mir": "me",
    "möchte": "would like",
    "möchten": "would like",
    "muss": "must",
    "müssen": "must",
    "morgen": "tomorrow",
    "morgens": "in the morning",
    "nächste": "next",
    "nette": "nice",
    "neue": "new",
    "neuer": "newer",
    "neues": "new",
    "normalen": "normal",
    "passende": "suitable",
    "passiert": "happened",
    "passt": "fits",
    "planst": "plans",
    "reist": "travels",
    "renovierte": "renovated",
    "repariert": "repaired",
    "räumt": "clears",
    "sage": "say",
    "schief": "crooked",
    "schlafe": "sleep",
    "schlägt": "beats",
    "schreibt": "writes",
    "schwimm": "swim",
    "schöne": "beautiful",
    "schönen": "beautiful",
    "schönsten": "most beautiful",
    "selbst": "self",
    "seltene": "rare",
    "sichert": "secures",
    "soll": "should",
    "sollen": "should",
    "stressigen": "stressful",
    "stehe": "stand",
    "stunden": "hours",
    "tagen": "days",
    "tauber": "deaf",
    "tolle": "great",
    "tolles": "great",
    "tote": "dead",
    "trägt": "carries",
    "unterstützt": "supports",
    "unseren": "our",
    "versuche": "try",
    "versuchst": "try",
    "viert": "fourth",
    "vom": "from the",
    "vorbei": "over",
    "weitere": "additional",
    "welchem": "which",
    "wenig": "little",
    "wichtige": "important",
    "wichtigen": "important",
    "wollen": "want",
    "wählt": "chooses",
    "wäre": "would be",
    "wünscht": "wishes",
    "würde": "would",
    "würden": "would",
    "zweit": "second",
    "zum": "to the",
}

# Entries that are clearly OCR errors, noise, or unnecessary junk.
REMOVE = {
    "alt",  # keep useful adjective only if needed elsewhere
}

lines = INPUT.read_text(encoding="utf-8").splitlines()

output = []
seen = set()

for line in lines:
    if " — " not in line:
        continue

    word, meaning = line.split(" — ", 1)
    word = word.strip().lower()
    meaning = meaning.strip()

    if not word or word in REMOVE:
        continue

    if word in CORRECTIONS:
        meaning = CORRECTIONS[word]

    # Remove exact duplicates.
    key = word
    if key in seen:
        continue

    seen.add(key)
    output.append(f"{word} — {meaning}")

OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")

print(f"Input:  {len(lines)}")
print(f"Final:  {len(output)}")
print(f"Saved:  {OUTPUT}")