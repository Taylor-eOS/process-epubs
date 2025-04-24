import os
import re
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup, NavigableString, Tag
import pysbd

def extract_text_with_tag_markers(soup):
    output = []

    def recurse(node):
        if isinstance(node, NavigableString):
            output.append(str(node))
        elif isinstance(node, Tag):
            output.append(' [[TAG]] ')
            for child in node.children:
                recurse(child)
            output.append(' [[TAG]] ')

    body = soup.find('body')
    recurse(body if body else soup)
    return ''.join(output)

def count_tag_interruptions(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    marked_text = extract_text_with_tag_markers(soup)
    segmenter = pysbd.Segmenter(language="en", clean=False)
    sentences = segmenter.segment(marked_text)
    if False and len(sentences) > 10:
        print(f"{sentences[6]}\n")
    interruptions = 0
    for sentence in sentences:
        interruptions += sentence.count('[[TAG]]')
    return interruptions, len(sentences)

def score_epub(epub_path):
    try:
        book = read_epub(epub_path, options={'ignore_missing_items': True})
    except Exception as e:
        print(f"Error reading {os.path.basename(epub_path)}: {e}")
        return None
    total_interrupts = 0
    total_sentences = 0
    doc_items = list(book.get_items_of_type(ITEM_DOCUMENT))
    if len(doc_items) <= 1:
        return None
    for item in doc_items[1:]:
        try:
            html = item.get_content().decode('utf-8')
        except Exception as e:
            print(f"Error decoding {item.file_name}: {e}")
            continue
        interrupts, sentences = count_tag_interruptions(html)
        total_interrupts += interrupts
        total_sentences += sentences
    if total_sentences == 0:
        return None
    return (total_interrupts / total_sentences) * 100

def main():
    input_dir = "./input_files"
    log_path = "log.txt"
    epub_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.epub')]
    with open(log_path, 'w', encoding='utf-8') as log:
        for fname in epub_files:
            fpath = os.path.join(input_dir, fname)
            score = score_epub(fpath)
            file_basename = os.path.splitext(os.path.basename(fname))[0]
            if score is not None:
                log.write(f"{file_basename};{score:.2f}\n")
                print(f"Processed {file_basename}: score = {score:.2f}")
            else:
                log.write(f"{file_basename};ERROR\n")
                print(f"Could not compute score for {file_basename}.")
    print(f"Evaluation complete. Results written to {log_path}")

if __name__ == "__main__":
    main()

