import datetime
from google.cloud import datastore
import google.oauth2.id_token
from flask import Flask, render_template, request
from google.auth.transport import requests


app = Flask(__name__)

datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

def store_time(dt):
    entity = datastore.Entity(key = datastore_client.key('visit'))
    entity.update({'timestamp' : dt})
    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']
    times = query.fetch(limit=limit)
    return times





@app.route('/')
def root():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token,
            firebase_request_adapter)
        except ValueError as exc:
            error_message = str(exc)
    store_time(datetime.datetime.now())
    times = list(fetch_times(10))
    return render_template('index.html', user_data=claims, times=times, 
                           error_message=error_message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)