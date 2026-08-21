from pathlib import Path
import sqlite3
import re
import sys


BASE = Path(__file__).resolve().parent

if len(sys.argv) != 2:
    print("Usage: python build_glossary.py <chapter_number>")
    sys.exit(1)

CHAPTER_NUMBER = int(sys.argv[1])

CANDIDATES = BASE / f"Kapitel_{CHAPTER_NUMBER:02d}_vocab_candidates.txt"
CHAPTER = BASE / "chapters" / f"Kapitel_{CHAPTER_NUMBER:02d}.txt"
DB = BASE / "dictionary-de.db"
OUTPUT = BASE / f"Kapitel_{CHAPTER_NUMBER:02d}_glossary_corrected.txt"


# ============================================================
# Words that are not useful as standalone flashcards.
# ============================================================

IGNORE = {
    "ich", "du", "er", "sie", "es", "wir", "ihr",
    "mich", "dich", "ihn", "ihm", "uns", "euch",
    "mein", "meine", "meinen", "meinem", "meiner",
    "dein", "deine", "deinen", "deinem", "deiner",
    "sein", "seine", "seinen", "seinem", "seiner",
    "unser", "unsere", "unseren", "unserem", "unserer",
    "euer", "eure", "euren", "eurem", "eurer",

    "der", "die", "das", "den", "dem", "des",
    "ein", "eine", "einen", "einem", "einer", "eines",

    "und", "oder", "aber", "denn", "weil", "dass",
    "wenn", "als", "ob", "auch", "nur", "schon", "noch",
    "nicht", "kein", "keine", "keinen", "keinem", "keiner",

    "hier", "dort", "wo", "wer", "was", "wie", "wann",
    "warum", "wieso",

    "beim", "vom", "zum", "zur", "im", "am",
}


# ============================================================
# Proper names.
# ============================================================

PROPER_NAMES = {
    "aachen", "anna", "annas", "anton", "axel",
    "berlin", "berlins", "bergner", "bergner-alm",
    "blömecke", "dinklage", "dinlage",
    "finenstein", "fingenstein", "finkenstein",
    "florian", "heringsdorf", "hofmann",
    "kevin", "liam", "stuttgart",
    "theresia", "thomas", "timo", "timos",
    "usedom", "wien", "würzburg", "zermatt",
}


# ============================================================
# OCR garbage.
# ============================================================

OCR_GARBAGE = {
    "adiektiv", "affing", "affink", "beob", "brem",
    "chmlttag", "dabel", "daort", "dieuhr",
    "dinglage", "durchsa", "gutläuft",
    "haren", "hareng", "harenk", "hul",
    "iich", "kannn", "kkindern", "swn",
    "stunder", "zuu", "vergesscn", "weilig",
    "wöärter",
}


# ============================================================
# Explicit corrections for forms seen in the chapters.
# These always override the dictionary.
# ============================================================

NORMALIZE = {
    "abends": "abend",
    "abneigungen": "abneigung",
    "alle": "all",
    "aktivitäten": "aktivität",

    "alte": "alt",
    "alten": "alt",
    "altes": "alt",

    "anderes": "andere",
    "anderen": "andere",
    "anderem": "andere",
    "anderer": "andere",

    "angebote": "angebot",
    "aufgaben": "aufgabe",
    "aufgestanden": "aufstehen",

    "ausflüge": "ausflug",
    "ausstellungen": "ausstellung",
    "auszuruhen": "ausruhen",
    "auszuschlafen": "ausschlafen",

    "bäume": "baum",
    "bäumen": "baum",

    "beschreibungen": "beschreibung",
    "besonderheiten": "besonderheit",
    "besuchern": "besucher",

    "besten": "gut",
    "beliebtesten": "beliebt",

    "bilder": "bild",
    "bisschen": "bisschen",

    "arbeitet": "arbeiten",
    "arbeite": "arbeiten",
    "gearbeitet": "arbeiten",

    "bekommt": "bekommen",
    "besucht": "besuchen",
    "braucht": "brauchen",
    "bringt": "bringen",
    "bleibe": "bleiben",

    "blicken": "blick",
    "bocken": "bock",
    "booten": "boot",

    "buche": "buchen",
    "denke": "denken",

    "diesen": "dies",
    "diesem": "dies",
    "diese": "dies",

    "fahre": "fahren",
    "fährt": "fahren",
    "finde": "finden",
    "findest": "finden",
    "findet": "finden",

    "freue": "freuen",
    "fühle": "fühlen",
    "führt": "führen",

    "gehe": "gehen",
    "geht": "gehen",
    "gemacht": "machen",
    "gefällt": "gefallen",

    "geschäfte": "geschäft",
    "gespräche": "gespräch",

    "komm": "kommen",
    "kommt": "kommen",

    "tolle": "toll",
    "tolles": "toll",

    "tipps": "tipp",
    "touristen": "tourist",
    "trauben": "traube",

    "verspätungen": "verspätung",
    "versuche": "versuchen",
    "versuchst": "versuchen",

    "viele": "viel",
    "wichtige": "wichtig",
    "wichtigen": "wichtig",

    "wochen": "woche",

    "wollte": "wollen",
    "wollten": "wollen",

    "wählt": "wählen",

    "wäre": "sein",

    "würde": "werden",
    "würden": "werden",

    "wörter": "wort",
    "wörtern": "wort",

    "wünscht": "wünschen",

    "zugnummern": "zug",
    "mass": "ma\u00df",
    "weiss": "wei\u00df",
}


