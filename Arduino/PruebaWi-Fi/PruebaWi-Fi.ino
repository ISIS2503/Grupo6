#include <Bridge.h>
#include <Console.h>
#include <FileIO.h>
#include <HttpClient.h>
#include <Mailbox.h>
#include <Process.h>
#include <YunClient.h>
#include <YunServer.h>

#include <SPI.h>
//char server[] = "192,168,43,254"; // IMPORTANT: If you are using XAMPP you will have to find out the IP address of your computer and put it here (it is explained in previous article). If you have a web page, enter its address (ie. "www.yourwebpage.com")
IPAddress server(157,253,210,190);
//IPAddress ip(192,168,43,254);
YunClient client;

void setup() {

  // Serial.begin starts the serial connection between computer and Arduino
  Serial.begin(9600);
  Bridge.begin();
  Serial.println("Inicio");

}

void loop() {
  if (client.connect(server, 80))
  {
    Serial.println("connected");
    String valor = "{\n\t\"data\": 10,\n\t\"unit\": C,\n\t\"place\": \"AREA 1\"\n}";
    client.println("POST /valor HTTP/1.1");
    // client.print("Content-length:");
    // client.println(sensorvalue1.length());
    //  client.println(sensorvalue2.length());
    //  Serial.println(sensorvalue2.length());
    // Serial.println(sensorvalue2);

    client.println("Connection: close" );
    client.println("Host: 157.253.210.190" );//ur web server
    client.println("Content-Type: application/json");
    String cont = "Content-Length: ";
    cont += sizeof(valor);
    client.println(cont);
    client.println();
    client.println(valor);
    //  client.get("localhost/insert.php?sensor1=20&&sensor2=21");
  }
  else
  {
    Serial.println("connection failed");
  }
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
    delay(10000);
  }
}
