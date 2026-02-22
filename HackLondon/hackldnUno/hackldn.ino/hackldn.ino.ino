#include <Arduino_RouterBridge.h>
#include <Arduino_Modulino.h>

ModulinoThermo thermo;

void setup() {
  Monitor.begin(9600);
  while (!Monitor); 
  Modulino.begin();
  thermo.begin();
}

void loop() {
  float temp = thermo.getTemperature();
  float humi = thermo.getHumidity();
  
  // This format MUST match the bridge
  Monitor.print("Temp: ");
  Monitor.print(temp);
  Monitor.print("°C | Humidity: ");
  Monitor.print(humi);
  Monitor.print("% | Light Level: ");
  Monitor.println(analogRead(A0)); // Assuming LDR is on A0

  delay(500); // Faster updates for the demo!
}