# ============================================================
# Manual meanings.
# These have absolute priority.
# ============================================================

MANUAL = {
    "abend": "evening",
    "absatz": "paragraph",
    "abenteuer": "adventure",
    "abneigung": "dislike",
    "ach": "oh",
    "acht": "eight",
    "achten": "to pay attention to",
    "adjektiv": "adjective",
    "aktivität": "activity",
    "aktuell": "current",
    "all": "all",
    "angabe": "information",
    "andere": "other",
    "alles": "everything",
    "alltag": "everyday life",
    "alm": "alpine pasture",
    "alt": "old",
    "altstadt": "old town",
    "anders": "different",
    "anfang": "beginning",
    "anfangen": "to begin",
    "angebot": "offer",
    "angenehm": "pleasant",
    "angst": "fear",
    "ankommen": "to arrive",
    "anrufen": "to call",
    "anstrengen": "to make an effort",
    "anspruch": "claim",
    "arbeit": "work",
    "arbeiten": "to work",
    "aufbauen": "to build",
    "aufenthalt": "stay",
    "aufgabe": "task",
    "aufgeben": "to give up",
    "aufhören": "to stop",
    "aufstehen": "to get up",
    "ausdruck": "expression",
    "ausdr\u00fccken": "to express",
    "ausflug": "excursion",
    "ausgehen": "to go out",
    "auspacken": "to unpack",
    "ausruhen": "to rest",
    "aussage": "statement",
    "ausschlafen": "to sleep in",
    "aussicht": "view",
    "aussprache": "pronunciation",
    "ausstellung": "exhibition",
    "auto": "car",
    "außerdem": "besides",
    "baden": "to bathe",
    "bahn": "railway",
    "bahnhof": "station",
    "baum": "tree",
    "bedanken": "to thank",
    "begeistert": "enthusiastic",
    "beginn": "beginning",
    "beginnen": "to begin",
    "beide": "both",
    "beinahe": "almost",
    "beispiel": "example",
    "bekannt": "familiar",
    "bekommen": "to receive",
    "beliebt": "popular",
    "bericht": "report",
    "beruflich": "professional",
    "berühmt": "famous",
    "beschreibung": "description",
    "besichtigen": "to visit",
    "besonderheit": "feature",
    "besonders": "especially",
    "besser": "better",
    "bestimmt": "certain",
    "besuch": "visit",
    "besuchen": "to visit",
    "besucher": "visitor",
    "bett": "bed",
    "bild": "picture",
    "bilden": "to form",
    "bis": "until",
    "bisschen": "a little",
    "bleiben": "to stay",
    "blick": "view",
    "blog": "blog",
    "blöd": "stupid",
    "bock": "buck",
    "boot": "boat",
    "brauchen": "to need",
    "brennen": "to burn",
    "bringen": "to bring",
    "buchen": "to book",
    "bucht": "bay",
    "bushaltestelle": "bus stop",
    "büro": "office",
    "chat": "chat",
    "dabei": "with it",
    "danach": "afterwards",
    "darauf": "on it",
    "daten": "data",
    "dauern": "to last",
    "denken": "to think",
    "derselbe": "the same",
    "deutschland": "Germany",
    "direkt": "direct",
    "dorthin": "there",
    "draußen": "outside",
    "drüben": "over there",
    "echt": "really",
    "eher": "rather",
    "eigentlich": "actually",
    "einfach": "simple",
    "einhalten": "to comply with",
    "einmal": "once",
    "einpacken": "to pack",
    "einsam": "lonely",
    "einsamkeit": "loneliness",
    "empfang": "reception",
    "empfehlen": "to recommend",
    "ende": "end",
    "endlich": "finally",
    "entfernung": "distance",
    "enthalten": "to contain",
    "entscheiden": "to decide",
    "entschlossen": "determined",
    "entspannen": "to relax",
    "enttäuscht": "disappointed",
    "erfahrung": "experience",
    "ergänzen": "to complete",
    "erholen": "to recover",
    "erklärung": "explanation",
    "erkältet": "sick with a cold",
    "erleben": "to experience",
    "erlebnis": "experience",
    "erst": "only",
    "erwarten": "to expect",
    "erzählen": "to tell",
    "essen": "to eat",
    "etwas": "something",
    "fahren": "to travel",
    "fahrrad": "bicycle",
    "fahrt": "journey",
    "fall": "case",
    "fallen": "to fall",
    "falls": "if",
    "falsch": "wrong",
    "familie": "family",
    "fan": "fan",
    "fast": "almost",
    "faulenzen": "to laze around",
    "feierabend": "end of work",
    "feiern": "to celebrate",
    "ferienhaus": "holiday home",
    "ferienwohnung": "holiday apartment",
    "fest": "festival",
    "feuer": "fire",
    "finden": "to find",
    "fit": "fit",
    "flug": "flight",
    "flughafen": "airport",
    "foto": "photo",
    "frage": "question",
    "fragen": "to ask",
    "freund": "friend",
    "freundin": "female friend",
    "früh": "early",
    "frühstück": "breakfast",
    "funktionieren": "to function",
    "fuß": "foot",
    "fühlen": "to feel",
    "führen": "to lead",
    "ganz": "whole",
    "gar": "at all",
    "gebirge": "mountains",
    "geburtstag": "birthday",
    "gefühl": "feeling",
    "gehen": "to go",
    "genervt": "annoyed",
    "genug": "enough",
    "genuss": "enjoyment",
    "geplant": "planned",
    "gepäck": "luggage",
    "geregnet": "rained",
    "gern": "gladly",
    "geschichte": "story",
    "geschmack": "taste",
    "gestern": "yesterday",
    "gesund": "healthy",
    "gespräch": "conversation",
    "heizung": "heating",
    "helfen": "to help",
    "hören": "to hear",
    "interessant": "interesting",
    "kennen": "to know",
    "klar": "clear",
    "klein": "small",
    "koffer": "suitcase",
    "kofferraum": "trunk",
    "kommen": "to come",
    "kompromiss": "compromise",
    "kosten": "to cost",
    "krank": "ill",
    "kultur": "culture",
    "kunde": "customer",
    "kundin": "female customer",
    "kurs": "course",
    "kurz": "short",
    "mio": "million",
    "verkehr": "traffic",
    "vertiefung": "deepening",
}


