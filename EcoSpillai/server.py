from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Папка для хранения изображений
UPLOAD_FOLDER = 'Eco_project/uploads'
PROCESSED_FOLDER = 'Eco_project/uploads/processed_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Устанавливаем путь для загрузки
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Функция для проверки допустимых типов файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    
    # Если файл не выбран, возвращаем ошибку
    if file.filename == '':
        return 'No selected file'
    
    # Если файл подходит по типу, сохраняем его
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Здесь вы можете вызвать вашу модель для обработки изображения
        # Например, анализировать изображение и сохранить обработанный результат:
        processed_filename = 'processed_' + filename
        processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)

        # Пример обработки (замените на реальную обработку):
        # image = cv2.imread(filepath)
        # processed_image = model.predict(image)
        # cv2.imwrite(processed_filepath, processed_image)

        return redirect(url_for('visualization', filename=processed_filename))

    return 'Invalid file type. Only images are allowed.'

@app.route('/visualization/<filename>')
def visualization(filename):
    return render_template('visual.html', image_filename=filename)

if __name__ == '__main__':
    # Создаем папки, если их нет
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(PROCESSED_FOLDER):
        os.makedirs(PROCESSED_FOLDER)
    
    app.run(debug=True)
