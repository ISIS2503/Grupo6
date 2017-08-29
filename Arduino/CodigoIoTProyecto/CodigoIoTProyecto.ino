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

//Audio pin definition
const int audioPin = A3;

//Audio variables defined
float audioIntensity = 0;
float db = 0;

//CO gas detector pin
const int analogCO2InPin = A0;  // Analog input pin that the potentiometer is attached to             


int sensorCO2Value = 0;        // value read from the sensor
float timeSpam;
int intSpam = 0;

//Atributo que modela si se está en un minuto par para el envío de información
boolean biMinute;

void setup() {
  //Inicialización del puerto serial para imprimir en monitor
  Serial.begin(9600);
  //Inicialización de la instancia del sensor de temperatura
  dht.begin();

  if (!tsl.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */

    //Serial.print("Ooops, no TSL2561 detected ... Check your wiring or I2C ADDR!");
    while (1);

  }
  /* Setup the sensor gain and integration time */
  configureSensor();

  biMinute = false;
}

void loop()
{
  timeSpam = millis();
  intSpam = 0;
  float t = 0;
  while (millis() - timeSpam < 14999) {

    t = (t * (intSpam++) + dht.readTemperature()) / intSpam;

  }
  Serial.print("T: ");
  Serial.print(t);
  Serial.println(" *C ");

  if (biMinute) {
    timeSpam = millis();
    intSpam = 0;
    double light = 0.0;

    while (millis() - timeSpam < 14999) {
      sensors_event_t event;
      tsl.getEvent(&event);

      if (event.light)
      {

        light = light * ((intSpam++) + event.light) / intSpam;

      }
      else
      {
        /* If event.light = 0 lux the sensor is probably saturated
           and no reliable data could be generated! */


        //Serial.println("Sensor overload");
      }

    }
    Serial.print("L: ");
    Serial.print(light);
    Serial.println(" lx");
  } else {
    delay(14999);
  }

  if (biMinute) {
    timeSpam = millis();
    intSpam = 0;
    double promedioRuido = 0;
    while (millis() - timeSpam < 14999) {

      float tt = millis();


      double min = 6;
      double max = -1;
      while (millis() - tt < 200) {

        audioIntensity = analogRead (audioPin) * (5.0 / 1023.0);

        if (audioIntensity > max) {
          max = audioIntensity;
        }
        else {
          if (audioIntensity < min) {
            min = audioIntensity;
          }
        }

      }
      db = 20 * log10((max - min) / (0.000031623));
      promedioRuido = (promedioRuido * (intSpam++) + db) / intSpam;

    }
    Serial.print("R: ");
    Serial.print(promedioRuido);
    Serial.println(" db");
  }else{
    delay(14999);
  }


  /*
    CO2 Sensor
  */
  timeSpam = millis();
  intSpam = 0;
  double promedioGas = 0;
  int ppm;
  while (millis() - timeSpam < 14999) {

    sensorCO2Value = analogRead(analogCO2InPin);
    ppm = map(sensorCO2Value, 0, 1023, 20, 20000); //Convierte datosAnalogos a PPM
    promedioGas = (promedioGas * (intSpam++) + db) / intSpam;
  }


  /*/ determine alarm status
    if (sensorValue >= 750)
    {
    digitalWrite(ledPin, HIGH);   // sets the LED on
    }
    else
    {
    digitalWrite(ledPin, LOW);    // sets the LED off
    }
  */
  // print the results to the serial monitor:
  Serial.print("G: " );
  Serial.print (promedioGas);
  Serial.println(" ppm \n");

  biMinute = !biMinute;

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
