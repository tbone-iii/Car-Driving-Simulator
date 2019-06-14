# Car-Driving-Simulator
Basic simulation of a car based on the Ackermann steering model.

<h1> Getting Started </h1>
These instructions will help you get the program running.

<h2> Prerequisites </h2>
Requires the following external modules in Python 3.7+: <br>
<pre><code>pygame
pathlib </code></pre>
This can be possibly be done with the following commands:

<pre><code>> pip3 install pygame
> pip3 install pathlib </code></pre>

<h2> Installation </h2>
Download all the files and run the "main_game.py" file to begin the top-down simulation.

<h1> Details </h1>

Click to play video of a demo: <br>
<a href="https://giant.gfycat.com/ThriftyAnguishedCoral.webm">
<img alt="Thumbnail" src="https://raw.githubusercontent.com/tbone-iii/Car-Driving-Simulator/master/Video/video%20screenshot.png" width="400" height="400">
</a>

<h2> Physics </h2>
The car's steering angle is limited to the maximum centripetal acceleration allowable
before sliding begins. This is theoretically 1G (32.2 ft/s^2 or 9.80 m/s^2) if the coefficient
of static friction between the tires and the ground is 1. <br> <br>
The simulation automatically converts the English units provided to their pixel equivalents. The parameters of the car are defined in the <a href="https://github.com/tbone-iii/Car-Driving-Simulator/blob/master/car.py"> car.py </a> file. Such parameters include the car length (in feet), the maximum car tire steering angle, the braking power, the wheelbase, the 0 to 60 mph time. <br><br>

<h2> Control </h2>
Summary:
<pre><code>Up-Arrow:    Maximum throttle
Down-Arrow:  Brake
Left-Arrow:  Steer left
Right-Arrow: Steer right
Escape:      QUIT
F1:          Open console
D:           Toggle car information (technical info)
</code></pre>

To use the simulator, the up arrow key accelerates the car, the down arrow brakes the car, and the left and right arrows steer the car. Pressing "F1" opens the console menu, which shows input commands
that you can type to change parameters. For example, to increase the car's maximum speed, type in
"max_v_mph 89" to increase the maximum speed to 89 miles per hour. Escape closes the program completely.

<h1> Future Work </h1>
In the future, I would like to allow analog input by a remote controller's analog stick. By switching to analog input, the steering angle would neither have to be limited nor computationally increased/decreased according to the player input. Additionally, I would like to update the visuals, include obstacles and collision detection, and add skidding to the simulation. Another capability to add is selecting "predetermined" cars whose values have already been determined via testing in real-world experiments. This could be done by shifting the built-in car values from the <a href="https://github.com/tbone-iii/Car-Driving-Simulator/blob/master/car.py"> car.py </a> file to an external save file of some sort.<br><br>
Note that some of the code will require slight refactoring to permit these updates.

<h1> License </h1>
This project is licensed under the MIT License - see the <a href="https://github.com/tbone-iii/Car-Driving-Simulator/blob/master/LICENSE.md"> LICENSE.md </a>
file for details.