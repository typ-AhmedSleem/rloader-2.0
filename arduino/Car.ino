// Includes
#include "AFMotor.h"
// Hardware components pins
#define PIN_DRIVE_FORWARD A0
#define PIN_DRIVE_BACKWARD A1
#define PIN_STEER_RIGHT A2
#define PIN_STEER_LEFT A3
// Constants
const int MAX_SPEED = 255;
// Car states
#define CAR_IDLE 0
#define DRIVING_FORWARD 1
#define DRIVING_BACKWARD 2
#define STEERING_RIGHT 3
#define STEERING_LEFT 4
// Runtime
int carState = CAR_IDLE;
int dummyState = CAR_IDLE;
// Hardware
AF_DCMotor leftFrontMotor(4);
AF_DCMotor rightFrontMotor(3);

// Functions
void driveMotor(AF_DCMotor motor, int direction, int speed);
void driveMotor(AF_DCMotor motor, int direction, int speed)
{
  motor.setSpeed(speed);
  motor.run(direction);
}

void setup()
{
  Serial.begin(9600);
  // Setup IO pins
  pinMode(PIN_STEER_LEFT, INPUT_PULLUP);
  pinMode(PIN_STEER_RIGHT, INPUT_PULLUP);
  pinMode(PIN_DRIVE_FORWARD, INPUT_PULLUP);
  pinMode(PIN_DRIVE_BACKWARD, INPUT_PULLUP);
  // Release motors from any movement
  carState = CAR_IDLE;
  driveMotor(leftFrontMotor, RELEASE, 0);
  driveMotor(rightFrontMotor, RELEASE, 0);
  Serial.println("Car is Idle.");
}

void loop()
{
  // Grab reading from RPi
  bool forward = digitalRead(PIN_DRIVE_FORWARD) == HIGH;
  bool backward = digitalRead(PIN_DRIVE_BACKWARD) == HIGH;
  bool right = digitalRead(PIN_STEER_RIGHT) == HIGH;
  bool left = digitalRead(PIN_STEER_LEFT) == HIGH;
  // Drive both motors according to direction to be determined
  if ((forward && !backward && !right && !left) && carState != DRIVING_FORWARD)
  {
    carState = DRIVING_FORWARD;
    driveMotor(leftFrontMotor, FORWARD, MAX_SPEED);
    driveMotor(rightFrontMotor, FORWARD, MAX_SPEED);
    Serial.println("Drive Forward");
  }
  else if ((!forward && backward && !right && !left) && carState != DRIVING_BACKWARD)
  {
    carState = DRIVING_BACKWARD;
    driveMotor(leftFrontMotor, BACKWARD, MAX_SPEED);
    driveMotor(rightFrontMotor, BACKWARD, MAX_SPEED);
    Serial.println("Drive Backward");
  }
  else if ((!forward && !backward && right && !left) && carState != STEERING_RIGHT)
  {
    carState = STEERING_RIGHT;
    driveMotor(leftFrontMotor, FORWARD, MAX_SPEED);
    driveMotor(rightFrontMotor, BACKWARD, MAX_SPEED);
    Serial.println("Rotate Right");
  }
  else if ((!forward && !backward && !right && left) && carState != STEERING_LEFT)
  {
    carState = STEERING_LEFT;
    driveMotor(leftFrontMotor, BACKWARD, MAX_SPEED);
    driveMotor(rightFrontMotor, FORWARD, MAX_SPEED);
    Serial.println("Rotate Left");
  }   else if ((!forward && !backward && !right && !left) && carState != CAR_IDLE)
  {
    carState = CAR_IDLE;
    driveMotor(leftFrontMotor, RELEASE, 0);
    driveMotor(rightFrontMotor, RELEASE, 0);
    Serial.println("Stopped");
  }
  // Delay for 50 ms
  delay(50);
}
