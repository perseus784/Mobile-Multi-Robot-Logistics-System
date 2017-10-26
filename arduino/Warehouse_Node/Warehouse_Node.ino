unsigned long LastMillis = 0;

#include "I2Cdev.h"

#include "MPU6050_6Axis_MotionApps20.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif
#include <SPI.h>
#include <MFRC522.h>


//MPU 6050 Configuration setup

MPU6050 mpu;
//MPU6050 mpu(0x69); // <-- use for AD0 high

#define OUTPUT_READABLE_YAWPITCHROLL
bool blinkState = false;


int current_status = 0;
int last_status = 0;
int incomingByte = 0;

// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector
float yprf[3];
float yprf1[3];
float target;
float current;
float error_angle;
int count = 0;
int count_stop = 0;
int count1 = 0;
float temp = 0;
float angle();
unsigned long previousMillis = 0;
unsigned long previousStop = 0;
float Error(float target);
// packet structure for InvenSense teapot demo
uint8_t teapotPacket[14] = { '$', 0x02, 0, 0, 0, 0, 0, 0, 0, 0, 0x00, 0x00, '\r', '\n' };



// ================================================================
// ===               INTERRUPT DETECTION ROUTINE                ===
// ================================================================

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
  mpuInterrupt = true;
}




#define IN1 5
#define IN2 6
#define IN3 22
#define IN4 23


#define IN5 24
#define IN6 25
#define IN7 11
#define IN8 12

#define Flash 26


int L1 = 155;//210
int R1 = 140;//190
int L2 = 155;
int R2 = 140;

int L11 = 155;
int R12 = 155;
int L21 = 155;
int R22 = 155;
char rpi = '3';

int F = 0;
int S = 0;
int L = 0;
int R = 0;
int B = 0;


float Threshold = 3.5;       //2.5
float Threshold_1 = 4.0;     //3.5



const int Kp = 10;   // Kp value that you have to change
const int Kd = 0;   // Kd value that you have to change
const int setPoint = 35;    // Middle point of sensor array
const int baseSpeed = 120;    // Base speed for your motors
const int maxSpeed = 220;   // Maximum speed for your motors

const byte rx = 0;    // Defining pin 0 as Rx
const byte tx = 1;    // Defining pin 1 as Tx
const byte serialEn = 2;    // Connect UART output enable of LSA08 to pin 2
const byte junctionPulse = 4;   // Connect JPULSE of LSA08 to pin 4





