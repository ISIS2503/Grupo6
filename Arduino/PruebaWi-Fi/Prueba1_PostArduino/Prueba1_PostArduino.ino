#include <Bridge.h>
#include <Console.h>
#include <FileIO.h>
#include <HttpClient.h>
#include <Mailbox.h>
#include <Process.h>
#include <YunClient.h>
#include <YunServer.h>

#include <SPI.h>
//#include <Ethernet.h>


//byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress server(198,168,43,241); // 
//EthernetClient client;
YunClient client;

int temp = 64;

void setup()
{
  //Ethernet.begin(mac);
  Bridge.begin();
  Serial.begin(9600);
  String parametri ="";
  //delay(5000);
  //Serial.println("XXXXXXXXX");
  Serial.println("connecting...");
  delay(2500);
  Serial.println("connecting...");
  
  if (client.connect(server,80)) 
  {
    Serial.println("connected");
    delay(2500);
    parametri="rem_temp="+String(temp);
    
    client.println("POST /normal/rango HTTP/1.1");
    client.print("Content-length:");
    client.println(parametri.length());
    Serial.println(parametri.length());
    Serial.println(parametri);
    client.println("Connection: Close");
    client.println("Host:10.33.66.149");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.println();
    client.println(parametri);     //Set Remote temperture to ___
    //client.print(temp);
    //client.println("}");
  } 
    else 
    {
    Serial.println("connection failed");
    }
}
void loop()
{
  if (client.available()) {
    char c = client.read();
    Serial.print(c);  
  }
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
    for(;;)
  ;
  }
}
