//Inclusión de librerías
#include "DHT.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>

//Definición de pines para los sensores
#define DHTPIN 7

//Definición del sensor de temperatura
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

//Definición del sensor de luminosidad
Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);

const int audioPin = A3;

float audioIntensity = 0;
float db=0;

void setup() {
  //Inicialización del puerto serial para imprimir en monitor
  Serial.begin(9600);
  //Inicialización de la instancia del sensor de temperatura
  dht.begin();

  if (!tsl.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.print("Ooops, no TSL2561 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }
  /* Setup the sensor gain and integration time */
  configureSensor();

}

void loop()
{
  float t = dht.readTemperature();
  //Serial.print("Temperature: ");
  //Serial.print(t);
  //Serial.print(" *C ");
  //Serial.println("");

  sensors_event_t event;
  tsl.getEvent(&event);
  if (event.light)
  {
    //Serial.print("Luminosidad: ");
    //Serial.print(event.light); Serial.println(" lux");
  }
  else
  {
    /* If event.light = 0 lux the sensor is probably saturated
       and no reliable data could be generated! */
    //Serial.println("Sensor overload");
  }
 // audioIntensity = analogRead (audioPin) * (5.0 / 1023.0);
  float tt=millis();
 // double promedio=0;
//int i =0;
double min=6;
double max=-1;
  while(millis()-tt<200){
    
    audioIntensity = analogRead (audioPin) * (5.0 / 1023.0);
    //promedio=(promedio*(i++)+audioIntensity)/i;
    if(audioIntensity>max){
      max=audioIntensity;
    }
    else{
      if(audioIntensity<min){
        min=audioIntensity;
      }
    }
    
  }
  db=20*log10((max-min)/(0.000031623));
  //Serial.print("Ruido: ");
  Serial.println(max);
  Serial.println(min);
  Serial.print("DB: ");
  Serial.println(db);
  
  //delay(200);
}

//Método que configura el sensor de iluminación
void configureSensor(void)
{
  /* You can also manually set the gain or enable auto-gain support */
  // tsl.setGain(TSL2561_GAIN_1X);      /* No gain ... use in bright light to avoid sensor saturation */
  // tsl.setGain(TSL2561_GAIN_16X);     /* 16x gain ... use in low light to boost sensitivity */
  tsl.enableAutoRange(true);            /* Auto-gain ... switches automatically between 1x and 16x */

  /* Changing the integration time gives you better sensor resolution (402ms = 16-bit data) */
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);      /* fast but low resolution */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_101MS);  /* medium resolution and speed   */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_402MS);  /* 16-bit data but slowest conversions */
}
