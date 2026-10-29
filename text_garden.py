#!/usr/bin/env python3
"""A tiny offline Unicode text statistics CLI. No dependencies or network."""
import argparse,collections,json,pathlib,re,sys

def analyze(text):
    words=re.findall(r"[^\W_]+(?:['’][^\W_]+)*",text,re.UNICODE)
    return {'characters':len(text),'bytes_utf8':len(text.encode('utf-8')),'words':len(words),'lines':len(text.splitlines()),'unique_words':len(set(w.casefold() for w in words)),'top_words':[{'word':word,'count':count} for word,count in collections.Counter(w.casefold() for w in words).most_common(5)]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file',nargs='?',help='UTF-8 file; omit or use - for stdin');p.add_argument('--json',action='store_true',help='machine-readable output');args=p.parse_args(argv)
    try:
        if args.file and args.file!='-':
            with pathlib.Path(args.file).open(encoding='utf-8', newline='') as source:
                text=source.read()
        else:
            text=sys.stdin.read()
        result=analyze(text)
    except (OSError,UnicodeError) as e:print('text-garden: '+str(e),file=sys.stderr);return 2
    if args.json:print(json.dumps(result,ensure_ascii=False))
    else:
        for name in ['characters','bytes_utf8','words','lines','unique_words']:print(f'{name.replace("_"," "):15} {result[name]}')
        if result['top_words']:print('frequent words  '+', '.join(f'{x["word"]} ({x["count"]})' for x in result['top_words']))
    return 0
if __name__=='__main__':sys.exit(main())
