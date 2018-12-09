About:
It is a warehouse management system. The system contains Multiple robots and one central processing system for it to control it. Each robot is comprised of two parts. One is the arduino controller for the robot and the NodeMCU intermediate. Each of it's fucntions are explained below.

Setup: Since it is a warehouse project, we need to put a layout of grid. The grid is layed out by using any normal tape(black). Before laying it out, a rfid tag is put in a proper form where the robot needs to stop. These places are called spots. These spots have something which will be picked up by the robot and deliver it to the other point of the warehouse.

Initially, we were trying to use aruco markers for localizing the robots in the spots. Due to the complexities involved in that and Hardware required a camera for it, so called it out and replaced localising mechanism with Rfid tags. which are easy and more efficent and doesn't need a camera

Requirements and specifications: robot specs

High level algorithm Arduino robot Nodemcu interface

High level Algorithm: This calculates the the given task and formulates a path for navigational purposes. it uses A* algorithm to navigate through. It calculates the shortest possible path and also avoids the path which was already taken by another robot.

Arduino robot: The arduino in the robot listens to very particular set of commands and it executes it systematically. While monitering its own positional stability with auto correction. It uses a line following sensor which gives very accurate results. The robot has rfid sensors at each node of the path. A node is a crosssection of two paths. The sensors that we used can identify all different colors. So, can work wide variety of range. the main thing is that using this sensor, it was very easy to find the line even in low lights. The robot can move in constant phase and it is non suceptible to shakes and small occlusions.

Nodemcu: nodemcu plays a great role in communication sync. It facilitates the algorithm and the robot to talk to each other. the node mcu is written on a python mod so, direct can be used for it. Since, the Algorithm is written in python it is very easy for it to communicate to the node mcu.

Since we were on a tight schedule, we haven't taken much photos/videos. This is the one that I found after some search.

Multiprocessing, Multithreading , warehouse algorithm, multiple robot control, two bots


This is an RFID based localisation and navigational system for multiple mobile robots within a given environment

Localization is done for the workspace using the nodes with RFID tags and black strips of lines were used for assisting 
the navigation across the arena.
The robot basically consists of two controllers:ie primary  controller with a NodeMCU and a  secondary  controller with 
an Arduino Mega for motion control 	
Primary controller deals with the commands sending and receival with the CPS(Central Processing 
System) and secondary controller.In other terms it could be defined as the brain  of the system
Secondary controller deals with the basic motion across the grids.It consists of LSA 08 advanced line sensor and the MPU 6050 IMU which asssists its motion through the environment
Communication between primary and secondary controllers happens through serial communication.
Communication between primary controller and the CPS (Central Processing System) happens across MQTT.

Create circuit connections as mentioned below.The attached images are just for reference,USE THE FOLLOWING CONNECTION ONLY

Arduino Mega-IMU 6050

Arduino	IMU   6050
VCC	          VCC
GND       	  GND
SCL       	  SCL
SDA       	  SDA
18(int 5)	    INT 


Arduino Mega-LSA 08

Arduino Mega	LSA 08
0	            RX pin 1
1	            TX pin 2
2	            digital pin 3
4             digital pin 5
GND	          GND
VCC(12 V)    	VCC


Arduino Mega-NodeMCU Serial Communication

Arduino Mega	Node MCU
VCC	          VCC
GND         	GND
RX3      	    TXD1 (GPIO 2) D4



Node MCU- EM 18 RFID card reader

NodeMCU	      EM 18 Card Reader
GPIO3(RXD0)  	TX
GND	          GND



Arduino Mega-Motor Driver


Arduino Mega	Motor Driver board
5	            IN1   (Driver 1)
6           	IN2  (Driver 1)
7           	IN3  (Driver 1)
8	            IN4 (Driver 1)
9	            IN1  (Driver 2)
10          	IN2  (Driver 2)
11          	IN3  (Driver 2)
12          	IN4  (Driver 2)


