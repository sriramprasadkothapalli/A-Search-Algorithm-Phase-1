README for A* Algorithm Pathfinding
This project implements A* algorithm to find the shortest path between two points in a given obstacle environment. The algorithm visualizes the pathfinding process and the final path.

Dependencies
To run this code, you will need Python installed on your system along with the following libraries:

NumPy
Matplotlib
OpenCV-Python
Shapely  (for defining hexagon as obstacle in the region)
You can install these dependencies via pip:
pip install numpy matplotlib opencv-python shapely


Running the Code
Open a Terminal or Command Prompt.

Navigate to the directory containing the script. If your script is in a folder called "A_star_Pathfinding" on your desktop, you would use a command like:
cd Desktop/A_star_Pathfinding


Providing Inputs
After running the script, you will be prompted to enter the start and goal coordinates in the terminal or command prompt. Here's the format you should follow:
Enter Robot radius(5mm) : Enter 5mm as the radius of the robot
Enter clearance value(5mm) : Enter 5mm as the clearance value 
Enter x co-ordinate of start position: Enter the X-coordinate of the start position and press Enter.
Enter y co-ordinate of start position: Enter the Y-coordinate of the start position and press Enter.
Enter start angle (theta) : Enter the theta value and press ENTER 
Enter x co-ordinate of goal position: Enter the X-coordinate of the goal position and press Enter.
Enter y co-ordinate of goal position: Enter the Y-coordinate of the goal position and press Enter.
Enter step length(L) 1-10: ENter the step length   

EXAMPLE Input
Enter x co-ordinate of start position: 220
Enter y co-ordinate of start position: 480
Enter start angle (theta): 30
Enter x co-ordinate of goal position: 1150
Enter y co-ordinate of goal position: 20
End point angle (theta): 30
Enter the step size (L): 10


OUTPUT
The program visualizes the exploration process and the final path.





Github repo for the project
https://github.com/sriramprasadkothapalli/A-Star-Search-Algorithm-Phase-1
