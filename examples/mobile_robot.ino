#include <Servo.h>

int NO_LINEA = LOW; // También podría ponerse 0
int LINEA = HIGH; // También podría ponerse 1

Servo servoIzq;
Servo servoDer;

int pinAnalog = A0;
int pinIrDer = 3;
int pinIrIzq = 2;

int pinServoDer = 9;
int pinServoIzq = 8;

void setup() {
 pinMode(pinIrDer, INPUT);
 pinMode(pinIrIzq, INPUT);

 servoIzq.attach(pinServoIzq);
 servoDer.attach(pinServoDer);
}

void loop() {
 if(digitalRead(pinIrIzq) == LINEA && digitalRead(pinIrDer) == LINEA){
  avanzar(90);
 } else if(digitalRead(pinIrIzq) == NO_LINEA && digitalRead(pinIrDer) == NO_LINEA){
  espiral();
  izquierda(30);
 } else if(digitalRead(pinIrDer) == NO_LINEA){
  derecha(30);
 } else {
  izquierda(30);
 }
}

void detener(){
 servoIzq.write(90);
 servoDer.write(90);
}

void avanzar(int v){
  int velocidadI = 90 - v;
  servoIzq.write(velocidadI);
  int velocidadD = 90 + v;
  servoDer.write(velocidadD);
}

void retroceder(int v){
  int velocidadI = 90 + v;
  servoIzq.write(velocidadI);
  int velocidadD = 90 - v;
  servoDer.write(velocidadD);
}

void derecha(int v){
  int velocidad = 90 + v;
  servoDer.write(velocidad);
  servoIzq.write(velocidad);
}

void espiral(){
  boolean perdido = true;
  int tiempoEspiral = 1000;
  while(perdido){
    avanzar(90);
    double inicioCuentaTiempo = millis();
    while(millis() - inicioCuentaTiempo <= tiempoEspiral){
      if(digitalRead(pinIrIzq) == LINEA || digitalRead(pinIrDer) == LINEA){
        perdido = false;
        detener();
        break;
      }
    }
    if(perdido){
      tiempoEspiral += 1000;
      derecha(30);
      delay(425);
    }
  }
}

void izquierda(int v){
  int velocidad = 90 - v;
  servoDer.write(velocidad);
  servoIzq.write(velocidad);
}