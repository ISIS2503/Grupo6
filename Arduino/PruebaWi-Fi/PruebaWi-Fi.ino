#include <PubSubClient.h>

#include "DHT.h"
#include <YunClient.h>
#include <Console.h>

YunClient yunClient;
PubSubClient client(yunClient);
//IPAddress ip(157, 253, 204, 104);
IPAddress server(157,253,204,104);

//Definición de pines para los sensores
#define DHTPIN 7

//Definición del sensor de temperatura
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

float temp;
long idSensor;
String topics[8] = {"normal.rango1", "normal.rango2", "normal.rango3", "normal.rango4", "normal.rango5", "normal.rango6", "normal.rango7", "normal.rango8"};

void setup()
{
  Serial.begin(9600);
  Serial.print("1");
  Bridge.begin();
  Serial.print("2");
  client.setServer(server, 8083);
  Serial.print("3");
  client.setCallback(callback);
  Serial.print("4");
  dht.begin();
  Serial.print("5");
  idSensor = 0;
  Serial.print("6");
  Serial.println("Camilo MK");
  String message = "{ \"data\":" + String(temp) + ", \"unit\":\"*C\", \"idSensor\":" + String(idSensor) + "}";
  Serial.print("7");
  char buff[2000];
  Serial.print("8");
  message.toCharArray(buff, 2000);
  Serial.print("9");
  Serial.println(buff);
  Serial.print("10");
  //delay(1500);
}

void loop()
{
  Serial.println("Camilo MK");
  if (!client.connected()) {
    reconnect();
  } else {
    temp = dht.readTemperature();
    String message = "{ \"data\":" + String(temp) + ", \"unit\":\"*C\", \"idSensor\":" + String(idSensor) + "}";
    char buff[2000];
    message.toCharArray(buff, 2000);
    String topic = topics[0];
    char buffTopic[2000];
    topic.toCharArray(buffTopic, 2000);
    client.publish(buffTopic, buffTopic);
  }
  //client.loop();
  //delay(1000);
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("arduinoClient")) {

      Serial.println("connected");
      // Once connected, publish an announcement...
      temp = dht.readTemperature();
      String message = "{ \"data\":" + String(temp) + ", \"unit\":\"*C\", \"idSensor\":" + String(idSensor) + "}";
      char buff[2000];
      message.toCharArray(buff, 2000);
      String topic = topics[0];
      char buffTopic[2000];
      topic.toCharArray(buffTopic, 2000);
      client.publish(buffTopic, buffTopic);
      // ... and resubscribe
      //client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(1000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) { }
