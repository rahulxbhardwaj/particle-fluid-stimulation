#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <WiFi.h>
#include <WiFiUdp.h>

// Custom I2C Pins
#define SDA_PIN 33
#define SCL_PIN 26

// Wi-Fi credentials
const char* ssid = "PutYourSSIDHere";
const char* password = "putYourPasswordHere";
// Replace with your laptop's IP
// Make sure to use the correct IP address of your laptop
// and ensure that the laptop is connected to the same network as the ESP32
// and that the firewall allows incoming UDP packets on the specified port.
const char* udpAddress = "192.168.0.197";  // Replace with your laptop's IP
const int udpPort = 4210;

WiFiUDP udp;
Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);

  // Start I2C with custom pins
  Wire.begin(SDA_PIN, SCL_PIN);

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) { delay(10); }
  }
  Serial.println("MPU6050 Found!");

  // Wi-Fi connection
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nWi-Fi Connected");
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Prepare data string
  String data = String(a.acceleration.x) + "," +
                String(a.acceleration.y) + "," +
                String(a.acceleration.z) + "," +
                String(g.gyro.x) + "," +
                String(g.gyro.y) + "," +
                String(g.gyro.z);

  // Send via UDP
  udp.beginPacket(udpAddress, udpPort);
  udp.print(data);
  udp.endPacket();

  Serial.println(data);
  delay(50);  // ~20 packets/sec
}
