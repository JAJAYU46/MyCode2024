String command;

#define LEDPin_L 7
#define LEDPin_R 8
#define leftMotorPin1  5   //左正
#define leftMotorPin2  6   //左負
#define rightMotorPin1  10  //右負
#define rightMotorPin2  11  //右正
#define VacuumRelayPin 13
#define LEDPin 12

#include "MoveFunction.h"
#include "UltraSensor.h"

#define trigPinR A0    // 超音波感測器 Trig腳接 Arduino pin 11
#define echoPinR A1    //超音波感測器 Echo 腳接 Arduino pin 12
#define trigPinF A2 
#define echoPinF A3 
#define trigPinRB A4 
#define echoPinRB A5 

// int speakerpin = 7;  //蜂鳴器 + 腳接 Arduino pin 7
// long duration, cm ;  //宣告計算距離時，需要用到的兩個實數
double distanceR, distanceF, distanceRB;


void setup() {
  Serial.begin(9600);
  pinMode(LEDPin_L, OUTPUT);
  pinMode(LEDPin_R, OUTPUT);
  // 將馬達控制引腳設置為輸出
  pinMode(leftMotorPin1, OUTPUT);
  pinMode(leftMotorPin2, OUTPUT);
  pinMode(rightMotorPin1, OUTPUT);
  pinMode(rightMotorPin2, OUTPUT);
  pinMode(VacuumRelayPin, OUTPUT);
  // digitalWrite(LEDPin_L, HIGH);
  // digitalWrite(LEDPin_R, HIGH);
  // delay(2000);
  // digitalWrite(LEDPin_L, LOW);
  // digitalWrite(LEDPin_R, LOW);

  //超音波感測器
  pinMode(trigPinR, OUTPUT);      //Arduino 對外啟動距離感測器Trig腳，射出超音波 
  pinMode(echoPinR, INPUT);       //超音波被障礙物反射後，Arduino讀取感測器Echo腳的時間差
  // pinMode(speakerpin, OUTPUT);   //Arduino對蜂鳴器送出電壓，使其鳴叫

  pinMode(trigPinF, OUTPUT);      //Arduino 對外啟動距離感測器Trig腳，射出超音波 
  pinMode(echoPinF, INPUT);       //超音波被障礙物反射後，Arduino讀取感測器Echo腳的時間差
  // pinMode(speakerpin, OUTPUT);   //Arduino對蜂鳴器送出電壓，使其鳴叫
 
  pinMode(trigPinRB, OUTPUT);      //Arduino 對外啟動距離感測器Trig腳，射出超音波 
  pinMode(echoPinRB, INPUT);  
  //Serial.println("Type Command (white, blue, red, all, off)");
  // Frontward();
  // delay(3000);
  // BigTurnRight();
  // delay(2000);  
  // Stop();
  // delay(500);  
}

