import datetime
import json
from pymongo import MongoClient
from django.utils.deprecation import MiddlewareMixin
from dotenv import load_dotenv
from decouple import config, Csv

load_dotenv()

# Set up MongoDB connection
client = MongoClient(config("MONGO_URL"))
db = client[config("MONGO_DB_NAME")]
logs_collection = db[config("MONGO_COLLECTION_NAME")]

class LogToMongoMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        log_entry = {
            "path": request.path,
            "method": request.method,
            "status_code": response.status_code,
            "timestamp": datetime.datetime.utcnow(),
            "user": request.session['user_name'],
            "body": request.body.decode('utf-8') if request.body else None,
        }
        logs_collection.insert_one(log_entry)
        return response