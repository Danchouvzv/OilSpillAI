import os

UPLOAD_FOLDER = 'uploads/'  # Папка, где будут храниться изображения

# Проверяем, существует ли папка, если нет — создаем
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
