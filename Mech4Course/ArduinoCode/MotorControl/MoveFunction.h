double TurnFPer = 230 / 150;  //150
double TurnBPer = 1;          //150
double TurnRPer = 230 / 200;  //想要右轉照比例條多快多慢//200
double TurnLPer = 230 / 200;  //200

// double TurnFPer = 0.5;  //150
// double TurnBPer = 0.5;          //150
// double TurnRPer = 150/250;  //想要右轉照比例條多快多慢//200
// double TurnLPer = 150/250;  //200
double RMTonePara = 1.0;  //(調整左右馬達速差的參，乘在右邊馬達數值上)

void TurnRight(int lm1 = 0, int lm2 = 250, int rm1 = 100, int rm2 = 0) {  //leftMotor(1是逆轉)//200,200//200
  int NowTurnPer = TurnRPer;

  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}

void TurnLeft(int lm1 = 100, int lm2 = 0, int rm1 = 0, int rm2 = 250) {  //leftMotor(1是逆轉)
  int NowTurnPer = TurnLPer;

  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}

void Backward(int lm1 = 150, int lm2 = 0, int rm1 = 150, int rm2 = 0) {  //leftMotor(1是逆轉)
  int NowTurnPer = TurnBPer;

  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}

void Frontward(int lm1 = 0, int lm2 = 150, int rm1 = 0, int rm2 = 150) {
  int NowTurnPer = TurnFPer;

  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
}

void Stop(int lm1 = 0, int lm2 = 0, int rm1 = 0, int rm2 = 0) {
  int NowTurnPer = 1;
  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
  delay(100);
}

void NormalT(int lm1 = 0, int lm2 = 0, int rm1 = 0, int rm2 = 0) {
  int NowTurnPer = 1;
  analogWrite(leftMotorPin1, int(lm1 * NowTurnPer));
  analogWrite(leftMotorPin2, int(lm2 * NowTurnPer));
  analogWrite(rightMotorPin1, int(rm1 * NowTurnPer * RMTonePara));
  analogWrite(rightMotorPin2, int(rm2 * NowTurnPer * RMTonePara));
  delay(100);
}