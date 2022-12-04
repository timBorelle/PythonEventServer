#!/usr/bin/env python
import os

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongo:27017")

# Add event
# args : start, stop (optional) and tags
@app.route('/add_event', methods = ['POST'])
def add_event():
    start = request.args.get('start', None)
    stop = request.args.get('stop', None)
    tags = request.args.get('tags', None)
    if start is None:
        return jsonify({'success': False, 'message': 'Your event can\'t be added. It needs start argument.'})
    if tags is None:
        return jsonify({'success': False, 'message': 'Your event can\'t be added. It needs tags argument.'}) 
    elif tags:
        tags = tags.split(",")

    data = {"start": start, "stop": stop, "tags": tags}
    db = client["local"]
    col = db["events"]
    try:
        x = col.insert_one(data)
    except:
        return jsonify({'success': False, 'message': 'Your event can\'t be inserted into MongoDB.'})  
    return jsonify({'success': True, 'message': 'Your event has been added', 'event': str(data)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
