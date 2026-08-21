from pathlib import Path

INPUT = Path("Kapitel_01_translated.txt")
OUTPUT = Path("Kapitel_01_glossary.txt")

# Forms that should point to their base vocabulary item.
NORMALIZE = {
    "abends": ("abends", "in the evening"),
    "abneigungen": ("abneigung", "dislike"),
    "aktivitäten": ("aktivität", "activity"),
    "angebote": ("angebot", "offer"),
    "ausflüge": ("ausflug", "excursion"),
    "ausstellungen": ("ausstellung", "exhibition"),
    "aufgaben": ("aufgabe", "task"),
    "bilder": ("bild", "picture"),
    "bäume": ("baum", "tree"),
    "beschreibungen": ("beschreibung", "description"),
    "besonderheiten": ("besonderheit", "feature"),
    "besuchern": ("besucher", "visitor"),
    "freunde": ("freund", "friend"),
    "freunden": ("freund", "friend"),
    "fotos": ("foto", "photo"),
    "erfahrungen": ("erfahrung", "experience"),
    "fahrräder": ("fahrrad", "bicycle"),
    "farben": ("farbe", "color"),
    "gebäuden": ("gebäude", "building"),
    "angebote": ("angebot", "offer"),
    "beliebtesten": ("beliebt", "popular"),
    "besten": ("gut", "good"),
    "bestimmten": ("bestimmt", "certain"),
    "denselben": ("derselbe", "the same"),
    "eure": ("euer", "your"),
    "euren": ("euer", "your"),
    "fotos": ("foto", "photo"),
    "fünfzehn": ("fünfzehn", "fifteen"),
    "dreizehn": ("dreizehn", "thirteen"),
    "zwanzig": ("zwanzig", "twenty"),
    "elf": ("elf", "eleven"),
    "drei": ("drei", "three"),
    "acht": ("acht", "eight"),
    "fünf": ("fünf", "five"),
}

# Verb conjugations: keep the infinitive instead.
VERB_FORMS = {
    "arbeite": "arbeiten",
    "arbeitet": "arbeiten",
    "bekommt": "bekommen",
    "braucht": "brauchen",
    "bringt": "bringen",
    "dauert": "dauern",
    "denke": "denken",
    "fahre": "fahren",
    "fährt": "fahren",
    "finde": "finden",
    "findest": "finden",
    "findet": "finden",
    "freue": "freuen",
    "fühle": "fühlen",
    "fühlt": "fühlen",
    "gehe": "gehen",
    "geht": "gehen",
    "hast": "haben",
    "kommt": "kommen",
    "macht": "machen",
    "spielt": "spielen",
    "steht": "stehen",
    "stelle": "stellen",
    "stellt": "stellen",
    "sucht": "suchen",
    "will": "wollen",
    "wollte": "wollen",
    "wollten": "wollen",
}

# Words that are names, OCR garbage, or clearly not useful vocabulary.
REMOVE = {
    "aachen", "anna", "annas", "anton", "axel",
    "berlin", "berlins", "bergner", "bergner-alm",
    "blömecke", "chmlttag", "dabel", "daort",
    "dieuhr", "dinglage", "dinklage", "dinlage",
    "durchsa", "finenstein", "fingenstein", "finkenstein",
    "florian", "forumstexte", "affing", "affink",
    "adiektiv", "beob", "bild-geschichte", "blogeintrag",
    "ferienclub", "ferienhaus", "ferienwohnung",
    "fahrtzeit", "fotos",
}

