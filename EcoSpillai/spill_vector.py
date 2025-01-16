import os
import cv2
import numpy as np
import base64
import matplotlib
matplotlib.use('Agg')  # Устанавливает backend, не использующий Tkinter
from matplotlib import pyplot as plt
import io
from PIL import Image

def predict_spread(image_filename):
    def calculate_bgr_difference(pixel1, pixel2):
        return np.abs(int(pixel1[0]) - int(pixel2[0])) + np.abs(int(pixel1[1]) - int(pixel2[1])) + np.abs(int(pixel1[2]) - int(pixel2[2]))

    # Путь к изображению в папке uploads
    uploads_folder = 'static/uploads'
    image_path = os.path.join(uploads_folder, image_filename)

    if not os.path.exists(image_path):
        print(f"Изображение {image_filename} не найдено в папке {uploads_folder}.")
        return

    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    height, width = image.shape[:2]
    black_mask = cv2.inRange(image, (0, 0, 0), (50, 50, 50))
    contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best_candidate = None
    max_black_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_black_area:
            max_black_area = area
            best_candidate = contour

    if best_candidate is not None:
        moments = cv2.moments(best_candidate)
        if moments["m00"] != 0:
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])
        else:
            cX, cY = 0, 0

        min_distance = float('inf')
        closest_pixel = None
        for y in range(height):
            for x in range(width):
                if black_mask[y, x] == 255:
                    dist = np.sqrt((x - cX) ** 2 + (y - cY) ** 2)
                    if dist < min_distance:
                        min_distance = dist
                        closest_pixel = (x, y)

        if closest_pixel is not None:
            current_pixel = (cX, cY)
            image_with_arrow = image.copy()
            color = (0, 0, 255)
            thickness = 2
            prev_pixel = closest_pixel
            drawn_arrow = False
            max_arrow_length = 200
            arrow_length = 0

            for i in range(0, height, 10):
                for j in range(0, width, 10):
                    if black_mask[i, j] == 255:
                        diff = calculate_bgr_difference(image[prev_pixel[1], prev_pixel[0]], image[i, j])
                        if diff < 50:
                            arrow_length = np.sqrt((prev_pixel[0] - j) ** 2 + (prev_pixel[1] - i) ** 2)
                            if arrow_length > max_arrow_length:
                                scale_factor = max_arrow_length / arrow_length
                                j = int(prev_pixel[0] + (j - prev_pixel[0]) * scale_factor)
                                i = int(prev_pixel[1] + (i - prev_pixel[1]) * scale_factor)
                                arrow_length = max_arrow_length
                            image_with_arrow = cv2.arrowedLine(image_with_arrow, prev_pixel, (j, i), color, thickness)
                            prev_pixel = (j, i)
                            drawn_arrow = True
                            break
                if drawn_arrow:
                    break

            arrow_img_rgb = cv2.cvtColor(image_with_arrow, cv2.COLOR_BGR2RGB)
            _, arrow_img_encoded = cv2.imencode('.jpeg', arrow_img_rgb)
            arrow_img_pil = Image.open(io.BytesIO(arrow_img_encoded))
            img_byte_arr = io.BytesIO()
            arrow_img_pil.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            return img_byte_arr
        else:
            print("Не удалось найти ближайший чёрный пиксель.")
    else:
        print("Не удалось найти подходящую область с чёрными пикселями.")
