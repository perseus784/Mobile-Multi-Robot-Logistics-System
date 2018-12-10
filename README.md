# Overview: 

<img align="center" src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/grid_move1.gif" width=890 height=500>

The proposed project is a Mutli Robot Warehouse Management System. It involved us working on variety of concepts and gave a in-depth knowledge in both hardware and software aspects. The entire system is completly modular and constructed with serious scope for future modifications.

## Key Features:
* The robots navigate their way using grid path lines which is sensed by the highly accurate light sensing sensor-> **LSA 08**.

* Each robot is comprised of two parts, One is the **Arduino MEGA** controller for the robot and the **NodeMCU** intermediate.

* Localisation of the robots are done using RFID tags layed under the intersections of the grid which is read by RFID reader-> **EM 18 RFID reader**.

* Inertial Measure Unit for stabilty and control -> **MPU 6050 IMU**.

* A* is used for Dynamic path planning even with obstacles and multiple robots.

* Communication is based entirely on **MQTT**.

* Robots are **Stateless**, which means even if the robots malfucntioned or disturbed, CPS can reboot the robot and continue its job without hiderance.


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

# Design Consideraion:

* A lot of literature survey and study went in this section to design it in every aspect like cost efficient, reliable, extensible and modular aspects.
* The whole system is very modular in both Hardware and Software level, it is made that way so that it can experimented with differented things.
* Python is used as the chief software for CPS. Python provides easy prototying and extensibility.
* Path planning was initially done using custom simple algorithm and then we moved to A* algorithm for dynamic path planning with obstacles.
* Initially, we were trying to use aruco markers for localizing the robots in the spots. Due to the complexities involved in that and Hardware required a camera for it, so called it out and replaced localising mechanism with Rfid tags. which are easy and more efficent and doesn't need a camera.
* At first, we designed it for only one robot but later on we added multiple robots which can work side by side and CPS can give them commands simultaneously.

## Setup: 
Since it is a warehouse project, we need to put a layout of grid. The grid is layed out by using any normal tape(black). Before laying it out, a RFID tag is put in a proper form where the robot needs to stop in the cross section of the grid. These spots have something which will be picked up by the robot and deliver it to the other point of the warehouse.

## Connections and Circuit diagrams: 
The circuit diagrams for the compoenents are given below. The respective tables shows the pin connections between the componenets.

### Arduino and Motor driver
<br>
<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/Arduino_L298N.jpg" width=600 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/motordriver.png" width=290 height=300>
</p>
<br>

### Arduino and IMU
<br>

<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/Arduino_MPU6050.jpg" width=600 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/imu.png" width=290 height=300>
</p>
<br>

### Arduino and NodeMCU
<br>

<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/Arduino_NodeMCU.png" width=600 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/nodemcu.png" width=290 height=300>
</p>

<br>
<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/lsa.png" width=400 height=400>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/rfidreader.png" width=400 height=300>
</P>

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
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/workflow.png" width=750 height=750>
</p>

## Working:

### GUI: 

Run the gui program for selecting the items that is required.

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/gui.png" width=880 height=500>
</p> 

### CPS Functions:

* receive items from gui via mqtt
* convert items to markerids
* populate the grid by calculating the spaces
* locate the markerid in the grid
* get coordinates of the marker id in grid
* calculate the path using A*
* check for collision avaoidance.
* give instructions to the respective robot one node at a time. Once acknowledged that it reached the Node, then give the next node to the robot.
 

### Path palnning: 

* A* algorithm is used to calculate the path and using this can give us dynamic path planning with obstacles.
* It calculates the shortest possible path and also avoids the path which was already taken by another robot. 
The following setup is considered as the arena and the system is based on this,

<p align="center">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2583.JPG" width=880 height=400>
</p>

<p align="left">
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2686.JPG" width=440 height=300>
<img src="https://github.com/perseus784/Mobile-Multi-Robot-Logistics-System/blob/master/Media/IMG_2689.JPG" width=440 height=300>
</p>



### NodeMCU Functions:

* NodeMCU facilitates the algorithm and the Arduino in the robot to talk to each other.
* Nodemcu will receive the next marker id to be found and it will keep moving checking the RFID tags on the way.
* Once the marker id is found, it will inform the cps that it has reached the marker id. 
* The event is logged and the NodeMCU waits for the next command from CPS.

### Localisation: 

* After trying various localisation methods, we first decided to localize the robots with ARUCO markers. But the problem with ARUCO markers are it requires a vision system, means it requires a camera and a raspberry pi to run it.
* Another problem with ARUCO markers are they need to sticked in a certain way requires a very rigid rack also it suffers in low light condiations.
* After all these drawbacks we decided replace the localisation with RFID readers.
* We used EM18 RFID readers attached at the bottom of the robot and placed the RFID tags at the intersection of the grid lines.
* Each RFID tag is cross referenced to a grid co-ordinate and that file is stored in memory.
* This method can work even in no light conditions and it is much more robust than the ARUCO markers.

### Arduino MEGA:

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

* Adding functionality to move from the destination point to the next destination point without coming to Home point. 

* Battery level monitoring system for each robot, which could be the first step for the auto charge docking.

* Design/ Develop a system for lifting or carrying the loads across the environment. 
