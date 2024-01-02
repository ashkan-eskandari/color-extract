from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, IMAGES, configure_uploads, DOCUMENTS
from colorExtract import ExtractColors
import os, shutil

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "123123123123dasdasd"
app.config['UPLOADED_PHOTOS_DEST'] = "UPLOADS/photos"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
extract_colors = ExtractColors()


def empty(path):
    folder = f'UPLOADS/{path}'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@app.route('/', methods=["POST", "GET"])
def homepage():
    return render_template("index.html")

@app.route('/UPLOADS/photos/<filename>')
def get_photo(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == "POST":
        empty("photos")
        file = request.files['photo']
        extract_colors.reset_extract_colors()
        if file and allowed_file(file.filename):
            filename = photos.save(file)
            file_url = url_for("get_photo", filename=filename)
            img_path = f"UPLOADS/photos/{filename}"
            dominant_colors, counts = extract_colors.extract_dominant_colors(image_path=img_path)
            dominant_colors = dominant_colors.tolist()
            counts = counts.tolist()
            return jsonify({"colors": dominant_colors, "counts": counts, "file_url": file_url})
        else:
            return jsonify({"error": "Invalid file type. Please choose a valid image file."})


if __name__ == "__main__":
    app.run()