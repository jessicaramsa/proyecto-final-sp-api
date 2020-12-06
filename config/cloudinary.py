import os
import cloudinary as Cloud
from config.config_json import get_config

def config_cloudinary():
    cloudinary_config = get_config()["cloudinary"]
    cloud_name = cloudinary_config["cloud_name"]
    api_key = cloudinary_config["api_key"]
    api_secret = cloudinary_config["api_secret"]

    return {
        "cloud_name": os.environ.get("CLOUDINARY_CLOUD_NAME") or cloud_name,
        "api_key": os.environ.get("CLOUDINARY_API_KEY") or api_key,
        "api_secret": os.environ.get("CLOUDINARY_API_SECRET") or api_secret
    }
