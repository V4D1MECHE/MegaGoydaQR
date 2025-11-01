import requests
import json
import sys
import base64
import os

# Проверка аргументов
if len(sys.argv) < 4:
    print("Использование: python3 sticker.py [url] [text] [output.svg]")
    sys.exit(1)

qr_url = sys.argv[1]
sticker_text = sys.argv[2]
output_file = sys.argv[3]

# Загрузка и кодирование шрифта Gilroy
font_path = os.path.join(os.path.dirname(__file__), "Gilroy", "Gilroy-Bold.ttf")
with open(font_path, "rb") as f:
    font_base64 = base64.b64encode(f.read()).decode()

# Загрузка и кодирование язычка (tongue.svg)
tongue_path = os.path.join(os.path.dirname(__file__), "tongue.svg")
with open(tongue_path, "rb") as f:
    tongue_base64 = base64.b64encode(f.read()).decode()

# Функция для разбивки текста на строки
def split_text_to_lines(text, font_size, max_width=320):
    words = text.split()
    lines = []
    current_line = []

    # Примерная ширина символа для Gilroy Bold (~0.65 от размера шрифта)
    avg_char_width = font_size * 0.65

    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width = len(test_line) * avg_char_width

        if test_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Если одно слово не влезает, всё равно добавляем его
                lines.append(word)

    if current_line:
        lines.append(' '.join(current_line))

    return lines

# Функция для автоматического уменьшения размера шрифта и разбивки на строки
def calculate_font_size_and_lines(text, max_width=320, max_font_size=120, min_font_size=64):
    font_size = max_font_size
    # Примерная ширина символа для Gilroy Bold (~0.65 от размера шрифта)
    avg_char_width = font_size * 0.65
    text_width = len(text) * avg_char_width

    if text_width > max_width:
        font_size = int((max_width / len(text)) / 0.65)
        font_size = max(font_size, min_font_size)

    # Проверяем, нужно ли разбивать на строки
    final_width = len(text) * (font_size * 0.65)
    if final_width > max_width:
        # Разбиваем на строки с минимальным размером шрифта
        lines = split_text_to_lines(text, min_font_size, max_width)
        return min_font_size, lines
    else:
        return font_size, [text]

# Конфигурация QR кода
config = {
    "body": "circular",
    "eye": "frame13",
    "eyeBall": "ball15",
    "erf1": [],
    "erf2": [],
    "erf3": [],
    "brf1": [],
    "brf2": [],
    "brf3": [],
    "bodyColor": "#000000",
    "bgColor": "transparent",
    "eye1Color": "#000000",
    "eye2Color": "#000000",
    "eye3Color": "#000000",
    "eyeBall1Color": "#7c95e8",
    "eyeBall2Color": "#7c95e8",
    "eyeBall3Color": "#7c95e8",
    "gradientColor1": "",
    "gradientColor2": "",
    "gradientType": "linear",
    "gradientOnEyes": False,
    "logo": "",
    "logoMode": "default"
}

# Генерация QR кода
api_url = "https://api.qrcode-monkey.com/qr/custom"
params = {
    "download": "true",
    "file": "svg",
    "data": qr_url,
    "size": 800,
    "config": json.dumps(config)
}

response = requests.get(api_url, params=params)
qr_svg_content = response.text
qr_base64 = base64.b64encode(qr_svg_content.encode()).decode()

# Параметры наклейки
sticker_width = 424
side_padding = 52
top_padding = 64
bottom_padding = 52
text_top_padding = 32
text_bottom_padding = 16
text_block_to_line_padding = 48
line_to_qr_padding = 48
tongue_height = 56
tongue_width = 303  # оригинальная ширина tongue.svg

qr_size = sticker_width - (side_padding * 2)  # 320px

# Вычисляем размер шрифта и разбиваем текст на строки
font_size, text_lines = calculate_font_size_and_lines(sticker_text)
num_lines = len(text_lines)

# Высота текстового блока (с учетом количества строк)
text_block_height = font_size * num_lines

# Высота белого фона
white_bg_height = top_padding + text_top_padding + text_block_height + text_bottom_padding + text_block_to_line_padding + line_to_qr_padding + qr_size + bottom_padding

# Автоматическая высота (белый фон + язычок)
sticker_height = white_bg_height + tongue_height

# Позиции элементов
text_y = top_padding + text_top_padding  # верх текста (с dominant-baseline="hanging")
text_block_end = text_y + text_block_height + text_bottom_padding  # конец текстового блока
line_y = text_block_end + text_block_to_line_padding  # линия после отступа
qr_y = line_y + line_to_qr_padding
qr_x = side_padding

# Позиция язычка (по центру, сразу после белого фона)
tongue_x = (sticker_width - tongue_width) / 2
tongue_y = white_bg_height

# Координаты линии (от края до края с учетом отступов)
line_x1 = side_padding
line_x2 = sticker_width - side_padding

# Генерация текстовых строк для SVG
if num_lines == 1:
    text_svg = f'  <text x="50%" y="{text_y}" text-anchor="middle" dominant-baseline="hanging"\n        font-family="Gilroy" font-size="{font_size}px" font-weight="bold" fill="black">\n    {text_lines[0]}\n  </text>'
else:
    tspan_lines = []
    for i, line in enumerate(text_lines):
        if i == 0:
            tspan_lines.append(f'    <tspan x="50%" dy="0">{line}</tspan>')
        else:
            tspan_lines.append(f'    <tspan x="50%" dy="{font_size}">{line}</tspan>')

    text_svg = f'  <text x="50%" y="{text_y}" text-anchor="middle" dominant-baseline="hanging"\n        font-family="Gilroy" font-size="{font_size}px" font-weight="bold" fill="black">\n' + '\n'.join(tspan_lines) + '\n  </text>'

# Создание SVG вручную
svg_content = f'''<svg width="{sticker_width}" height="{sticker_height}" viewBox="0 0 {sticker_width} {sticker_height}"
     fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <style>
      @font-face {{
        font-family: 'Gilroy';
        src: url(data:font/truetype;charset=utf-8;base64,{font_base64}) format('truetype');
        font-weight: bold;
      }}
    </style>
  </defs>

  <!-- Фон со скругленными углами (только белая часть) -->
  <rect width="{sticker_width}" height="{white_bg_height}" rx="64" fill="white"/>

  <!-- Текст сверху -->
{text_svg}

  <!-- Разделительная линия -->
  <line x1="{line_x1}" y1="{line_y}" x2="{line_x2}" y2="{line_y}" stroke="#E6E6E6" stroke-width="2"/>

  <!-- QR код -->
  <image x="{qr_x}" y="{qr_y}" width="{qr_size}" height="{qr_size}"
         xlink:href="data:image/svg+xml;base64,{qr_base64}"/>

  <!-- Язычок с логотипом -->
  <image x="{tongue_x}" y="{tongue_y}" width="{tongue_width}" height="{tongue_height}"
         xlink:href="data:image/svg+xml;base64,{tongue_base64}"/>
</svg>'''

# Сохранение файла
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f"Наклейка сохранена в {output_file}")
