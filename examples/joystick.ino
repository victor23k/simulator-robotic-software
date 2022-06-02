//1.-
#define boton_pin 8 // Pin digital para el botón
#define X_pin A0 // Pin analógico para leer eje X
#define Y_pin A1 // Pin analógico para leer eje Y

void setup() {
 //2.- Inicializar pin 8 (Entrada) con resistencia
 Serial.begin(9600);
 pinMode(boton_pin, INPUT_PULLUP);
}

void loop() {
 //3.-
 Serial.print("Boton pulsado:");
 Serial.println(digitalRead(boton_pin));
 int valorX = analogRead(X_pin);
 Serial.print("X: ");
 Serial.println(valorX);
 int valorY = analogRead(Y_pin);
 Serial.print("Y: ");
 Serial.println(valorY);
 delay(100);
}