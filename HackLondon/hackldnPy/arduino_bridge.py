import serial
import requests
import time

# Update to your COM port
ser = serial.Serial('COM7', 9600, timeout=1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"DEBUG: {line}") # This helps you see if the Arduino is actually talking

        if "Temp:" in line and "Humidity:" in line:
            try:
                # Extract values using split
                t = line.split("Temp: ")[1].split("°C")[0]
                h = line.split("Humidity: ")[1].split("%")[0]
                l = line.split("Light Level: ")[1]

                # Send to Flask
                requests.post("http://127.0.0.1:5000/update", json={
                    "temperature": t,
                    "humidity": h,
                    "light": l
                })
            except:
                pass
    time.sleep(0.1)