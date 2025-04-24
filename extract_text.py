import os
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

def extract_text_from_item(item):
    html = item.get_content().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    if body:
        raw = body.get_text(separator=' ')
        return ' '.join(raw.split())
    return ''

def main(epub_path):
    output_path = 'output.txt'
    book = epub.read_epub(epub_path, options={'ignore_ncx': True})
    with open(output_path, 'w', encoding='utf-8') as out:
        for item in book.get_items_of_type(ITEM_DOCUMENT):
            text = extract_text_from_item(item)
            if text:
                out.write(text + '\n\n')
    print('Extracted content saved to', output_path)

if __name__ == '__main__':
    epub_path = 'input.epub'
    main(epub_path)

