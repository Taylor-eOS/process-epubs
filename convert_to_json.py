import json

INPUT_FILE = 'input.txt'
OUTPUT_FILE = 'output.json'

def main():
    with open(INPUT_FILE) as f:
        lines = [l.rstrip('\n') for l in f]
    segments = []
    segment = []
    for line in lines:
        if line.strip() == '':
            if segment:
                segments.append(segment)
                segment = []
        else:
            segment.append(line)
    if segment:
        segments.append(segment)
    with open(OUTPUT_FILE,'w') as f:
        for seg in segments:
            for idx,line in enumerate(seg):
                label = 'h1' if idx == 0 and len(line) < 80 else 'p'
                f.write(json.dumps({'label': label, 'text': line}, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()

