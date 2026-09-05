import paho.mqtt.client as mqtt
from datetime import datetime
from db import sensor_collection

# Stable Public MQTT Broker Settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "coldchain/temp"  

# Connection callback function matching Paho-MQTT v2 specifications
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Successfully connected to HiveMQ Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Connection failed with code {rc}")

# Callback function when a new string message arrives from ESP32
def on_message(client, userdata, msg):
    try:
        # Decode incoming string from ESP32 (e.g., "25.5,60.0,NORMAL")
        data_string = msg.payload.decode('utf-8')
        print(f"Received raw data from ESP32: {data_string}")
        
        # Split string by comma to separate metrics
        data_parts = data_string.split(',')
        
        if len(data_parts) == 3:
            temp = float(data_parts[0])
            hum = float(data_parts[1])
            
            # 🟢 Dynamic Alert Decision Logic (Below 18°C or Above 30°C)
            if temp < 18.0 or temp > 30.0:
                status = "ALERT"
            else:
                status = "NORMAL"
            
            # Create a structured dictionary payload for MongoDB and React
            payload = {
                "temperature": temp,
                "humidity": hum,
                "status": status,
                "sensor_type": "DHT11",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save the record directly into MongoDB
            sensor_collection.insert_one(payload)
            print(f"[{status}] Successfully saved to MongoDB: {payload}")
            
    except Exception as e:
        print(f"Error parsing MQTT message: {e}")

# Creating MQTT Client instance using the new Callback API Version 2 standard
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("Starting MQTT Subscriber Client for ESP32 String Data...")
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"\n[ERROR] An issue occurred: {e}")
