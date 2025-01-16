from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, session
import os
from werkzeug.utils import secure_filename
import spill_vector
import uuid
import sqlite3
import secrets

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['AVATAR_FOLDER'] = 'static/avatars'
app.config['PREDICTIONS_FOLDER'] = 'static/predictions'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
db_file = 'users.db'

def init_db():
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT UNIQUE,
                        password TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        path TEXT,
                        title TEXT,
                        description TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS form_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        image_path TEXT,
                        title TEXT,
                        description TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')
        # Добавление столбца avatar, если он не существует
        c.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in c.fetchall()]
        if 'avatar' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN avatar TEXT")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return redirect(url_for('auth'))
@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/profile.html')
def profile_html():
    return redirect(url_for('profile.html'))

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/about.html')
def about_html():
    return redirect(url_for('about'))

@app.route('/problem')
def problem():
    return render_template('problem.html')
@app.route('/problem.html')
def problem_html():
    return redirect(url_for('problem'))

@app.route('/solutions')
def solutions():
    return render_template('solutions.html')
@app.route('/solutions.html')
def solutions_html():
    return redirect(url_for('solutions'))

@app.route('/gemini')
def gemini():
    return render_template('gemini.html')
@app.route('/gemini.html')
def gemini_html():
    return redirect(url_for('gemini'))

@app.route('/formpage')
def formpage():
    return render_template('formpage.html')
@app.route('/formpage.html')
def formpage_html():
    return redirect(url_for('formpage'))

@app.route('/visual')
def visual():
    image_path = request.args.get('image_path')
    if image_path is None:
        return "Image path is missing", 400
    return render_template('visual.html', image_path=image_path)
@app.route('/visual.html')
def visual_html():
    return redirect(url_for('visual'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return render_template('formpage.html', uploaded_image=filename)
                               
@app.route('/process_image', methods=['POST'])
def process_image():
    filename = request.form['filename']
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return "File not found", 404
    processed_image = spill_vector.predict_spread(filename)
    if processed_image is None:
        return jsonify(success=False, message="Не удалось найти подходящую область с чёрными пикселями."), 400
    unique_filename = f"{uuid.uuid4().hex[:8]}.jpeg"
    processed_image_path = os.path.join(app.config['PREDICTIONS_FOLDER'], unique_filename)
    with open(processed_image_path, 'wb') as f:
        f.write(processed_image.getvalue())
    return render_template('visual.html', image_path=processed_image_path)

@app.route('/static/predictions/', methods=['GET'])
def get_predictions():
    try:
        files = os.listdir(app.config['PREDICTIONS_FOLDER'])
        image_files = [
            url_for('static', filename=f'predictions/{file}')
            for file in files if allowed_file(file)
        ]
        return jsonify(image_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        with sqlite3.connect(db_file) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                return jsonify(success=True)
            else:
                return jsonify(success=False, message="Invalid credentials"), 401
    return render_template('auth.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            return jsonify(success=True)
        except sqlite3.IntegrityError:
            return jsonify(success=False, message="User already exists"), 400

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    user_id = session['user_id']
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute("SELECT name, email, avatar FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()
    return render_template('index.html', user=user)

@app.route('/index.html')
def index_html():
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return jsonify(success=False, message="User not logged in"), 401
    user_id = session['user_id']
    new_password = request.form.get('new_password')
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
        conn.commit()
    return jsonify(success=True)

@app.route('/get_form_history')
def get_form_history():
    if 'user_id' not in session:
        return jsonify(success=False, message="User not logged in"), 401
    user_id = session['user_id']
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute("SELECT id, image_path, title, description FROM form_history WHERE user_id = ?", (user_id,))
        history = c.fetchall()
    return jsonify([{'id': row[0], 'image_path': row[1], 'title': row[2], 'description': row[3]} for row in history])

@app.route('/add_form_history', methods=['POST'])
def add_form_history():
    if 'user_id' not in session:
        return jsonify(success=False, message="User not logged in"), 401
    user_id = session['user_id']
    data = request.json
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO form_history (user_id, image_path, title, description) VALUES (?, ?, ?, ?)",
                  (user_id, data['image_path'], data['title'], data['description']))
        conn.commit()
    return jsonify(success=True)

@app.route('/update_form_history', methods=['POST'])
def update_form_history():
    if 'user_id' not in session:
        return jsonify(success=False, message="User not logged in"), 401
    user_id = session['user_id']
    data = request.json
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute("UPDATE form_history SET title = ?, description = ? WHERE id = ? AND user_id = ?",
                  (data['title'], data['description'], data['id'], user_id))
        conn.commit()
    return jsonify(success=True)

@app.route('/delete_form_history', methods=['POST'])
def delete_form_history():
    if 'user_id' not in session:
        return jsonify(success=False, message="User not logged in"), 401
    user_id = session['user_id']
    data = request.json
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM form_history WHERE id = ? AND user_id = ?", (data['id'], user_id))
        conn.commit()
    return jsonify(success=True)

if __name__ == '__main__':
    init_db()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)