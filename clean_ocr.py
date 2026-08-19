from pathlib import Path


INPUT_FILE = Path("Netzwerk B1 Neu_OCR.txt")
OUTPUT_FILE = Path("Netzwerk B1 Neu_clean.txt")


def fix_mojibake(text):
    """
    Repair UTF-8 text that was incorrectly decoded as Latin-1/Windows-1252.
    """

    for _ in range(3):
        try:
            fixed = text.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            break

        # Only accept the conversion if it actually improves the text.
        bad_chars_before = text.count("Ã") + text.count("Â") + text.count("â")
        bad_chars_after = fixed.count("Ã") + fixed.count("Â") + fixed.count("â")

        if bad_chars_after < bad_chars_before:
            text = fixed
        else:
            break

    return text


text = INPUT_FILE.read_text(encoding="utf-8")

cleaned_text = fix_mojibake(text)

OUTPUT_FILE.write_text(
    cleaned_text,
    encoding="utf-8"
)

print("Cleaning complete.")
print(f"Output: {OUTPUT_FILE}")