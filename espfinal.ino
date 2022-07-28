#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h> 
#include <ESP8266HTTPClient.h>
#include<SoftwareSerial.h>
#include <SPI.h>
#include <MFRC522.h>
SoftwareSerial s(3,1);

//const char* ssid = "STUDBME2";
//const char* password = "BME2Stud";
const char* ssid = "Meirna";
const char* password = "123456789";
//const char* ssid = "8b7ddISP";
//const char* password = "19381940";
constexpr uint8_t RST_PIN = 0;    //D3 
constexpr uint8_t SS_PIN = 2;    //D4

MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;
String tag="";
String payload="";
char server=' ';
void connect_to_WiFi();


void setup () {
  s.begin(9600);
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init(); // Init MFRC522
  connect_to_WiFi();
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
}
 
/*void loop() {
 
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
            HTTPClient http;  //Declare an object of class HTTPClient
     http.begin("http://192.168.43.90/GetDirection/");  //Specify request destination
     int httpCode = http.GET();     //Send the request
     if (httpCode > 0) { //Check the returning code
       payload = http.getString(); //Get the request response payload
       s.write(payload[1]); //connection bet esp & arduino
       Serial.println(payload[1]); 
     
     delay(100);
     http.end(); }
       }
} */

void loop() {
  
if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

  HTTPClient http;  //Declare an object of class HTTPClient
  http.begin("http://192.168.43.90:8000/GetMode/"); //Specify request destination
  //http.begin("http://toto3.pythonanywhere.com/Get_Position/");  //Specify request destination
  //http.begin("http://172.28.128.46:8000/GetMode/");  //Specify request destination
  int httpCode = http.GET();                                                                  //Send the request
  if (httpCode > 0) { //Check the returning code
    payload = http.getString(); //Get the request response payload
    s.write(payload[1]);
    Serial.println(payload[1]);
    if (payload[1] == 'A' || payload[1]== 'M'){
      server = payload[1];
    }; 
    http.end();
  }

  
  if (server == 'M'){
        //Specify request destination
    if ( ! rfid.PICC_IsNewCardPresent()){
      http.begin("http://192.168.43.90:8000/GetDirection/");  //Specify request destination
      //http.begin("http://toto3.pythonanywhere.com/Get_Position/");  //Specify request destination
      int httpCode = http.GET();    //Send the request
      if (httpCode > 0) { //Check the returning code
      payload = http.getString(); //Get the request response payload
      s.write(payload[1]);
      Serial.println(payload[1]); 
      delay(100);   
      http.end();   //Close connection 
       }
    }

   if (rfid.PICC_ReadCardSerial()) {
      http.begin("http://192.168.43.90:8000/PostScannedNum/");
      for (byte i = 0; i < 4; i++) {
        tag += rfid.uid.uidByte[i];
      }
      Serial.println(tag);
      rfid.PICC_HaltA();
      rfid.PCD_StopCrypto1();
   
    http.addHeader("Content-Type", "application/json");
    String httpRequestData = "{\"id\":\"" + String(tag) + "\"}";           
    // Send HTTP POST request
    int httpResponseCode = http.POST(httpRequestData);
    tag = "";
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    delay(100);   
    http.end(); } 
 }
}
}
//scanning networks and conncting to one of them
void connect_to_WiFi() {
  
   WiFi.begin(ssid, password);
   Serial.println(); 
   Serial.println("connecting");
   
   while (WiFi.status() != WL_CONNECTED)
   {
    Serial.print("..");
    delay(500); 
   }
    Serial.println();
    Serial.print("connected to:");
    Serial.println(ssid);   
}
