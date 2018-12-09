Overview: 

<img align="center" src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/grid_move1.gif">

It is a warehouse management system. The system contains Multiple robots and one central processing system for it to control it. Each robot is comprised of two parts. One is the arduino controller for the robot and the NodeMCU intermediate. Each of it's fucntions are explained below.


Setup: Since it is a warehouse project, we need to put a layout of grid. The grid is layed out by using any normal tape(black). Before laying it out, a rfid tag is put in a proper form where the robot needs to stop. These places are called spots. These spots have something which will be picked up by the robot and deliver it to the other point of the warehouse.

Initially, we were trying to use aruco markers for localizing the robots in the spots. Due to the complexities involved in that and Hardware required a camera for it, so called it out and replaced localising mechanism with Rfid tags. which are easy and more efficent and doesn't need a camera

Requirements and specifications: 
<img align="right" src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/IMG_2766.JPG" width= 400 height=300>

robot specs


Connections and Circuit diagrams:
<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/Arduino_L298N.jpg" width=600 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/motordriver.png" width=200 height=400>
</p>

<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/Arduino_MPU6050.jpg" width=600 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/imu.png" width=200 height=400>

</p>

<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/Arduino_NodeMCU.png" width=600 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/nodemcu.png" width=200 height=400>

</p>

LSA to Arduino MEGA | RFID Reader to NodeMCU
------------ | -------------
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/lsa.png" width=300 height=300> | <img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/rfidreader.png" width=300 height=300>


Software reqs:

Architecture:

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/architecture.png">
</p>

Workflow:
<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/workflow.png">
</p>

Execution:
Path palnning:

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/IMG_2583.JPG" width=600 height=400>
</p>

<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/IMG_2586.JPG" width=400 height=300>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/IMG_2589.JPG" width=400 height=300>

</p>

GUI DSELECTION:
<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/gui.png" width=600 height=400>

</p>

Working:
<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/grid_move2.gif" width=600 height=400>

</p>

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/tree/master/Media/grid_move3.gif" width=600 height=400>

</p>
FUTURE PLANS:


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

from notes:
gui:
Run the gui program for selecting the items that is required.

CPS:

run the cps program to cps.py 

Functions:
- receive items from gui via mqtt
- convert items to markerids
- populate the grid by calculating the spaces
- locate the markerid in the grid
- get coordinates of the marker id in grid
- now first move horizontally till you reach the x coordinate
- move vertically till you reach the y coordinate
- repeat the same for going to other positions too

Things to be added:
multithreading control of multiple robots using the same cps

Nodemcu:

Nodemcu will receive the next marker id to be found and
 once the marker id is found, it will inform the cps that It has reached
the marker id. now cps will agan give the next marker for which the robot moves

Things to be added:
Perfect navigation for special cases by testing in differnt positions of the bot.

rajmohan:

Overview

The proposed system consists of three mobile robots for the warehouse management.

Localization is done for the workspace using the nodes with RFID tags and black strips of lines were used for assisting the navigation across the arena.

The robot basically consists of two controllers:ie primary  controller with a NodeMCU and a  secondary  controller with an Arduino Mega for motion control 	

Primary controller deals with the commands sending and receival with the CPS(Central Processing 
System) and secondary controller.In other terms it could be defined as the brain  of the system

Secondary controller deals with the basic motion across the grids.It consists of LSA 08 advanced line sensor and the MPU 6050 IMU which asssists its motion through the environment

Communication between primary and secondary controllers happens through serial communication

Communication between primary controller and the CPS (Central Processing System) happens across MQTT


Progress so far

Designed and developed three mobile robots with LSA 08 line sensor,EM 18 RFID reader and MPU 6050 IMU ,which could be controlled by commands across MQTT.

Developed an ArUco based frame work for controlling the motion of the robot between two different points.

Changing the ArUco based framework to the RFID based one for controlling the motion of the robot from points A to B ,B to C.(for a single robot ONLY)


Future Plans

Need to develop an algorithmic architecture with the following functionalities:
•	Path planning  with obstacle avoidance ,which is scalable for n-robots
•	Multiple robots could be controlled independently  simultaneously
•	Each robot should be able to move from A->B->C
	
Integrating dynamic obstacle detection with the existing robots and necessary modifications in the algorithm

Battery level monitoring system for each robot, which could be the first step for the auto charge docking

Need to design/develop  a system for lifting or carrying the loads across the environment. 



