#include <Servo.h>

const int sensorPin = 2; // Sensor IR no pino digital 2
Servo cancela;

bool veiculoDetectado = false;

void setup() {
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);
  cancela.attach(9); // Servo no pino 9
  cancela.write(0);  // Posição inicial da cancela (fechada)
  pinMode(3, OUTPUT);
}

void loop() {
  int sensorValue = digitalRead(sensorPin);

  if (sensorValue == LOW && !veiculoDetectado) { // Sensor IR detecta presença
    veiculoDetectado = true;
    Serial.println("VEICULO_DETECTADO");
  }

  if (sensorValue == HIGH) {
    veiculoDetectado = false;
  }

  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "ABRIR_CANCELA") {
      cancela.write(90); 
      delay(5000);      
      cancela.write(0);
    }

    if (comando == "NAO_AUTORIZADO") {
      digitalWrite(3, HIGH);
      delay(1000); 
      digitalWrite(3, LOW);
    }
  }
}
