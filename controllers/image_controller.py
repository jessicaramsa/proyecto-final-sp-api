import flask, json, os, hashlib, requests

from flask import request, jsonify, current_app, url_for
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from database.db_connection import connection
from config.config_json import get_config
from config.cloudinary import config_cloudinary
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
            response = jsonify(
                headers = { "Content-Type": "application/json" },
                statusCode = 200,
                data = json.loads(dumps(list(images))),
                count = images.count()
            )
            response.headers.add("Access-Controll-Allow-Origin", "*")
            return response
    
    def upload_cloudinary(self, filename):
        cloud_name = get_config()["cloudinary"]["cloud_name"] or os.environ.get("CLOUDINARY_CLOUD_NAME")
        upload_preset = get_config()["cloudinary"]["upload_preset"] or os.environ.get("CLOUDINARY_UPLOAD_PRESET")
        api = get_config()["cloudinary"]["api"] or os.environ.get("CLOUDINARY_API")
        upload_url = f"{api}/{cloud_name}/image/upload"

        response = requests.post(
            upload_url,
            params={ "upload_preset": upload_preset },
            files={ "file": filename }
        )
        print(response.json())
        return response.json()["secure_url"]

    def create(self, req):
        imageFile = request.files["file"]
        if "files" in req.files or imageFile.filename != "":
            if imageFile and self.allowed_file(imageFile.filename):
                url = self.upload_cloudinary(imageFile)
                payload = { "url": url }

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