# ============================================================
# Dictionary metadata that must NEVER be used as meanings.
# ============================================================

BAD_MEANING_PATTERNS = (
    "inflection of",
    "plural of",
    "genitive",
    "dative",
    "accusative",
    "nominative",
    "subjunctive",
    "past participle",
    "present participle",
    "superlative degree",
    "comparative degree",
    "gerund of",
    "zu-infinitive",
    "nominalization",
    "weak/mixed",
    "first-person",
    "second-person",
    "third-person",
    "dependent present",
    "dependent preterite",
    "imperative",
    "agent noun of",
    "given name",
    "contraction of",
    "alternative spelling",
    "standard spelling",
    "verbal noun of",
    "abbreviation of",
    "form of",
    "surname",
    "proper noun",
)


def clean(word):
    word = word.strip().lower()
    word = re.sub(r"^[^a-zäöüß]+|[^a-zäöüß]+$", "", word)
    return word if word else None


def is_bad_meaning(text):
    lower = text.lower()
    return (
        lower.startswith("see ")
        or any(pattern in lower for pattern in BAD_MEANING_PATTERNS)
    )


def one_meaning(text):
    """Keep one short, flashcard-friendly meaning."""

    return re.split(r"[,;/(]", text, maxsplit=1)[0].strip()


def get_dictionary_meaning(db, word):
    """
    Return the first useful English dictionary meaning for a lemma.
    """

    if word in MANUAL:
        return MANUAL[word]

    rows = db.execute(
        """
        SELECT gloss
        FROM senses
        WHERE lower(word) = ?
        ORDER BY sort_order
        """,
        (word,),
    ).fetchall()

    for (gloss,) in rows:
        if not gloss:
            continue

        text = gloss.strip()

        if is_bad_meaning(text):
            continue

        text = one_meaning(text)

        if 2 <= len(text) <= 80:
            return text

    return None


def load_dictionary(db):
    """
    Load all useful dictionary senses into memory.

    This avoids performing hundreds of thousands of SQLite queries.
    """

    print("Loading dictionary...")

    dictionary = {}

    rows = db.execute(
        """
        SELECT lower(word), gloss
        FROM senses
        ORDER BY sort_order
        """
    )

    for word, gloss in rows:
        if not word or not gloss:
            continue

        if word in dictionary:
            continue

        text = gloss.strip()

        if is_bad_meaning(text):
            continue

        text = one_meaning(text)

        if 2 <= len(text) <= 80:
            dictionary[word] = text

    print(f"Dictionary senses loaded: {len(dictionary)} words")

    return dictionary


