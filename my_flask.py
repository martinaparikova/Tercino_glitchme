from flask import Flask, redirect, request, render_template, url_for, flash, send_file
from data_transform_terka import create_csv

UPLOAD_FOLDER = 'upload'

app = Flask(__name__, static_folder='static')
app.secret_key = "super secret key"


@app.route("/")
def front_page():
    return render_template('fileform.html')


@app.route("/handleUpload", methods=['POST'])
def file_upload():
    if 'file_zadatele' in request.files:
        file_zadatele = request.files['file_zadatele']
        if file_zadatele.filename != '':
            new_filename_zadatele = str(file_zadatele.filename).replace('xlsx', 'csv').replace('xls', 'csv')
            new_file_path = UPLOAD_FOLDER + '/' + new_filename_zadatele
            create_csv(file_zadatele, new_file_path, 'zadatele')
            # flash(F'Dobre ty! CSV s nazvem {new_filename_zadatele} se ted stahuje do tve Downloads slozky')
            return send_file(new_file_path, as_attachment=True)
        else:
            flash('Nemas vybranej soubor!')
    elif 'file_projekty' in request.files:
        file_projekty = request.files['file_projekty']
        if file_projekty.filename != '':
            new_filename_projekty = str(file_projekty.filename).replace('xlsx', 'csv').replace('xls', 'csv')
            new_file_path = UPLOAD_FOLDER + '/' + new_filename_projekty
            create_csv(file_projekty, new_file_path, 'projekty')
            # flash(F'Dobre ty! CSV s nazvem {new_filename_zadatele} se ted stahuje do tve Downloads slozky')
            return send_file(new_file_path, as_attachment=True)
        else:
            flash('Nemas vybranej soubor!')
    return redirect(url_for('front_page'))


if __name__ == "__main__":
    app.run(debug=True)
