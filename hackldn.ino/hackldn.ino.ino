#include <Arduino_RouterBridge.h>
#include <Arduino_Modulino.h>

// Pin for the Photoresistor
const int lightPin = A0; 

// Modulino Object
ModulinoThermo thermo;

void setup() {
  // Uno Q Bridge initialization
  Monitor.begin(9600);
  while (!Monitor); 
  
  Monitor.println("Uno Q: Climate & Light Monitor Starting...");

  // Start Modulino hardware
  Modulino.begin();
  thermo.begin();

  // No setup needed for A0, it is an input by default
  Monitor.println("---------------------------------------");
}

void loop() {
  // 1. Get Modulino Data (Temp & Humidity)
  float tempC = thermo.getTemperature();
  float humidity = thermo.getHumidity();

  // 2. Get Light Data
  // analogRead returns a value from 0 (dark) to 1023 (very bright)
  int lightLevel = analogRead(lightPin);

  // 3. Print the results to the Monitor
  Monitor.print("Temp: ");
  Monitor.print(tempC);
  Monitor.print("C | ");

  Monitor.print("Humidity: ");
  Monitor.print(humidity);
  Monitor.print("% | ");

  Monitor.print("Light Level: ");
  Monitor.println(lightLevel);

  // Update every second
  delay(1000);
}