# Final flashcard-friendly meanings for words where automatic translation
# is misleading or unnecessarily complicated.
MEANINGS = {
    "abend": "evening",
    "abends": "in the evening",
    "ach": "oh",
    "achten": "to pay attention to",
    "adjektiv": "adjective",
    "affin": "related to",
    "alle": "all",
    "alles": "everything",
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
    "anstrengend": "strenuous",
    "arbeit": "work",
    "arbeiten": "to work",
    "aufbauen": "to build",
    "aufenthalt": "stay",
    "aufgabe": "task",
    "aufhören": "to stop",
    "aufstehen": "to get up",
    "ausdrücken": "to express",
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
    "bad": "bathroom",
    "baden": "to bathe",
    "bahn": "railway",
    "bahnhof": "station",
    "baum": "tree",
    "bedanken": "to thank",
    "begeistert": "enthusiastic",
    "beginn": "beginning",
    "beide": "both",
    "beinahe": "almost",
    "beispiel": "example",
    "bekannt": "known",
    "bekommen": "to receive",
    "beliebt": "popular",
    "berichten": "to report",
    "beruflich": "professional",
    "berühmt": "famous",
    "beschreibung": "description",
    "besichtigen": "to visit",
    "besonderheit": "feature",
    "besonders": "especially",
    "besser": "better",
    "bestimmt": "certain",
    "besuchen": "to visit",
    "besucher": "visitor",
    "bett": "bed",
    "bild": "picture",
    "bilden": "to form",
    "bis": "until",
    "bisschen": "a little",
    "bleiben": "to stay",
    "blick": "view",
    "blöd": "stupid",
    "bock": "desire",
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
    "dieser": "this",
    "diktieren": "to dictate",
    "direkt": "direct",
    "dorthin": "there",
    "draußen": "outside",
    "drüben": "over there",
    "durchsage": "announcement",
    "durchsagen": "to announce",
    "echt": "real",
    "eher": "rather",
    "eigentlich": "actually",
    "eimer": "bucket",
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
    "entspannend": "relaxing",
    "enttäuscht": "disappointed",
    "erfahrung": "experience",
    "ergänzen": "to add",
    "erholen": "to recover",
    "erklären": "to explain",
    "erkältet": "having a cold",
    "erleben": "to experience",
    "erlebnis": "experience",
    "erst": "first",
    "erwarten": "to expect",
    "erzählen": "to tell",
    "essen": "to eat",
    "etwas": "something",
    "fahren": "to drive / ride",
    "fahrrad": "bicycle",
    "fahrt": "journey",
    "fall": "case",
    "fallen": "to fall",
    "falls": "if",
    "falsch": "wrong",
    "familie": "family",
    "farbe": "color",
    "fassen": "to grasp",
    "fast": "almost",
    "faulenzen": "to relax",
    "feierabend": "end of work",
    "feiern": "to celebrate",
    "fest": "firm",
    "feuer": "fire",
    "finden": "to find",
    "flug": "flight",
    "flughafen": "airport",
    "folgend": "following",
    "forschung": "research",
    "foto": "photo",
    "frage": "question",
    "fragen": "to ask",
    "freuen": "to be happy",
    "freund": "friend",
    "freundin": "girlfriend",
    "früh": "early",
    "frühstück": "breakfast",
    "funktionieren": "to function",
    "fuß": "foot",
    "fühlen": "to feel",
    "führen": "to lead",
    "ganz": "whole",
    "gar": "even",
    "geben": "to give",
    "gebiet": "area",
    "gebirge": "mountains",
    "geburtstag": "birthday",
    "gebäude": "building",
    "gefallen": "to like",
    "gefühl": "feeling",
    "gehen": "to go",
    "gelandet": "landed",
    "gelaunt": "in a mood",
    "gelten": "to apply",
    "gemacht": "made",
    "genervt": "annoyed",
    "genug": "enough",
    "genuss": "enjoyment",
    "geplant": "planned",
}

lines = INPUT.read_text(encoding="utf-8").splitlines()

result = {}
removed = []

for line in lines:
    if "—" not in line:
        continue

    word, translation = line.split("—", 1)
    word = word.strip().lower()
    translation = translation.strip()

    if word in REMOVE:
        removed.append(word)
        continue

    # Convert plural/inflected form to base form where explicitly known.
    if word in NORMALIZE:
        word, translation = NORMALIZE[word]

    # Convert conjugated verb to infinitive.
    if word in VERB_FORMS:
        word = VERB_FORMS[word]

    # Use our controlled flashcard meaning where available.
    if word in MEANINGS:
        translation = MEANINGS[word]

    # Never allow exact duplicate vocabulary entries.
    if word not in result:
        result[word] = translation

OUTPUT.write_text(
    "\n".join(f"{word} — {meaning}" for word, meaning in sorted(result.items()))
    + "\n",
    encoding="utf-8"
)

print(f"Input:   {len(lines)}")
print(f"Final:   {len(result)}")
print(f"Removed: {len(removed)}")
print(f"Saved:   {OUTPUT}")