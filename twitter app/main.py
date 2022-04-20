import datetime
from flask import Flask, render_template
from google.cloud import datastore

app = Flask(__name__)

datastore_client = datastore.Client()

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
    store_time(datetime.datetime.now())
    times = fetch_times(5)
    print(list(times))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)