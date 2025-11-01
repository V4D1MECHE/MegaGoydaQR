import requests
import json
import sys

# Проверка аргументов
if len(sys.argv) < 3:
    print("Использование: python3 qr_generator.py [url] [output.file]")
    sys.exit(1)

qr_data = sys.argv[1]
output_file = sys.argv[2]

# Конфигурация
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

# Параметры запроса
url = "https://api.qrcode-monkey.com/qr/custom"
params = {
    "download": "true",
    "file": "svg",
    "data": qr_data,
    "size": 1000,
    "config": json.dumps(config)
}

# Генерация QR кода
response = requests.get(url, params=params)

with open(output_file, "wb") as f:
    f.write(response.content)

print(f"QR код сохранен в {output_file}")
