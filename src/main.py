"""!
@file main.py
    This file contains two tasks that involve setting up encoders and motor drivers.
    It allows for both motors to be proportionally controlled while the code is being run
    through the use of generator object and task priority and sequencing. Main file for
    lab 3

TODO: N/A

@author Mech-07 and JR Ridgely
@date   10-Feb-2023
@copyright (c) 2023 by Mech-07 and JR Ridgely and released under GNU Public License v3
"""

import gc
import pyb
import cotask
import task_share

import utime

import motor_driver    #Classes we have written for driving the motor and reading the encoder
import encoder_reader
import porportional_controller


def task1_fun(shares):
    """!
    Task sets up the first motor and encoder and runs a proportional
    controller with a set position on this motor. 
    @param shares A list holding the share and queue used by this task
    """ 
    #Encoder initializing. Includes defining the timer and the pins for our encoder class
    pinB6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
    pinB7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
    timer = pyb.Timer(4, prescaler=0, period=0xFFFF)
    ch1 = timer.channel (1, pyb.Timer.ENC_AB, pin=pinB6)
    ch2 = timer.channel (2, pyb.Timer.ENC_AB, pin=pinB7)
    
    #calling the encoder class, then calling the zero() function to zero the encoder
    encode = encoder_reader.Encoder(pinB6, pinB7, timer, ch1, ch2)
    encode.zero()
    
    #Motor driver initializing. Includes defining pin and setting up the PWM timer
    pinB4 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    timer = pyb.Timer (3, freq=10000)
     
    #calling the motor driver class and giving the object name "moe"
    moe = motor_driver.MotorDriver(pinA10,pinB4,pinB5, timer)
    
    controller = porportional_controller.PorportionalController(.025)
    
    
    inittime = utime.ticks_ms()
    
    
    while True:
        position = encode.read() #find current position
        control_output = controller.run(20000, position) #run control

        print(control_output)
        moe.set_duty_cycle(control_output) #set the duty cycle to value found from control
        
        time = utime.ticks_ms() - inittime #find the current time
        pos = position #find the current position
        
        timedata = time 
        posdata = pos
        u2.write(f'{timedata},{posdata}\r\n') #send data to computer 
    
        yield 0 #return nothing


def task2_fun(shares):
    """!
    Task sets up a second motor and encoder and runs a proportional
    controller with a set position on this motor. 
    @param shares A list holding the share and queue used by this task
    """ 
    pinC6 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
    timer8 = pyb.Timer(8, prescaler=0, period=0xFFFF)
    ch1 = timer8.channel (1, pyb.Timer.ENC_AB, pin=pinC6)
    ch2 = timer8.channel (2, pyb.Timer.ENC_AB, pin=pinC7)
    
    #calling the encoder class, then calling the zero() function to zero the encoder
    encode2 = encoder_reader.Encoder(pinC6, pinC7, timer8, ch1, ch2)
    encode2.zero()
    
    #Motor driver initializing. Includes defining pin and setting up the PWM timer
    pinA0 = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    pinA1 = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    timer5 = pyb.Timer (5, freq=10000)
     
    #calling the motor driver class and giving the object name "moe"
    moe2 = motor_driver.MotorDriver(pinC1,pinA0,pinA1, timer5)
    
    controller2 = porportional_controller.PorportionalController(.025)
    
    while True:
        position2 = encode2.read() #find current position
        control_output2 = controller2.run(-30000, position2) #run controller 

        #print(control_output2)
        moe2.set_duty_cycle(control_output2) 

        yield 0 #return nothing

    
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=25,
                        profile=True, trace=False, shares=(share0, q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=25,
                        profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()
    
    
    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    
    #set up UART and send the data to the computer 
    u2 = pyb.UART(2, baudrate=115200, timeout= 50)
    
    i=0
    while i < 3000:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break
        i += 1
    
    #send end to computer when data sent 
    u2.write(f'end,end\r\n')
    
    # Print a table of task data and a table of shared information data
    #print('\n' + str (cotask.task_list))
    #print(task_share.show_all())
    #print(task1.get_trace())
    #print('')