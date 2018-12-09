# Overview: 

<img align="center" src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/grid_move1.gif" width=890 height=500>

It is a warehouse management system. The system contains Multiple robots and one central processing system for it to control it. Each robot is comprised of two parts. One is the arduino controller for the robot and the NodeMCU intermediate. Each of it's fucntions are explained below.

The proposed system consists of three mobile robots for the warehouse management.

Localization is done for the workspace using the nodes with RFID tags and black strips of lines were used for assisting the navigation across the arena.

The robot basically consists of two controllers:ie primary  controller with a NodeMCU and a  secondary  controller with an Arduino Mega for motion control.

Primary controller deals with the commands sending and receival with the CPS(Central Processing 
System) and secondary controller.In other terms it could be defined as the brain  of the system

Secondary controller deals with the basic motion across the grids.It consists of LSA 08 advanced line sensor and the MPU 6050 IMU which asssists its motion through the environment

Communication between primary and secondary controllers happens through serial communication

Communication between primary controller and the CPS (Central Processing System) happens across MQTT

## Requirements and specifications: 
<img align="right" src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2766.JPG" width= 400 height=300>

* Arduino MEGA.
* EM18 RFID Card Reader.
* LSA08 for Line following operation.
* NodeMCU.
* Motors and respective Motor Drivers.
* LiPo Battery -> 11.1V and 2200 mAh and 25C.
* Voltage regulator board/Buck convertor (5V).
* A grid base layed with black tape.
* Miscellaneous items like dotted PCB, Bread Board, Switches, Wheels, Acrylic Base, Wires.
* A Computer with Ubuntu or Windows capable of running Python.

# Design Consideraion (Very Important):

Initially, we were trying to use aruco markers for localizing the robots in the spots. Due to the complexities involved in that and Hardware required a camera for it, so called it out and replaced localising mechanism with Rfid tags. which are easy and more efficent and doesn't need a camera
Setup: Since it is a warehouse project, we need to put a layout of grid. The grid is layed out by using any normal tape(black). Before laying it out, a rfid tag is put in a proper form where the robot needs to stop. These places are called spots. These spots have something which will be picked up by the robot and deliver it to the other point of the warehouse.

<br>
<br>
<br>
<br>
<br>
<br>

## Connections and Circuit diagrams: 
The circuit diagrams for the compoenents are given below. The respective tables shows the pin connections between the componenets.

### Arduino and Motor driver
<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/Arduino_L298N.jpg" width=600 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/motordriver.png" width=290 height=300>
</p>

### Arduino and IMU
<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/Arduino_MPU6050.jpg" width=600 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/imu.png" width=290 height=300>
</p>

### Arduino and NodeMCU
<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/Arduino_NodeMCU.png" width=600 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/nodemcu.png" width=290 height=300>
</p>

<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/lsa.png" width=400 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/rfidreader.png" width=400 height=300>
</P>

## Software reqs:

## Architecture:
* The Architecture gives the system flexibility and modularity.
* For example, if in future, Localization method is changed to something else, it can be easily replaced since it is modular and does not require a overall change in the architecture.
* The communication between each section is through MQTT. 
* The below diagram gives the overall architecture of the system, 

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/architecture.png" width=700 height=650>
</p>


## Workflow:
* As mentioned everything starts with a GUI. Once the user gives input it sent to CPS via MQTT.
* The CPS recieves the item that needs to be acquired and converts it into grid map co-ordinates. Then based on that, the path is planned using A* algorithm.
* Once the path is planned simlutaneously for each robot without any deadlock and collision conditions, the instrctions are sent through MQTT one by one through each node.
* This system system has an advantage that even if the robot has malfucntioned halfway or it has been reset, the commands can still be given because the robots are stateless meaning it does not keep track of the path. It's only goal is to reach next given point, it does not keep track of anything else. The co-ordinates are however stored to log the events.
* A brief circle of operations is given below,

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/workflow.png" width=650 height=650>
</p>

## Working:

**GUI:**
Run the gui program for selecting the items that is required.

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/gui.png" width=880 height=500>
</p> 

**CPS Functions:**

* receive items from gui via mqtt
* convert items to markerids
* populate the grid by calculating the spaces
* locate the markerid in the grid
* get coordinates of the marker id in grid
* calculate the path using A*
* check for collision avaoidance.
* give instructions to the respective robot one node at a time. Once acknowledged that it reached the Node, then give the next node to the robot.
 

**Path palnning:**

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2583.JPG" width=880 height=400>
</p>

<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2686.JPG" width=440 height=300>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2689.JPG" width=440 height=300>
</p>


**NodeMCU Functions:**

* Nodemcu will receive the next marker id to be found and it will keep moving checking the RFID tags on the way.
* Once the marker id is found, it will inform the cps that it has reached the marker id. 
* The event is logged and the NodeMCU waits for the next command from CPS.

## Execution:

Designed and developed three mobile robots with LSA 08 line sensor,EM 18 RFID reader and MPU 6050 IMU ,which could be controlled by commands across MQTT.

Developed an ArUco based frame work for controlling the motion of the robot between two different points.

Changing the ArUco based framework to the RFID based one for controlling the motion of the robot from points A to B ,B to C.(for a single robot ONLY)


<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/grid_move2.gif" width=880 height=500>
</p>

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/grid_move3.gif" width=880 height=500>
</p> 


High level algorithm Arduino robot Nodemcu interface

High level Algorithm: This calculates the the given task and formulates a path for navigational purposes. it uses A* algorithm to navigate through. It calculates the shortest possible path and also avoids the path which was already taken by another robot.

Arduino robot: The arduino in the robot listens to very particular set of commands and it executes it systematically. While monitering its own positional stability with auto correction. It uses a line following sensor which gives very accurate results. The robot has rfid sensors at each node of the path. A node is a crosssection of two paths. The sensors that we used can identify all different colors. So, can work wide variety of range. the main thing is that using this sensor, it was very easy to find the line even in low lights. The robot can move in constant phase and it is non suceptible to shakes and small occlusions.

Nodemcu: nodemcu plays a great role in communication sync. It facilitates the algorithm and the robot to talk to each other. the node mcu is written on a python mod so, direct can be used for it. Since, the Algorithm is written in python it is very easy for it to communicate to the node mcu.

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

## Future Plans:

Need to develop an algorithmic architecture with the following functionalities:
•   Path planning  with obstacle avoidance ,which is scalable for n-robots
•	Multiple robots could be controlled independently  simultaneously
•	Each robot should be able to move from A->B->C
	
Integrating dynamic obstacle detection with the existing robots and necessary modifications in the algorithm

Battery level monitoring system for each robot, which could be the first step for the auto charge docking

Need to design/develop  a system for lifting or carrying the loads across the environment. 



