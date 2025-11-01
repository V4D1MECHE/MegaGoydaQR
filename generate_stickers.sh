#!/bin/bash

# Генерация трех стикеров с разными данными

python3 sticker.py "https://github.com" "GitHub Repository" sticker1.svg --tag "code"

python3 sticker.py "https://example.com" "Check this out" sticker2.svg

python3 sticker.py "https://google.com" "Search Engine" sticker3.svg --tag "popular"

echo "All stickers generated!"
