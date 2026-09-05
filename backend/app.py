from flask import Flask, jsonify
from flask_cors import CORS
from db import sensor_collection

app = Flask(__name__)
# CORS लगाना ज़रूरी है ताकि रिएक्ट ऐप (Port 3000) बिना किसी सिक्योरिटी एरर के Flask (Port 5000) से डेटा ले सके
CORS(app)

# एंडपॉइंट 1: सबसे नया (Latest) डेटा लेने के लिए
@app.route('/latest', methods=['GET'])
def get_latest_data():
    try:
        # डेटाबेस से सबसे आखिरी एंट्री निकालना (_id को हटाकर क्योंकि वह JSON में एरर देता है)
        latest_record = sensor_collection.find_one({}, sort=[('_id', -1)], projection={'_id': 0})
        if latest_record:
            return jsonify(latest_record), 200
        else:
            return jsonify({"temperature": 0, "humidity": 0, "status": "NO_DATA", "sensor_type": "DHT11"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# एंडपॉइंट 2: पुराना सारा डेटा (History) देखने के लिए
@app.route('/data', methods=['GET'])
def get_all_history():
    try:
        
        records = list(sensor_collection.find({}, projection={'_id': 0}).sort('_id', -1).limit(50))
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Flask Server is running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
