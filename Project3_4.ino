#include "SR04.h"
#include <Servo.h>

#define TRIG_PIN 2
#define ECHO_PIN 3
#define RED 4
#define BUZZER 5
#define SERVO 6
long duration, distance;

SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
Servo myservo;
int camera = 0;
int turnOnCamera = 1;
int turnOffCamera = 0;
int i = 0;
void setup() {
  Serial.begin(9600);
  
  pinMode(RED, OUTPUT); 
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER,OUTPUT);
  myservo.attach(SERVO);
  myservo.write(90);
   
}

void loop() {
  distance=sr04.Distance();
  delay(100);
  byte a;
  if(distance<30){
    if(camera != turnOnCamera){
      Serial.println(turnOnCamera);
      camera = 1;
    }
    digitalWrite(BUZZER,HIGH);
    digitalWrite(RED, HIGH);
  }
  else{
    if(camera != turnOffCamera){
      Serial.println(turnOffCamera);
      camera = 0;
    }
    digitalWrite(BUZZER,LOW);
    digitalWrite(RED, LOW);

  }
  if(Serial.available() >0 ){   
    int angle = Serial.parseInt();
    Serial.println(angle);
    if(angle > 15){
      
      myservo.write(angle);
    }
    
  }
}
