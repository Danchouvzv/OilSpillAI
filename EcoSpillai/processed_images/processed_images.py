import os

PROCESSED_FOLDER = 'uploads/processed_images/'  # Папка для сохранения обработанных изображений

# Проверка существования папки и её создание, если не существует
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)
