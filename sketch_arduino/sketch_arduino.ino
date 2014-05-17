#include <TinkerKit.h>

TKLightSensor ldr(I0);
TKThermistor therm(I1);  // Dichiaro i sensori
	 
int C; // Misura in Celsius

void setup() {
  // Setto comunicazione a 9600 bps
  Serial.begin(9600);
}

void loop() {
  // Salvo i dati del sensore di luminosità in luce
  int luce = ldr.read();            
  // Salvo i valori della temperatura con C               
  C = therm.readCelsius();     
  
  Serial.print(C);
  Serial.print(brightnessVal);
  Serial.print("\n"); // Per utilizzare il readline() in Python

  delay(100);     // Delay per la prossima misurazione           
}
