#include <Servo.h>
Servo servo_izq;

int led_rojo1 = 2;
int led_rojo2 = 3;
int pin_servo_izq = 8;
int pin_servo_dch = 9;

void setup(){
    pinMode(led_rojo1, INPUT);
    pinMode(led_rojo2, INPUT);
    Serial.begin(9600);
    servo_izq.attach(pin_servo_izq);
}

void loop(){
    servo_izq.write(180);
    Serial.println("180");
    servo_izq.write(90);
    Serial.println("90");
    servo_izq.write(0);
    Serial.println("0");
}
