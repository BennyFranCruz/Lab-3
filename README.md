# Lab 3

## Time Scheduled Multitasking

### By: Benny Cruz, Arfan Ansar, Noah Johnson

We began by downloading the cotask, taskshare, and basic task files
from the ME 405 support repository on Github.

Similar to lab 2 we run the motor task and pint the results and
plot the step response. The task is continuously run at a slower 
and slower rate until the controller's performance has significantly
gotten worse compared to the optimal response. This is done to choose
an optimal run rate for the motor control task. The plots for both
the .....response and .....response can be seen below.

A task was created to run two motors simultaneously under closed-loop
control. This test program moves the motors different distances and holds
them at the desired positions.

![Slower_Rate_with_Bad_Response](Slower Rate with Bad Response.png)
![Slower Rate with Bad Response](https://user-images.githubusercontent.com/123694704/219268876-45f0ce7a-a916-47ad-aac4-bf969f6a9482.png)

![Slowest_Rate_for_Good_Response](Slowest Rate for Good Response.png)
![Slowest Rate for Good Response](https://user-images.githubusercontent.com/123694704/219268935-c93f4b3b-67dd-4689-9a36-fa8834603b16.png)
