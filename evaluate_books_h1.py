import os
import re
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

SEG_ID_RE = re.compile(r'^(?:segment|section)-\d+', re.IGNORECASE)

def count_tags_in_epub(path):
    book = epub.read_epub(path, options={'ignore_missing_items': True})
    docs = book.get_items_of_type(ITEM_DOCUMENT)

    h1_total = 0
    literal_segment_total = 0
    section_total = 0
    id_based_total = 0

    for item in docs:
        html = item.get_content().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'lxml')

        h1_total += len(soup.find_all('h1'))
        literal_segment_total += len(soup.find_all('segment'))
        section_total += len(soup.find_all('section'))

        # any tag whose id looks like "segment-<n>" or "section-<n>"
        for tag in soup.find_all(attrs={"id": True}):
            if SEG_ID_RE.match(tag['id']):
                id_based_total += 1

    return h1_total, literal_segment_total, section_total, id_based_total

def main():
    inputs = "./input_files"
    out_csv = "tag_counts.csv"

    with open(out_csv, 'w', encoding='utf-8') as w:
        w.write("file,h1_count,literal_segment_count,section_count,id_matched_segment_or_section\n")

        for fn in os.listdir(inputs):
            if not fn.lower().endswith('.epub'):
                continue

            path = os.path.join(inputs, fn)
            try:
                h1c, segc, sec_c, idc = count_tags_in_epub(path)
                w.write(f"{fn},{h1c},{segc},{sec_c},{idc}\n")
                print(f"{fn}: h1={h1c}, <segment>={segc}, <section>={sec_c}, id-segments={idc}")
            except Exception as e:
                w.write(f"{fn},ERROR,ERROR,ERROR,ERROR\n")
                print(f"{fn}: ERROR ({e})")

if __name__ == '__main__':
    main()

