
// void setup() {
//   Serial.begin (9600);           //設定序列埠監控視窗 (Serial Monitor) 和 Arduino資料傳輸速率為 9600 bps (Bits Per Second)
//   pinMode(trigPin, OUTPUT);      //Arduino 對外啟動距離感測器Trig腳，射出超音波 
//   pinMode(echoPin, INPUT);       //超音波被障礙物反射後，Arduino讀取感測器Echo腳的時間差
//   pinMode(speakerpin, OUTPUT);   //Arduino對蜂鳴器送出電壓，使其鳴叫
// }
long duration, cm ;  //宣告計算距離時，需要用到的兩個實數
double getDistance(int trigPin, int echoPin)
{                                  //程式計算出距離值 cm
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
  cm = (duration/2) / 29.1;  

  // Serial.print(cm);     //印出距離值 cm 在序列埠監控顯示器 單位公分
  // Serial.println(" cm");
  return cm;

  //  if (cm <= 5) {                       //距離小於5公分，蜂鳴器一直叫 
  //   digitalWrite(speakerpin, HIGH);
  //   delay (20);
  //     }
  // if (cm > 5 && cm <= 15) {             //距離介於5到15公分，蜂鳴器斷斷續續叫，每次0.1秒 
  //   digitalWrite(speakerpin, HIGH);
  //   delay (100);
  //   digitalWrite(speakerpin, LOW);
  //   delay (100);
  //  }
  // if (cm > 15){                        // 距離大於15公分，蜂鳴器斷斷續續叫，每次0.5秒 
  //    digitalWrite(speakerpin, HIGH);
  //   delay (500);
  //   digitalWrite(speakerpin, LOW);
  //   delay (500);
  //     }
  // delay(10); 
}