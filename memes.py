import os
from collections import namedtuple
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from flask import send_from_directory
from werkzeug.middleware.shared_data import SharedDataMiddleware
from meme_site.module_database import db_app_connection as db_conn

Message = namedtuple('Message', 'user text meme')
messages = []
user = '@dDmIn4iK2007_XD'

working_dir = str(os.path.dirname(__file__))
folder = '/img'
full_path = working_dir + folder
# UPLOAD_FOLDER = r'C:\Users\lynnk\OneDrive\Рабочий стол\Домашка\memes\img'  # сюда полный путь к папке для картинок
UPLOAD_FOLDER = full_path  # сюда полный путь к папке для картинок
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    messages.clear()
    data = db_conn.get_db('module_database/database.db')
    if data is None:
        return redirect('/make_post')
    for post_id in data:
        text = data[post_id][2]
        meme = data[post_id][3]
        messages.append(Message(user, text, meme))
    return render_template('index.html', messages=messages)


@app.route('/make_post', methods=['GET', 'POST'])
def make_post():
    return render_template('make_post.html', messages=messages)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_post', methods=['GET', 'POST'])
def add_message():
    if request.method == 'POST':
        if 'meme' not in request.files:
            flash('No file part')
            return redirect(request.url)

        meme = request.files['meme']

        if meme.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if meme and allowed_file(meme.filename):
            filename = secure_filename(meme.filename)
            meme.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        text = request.form['text']
        # messages.append(Message(user, text, filename))

        db_conn.push_post('module_database/database.db', 'posts', user, text, meme.filename)

        data = db_conn.get_last_row('module_database/database.db')
        for post_id in data:
            text = data[post_id][2]
            meme = data[post_id][3]
            messages.append(Message(user, text, meme))

    # return render_template('index.html', messages=messages)
    return redirect('/')


@app.route('/img/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


app.add_url_rule('/img/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/':  app.config['UPLOAD_FOLDER']
})


if __name__ == '__main__':
    app.run(debug=True)


# print(os.path.dirname())
# print(os.path.dirname(__file__))
# print(os.path.dirname(os.path.realpath(__file__)))

