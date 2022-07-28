#include <SoftwareSerial.h>

int enA = 5;
int in1 = 7; 
int in2 = 17;
int enB = 6;
int in3 =18;
int in4 = 19;
int read1;
int read2;
float volt1;
float volt2;

const int VOL_PIN1 = 15; //5
const int VOL_PIN2 = 16; //4

const int trigPinL = 8;

const int echoPinL = 9;
const int trigPinR = 2;
const int echoPinR = 3;
long duration = 0;
int distance=0;
int distanceL=0;
int distanceR=0;
int sumRight=0;
int sumLeft=0;
float Distance(const int trigPin,const int echoPin);

char espData = '0';
char server =' ';
char Dir;
char readStringEsp();

void Forword();
void Backword();
void Left();
void Right();
void Stop();


void setup(){
Serial.begin(9600);
//espSerial.begin(115200);
 
pinMode(enA, OUTPUT);
pinMode(enB, OUTPUT);
pinMode(in1, OUTPUT);
pinMode(in2, OUTPUT);
pinMode(in3, OUTPUT);
pinMode(in4, OUTPUT);

pinMode(VOL_PIN1, INPUT);
pinMode(VOL_PIN2, INPUT);

pinMode(trigPinL, OUTPUT); 
pinMode(echoPinL, INPUT);
pinMode(trigPinR, OUTPUT); 
pinMode(echoPinR, INPUT);

}

void loop() {
  
espData = readStringEsp();
if (espData == 'A' || espData == 'M'){
  server = espData;
  }
else{
  Dir = espData;
  } 

while(server == 'M'){
  espData = readStringEsp();
  Serial.println(espData); 

 if (espData == 'A' || espData == 'M'){
    server = espData;
  }
  else{
    Dir = espData;
  }  
 // Serial.println("Manual");
  if(Dir == 's'){
   Serial.println("Stop");
   Stop();
   }
  else if(Dir == 'b'){
    Serial.println("back");
    Backword();
    }
  else if(Dir == 'f'){
    Serial.println("Forword");
    Forword();
    }
  else if(Dir == 'l'){
    Serial.println("Left");
    Left();
    }  
  else if(Dir == 'r'){
    Serial.println("Right");
    Right();
    }
 }  

while(server == 'A'){
  /*espData = readStringEsp();
  Serial.println(espData);
  
  if (espData == 'A' || espData == 'M'){
    server = espData;
  }
  else{
    Dir = espData;
  } */
 Serial.println("Automatic");
 while ( espData != 'M' )
 {
read1 = analogRead( VOL_PIN1 );
read1 = analogRead( VOL_PIN2 );
volt1 = read1 * 5.0 / 1023.0;
volt2 = read2 * 5.0 / 1023.0;
Serial.println(volt1);
Serial.println(volt2);

if ((volt1 >3) && (volt2 >3)){
//  digitalWrite(7,HIGH);
      Stop();
      Forword();
     // delay(50);
      delay(250);
      Stop();      
    }
 else if ((volt1 >3) && (volt2 <3)){
//      digitalWrite(7,HIGH);  
      Stop(); 
      Right();
      delay(250);
      Stop();   
    }
 else if ((volt2 >3) && (volt1 <3)){
//      digitalWrite(7,LOW);
     // Right();
     // delay(250);
      Stop();
    }
 else if ((volt1 <3) && (volt2 <3)){
//      digitalWrite(7,LOW);
       Stop();
       Left();
      delay(250);
      // delay(50);
      Stop();
    }
 else {
        analogWrite(enA, 0);
        analogWrite(enB, 0); }


  distanceR =Distance(trigPinR,echoPinR);
  Serial.println(distanceR);
  distanceL = Distance(trigPinL,echoPinL);
  Serial.println(distanceL);
  
  if((distanceR <20)&&(distanceL > 20) && (distanceR != 0)&&(distanceL != 0)){
    Serial.println("Right Object");
    Left();
    delay(300);
    Forword();
    delay(400);
    Stop();
    
    }
  else if((distanceR >20)&&(distanceL < 20) && (distanceR != 0)&&(distanceL != 0)){
    Serial.println("Left Object");
    Right();
    delay(300);
    Forword();
    delay(400);
    Stop();
    }
    //delay(3000)  
 
   } 
}
}

void Forword(){

  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);  
  digitalWrite(in3, LOW);
  digitalWrite(in4,HIGH); 
  analogWrite(enA, 130);
  analogWrite(enB, 100);  

  }
  
void Backword(){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);  
  digitalWrite(in3, HIGH);  
  digitalWrite(in4, LOW)  ; 
  analogWrite(enA, 100);
  analogWrite(enB, 100);
 //analogWrite(enA, 130);
  //analogWrite(enB, 215);
}
void Left(){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);  
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH); 
  analogWrite(enA, 0);
  analogWrite(enB, 130);
 /* analogWrite(enA, 130);
  analogWrite(enB, 215);
  digitalWrite(in1,HIGH);*/
  //Stop();
  }
void Right(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);  
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW); 
  analogWrite(enA, 130);
  analogWrite(enB, 0);
  delay(30);
  }  
void Stop(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);  
  digitalWrite(in3, LOW);  
  digitalWrite(in4, LOW); 
  analogWrite(enA, 0);
  analogWrite(enB, 0); 
  }

 char readStringEsp() {
  char dataRecieved ;
  char chBuffer;
  while (Serial.available() > 0) {
    chBuffer =  (char) Serial.read();
    dataRecieved = chBuffer;
    //Serial.println(dataRecieved);
    return dataRecieved;
   }  
   }

 float Distance(const int trigPin,const int echoPin){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance= duration*0.034/2;
  return distance;
  }
