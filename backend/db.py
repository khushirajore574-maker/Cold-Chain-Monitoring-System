from pymongo import MongoClient

# MongoDB लोकल सर्वर से कनेक्शन स्थापित करना
# यह डिफ़ॉल्ट पोर्ट 27017 पर कनेक्ट होता है
client = MongoClient("mongodb://localhost:27017/")

# डेटाबेस का नाम सेट करें
db = client["cold_chain_db"]

# कलेक्शन (Table) का नाम जहां सेंसर का डेटा सेव होगा
sensor_collection = db["readings"]

print("MongoDB connection initialized inside db.py")
