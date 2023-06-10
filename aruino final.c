#include <Servo.h>

const int ENA = 5; // PWM pin for motor 1 speed
const int IN1 = 6; // Control pin 1 for motor 1 direction
const int IN2 = 7; // Control pin 2 for motor 1 direction
const int ENB = 10; // PWM pin for motor 2 speed
const int IN3 = 9; // Control pin 1 for motor 2 direction
const int IN4 = 8; // Control pin 2 for motor 2 direction
const int servoPin = 13;
const int pumpPin = 18;
const int servoPin2 = 11;


volatile bool catDetected = false;
volatile bool servoMoving = false;
volatile unsigned long servoStartTime = 0;
volatile unsigned long distanceTravelled = 0; // Declare distanceTravelled variable

Servo servo;
Servo servo2; // Declare the new servo

void setup() {
  pinMode(13, OUTPUT); // Set pin 13 as an output
  pinMode(8, INPUT); // Set pin 8 as an input
  pinMode(4, LOW); // Set pin 2 as an output
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(servoPin, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(pumpPin, OUTPUT);


  attachInterrupt(digitalPinToInterrupt(3), incrementDistance, RISING); // attach interrupt to digital pin 3

  servo.attach(servoPin);
  servo2.attach(servoPin2); // Attach the new servo

  Serial.begin(19200);
}

void loop() {
  if (Serial.available() > 0) {

    String signal = Serial.readStringUntil('\n');
    Serial.print(signal);
    if (signal == "cat") {
      Serial.print(signal);
      catDetected = true;
    }
  }

  if (catDetected && !servoMoving) {
    digitalWrite(pumpPin, HIGH); // Turn on the pump
    delay(5000); // Wait for 2 seconds
    digitalWrite(pumpPin, LOW); // Turn off the pump
    delay(5000); // Wait for 2 seconds

    digitalWrite(13, HIGH); // Turn on the built-in LED on pin 13
    moveMotors(200, 200, true, true); // Move motors forward
    delay(2000); // Wait for 2 seconds
    stopMotors(); // Stop motors
    moveServo(180, 10000); // Move servo to 180 degrees over 10 seconds
    delay(5000); // Wait for 5 seconds
    moveServo(90, 10000); // Move servo back to 0 degrees over 10 seconds
    servoMoving = false;
    moveMotors(150, 150, true, true); // Move motors forward for additional 200 mm
    delay(5000); // Wait for 5 seconds
    stopMotors(); // Stop motors
    moveMotors(-150, -150, true, true); // Move motors backwards for 120 mm
    delay(5000); // Wait for 5 seconds
    stopMotors(); // Stop motors
    catDetected = false;
  }

  int level = analogRead(A0);
  unsigned long distance = getDistanceTravelled();
  Serial.print("Water level: ");
  Serial.println(level);
  Serial.print("Distance travelled (in mm): ");
  Serial.println(distance);
}

// Interrupt service routine to increment the distance counter
void incrementDistance() {
  static unsigned long lastTime = 0;
  unsigned long now = millis();
  if (now - lastTime > 50) { // Ignore bounces shorter than 50 ms
    lastTime = now;
    distanceTravelled++;
  }
  
  if (distanceTravelled >= 200) { // Stop the motors after travelling 200mm
    stopMotors();
    moveServo(180, 5000); // Move the servo to 180 degrees over 5 seconds
    delay(5000); // Wait for 5 seconds
    moveMotors(150, 150, false, false); // Move motors backward for 120mm
    delay(5000); // Wait for 5 seconds
    stopMotors(); // Stop motors
    moveServo(0, 5000); // Move the servo back to 0 degrees over 5 seconds
    delay(5000); // Wait for 5 seconds
    moveServo2(40); // Move the new servo to 40 degrees
    delay(5000); // Wait for 5 seconds
    moveServo2(0, 5000); // Move the servo back to 0 degrees over 5 seconds
    moveMotors(-150, -150, true, true); // Move motors forward to starting position
    distanceTravelled = 0; // Reset the distance counter
  }
}



// Function to move both motors
void moveMotors(int speed1, int speed2, bool forward1, bool forward2) {
  // Set motor 1 direction
  digitalWrite(IN1, forward1 ? HIGH : LOW);
  digitalWrite(IN2, forward1 ? LOW : HIGH);
  
  // Set motor 2 direction
  digitalWrite(IN3, forward2 ? HIGH : LOW);
  digitalWrite(IN4, forward2 ? LOW : HIGH);
  
  // Set motor speeds
  analogWrite(ENA, speed1);
  analogWrite(ENB, speed2);
}

// Function to stop both motors
void stopMotors() {
digitalWrite(IN1, LOW);
digitalWrite(IN2, LOW);
digitalWrite(IN3, LOW);
digitalWrite(IN4, LOW);
analogWrite(ENA, 0);
analogWrite(ENB, 0);
}
void moveServo2(int angle) {
  servo2.write(angle);
}

void moveServo(int angle, unsigned long duration) {
servoMoving = true;
servoStartTime = millis();
servo.write(angle);
}

unsigned long getDistanceTravelled() {
noInterrupts(); // Disable interrupts while reading the distance counter
unsigned long distance = distanceTravelled;
distanceTravelled = 0;
interrupts(); // Enable interrupts again
return distance * 10; // Convert number of interrupts to distance in mm
}
 