void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial3.begin(9600);

  pinMode(serialEn, OUTPUT);  // Setting serialEn as digital output pin
  pinMode(junctionPulse, INPUT);  // Setting junctionPulse as digital input pin
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(IN5, OUTPUT);
  pinMode(IN6, OUTPUT);
  pinMode(IN7, OUTPUT);
  pinMode(IN8, OUTPUT);

  digitalWrite(serialEn, HIGH);


  SPI.begin();      // Initiate  SPI bus
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
  TWBR = 24; // 400kHz I2C clock (200kHz if CPU is 8MHz)
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(400, true);
#endif

  // initialize serial communication
  // (115200 chosen because it is required for Teapot Demo output, but it's
  // really up to you depending on your project)

  while (!Serial3); // wait for Leonardo enumeration, others continue immediately

  // NOTE: 8MHz or slower host processors, like the Teensy @ 3.3v or Ardunio
  // Pro Mini running at 3.3v, cannot handle this baud rate reliably due to
  // the baud timing being too misaligned with processor ticks. You must use
  // 38400 or slower in these cases, or use some kind of external separate
  // crystal solution for the UART timer.

  // initialize device
  // Serial.println(F("Initializing I2C devices..."));
  mpu.initialize();

  // verify connection
  // Serial.println(F("Testing device connections..."));
  //Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

  // wait for ready
  //    Serial.println(F("\nSend any character to begin DMP programming and demo: "));
  //    while (Serial.available() && Serial.read()); // empty buffer
  //    while (!Serial.available());                 // wait for data
  //    while (Serial.available() && Serial.read()); // empty buffer again

  // load and configure the DMP
  //Serial.println(F("Initializing DMP..."));
  devStatus = mpu.dmpInitialize();

  // supply your own gyro offsets here, scaled for min sensitivity
  mpu.setXGyroOffset(-7);
  mpu.setYGyroOffset(2);
  mpu.setZGyroOffset(17);
  mpu.setZAccelOffset(1445); // 1688 factory default for my test chip

  // make sure it worked (returns 0 if so)
  if (devStatus == 0) {
    // turn on the DMP, now that it's ready
    //Serial.println(F("Enabling DMP..."));
    mpu.setDMPEnabled(true);

    // enable Arduino interrupt detection
    //Serial.println(F("Enabling interrupt detection (Arduino external interrupt 4)..."));
    attachInterrupt(4, dmpDataReady, RISING);
    mpuIntStatus = mpu.getIntStatus();

    // set our DMP Ready flag so the main loop() function knows it's okay to use it
    //Serial.println(F("DMP ready! Waiting for first interrupt..."));
    dmpReady = true;

    // get expected DMP packet size for later comparison
    packetSize = mpu.dmpGetFIFOPacketSize();
  } else {
    // ERROR!
    // 1 = initial memory load failed
    // 2 = DMP configuration updates failed
    // (if it's going to break, usually the code will be 1)
    //Serial.print(F("DMP Initialization failed (code "));
    //Serial.print(devStatus);
    //Serial.println(F(")"));
  }






}
int lastError = 0;    // Declare a variable to store previous error
void loop() {

  
  int junction = digitalRead(junctionPulse);


  if (junction == HIGH)

  { 
    unsigned long currentStop = millis();  
    if (count_stop < 1)
    {
      Stop();
      Serial.write(rpi);
      count_stop = count_stop + 1;
    }
    else
    {
               //PROBLEM WITH IMU 6050,DRIFT of 1 degree/3.5 minute.SO hard coding to avoid DRIFT ERROR
      if ((currentStop - previousStop) < 2000)
      {

      }
      else
      {
        Stop();
        Serial.write(rpi);  
        previousStop = currentStop;
      }
    }
  }
  digitalWrite(serialEn, LOW);  // Set serialEN to LOW to request UART data
  if (count < 1)
  {
    if (millis() < 25000)
    {

    }
    else
    {
      target = angle();
      count = count + 1;
      digitalWrite(Flash, HIGH);
      delay(2000);
      digitalWrite(Flash, LOW);
    }
  } else {

    unsigned long currentMillis = millis();           //PROBLEM WITH IMU 6050,DRIFT of 1 degree/3.5 minute.SO hard coding to avoid DRIFT ERROR
    if (currentMillis - previousMillis >= 27000)
    {

      target = target - 0.15;                         // Updating target value in every 27 seconds...DONT WORRY ITS CALIBRATED SO THAT least DRIFT ERROR will occur
      if (target < 0)
      {
        target = 360 + target;
      }
      previousMillis = currentMillis;
    }
  }

  current = angle();

  error_angle = Error(target);
  //  Serial3.println(current);
  //  Serial.println(current);





  if (Serial.available())
  {
    incomingByte = Serial.read();
   // Serial.println(incomingByte);
    if (incomingByte == '1')                      //Forward
    {
      forward();

      //Serial.println("forward");
      // wait for a second
    }
    else if (incomingByte == '2')
    {
      //Serial.println("left");
      left();

    }
    else if (incomingByte == '3')
    {
      //Serial.println("right");
      right();

    }
    else if (incomingByte == '4')
    {
      back();

      //Serial.println("back");
    }
    else if (incomingByte == '5')
    {
      Stop();

      //Serial.println("Stop");
    }
    else
    {
      // Serial.println("fail");

    }



  }
  if (F == 1)
  {
    analogWrite(IN1, L1);          //Basic forwad motion code   FOR VISION BASED
    analogWrite(IN2, 0);
    analogWrite(IN3, R1);
    analogWrite(IN4, 0);

    analogWrite(IN5, 0);
    analogWrite(IN6, L2);
    analogWrite(IN7, 0);
    analogWrite(IN8, R2);
    //Serial3.println("Run");

    if (abs(target - current) < 180)        //CODE FOR AUTO CORRECTION IF error goes beyond threshold   FOR VISION BASED
    {
      if (current > target)
      {
        while (abs(error_angle) > Threshold )
        {
          //          Serial.println("Move left 1");

          current = angle();
          error_angle = Error(target);
          LEFT();


        }

      }
      else
      {

        while (abs(error_angle) > Threshold )
        {
          //          Serial.println("Move right 1");

          current = angle();
          error_angle = Error(target);
          RIGHT();
        }
      }
    }
    else
    {
      if (current > target)
      {

        while (abs(error_angle) > Threshold )
        {
          //          Serial.println("Move right 2");

          current = angle();
          error_angle = Error(target);
          RIGHT();

        }
      }
      else
      {

        while (abs(error_angle) > Threshold )
        {
          //          Serial.println("Move left 2");
          current = angle();
          error_angle = Error(target);
          LEFT();

        }
      }


    }























  }
  if (S == 1)
  {

    analogWrite(IN1, 0);          //Basic forwad motion code   FOR VISION BASED
    analogWrite(IN2, 0);
    analogWrite(IN3, 0);
    analogWrite(IN4, 0);

    analogWrite(IN5, 0);
    analogWrite(IN6, 0);
    analogWrite(IN7, 0);
    analogWrite(IN8, 0);
    if (abs(target - current) < 180)
    {
      if (current > target)
      {
        while (abs(error_angle) > Threshold_1 )
        {
          //          Serial.println("Move left 1");

          current = angle();
          error_angle = Error(target);
          LEFT();

        }

      }
      else
      {

        while (abs(error_angle) > Threshold_1 )
        {
          //          Serial.println("Move right 1");

          current = angle();
          error_angle = Error(target);
          RIGHT();

        }
      }
    }
    else
    {
      if (current > target)
      {

        while (abs(error_angle) > Threshold_1 )
        {
          //          Serial.println("Move right 2");

          current = angle();
          error_angle = Error(target);
          RIGHT();

        }
      }
      else
      {

        while (abs(error_angle) > Threshold_1 )
        {
          //          Serial.println("Move left 2");
          current = angle();
          error_angle = Error(target);
          LEFT();
        }
      }


    }
  }

  if (R == 1)
  {
    current = angle();

    if ( target > 270)
    {
      target = target - 270;
      error_angle = Error(target);
    }
    else if (target < 270)
    {
      target = target + 90;
      error_angle = Error(target);
    }

    Stop();

  }
  if (L == 1)
  {
    current = angle();


    if (target > 90)
    {
      target = target - 90;
      error_angle = Error(target);



    }

    else if (target < 90)
    {
      target = 270 + target ;
      error_angle = Error(target);


    }

    Stop();
  }
  if (B == 1)
  {
    analogWrite(IN1, 0);          //Basic forwad motion code   FOR VISION BASED
    analogWrite(IN2, L1);
    analogWrite(IN3, 0);
    analogWrite(IN4, R1);

    analogWrite(IN5, L2);
    analogWrite(IN6, 0);
    analogWrite(IN7, R2);
    analogWrite(IN8, 0);
    //Serial3.println("Run");

    if (abs(target - current) < 180)   //CODE FOR AUTO CORRECTION IF error goes beyond threshold   FOR VISION BASED
    {
      if (current > target)
      {
        while (abs(error_angle) > Threshold )
        {
          //        Serial.println("Move left 1");

          current = angle();
          error_angle = Error(target);
          LEFT();

        }

      }
      else
      {

        while (abs(error_angle) > Threshold )
        {
          //          Serial.println("Move right 1");

          current = angle();
          error_angle = Error(target);
          RIGHT();

        }
      }
    }
    else
    {
      if (current > target)
      {

        while (abs(error_angle) > Threshold )
        {
          // Serial.println("Move right 2");

          current = angle();
          error_angle = Error(target);
          RIGHT();

        }
      }
      else
      {

        while (abs(error_angle) > Threshold )
        {
          //          Serial.println("Move left 2");
          current = angle();
          error_angle = Error(target);
          LEFT();

        }
      }


    }

  }

}

