#include "DHT.h"

//Definición de pines para los sensores
#define DHTPIN 7

//Definición del sensor de temperatura
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  /*Serial.begin(9600);
  dht.begin();*/
}

void loop() {
  /*float t = dht.readTemperature();
  //Serial.print("0 ");
  Serial.print(t);
  Serial.println(" *C ");
  delay(1000);*/
}

