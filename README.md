# Gauss-Siedel-Value-Iteration

You are the CTO of a new startup company, SpeedRacer, and you want your autonomous cars to navigate throughout the city of Los Angeles. The cars can move North, South, East, or West. The city can be represented in a grid, as below:
<br>
![image](https://user-images.githubusercontent.com/42768898/50745636-328da180-11e0-11e9-84bf-b74ad6563cef.png)

There will be some obstacles, such as buildings, road closings, etc. If a car crashes into a building or road closure, SpeedRacer has to pay $100. You also spend $1 for gas when at each grid location along the way. The cars will start from a given SpeedRacer parking lot, and will end at another parking lot. When you arrive at your destination parking lot, you will receive $100. Your goal is to make the most money over time with the greatest likelihood. Your cars have a faulty turning mechanism, so they have a chance of going in a direction other than the one suggested by your model. They will go in the correct direction 70% of the time, with a 10% chance of going in each of the other three directions instead.
<br>
The first part of your task is to design an algorithm that determines where your cars should try to go in each city grid location given your goal of making the most money. Then, to make sure that this is a good algorithm when you present it to the rest of your board, you should simulate the car moving through the city grid. To do this, you will use your policy from your start location. You will then check to see if the car went in the correct direction using a random number generator with specific seeds to make sure you can reproduce your output. You will simulate your car moving through the city grid 10 times using the random seeds 1, 2, 3, 4, 5, 6, 7, 8, 9, and 10. You will report the mean over these 10 simulations as an integer after using the floor operation (e.g., numpy.floor(meanResult)). An example of this process is given in detail below.
<br><br>
<b>Input:</b> The file input.txt in the current directory of your program will be formatted as follows:<br>
First line: strictly positive 32-bit integer s, size of grid [grid is a square of size sxs]<br>
Second line: strictly positive 32-bit integer n, number of cars<br>
Third line: strictly positive 32-bit integer o, number of obstacles<br>
Next o lines: 32-bit integer x, 32-bit integer y, denoting the location of obstacles<br>
Next n lines: 32-bit integer x, 32-bit integer y, denoting the start location of each car<br>
Next n lines: 32-bit integer x, 32-bit integer y, denoting the terminal location of each car<br>
<br>
<b>Output:</b><br>
n lines: 32-bit integer, denoting the mean money earned in simulation for each car, integer result of floor operation<br>
<br>
<b>Example:</b><br>
<b>Input.txt</b><br>
3<br>
1<br>
1<br>
0,1<br>
2,0<br>
0,0<br><br>
<b>Output.txt</b><br>
95

![image](https://user-images.githubusercontent.com/42768898/50745649-42a58100-11e0-11e9-9e5e-6254cd6e772d.png)
<br>
Standard rounding rules apply. (draw random sample from a distribution: if value is <= 0.7 make the correct transition, otherwise randomly pick uniformly alternative direction) (rounding) Some code demonstrating how to do this is given below:<br>
<img src="https://user-images.githubusercontent.com/42768898/50745651-4507db00-11e0-11e9-978f-60fe18bb10ef.png" width="500">
