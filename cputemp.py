from gpiozero import CPUTemperature
#get temp
async def gettemp():
    global cpu_temp
    cpu = CPUTemperature()
    cpu_temp = cpu.temperature
    return cpu_temp
