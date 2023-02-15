# Lab 2

## Serial Communication with Proportional Controlled Motor

### By: Benny Cruz, Arfan Ansar, Noah Johnson

The closed loop controller implemented in our design is a classic
proportional control. The proportional controller takes the current
position of the motor and finds the difference between this value and
the value that the motor is set to rest at. This difference is
multiplyed by a constant value (A proportion) that determines how much
the motor should actuate or move to get to the desired final position.

The desired response of a proportional controller is one without too
much overshoot [^1] and with a small settling time. [^2]

We find these metrics by recording the time at intervals and the
cooresponding position of the motor and graphing these. In our
experiment we first graphed a response with large overshoot which
resulted in ringing. We then found a slow response time where the
settling time was large and did not reach the desired position quickly.
After testing these scenarios we then set out to find the best of both
worlds, with small overshoot, little ringing, and a fast settling time.

[^1]: (Overshoot is when the motors position goes over the desired
    position).

[^2]: (Settling time is the amount of time the motor takes to reach rest
    at the desired position)

![Optimal_Response](Optimal_Response.png)

![Slow_Settling](Slow_Settling.png)

![Ringing_Response](Ringing_Response.png)
