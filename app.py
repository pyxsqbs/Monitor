from pymongo import MongoClient
from flask import Flask, session, redirect, url_for, escape, request
import json
import re

app = Flask(__name__)

conn = MongoClient('0.0.0.0', 27017)
db = conn.test
monitor = db.monitor


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        args = request.args
        print args
        username = args.get('username')
        user_bubble = args.get('user_bubble')
        robot_bubble = args.get('robot_bubble')
        session_id = args.get('session_id')
        score = args.get('score')
        start_time = args.get('startTime')
        end_time = args.get('endTime')
        fuzzy = args.get('fuzzy')

        select_list = []
        query = {}

        if not fuzzy:
            if username:
                query[u'username'] = username
            if user_bubble:
                query[u'user_bubble'] = user_bubble
            if robot_bubble:
                query[u'robot_bubble'] = robot_bubble
            if session_id:
                query[u'session_id'] = session_id
        else:
            if username:
                query[u'username'] = re.compile(username)
            if user_bubble:
                query[u'user_bubble'] = re.compile(user_bubble)
            if robot_bubble:
                query[u'robot_bubble'] = re.compile(robot_bubble)
            if session_id:
                query[u'session_id'] = re.compile(session_id)

        if start_time or end_time:
            query[u'timestamp'] = {
                '$gte': int(start_time),
                '$lte': int(end_time),
            }

        print query
        for i in monitor.find(query):
            del i['_id']
            select_list.append(i)

        result = {"result": select_list}
        print json.dumps(result)
        return json.dumps(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088)
