# README #
The whole project can be divided into three main parts.
High level algorithm
Arduino robot 
Nodemcu interface

High level Algorithm:
This calculates the the given task and formulates a path for navigational purposes.
it uses A* algorithm to navigate through.
It calculates the shortest possible path and also avoids the path which was already taken by another robot.

Arduino robot:
The arduino in the robot listens to very particular set of commands and it executes it systematically.
While monitering its own positional stability with auto correction. It uses a line following sensor which gives very accurate results.
The robot has rfid sensors at each node of the path. A node is a crosssection of two paths. 
The sensors that we used can identify all different colors.

Nodemcu:
nodemcu plays a great role in communication sync. It facilitates the algorithm and the robot to talk to each other.

Multiprocessing, Multithreading , warehouse algorithm, multiple robot control, two bots
