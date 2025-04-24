import os
import re
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

def count_tags_and_words(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    tags = soup.find_all()
    body = soup.find('body')
    text = body.get_text(separator=' ') if body else soup.get_text(separator=' ')
    words = re.findall(r'\w+', text)
    return len(tags), len(words)

def score_epub(epub_path):
    try:
        book = epub.read_epub(epub_path)
    except Exception as e:
        print(f"Error reading {os.path.basename(epub_path)}: {e}")
        return None
    total_tags = 0
    total_words = 0
    doc_items = list(book.get_items_of_type(ITEM_DOCUMENT))
    if len(doc_items) <= 1:
        return None
    for item in doc_items[1:]:
        try:
            html = item.get_content().decode('utf-8')
        except Exception as e:
            print(f"Error decoding {item.file_name}: {e}")
            continue
        tags, words = count_tags_and_words(html)
        total_tags += tags
        total_words += words
    if total_words == 0:
        return None
    return (total_tags / total_words) * 100

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

