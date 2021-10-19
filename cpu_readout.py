import os
import time

from gpiozero import CPUTemperature
#get temp
def gettemp():
    while True:
        
        global cpu_temp
        cpu = CPUTemperature()
        cpu_temp = cpu.temperature
        print('CPU Temp')
        print(cpu_temp)
        time.sleep(2)
        os.system("clear")
gettemp()
