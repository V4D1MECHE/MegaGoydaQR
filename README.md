# MegaGoydaQR

qr code generator using qrcode-monkey api

## qr generator

basic qr code generation

```bash
python3 qr_generator.py [url] [output_file]
```

example:
```bash
python3 qr_generator.py "https://github.com" my_qr.svg
```

## sticker generator

creates fancy sticker with qr code, text and optional tag

```bash
python3 sticker.py [url] [text] [output_file]
python3 sticker.py [url] [text] [output_file] --tag [tag_text]
```

examples:
```bash
python3 sticker.py "https://github.com" "scan me" sticker.svg
python3 sticker.py "https://github.com" "check this out" sticker.svg --tag "new"
```

features:
- auto font sizing (120px to 64px)
- multiline text support
- optional tags with custom styling
- custom gilroy font
- branded tongue logo

## requirements

```bash
pip install requests
```


