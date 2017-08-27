//Inclusión de librerías
#include "DHT.h"

//Definición de pines para los sensores
#define DHTPIN 2

//Definición de sensor de temperatura 
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup(){
  //Inicialización del puerto serial para imprimir en monitor
  Serial.begin(9600);
  //Inicialización de la instancia del sensor de temperatura
  dht.begin();
}

void loop()
{
  float t = dht.readTemperature();
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(" *C ");
}
