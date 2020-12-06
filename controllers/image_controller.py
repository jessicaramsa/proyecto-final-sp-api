import flask, json, os, hashlib

from flask import request, jsonify, current_app, url_for
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from database.db_connection import connection
from models.image import Image

class ImageController:
    def allowed_file(self, filename):
        return "." in filename and \
            filename.split(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

    def get_images(self):
        if "id" in request.args:
            idImg = ObjectId(request.args["id"])
            image = connection().images.find({ "_id": idImg })
            return jsonify(
                headers = { "Content-Type": "application/json" },
                statusCode = 200,
                data = json.loads(dumps(list(image))),
            )
        else:
            images = connection().images.find()
            return jsonify(
                headers = { "Content-Type": "application/json" },
                statusCode = 200,
                data = json.loads(dumps(list(images))),
                count = images.count()
            )
    
    def create(self, req):
        imageFile = request.files["file"]
        if "files" in req.files or imageFile.filename != "":
            if imageFile and self.allowed_file(imageFile.filename):
                filename = secure_filename(imageFile.filename)
                uploadFolder = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

                payload = { "url": uploadFolder, "filename": filename }
                result = connection().images.insert_one(payload)
                if result.inserted_id:
                    image = connection().images.find({ "_id": ObjectId(result.inserted_id) })
                    return jsonify(
                        headers = { "Content-Type": "application/json" },
                        statusCode = 200,
                        data = json.loads(dumps(list(image)))
                    )
                else:
                    return jsonify(
                        statusCode = 500,
                        error = {
                            "message": "Error saving file! Try again later."
                        }
                    )
            else:
                return jsonify(
                    statusCode = 400,
                    error = {
                        "message": "File not supported!"
                    }
                )
        else:
            return jsonify(
                statusCode = 400,
                error = {
                    "message": "Select at least one file!"
                }
            )

    def delete(self):
        if "id" in request.args:
            idImg = ObjectId(request.args["id"])
            result = connection().images.delete_one({ "_id": idImg })
            images = connection().images.find()
            if result.deleted_count > 0:
                images = connection().images.find()
                return jsonify(
                    headers = { "Content-Type": "application/json" },
                    statusCode = 200,
                    data = json.loads(dumps(list(images))),
                    count = images.count()
                )
            else:
                return jsonify(
                    statusCode = 500,
                    error = {
                        "message": "Error deleting image! Try again later."
                    }
                )
        else:
            return jsonify(
                statusCode = 400,
                error = {
                    message: "Error: No ID field provided. Please specify an id."
                }
            )