bool FrontTurnflag = false;
void loop() {
  // Frontward();
  // TurnRight();
  // Serial.println("Type Command (white, blue, red, all, off)");

  // //現在由arduino 控制向右走了
  // distanceR = getDistance(trigPinR, echoPinR);
  // distanceF = getDistance(trigPinF, echoPinF);
  // distanceRB = getDistance(trigPinRB, echoPinRB);
  // Frontward();
  // // if (distanceF < 30) {
  // //     // Backward();
  // //     // delay(1200);
  // //     BigTurnLeft();
  // //     // delay(1000);
  // // }
  
  // //distanceR-distanceRB


  // // while(distanceF>90 && distanceR>60){
  // //   // Frontward();
  // //   // delay(600)
  // //   distanceR = getDistance(trigPinR, echoPinR);
  // //   distanceF = getDistance(trigPinF, echoPinF);
  // //   TurnRight(0, 250, 0, 200);
  // // }



  // while(distanceR<13){// && distanceF > 30){//15// && distanceF<10){ //如果右邊太近了，就一直左轉直到沒有這麼近 //但還是要繼續收有沒有要停下vacuum的資料
  //   distanceR = getDistance(trigPinR, echoPinR);
  //   distanceF = getDistance(trigPinF, echoPinF);
  //   // TurnLeft(0, 200, 0, 250);
  //   BigTurnLeft();
  //   if (distanceF < 15) {
  //     Backward();
  //     delay(500);
  //     BigTurnLeft();
  //     delay(500);
  //   }
  //   if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
  //     command = Serial.readStringUntil('\n');
  //     if (command.equals("VacuumOn")) {
  //     digitalWrite(VacuumRelayPin, HIGH);
  //     }else if (command.equals("VacuumOff")) {
  //     digitalWrite(VacuumRelayPin, LOW);
  //     }
  //   }
  //   // Serial.println();
    
  // }
  

  // if(distanceF<20 ){
  //   // while(distanceF<20||distanceR>distanceRB+2 ||distanceR>18){
  //   while(distanceF<20||distanceR>distanceRB ||distanceR>18){
  //     distanceR = getDistance(trigPinR, echoPinR);
  //     distanceF = getDistance(trigPinF, echoPinF);
  //     distanceRB = getDistance(trigPinRB, echoPinRB);

  //     BigTurnLeft();
      
  //   }
  // }
  
  // while(distanceR<13){// && distanceF > 30){//15// && distanceF<10){ //如果右邊太近了，就一直左轉直到沒有這麼近 //但還是要繼續收有沒有要停下vacuum的資料
  //   distanceR = getDistance(trigPinR, echoPinR);
  //   distanceF = getDistance(trigPinF, echoPinF);
  //   // TurnLeft(0, 200, 0, 250);
  //   BigTurnLeft();
  //   if (distanceF < 15) {
  //     Backward();
  //     delay(500);
  //     BigTurnLeft();
  //     delay(500);
  //   }
  //   if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
  //     command = Serial.readStringUntil('\n');
  //     if (command.equals("VacuumOn")) {
  //     digitalWrite(VacuumRelayPin, HIGH);
  //     }else if (command.equals("VacuumOff")) {
  //     digitalWrite(VacuumRelayPin, LOW);
  //     }
  //   }
  //   // Serial.println();
    
  // }
  

  // // while(distanceR<13 && distanceF > 30){//15// && distanceF<10){ //如果右邊太近了，就一直左轉直到沒有這麼近 //但還是要繼續收有沒有要停下vacuum的資料
  // //   distanceR = getDistance(trigPinR, echoPinR);
  // //   distanceF = getDistance(trigPinF, echoPinF);
  // //   // TurnLeft(0, 200, 0, 250);
  // //   BigTurnLeft();
  // //   // if (distanceF < 15) {
  // //   //   Backward();
  // //   //   delay(500);
  // //   //   BigTurnLeft();
  // //   //   delay(500);
  // //   // }
  // //   if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
  // //     command = Serial.readStringUntil('\n');
  // //     if (command.equals("VacuumOn")) {
  // //     digitalWrite(VacuumRelayPin, HIGH);
  // //     }else if (command.equals("VacuumOff")) {
  // //     digitalWrite(VacuumRelayPin, LOW);
  // //     }
  // //   }
  // //   // Serial.println();
    
  // // }
  // // while(distanceR>18 && distanceF > 30){//20// && distanceF>20){ //如果右邊太近了，就一直左轉直到沒有這麼近 //但還是要繼續收有沒有要停下vacuum的資料
  // //   // TurnLeft(0, 200, 0, 250);
  // //   distanceR = getDistance(trigPinR, echoPinR);
  // //   BigTurnRight();
  // //   if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
  // //     command = Serial.readStringUntil('\n');
  // //     if (command.equals("VacuumOn")) {
  // //     digitalWrite(VacuumRelayPin, HIGH);
  // //     }else if (command.equals("VacuumOff")) {
  // //     digitalWrite(VacuumRelayPin, LOW);
  // //     }
  // //   }
    
  // // }
  // // if (distanceF < 30 ){
  // //   FrontTurnflag = true;    
  // // }
  // // while(FrontTurnflag == true){//20// && distanceF>20){ //如果右邊太近了，就一直左轉直到沒有這麼近 //但還是要繼續收有沒有要停下vacuum的資料
  // //   // TurnLeft(0, 200, 0, 250);
  // //   distanceR = getDistance(trigPinR, echoPinR);
  // //   distanceF = getDistance(trigPinF, echoPinF);
  // //   BigTurnLeft();
  // //   if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
  // //     command = Serial.readStringUntil('\n');
  // //     if (command.equals("VacuumOn")) {
  // //     digitalWrite(VacuumRelayPin, HIGH);
  // //     }else if (command.equals("VacuumOff")) {
  // //     digitalWrite(VacuumRelayPin, LOW);
  // //     }
  // //   }
  // //   if (distanceF>200){
  // //     FrontTurnflag=false;
  // //     Serial.println("Now distanceF: ");
  // //     Serial.println(distanceF);

  // //   }
  // //   Serial.println("distanceF: ");
  // //   Serial.println(distanceF);
  // // }

  // // while(distanceR<13 && distanceF > 30){//15// && distanceF<10){ //如果右邊太近了，就一直左轉直到沒有這麼近 //但還是要繼續收有沒有要停下vacuum的資料
  // //   distanceR = getDistance(trigPinR, echoPinR);
  // //   distanceF = getDistance(trigPinF, echoPinF);
  // //   // TurnLeft(0, 200, 0, 250);
  // //   BigTurnLeft();
  // //   // if (distanceF < 15) {
  // //   //   Backward();
  // //   //   delay(500);
  // //   //   BigTurnLeft();
  // //   //   delay(500);
  // //   // }
  // //   if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
  // //     command = Serial.readStringUntil('\n');
  // //     if (command.equals("VacuumOn")) {
  // //     digitalWrite(VacuumRelayPin, HIGH);
  // //     }else if (command.equals("VacuumOff")) {
  // //     digitalWrite(VacuumRelayPin, LOW);
  // //     }
  // //   }
  // //   // Serial.println();
    
  // // }
  

  // // while(distanceR>18 && distanceF > 30){//20// && distanceF>20){ //如果右邊太近了，就一直左轉直到沒有這麼近 //但還是要繼續收有沒有要停下vacuum的資料
  // //   // TurnLeft(0, 200, 0, 250);
  // //   distanceR = getDistance(trigPinR, echoPinR);
  // //   distanceF = getDistance(trigPinF, echoPinF);
  // //   BigTurnRight();
  // //   if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
  // //     command = Serial.readStringUntil('\n');
  // //     if (command.equals("VacuumOn")) {
  // //     digitalWrite(VacuumRelayPin, HIGH);
  // //     }else if (command.equals("VacuumOff")) {
  // //     digitalWrite(VacuumRelayPin, LOW);
  // //     }
  // //   }
    
  // // }


  // while(distanceF>90 && distanceR>60){
  //   Frontward();
  //   delay(600);
  //   distanceR = getDistance(trigPinR, echoPinR);
  //   distanceF = getDistance(trigPinF, echoPinF);
  //   TurnRight(0, 250, 0, 200);
  // }

  // while(distanceR>18){// && distanceF>15){// && distanceF > 30){//20// && distanceF>20){ //如果右邊太近了，就一直左轉直到沒有這麼近 //但還是要繼續收有沒有要停下vacuum的資料
  //   // TurnLeft(0, 200, 0, 250);
  //   distanceR = getDistance(trigPinR, echoPinR);
  //   distanceF = getDistance(trigPinF, echoPinF);

  //   if(distanceF>150 && distanceR>100){
  //     // TurnRight(0, 250, 0, 200)
  //     Frontward();
  //     delay(50);//50 //100
  //     // TurnRight(0, 250, 0, 200);
      
  //     TurnRight(0, 250, 0, 50);
  //     // BigTurnRight();
  //     delay(50);//50
  //   }else{
      
  //     BigTurnRight();
  //   }
    
  //   // 
  //   if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
  //     command = Serial.readStringUntil('\n');
  //     if (command.equals("VacuumOn")) {
  //     digitalWrite(VacuumRelayPin, HIGH);
  //     }else if (command.equals("VacuumOff")) {
  //     digitalWrite(VacuumRelayPin, LOW);
  //     }
  //   }
    
  // }


  if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
    command = Serial.readStringUntil('\n');
    command.trim();
    if (command.equals("Left")) {
      // TurnLeft(0, 200, 0, 250);
      TurnLeft();
      //turn right
    }else if (command.equals("Right")) {
      // TurnRight(0, 250, 0, 100);
      TurnRight();
    }else if (command.equals("Front")) {
      Frontward();
    }else if (command.equals("Back")) {
      Backward();
    }else if (command.equals("Stop")) {
      Stop();
    }else if (command.equals("VacuumOn")) {
      digitalWrite(VacuumRelayPin, HIGH);
    }else if (command.equals("VacuumOff")) {
      digitalWrite(VacuumRelayPin, LOW);
    }else if (command.equals("BigLeft")) {
      Backward();
      delay(500);
      BigTurnLeft();
    }else if (command.equals("BigRight")) {
      BigTurnRight();
    }
    Serial.print("Command: ");
    Serial.println(command);
  }
}