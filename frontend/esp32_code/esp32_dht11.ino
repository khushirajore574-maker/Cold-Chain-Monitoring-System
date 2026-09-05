#include <WiFi.h>
#include <DHT.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ⚠️ यहाँ अपने घर या मोबाइल हॉटस्पॉट का नाम और पासवर्ड बदलें
#define WIFI_SSID "YOUR_WIFI_NAME"       
#define WIFI_PASSWORD "YOUR_PASSWORD"   

// Highly stable, alternative public broker updated
#define MQTT_SERVER "test.mosquitto.org"   
#define MQTT_PORT 1883
#define MQTT_TOPIC "coldchain/dht11"

#define DHTPIN 23       // DHT11 Pin connected to GPIO 23 of ESP32
#define DHTTYPE DHT11
#define BUZZER_PIN 22   // Buzzer positive pin connected to GPIO 22

DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  pinMode(BUZZER_PIN, OUTPUT);
  dht.begin();
  
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) { 
    delay(500); 
    Serial.print("."); 
  }
  Serial.println("\nWi-Fi Connected successfully!");
  
  client.setServer(MQTT_SERVER, MQTT_PORT);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32_ColdChain_Node_99")) {
      Serial.println("connected to Mosquitto Broker");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  String status = "NORMAL";
  if (t < 18 || t > 30) {
    status = "ALERT";
    digitalWrite(BUZZER_PIN, HIGH); // Buzzer ON
  } else {
    status = "NORMAL";
    digitalWrite(BUZZER_PIN, LOW);  // Buzzer OFF
  }

  StaticJsonDocument<200> doc;
  doc["temperature"] = t;
  doc["humidity"] = h;
  doc["status"] = status;
  doc["sensor_type"] = "DHT11";

  char msgBuffer;
  serializeJson(doc, msgBuffer);
  
  client.publish(MQTT_TOPIC, msgBuffer);
  Serial.print("Data Published: "); 
  Serial.println(msgBuffer);

  delay(2000); 
}
