# Text Garden

Text Garden is a small, dependency-free command-line tool for exploring text without sending it anywhere. It counts Unicode characters, UTF-8 bytes, lines, words, unique words, and the five most frequent words.

## Use

Analyze a UTF-8 file:

```sh
python3 text_garden.py document.txt
```

Read from standard input and return JSON:

```sh
printf 'one two two\n' | python3 text_garden.py --json
```

Use `-` as the file argument to read standard input explicitly. File input preserves line endings: CRLF counts as two characters and bytes, and one line break. Empty input has zero lines. Invalid UTF-8 and file errors are reported with exit status 2.

## Tests

```sh
python3 -m unittest discover -s . -v
```

Created by Wobblebyte, an AI software agent, as part of the Little Perhaps project.
