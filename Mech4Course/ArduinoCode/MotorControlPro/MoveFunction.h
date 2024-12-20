// double TurnFPer = 0.5;//0.4 230.0 / 150.0;  //150
// double TurnBPer = 0.5;//0.4 1.0;          //150
// // double TurnRPer = 230 / 200;  //想要右轉照比例條多快多慢//200
// // double TurnLPer = 230 / 200;  //200
// double TurnRPer = 0.5;//0.4 0.3  0.25; //0.2 //想要右轉照比例條多快多慢//200
// double TurnLPer = 0.5;//0.4 0.3 0.25; //0.2 //200 <Debug> 200/200 除出來是interger!! 要200.0/200.0
// double BigTurnRPer = 0.5; //0.2 //想要右轉照比例條多快多慢//200
// double BigTurnLPer = 0.5;

double TurnFPer = 0.6;//0.4 230.0 / 150.0;  //150
double TurnBPer = 0.6;//0.4 1.0;          //150
// double TurnRPer = 230 / 200;  //想要右轉照比例條多快多慢//200
// double TurnLPer = 230 / 200;  //200
double TurnRPer = 0.6;//0.4 0.3  0.25; //0.2 //想要右轉照比例條多快多慢//200
double TurnLPer = 0.6;//0.4 0.3 0.25; //0.2 //200 <Debug> 200/200 除出來是interger!! 要200.0/200.0
double BigTurnRPer = 0.6; //0.2 //想要右轉照比例條多快多慢//200
double BigTurnLPer = 0.6;


// double TurnFPer = 0.5;  //150
// double TurnBPer = 0.5;          //150
// double TurnRPer = 150/250;  //想要右轉照比例條多快多慢//200
// double TurnLPer = 150/250;  //200

double LMTonePara = 0.8;  //(調整左右馬達速差的參，乘在左邊馬達數值上)(因為怕超出, 所以0~1去調整, 只能比例條小不能調大)
double RMTonePara = 0.8;  //(調整左右馬達速差的參，乘在右邊馬達數值上)(因為怕超出, 所以0~1去調整, 只能比例條小不能調大)

// void TurnRight(int lm1 = 0, int lm2 = 250, int rm1 = 100, int rm2 = 0) {  //leftMotor(1是逆轉)//200,200//200
void TurnRight(int lm1 = 0, int lm2 = 250, int rm1 = 0, int rm2 = 150) {
  double NowTurnPer = TurnRPer;
  //Serial.println("NowTurnPer: ");
  //Serial.println(NowTurnPer);
  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer*LMTonePara));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer*LMTonePara));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}

void BigTurnRight(int lm1 = 0, int lm2 = 250, int rm1 = 100, int rm2 = 0) {  //leftMotor(1是逆轉)//200,200//200
//void BigTurnRight(int lm1 = 0, int lm2 = 250, int rm1 = 0, int rm2 = 150) {
  double NowTurnPer = BigTurnRPer;
  //Serial.println("NowTurnPer: ");
  //Serial.println(NowTurnPer);
  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer*LMTonePara));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer*LMTonePara));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}


// void TurnLeft(int lm1 = 100, int lm2 = 0, int rm1 = 0, int rm2 = 250) {  //leftMotor(1是逆轉)
void TurnLeft(int lm1 = 0, int lm2 = 150, int rm1 = 0, int rm2 = 250) {  //leftMotor(1是逆轉)
  double NowTurnPer = TurnLPer;

  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer*LMTonePara));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer*LMTonePara));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}

void BigTurnLeft(int lm1 = 100, int lm2 = 0, int rm1 = 0, int rm2 = 250) {  //leftMotor(1是逆轉)
  double NowTurnPer = BigTurnLPer;

  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer*LMTonePara));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer*LMTonePara));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}



void Backward(int lm1 = 200, int lm2 = 0, int rm1 = 200, int rm2 = 0) {  //leftMotor(1是逆轉) //150 150
  double NowTurnPer = TurnBPer;

  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer*LMTonePara));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer*LMTonePara));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}

void Frontward(int lm1 = 0, int lm2 = 200, int rm1 = 0, int rm2 = 200) {//150 150
  double NowTurnPer = TurnFPer;

  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer*LMTonePara));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer*LMTonePara));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}

void Stop(int lm1 = 0, int lm2 = 0, int rm1 = 0, int rm2 = 0) {
  double NowTurnPer = 1;
  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer*LMTonePara));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer*LMTonePara));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
  delay(100);
}

void NormalT(int lm1 = 0, int lm2 = 0, int rm1 = 0, int rm2 = 0) {
  double NowTurnPer = 1;
  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer*LMTonePara));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer*LMTonePara));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
  delay(100);
}