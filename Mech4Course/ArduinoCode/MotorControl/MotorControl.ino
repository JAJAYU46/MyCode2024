String command;

#define LEDPin_L 7
#define LEDPin_R 8
#define leftMotorPin1  5   //左正
#define leftMotorPin2  6   //左負
#define rightMotorPin1  10  //右負
#define rightMotorPin2  11  //右正
#define VacuumRelayPin 13

#include "MoveFunction.h"

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

  
  //Serial.println("Type Command (white, blue, red, all, off)");
}

void loop() {
  // Frontward();
  if (Serial.available()) { //如果有從USB那邊接收到Serial資料的話
    command = Serial.readStringUntil('\n');
    command.trim();
    if (command.equals("Left")) {
      TurnLeft();
      //turn right
    }else if (command.equals("Right")) {
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
    }
    Serial.print("Command: ");
    Serial.println(command);
  }
}