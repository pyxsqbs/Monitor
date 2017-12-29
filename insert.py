from pymongo import MongoClient
import time

conn = MongoClient('0.0.0.0', 27017)
db = conn.test
monitor = db.monitor

for i in range(1, 50):
    data = {
        'session_id': str(i),
        'username': chr(i + 50),
        'timestamp': int(time.time() * 1000),
        'robot_bubble': 'robot_%s' % chr(i + 50),
        'user_bubble': 'user_%s' % chr(i + 50),
    }
    print data
    monitor.insert(data)
