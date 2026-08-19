import pymupdf

pdf_path = r"D:\coding\german_b1\Goethe_german_b1\Netzwerk B1 Neu.pdf"

pdf = pymupdf.open(pdf_path)

print("Total pages:", len(pdf))
print()

text_pages = 0
image_pages = 0

for page_number, page in enumerate(pdf, start=1):

    text = page.get_text().strip()
    images = page.get_images(full=True)

    if text:
        text_pages += 1

    if images:
        image_pages += 1

    print(
        f"Page {page_number}: "
        f"{len(text):6} text chars | "
        f"{len(images):2} images"
    )

print()
print("Pages with text:", text_pages)
print("Pages with images:", image_pages)

pdf.close()