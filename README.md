# Robot-Invigilator
This is an automatic invigilator system that is capable of monitoring 2 examinees at a time and detecting simple cheating behaviours like peeking and speaking. Based on the cheating behaviour detected, the invigilator can give a warning message to the examinee or examinees. The output action or warning message is carried out by a Nao robot, either real or virtual. This automatic invigilator is designed to make a human invigilator's work easier. It could be used to warn a human invigilator if cheating behaviour is occurring when the exam hall is too big for one person. To use this project you need to use two python interpreters: version 2.7 for the Nao Robot module and version 3.6 or higher for the Invigibot module.

## Module 1: Invigibot
This module is responsible for monitoring examinees and detecting cheating behaviours and communicating the detecting behaviour to the NaoRobot module. This is achieved through head pose tracking as well speech recognition and TCP/IP communication. Requirements for this module include:
* Python interpreter v3.6 or higher
* Libraries:
  * socket
  * threading
  * time
  * cv2
  * mediapipe 
  * numpy
  * random
  * speech_recognition
* Hardware:
  * 1 Camera
  * 1 Microphone

## Module 2: NaoRobot
This module is responsible for making the Nao robot (real or virtual) move or speak according to the instructions received from Invigibot through TCP/IP. 
Requirements for this module include:
* Python interpreter v2.7 (for naoqi)
* Libraries:
  * naoqi
  * socket 
  * threading
  * time
  * pyaudio (only for virtual agent)
  * wave (only for virtual agent)

## Nao Robot
The Nao robot is the chosen form of output for this project. You can either use the physical Nao robot if available or the virtual agent. The virtual agent requires the Choregraphe software. The difference in coding between the robot and virtual agent is that the virtual agent does not have a text-to-speech feature. Hence, the spoken statements are recorded as WAV files and stored to be played instead. That explains the need for the pyaudio and wave libraries. In both cases, the **IP address** needs to be set in the robo_main.py file to communicate with the robot effectively. 

## Running 
To run this project, you need to:
1. run the NaoRobot/robo_main.py file first to run the server and allow the invigilator to introduce itself
2. run the Invigibot/main.py file so the invigilator can calibrate the allowed head motion for the examinees before starting their exam
3. run the Invigibot/listen.py file
Now all of these files should be running simultaneously. 