void forward()
{
  F = 1;
  S = 0;
  L = 0;
  R = 0;
  B = 0;
}
void Stop()
{
  F = 0;
  S = 1;
  L = 0;
  R = 0;
  B = 0;
}

void right()
{
  F = 0;
  S = 0;
  L = 0;
  R = 1;
  B = 0;
}
void left()
{
  F = 0;
  S = 0;
  L = 1;
  R = 0;
  B = 0;
}
//

void back()
{
  F = 0;
  S = 0;
  L = 0;
  R = 0;
  B = 1;
}

void LEFT()         // 90 degree LEFT ANDROID TABLET BASED
{
  analogWrite(IN1, 0);
  analogWrite(IN2, L11);
  analogWrite(IN3, R12);
  analogWrite(IN4, 0);

  analogWrite(IN5, L21);
  analogWrite(IN6, 0);
  analogWrite(IN7, 0);
  analogWrite(IN8, R22);


}


void RIGHT()       // 90 degree RIGHT ANDROID TABLET BASED
{
  analogWrite(IN1, L11);
  analogWrite(IN2, 0);
  analogWrite(IN3, 0);
  analogWrite(IN4, R12);

  analogWrite(IN5, 0);
  analogWrite(IN6, L21);
  analogWrite(IN7, R22);
  analogWrite(IN8, 0);


}















