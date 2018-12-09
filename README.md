# Overview: 

<img align="center" src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/grid_move1.gif" width=890 height=500>

* It is a warehouse management system. The system contains Multiple robots and one Central Processing System to control it. Each robot is comprised of two parts. One is the arduino controller for the robot and the NodeMCU intermediate.

* Designed and developed three mobile robots with LSA 08 line sensor,EM 18 RFID reader and MPU 6050 IMU, which could be controlled by commands across MQTT.

* The proposed system consists of three mobile robots for the warehouse management.
* This is an RFID based localisation and navigational system for multiple mobile robots within a given environment

* Localization is done for the workspace using the nodes with RFID tags and black strips of lines were used for assisting the navigation across the arena.
* 

* 


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

A lot of literature survey and search went in this section.
A lot of factors were considered such as financial, reliable, available, flexible, modular aspects.
software considerations
python usable extensible

Initially, we were trying to use aruco markers for localizing the robots in the spots. Due to the complexities involved in that and Hardware required a camera for it, so called it out and replaced localising mechanism with Rfid tags. which are easy and more efficent and doesn't need a camera 


Developed an ArUco based frame work for controlling the motion of the robot between two different points.

Changing the ArUco based framework to the RFID based one for controlling the motion of the robot from points A to B ,B to C.(for a single robot ONLY) 
 A node is a crosssection of two paths. The sensors that we used can identify all different colors. So, can work wide variety of range. the main thing is that using this sensor, it was very easy to find the line even in low lights. 


**Setup:** 
Since it is a warehouse project, we need to put a layout of grid. The grid is layed out by using any normal tape(black). Before laying it out, a RFID tag is put in a proper form where the robot needs to stop in the cross section of the grid. These spots have something which will be picked up by the robot and deliver it to the other point of the warehouse.

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
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/architecture.png" width=800 height=650>
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

* **(A*)** algorithm is used to calculate the path and using this can give us dynamic path planning with obstacles.
* It calculates the shortest possible path and also avoids the path which was already taken by another robot. 
The following setup is considered as the arena and the system is based on this,

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2583.JPG" width=880 height=400>
</p>

<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2686.JPG" width=440 height=300>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2689.JPG" width=440 height=300>
</p>


**NodeMCU Functions:** 

* NodeMCU facilitates the algorithm and the Arduino in the robot to talk to each other.
* Nodemcu will receive the next marker id to be found and it will keep moving checking the RFID tags on the way.
* Once the marker id is found, it will inform the cps that it has reached the marker id. 
* The event is logged and the NodeMCU waits for the next command from CPS.

**Localisation:** 

* After trying various localisation methods, we first decided to localize the robots with ARUCO markers. But the problem with ARUCO markers are it requires a vision system, means it requires a camera and a raspberry pi to run it.
* Another problem with ARUCO markers are they need to sticked in a certain way requires a very rigid rack also it suffers in low light condiations.
* After all these drawbacks we decided replace the localisation with RFID readers.
* We used EM18 RFID readers attached at the bottom of the robot and placed the RFID tags at the intersection of the grid lines.
* Each RFID tag is cross referenced to a grid co-ordinate and that file is stored in memory.
* This method can work even in no light conditions and it is much more robust than the ARUCO markers.

**Arduino MEGA:**

 * Communication NodeMCU and Arduino happens through serial communication.
 * The arduino in the robot listens to very particular set of commands and it executes it systematically.
 * It consists of LSA 08 advanced line sensor and the MPU 6050 IMU which asssists its motion through the environment
 * The Arduino moniters its own positional stability with auto correction. 
 * The robot has RFID detectors placed on the bottom for localization.
 * The robot can move in constant phase and it is non susceptible to shakes and small occlusions.

## Execution:

One robot navigating it's way through the grid,

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/grid_move3.gif" width=880 height=500>
</p>

Robot navigating it's way when another robot is present in the same grid,

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/grid_move2.gif" width=880 height=500>
</p> 


## Future Plans:

* Each robot should be able to move from A->B->C

* Battery level monitoring system for each robot, which could be the first step for the auto charge docking

* Need to design/develop  a system for lifting or carrying the loads across the environment. 
