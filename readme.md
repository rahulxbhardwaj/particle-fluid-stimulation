## Wiring and Setup for UDP Controlled Fluid Simulation

This section outlines the hardware requirements and wiring instructions to enable UDP control of the fluid simulation using an ESP32 and an MPU-6050 sensor.

### Hardware Requirements:

* ESP32 Dev Module (34 GPIO variant recommended)
* Jumper Wires
* Breadboard (Optional but highly recommended for easier connections)
* MPU-6050 Sensor (for accelerometer and gyroscope sensing - we will primarily use accelerometer data)

### Connections:

Connect the MPU-6050 sensor to the ESP32 development module as follows:

| MPU-6050 Pin | ESP32 Pin |
|--------------|-----------|
| VCC          | 3.3V      |
| GND          | GND       |
| SCL          | P26       |
| SDA          | P33       |

**Note:** Ensure secure and correct connections to avoid damaging your components. Refer to the datasheets for your specific ESP32 and MPU-6050 modules if needed.

### Changes in the Arduino (ESP32) Code File:

To enable the ESP32 to send sensor data to your Python simulation, you'll need to modify the Arduino code that will run on the ESP32.

1.  **Wi-Fi Credentials:**
    * Locate the section in your ESP32 code where Wi-Fi credentials are set.
    * Replace the placeholder SSID and password with your actual 2.4 GHz Wi-Fi network SSID and password. **Important:** ESP32 modules typically only support 2.4 GHz Wi-Fi networks.

    ```arduino
    const char* ssid = "YOUR_WIFI_SSID";
    const char* password = "YOUR_WIFI_PASSWORD";
    ```

2.  **Target IP Address:**
    * You need to specify the IP address of the computer running the Python fluid simulation.
    * Open your computer's command prompt or terminal and use the `ipconfig` command (on Windows) or `ifconfig` (on macOS/Linux) to find your computer's IPv4 address.
    * In your ESP32 code, find the line defining the UDP target address (it might be named `udpAddress` or similar).
    * Update the IP address within the double quotes to match the IPv4 address of your computer.

    ```arduino
    const char* udpAddress = "YOUR_COMPUTER_IPV4_ADDRESS"; // Example: "192.168.1.100"
    const int udpPort = 4210; // Ensure this port matches the Python script's UDP port
    ```

### Software Setup:

1.  **Install Required Libraries:**
    * **For the Python Simulation:** Ensure you have the necessary Python libraries installed. You can install them using pip:
        ```bash
        pip install pygame numpy numba
        ```
    * **For the ESP32 (Arduino IDE):** You will likely need to install libraries for Wi-Fi connectivity and interacting with the MPU-6050 sensor. In the Arduino IDE, go to `Sketch` -> `Include Library` -> `Manage Libraries...` and search for and install:
        * `WiFi` (usually built-in but ensure it's available)
        * `Adafruit MPU6050` or a similar MPU-6050 library (choose one based on your code)
        * `Adafruit Unified Sensor` (often a dependency for the MPU6050 libraries)

2.  **Upload ESP32 Code:** Compile and upload the Arduino code to your ESP32 development board using the Arduino IDE. Make sure you have selected the correct board and port in the IDE.

### Running the Simulation:

1.  **Power On Hardware:** Connect the ESP32 to a power source (e.g., via USB). Ensure the MPU-6050 sensor is also powered through its connection to the ESP32.
2.  **Open Python File:** Run the `fluid_sim.py` Python script on your computer.

The Python script will now listen for UDP packets sent by the ESP32 containing accelerometer data from the MPU-6050 sensor. As you move or tilt the MPU-6050, this data will be transmitted to your computer and used to influence the movement of the particles in the fluid simulation.