float angle()         //Getting live angles from IMU 6050
{

  if (!dmpReady) return;

  // wait for MPU interrupt or extra packet(s) available
  while (!mpuInterrupt && fifoCount < packetSize) {
    // other program behavior stuff here
    // .
    // .
    // .
    // if you are really paranoid you can frequently test in between other
    // stuff to see if mpuInterrupt is true, and if so, "break;" from the
    // while() loop to immediately process the MPU data
    // .
    // .
    // .
  }

  // reset interrupt flag and get INT_STATUS byte
  mpuInterrupt = false;
  mpuIntStatus = mpu.getIntStatus();

  // get current FIFO count
  fifoCount = mpu.getFIFOCount();

  // check for overflow (this should never happen unless our code is too inefficient)
  if ((mpuIntStatus & 0x10) || fifoCount == 1024) {
    // reset so we can continue cleanly
    mpu.resetFIFO();
    // Serial.println(("FIFO overflow!"));

    // otherwise, check for DMP data ready interrupt (this should happen frequently)
  } else if (mpuIntStatus & 0x02) {
    // wait for correct available data length, should be a VERY short wait
    while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();

    // read a packet from FIFO
    mpu.getFIFOBytes(fifoBuffer, packetSize);

    // track FIFO count here in case there is > 1 packet available
    // (this lets us immediately read more without waiting for an interrupt)
    fifoCount -= packetSize;



    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);





    yprf[0] = (ypr[0] * 180 / M_PI);
    yprf[1] = (ypr[1] * 180 / M_PI);
    yprf[2] = (ypr[2] * 180 / M_PI);

    if (yprf[0] > 0 )
    {
      temp = yprf[0];

    }
    else
    {
      temp = 360 + yprf[0];

    }
   
    return temp;
    

  }


}




float Error(float target)   // Calculating error angle at every instant
{
  if (abs(target - current) < 180)
  {
    if (current > target)
    {
      error_angle = target - current;
    }
    else
    {
      error_angle = target - current;
    }
  }
  else
  {
    if (current > target)
    {
      error_angle = 360 + target - current;
    }
    else
    {
      error_angle = 360 - target + current;
    }
  }


  return error_angle;
}




void flash()          //Turning on flash for 2 seconds
{
  digitalWrite(Flash, HIGH);
  delay(2000);
  digitalWrite(Flash, LOW);
}


