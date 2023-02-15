"""!
@file Serial_Reader.py
This file contains the code which sends to the microcontroller the Proportional Control value inputted by the user
This file also reads the cooresponding data from the motor which was output from the microcontroller to the computer
using the ST_Link. This data is processed and results are graphed in this file.

TODO: N/A 

@author Mech-07
@date   2-Jan-2023 SPL Original file
@copyright (c) 2023 by Mech-07 and released under GNU Public License v3
"""
import serial
import matplotlib.pyplot as plt
import time

def main():
    """!
    Main code of program which first waits for a user input 'Kp' Value which is converted to a byte and sent to
    the microcontroller to be used.
    It then waits for the cooresponding data to be sent using the serial connection. Once it reads its data, it
    parses and organizes the data into cooresponding time and positon values. When 'end' is sent from the
    microcontroller it then graphs this data using matplotlib.pyplot library
    
    @param   Always when run as "__main__"
    @returns none
    """
    
    #opens serial connection as s_port and waits for user input which is then sent to the microcontroller
    with serial.Serial ('COM6', baudrate=115200, timeout=1000) as s_port:
        input1 = input('kp Value ')
        input1 = bytes(input1, 'utf-8')
        s_port.write(input1)
    
    #initilize data arrays for time and position to be saved to
    x_data = []
    y_data = []
    
    #reopens the serial connection as s_port
    with serial.Serial ('COM6', 115200) as s_port:
        while (True):
            #in this loop it reads data and converts it into an array with position 0 having the time data and
            #position 1 having the position data
            data_array = []
            data = s_port.readline() 
            data_array.append(data.strip().split(b",")) #split the comma seperated value sent in and remove new line
            if data_array[0][0] == b'end':#if end is transmitted break out
                break
            try:
                #turn data into a float - if error dont append either to the data arrays
                x_data_float = float(data_array[0][0]) 
                y_data_float = float(data_array[0][1])
                x_data.append(x_data_float)
                y_data.append(y_data_float)
            except ValueError: #check value error
                continue
            except IndexError: #check index error
                continue
            except UnicodeError: #check unicode error 
                break
    
    #use matplotlib to plot the data as time vs position. Label the plot and axis and show this plot
    plt.plot(x_data, y_data)
    plt.suptitle('Slow Settling Response')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.show()

# The following code only runs if this file is run as the main script;
# it does not run if this file is imported as a module
if __name__ == "__main__":
    main()