def load_inflections(db):
    """
    Load inflected form -> lemma mappings.

    The exact column names are detected from the database so that
    this remains compatible with the existing dictionary database.
    """

    print("Loading inflection forms...")

    columns = [
        row[1]
        for row in db.execute("PRAGMA table_info(inflections)").fetchall()
    ]

    if not columns:
        print("No inflections table found.")
        return {}

    lower_columns = {c.lower(): c for c in columns}

    form_column = None
    lemma_column = None

    for name in ("inflected_form", "form", "word", "inflection"):
        if name in lower_columns:
            form_column = lower_columns[name]
            break

    for name in ("lemma", "base", "root"):
        if name in lower_columns:
            lemma_column = lower_columns[name]
            break

    if not form_column or not lemma_column:
        print("Could not identify inflection columns.")
        print("Columns:", columns)
        return {}

    query = f"""
        SELECT lower("{form_column}"), lower("{lemma_column}")
        FROM inflections
    """

    inflections = {}

    for form, lemma in db.execute(query):
        if form and lemma:
            inflections.setdefault(form, []).append(lemma)

    for form, lemmas in inflections.items():
        inflections[form] = tuple(dict.fromkeys(lemmas))

    print(f"Inflection forms loaded: {len(inflections)}")

    return inflections


def resolve_inflection_lemma(word, inflections, dictionary):
    """Choose the most useful base form for a word without a direct sense."""

    options = []
    seen = set()

    for inflection_lemma in inflections.get(word, ()):
        candidate = NORMALIZE.get(inflection_lemma, inflection_lemma)

        if candidate in seen:
            continue

        seen.add(candidate)
        meaning = MANUAL.get(candidate) or dictionary.get(candidate)

        if not meaning:
            continue

        # Forms such as "brauche" can map to both a noun and a verb.
        # Prefer an infinitive when the direct form had no usable sense.
        options.append((not meaning.startswith("to "), candidate, meaning))

    if not options:
        return None

    _, lemma, meaning = min(options)
    return lemma, meaning


# ============================================================
# Load candidates.
# ============================================================

candidates = [
    clean(x)
    for x in CANDIDATES.read_text(encoding="utf-8").splitlines()
]

candidates = [x for x in candidates if x]


# ============================================================
# Open database ONCE.
# ============================================================

db = sqlite3.connect(DB)

dictionary = load_dictionary(db)
inflections = load_inflections(db)


# ============================================================
# Build glossary.
# ============================================================

glossary = {}
removed = []
normalized_forms = []


for word in candidates:

    # --------------------------------------------------------
    # Basic exclusions.
    # --------------------------------------------------------

    if word in IGNORE or word in PROPER_NAMES or word in OCR_GARBAGE:
        removed.append(word)
        continue

    # --------------------------------------------------------
    # Explicit chapter-specific normalization.
    # --------------------------------------------------------

    lemma = NORMALIZE.get(word, word)

    # --------------------------------------------------------
    # Manual meaning always wins.
    # --------------------------------------------------------

    if lemma in MANUAL:
        glossary[lemma] = one_meaning(MANUAL[lemma])

        if word != lemma:
            normalized_forms.append(f"{word} -> {lemma}")

        continue

    # Keep useful entries that are already dictionary headwords. Only resolve
    # an inflection when the direct form is absent or purely grammatical data.
    meaning = dictionary.get(lemma)

    if not meaning:
        resolved = resolve_inflection_lemma(lemma, inflections, dictionary)

        if resolved:
            lemma, meaning = resolved

            if word != lemma:
                normalized_forms.append(f"{word} -> {lemma}")
        else:
            removed.append(word)
            continue

    if lemma not in MANUAL and lemma not in dictionary:
        removed.append(word)
        continue

    # --------------------------------------------------------
    # Get meaning.
    # --------------------------------------------------------

    meaning = one_meaning(MANUAL.get(lemma) or meaning)

    # --------------------------------------------------------
    # Safety check.
    # --------------------------------------------------------

    if not meaning or is_bad_meaning(meaning):
        removed.append(word)
        continue

    glossary[lemma] = meaning


db.close()


# ============================================================
# Sort and save.
# ============================================================

glossary = dict(sorted(glossary.items()))

with OUTPUT.open("w", encoding="utf-8") as f:
    for word, meaning in glossary.items():
        f.write(f"{word} — {meaning}\n")


print()
print(f"Chapter:   {CHAPTER_NUMBER}")
print(f"Input:     {len(candidates)}")
print(f"Glossary:  {len(glossary)}")
print(f"Removed:   {len(removed)}")
print(f"Normalized: {len(normalized_forms)}")
print(f"Saved to:  {OUTPUT}")

print()
print("First removed words:")
print(", ".join(removed[:50]))

print()
print("First normalized forms:")
print(", ".join(normalized_forms[:50]))
