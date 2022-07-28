# Self-driving Car 
- A prototype system for driving a car automatically in lanes.
- The system consists of:
    - A prototype hardware for a car.
    - A simple piece of software presented in a mobile application for driving the car.
    - A server using computer vision that analyze the road, and conncets differnent system parts. 
## Mobile App
- Built using Flutter.
- Has two modes:
    - Manual mode: user may controll the movement of the car (forward, backwards, right, left or stop) through controllers in the app.
    - Automatic mode: uses mobile camera as a live stream to pictures of the road, sends these data to backend server that analyzes the road and move the car accordingly.
## Backend
- An api that receives the pictures from mobile app.
- A computer vision algorithm for lane detection using Python. Depending on the lane shape at each moment, the algorithm generates a direction for the car to move.
## Hardware
- Car chassis
- Four wheels
- 4 DC Motors
- Esp
- Arduino
