from flask import Flask, render_template, request, jsonify
import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app = Flask(__name__)

class ProjectStructure:
    def __init__(self):
        self.structure = []
        self.current_path = []  # Menyimpan folder/folder yang sedang aktif

    def add_folder(self, folder_name):
        """ Menambahkan folder ke struktur """
        folder_path = os.path.join(*self.current_path, folder_name)
        self.structure.append(folder_path)

    def add_file(self, file_name):
        """ Menambahkan file ke struktur """
        file_path = os.path.join(*self.current_path, file_name)
        self.structure.append(file_path)

    def display_structure(self):
        """ Menampilkan struktur dengan format garis vertikal dan sambungan """
        structure_str = ""
        for item in self.structure:
            indent_level = item.count(os.sep)  # Menghitung level indentasi berdasarkan folder
            folder_or_file = item.replace(os.sep, '---').strip()

            # Menampilkan folder/file dengan emoji
            if '.' in folder_or_file:
                structure_str += ' ' * indent_level * 2 + f'  ├── {folder_or_file} 📄\n'
            else:
                structure_str += ' ' * indent_level * 2 + f'  ├── {folder_or_file} 📁\n'

        return structure_str

    def navigate_folder(self, folder_name):
        """ Masuk ke folder """
        self.current_path.append(folder_name)

    def exit_folder(self):
        """ Keluar dari folder """
        if self.current_path:
            self.current_path.pop()

project = ProjectStructure()

@app.route('/')
def index():
    return render_template('index.html', structure=project.display_structure())

@app.route('/add_folder', methods=['POST'])
def add_folder():
    folder_name = request.form['folder_name']
    project.add_folder(folder_name)
    return jsonify({
        'structure': project.display_structure(),
        'message': f'Folder "{folder_name}" telah ditambahkan.'
    })

@app.route('/add_file', methods=['POST'])
def add_file():
    file_name = request.form['file_name']
    project.add_file(file_name)
    return jsonify({
        'structure': project.display_structure(),
        'message': f'File "{file_name}" telah ditambahkan.'
    })

@app.route('/navigate', methods=['POST'])
def navigate():
    folder_name = request.form['folder_name']
    project.navigate_folder(folder_name)
    return jsonify({
        'structure': project.display_structure(),
        'message': f'Anda telah masuk ke folder: {folder_name}.'
    })

@app.route('/exit', methods=['POST'])
def exit_folder():
    project.exit_folder()
    return jsonify({
        'structure': project.display_structure(),
        'message': 'Anda telah keluar dari folder saat ini.'
    })

@app.route('/done', methods=['POST'])
def done():
    # Anda dapat menambahkan logika untuk menandai struktur selesai
    return jsonify({
        'message': 'Struktur proyek selesai!',
        'structure': project.display_structure()
    })

# Serverless handler
def handler(event, context):
    with app.app_context():
        return DispatcherMiddleware(app.wsgi_app, {
            '/.netlify/functions/flask_app': app
        })

if __name__ == "__main__":
    run_simple('localhost', 5000, app)
