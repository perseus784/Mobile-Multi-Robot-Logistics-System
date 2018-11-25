README
The whole project can be divided into three main parts.

Can do: It is a warehouse management system. The system contains Multiple robots and one central processing system for it to control it. Each robot is comprised of two parts. One is the arduino controller for the robot and the NodeMCU intermediate. Each of it's fucntions are explained below.

Setup: Since it is a warehouse project, we need to put a layout of grid. The grid is layed out by using any normal tape(black). Before laying it out, a rfid tag is put in a proper form where the robot needs to stop. These places are called spots. These spots have something which will be picked up by the robot and deliver it to the other point of the warehouse.

Initially, we were trying to use aruco markers for localizing the robots in the spots. Due to the complexities involved in that and Hardware required a camera for it, so called it out and replaced localising mechanism with Rfid tags. which are easy and more efficent and doesn't need a camera

Requirements and specifications: robot specs

High level algorithm Arduino robot Nodemcu interface

High level Algorithm: This calculates the the given task and formulates a path for navigational purposes. it uses A* algorithm to navigate through. It calculates the shortest possible path and also avoids the path which was already taken by another robot.

Arduino robot: The arduino in the robot listens to very particular set of commands and it executes it systematically. While monitering its own positional stability with auto correction. It uses a line following sensor which gives very accurate results. The robot has rfid sensors at each node of the path. A node is a crosssection of two paths. The sensors that we used can identify all different colors. So, can work wide variety of range. the main thing is that using this sensor, it was very easy to find the line even in low lights. The robot can move in constant phase and it is non suceptible to shakes and small occlusions.

Nodemcu: nodemcu plays a great role in communication sync. It facilitates the algorithm and the robot to talk to each other. the node mcu is written on a python mod so, direct can be used for it. Since, the Algorithm is written in python it is very easy for it to communicate to the node mcu.

Since we were on a tight schedule, we haven't taken much photos/videos. This is the one that I found after some search.

Multiprocessing, Multithreading , warehouse algorithm, multiple robot control, two bots