#include <Servo.h>

Servo entryGate;
Servo exitGate;

// Define IR sensors for slots
const int slotSensors[] = {4, 5, 6, 7};
const int numSlots = 4;

// IR sensors for gates
const int entrySensor = 2;
const int exitSensor = 3;

// Servo pins
const int entryServoPin = 8;
const int exitServoPin = 9;

void setup() {
  Serial.begin(9600);

  // Setup slot IR sensors
  for (int i = 0; i < numSlots; i++) {
    pinMode(slotSensors[i], INPUT);
  }

  // Setup gate IR sensors
  pinMode(entrySensor, INPUT);
  pinMode(exitSensor, INPUT);

  // Attach servos
  entryGate.attach(entryServoPin);
  exitGate.attach(exitServoPin);

  // Close gates initially
  entryGate.write(0);
  exitGate.write(0);
}

void loop() {
  int availableSlots = 0;

  // Count available slots using only D4–D7
  for (int i = 0; i < numSlots; i++) {
    int state = digitalRead(slotSensors[i]);
    if (state == HIGH) { // No car = HIGH
      availableSlots++;
    }
  }

  // Send slot info to serial
  Serial.print("SLOTS:");
  Serial.println(availableSlots);

  // Entry gate control
  if (digitalRead(entrySensor) == LOW && availableSlots > 0) {
    entryGate.write(90);  // Open
    delay(2000);
    entryGate.write(0);   // Close
  }

  // Exit gate control
  if (digitalRead(exitSensor) == LOW) {
    exitGate.write(90);   // Open
    delay(2000);
    exitGate.write(0);    // Close
  }

  delay(500);
}
