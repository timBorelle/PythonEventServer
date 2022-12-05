#!/usr/bin/env python
import os

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongo:27017")
db = client["local"]
col = db["events"]


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
    try:
        x = col.insert_one(data)
    except:
        return jsonify({'success': False, 'message': 'Your event can\'t be inserted into MongoDB.'})  
    return jsonify({'success': True, 'message': 'Your event has been added', 'event': str(data)})

# List events
# no args
@app.route('/list_events', methods = ['GET'])
def list_events():
    data = []
    try:
        for x in col.find():
            data.append(str(x))
        return jsonify({'success': True, 'data': data})
    except:
        return jsonify({'success': False, 'message': 'You can\'t get all events from MongoDB.'})

# Remove all events
# no args
@app.route('/remove_events', methods = ['GET'])
def remove_events():
    try:
        x = col.delete_many({})
    except:
        return jsonify({'success': False, 'message': 'Failed to delete all documents inside events MongoDB collection.'})
    if x.deleted_count == 0:
        SuccessResult = False
    else:
        SuccessResult = True
    return jsonify({'success': SuccessResult, 'message': str(x.deleted_count)+" documents deleted."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
