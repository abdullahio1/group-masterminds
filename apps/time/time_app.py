from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import logging




app = Flask(__name__)



@app.route("/time", methods=["POST"])
def add_time():
    # JSON from Postman, calling a function in time_queries.py
    ...

if __name__ == "__main__":
    app.run(debug=True)