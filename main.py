import flask
import json
from flask import request, jsonify, send_from_directory
from controllers.note_controller import NoteController
from controllers.image_controller import ImageController

app = flask.Flask(__name__)
app.config.from_pyfile("config/config_flask.py")

@app.route("/", methods=["GET"])
def home():
    return "API proyecto final - Sistemas Programables"

# Notes endpoints
@app.route("/api/notes", methods=["GET"])
def get_notes():
    return NoteController().get_notes()

@app.route("/api/notes", methods=["POST"])
def create_note():
    return NoteController().create(request.form)

@app.route("/api/notes", methods=["PATCH"])
def update_note():
    return NoteController().update()

@app.route("/api/notes", methods=["DELETE"])
def delete_note():
    return NoteController().delete()

# Images endpoints
@app.route("/api/images", methods=["GET"])
def get_images():
    return ImageController().get_images()

@app.route("/api/images", methods=["POST"])
def create_image():
    return ImageController().create(request)

@app.route("/api/images/uploads")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/api/images", methods=["DELETE"])
def delete_image():
    return ImageController().delete()

app.run()
