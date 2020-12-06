import flask
import json
from flask import request, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
from database.db_connection import connection
from models.note import Note

class NoteController:
    def get_notes(self):
        if "id" in request.args:
            idNote = ObjectId(request.args["id"])
            note = connection().notes.find({ "_id": idNote })
            return jsonify(
                headers = { "Content-Type": "application/json" },
                statusCode = 200,
                data = json.loads(dumps(list(note))),
            )
        else:
            notes = connection().notes.find()
            return jsonify(
                headers = { "Content-Type": "application/json" },
                statusCode = 200,
                data = json.loads(dumps(list(notes))),
                count = notes.count()
            )
    
    def create(self, form):
        note = {
            "title": request.form.get("title"),
            "descrition": request.form.get("description")
        }
        result = connection().notes.insert_one(note)
        if result.inserted_id:
            note = connection().notes.find({ "_id": ObjectId(result.inserted_id) })
            return jsonify(
                headers = { "Content-Type": "application/json" },
                statusCode = 200,
                data = json.loads(dumps(list(note)))
            )
        else:
            return jsonify(
                statusCode = 500,
                error = {
                    "message": "Error creating new note! Try again later."
                }
            )

    def update(self):
        if "id" in request.args:
            idNote = ObjectId(request.args["id"])

            title = request.form.get("title")
            description = request.form.get("description")
            newData = {}
            if title is not None:
                newData["title"] = title
            if description is not None:
                newData["description"] = description
            result = connection().notes.update_one(
                { "_id": idNote },
                { "$set": newData },
                upsert = False
            )
            
            if result.modified_count > 0:
                note = connection().notes.find({ "_id": idNote })
                return jsonify(
                    headers = { "Content-Type": "application/json" },
                    statusCode = 200,
                    data = json.loads(dumps(list(note)))
                )
            else:
                return jsonify(
                    statusCode = 500,
                    error = {
                        "message": "Error updating note! Try again later."
                    }
                )
        else:
            return jsonify(
                statusCode = 400,
                error = {
                    message: "Error: No ID field provided. Please specify an id."
                }
            )

    def delete(self):
        if "id" in request.args:
            idNote = ObjectId(request.args["id"])
            result = connection().notes.delete_one({ "_id": idNote })
            notes = connection().notes.find()
            if result.deleted_count > 0:
                notes = connection().notes.find()
                return jsonify(
                    headers = { "Content-Type": "application/json" },
                    statusCode = 200,
                    data = json.loads(dumps(list(notes))),
                    count = notes.count()
                )
            else:
                return jsonify(
                    statusCode = 500,
                    error = {
                        "message": "Error deleting note! Try again later."
                    }
                )
        else:
            return jsonify(
                statusCode = 400,
                error = {
                    message: "Error: No ID field provided. Please specify an id."
                }
            )
