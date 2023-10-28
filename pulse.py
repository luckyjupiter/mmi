import tkinter as tk
from tkinter import Canvas
import os
from sys import platform
from ctypes import *
import time

# List of connected devices with serial numbers (key) and descriptions (value)
devices = {}

def load_library():
    # Load the MeterFeeter library
    global METER_FEEDER_LIB
    if platform == "linux" or platform == "linux2":
        # Linux
        METER_FEEDER_LIB = cdll.LoadLibrary(os.getcwd() + '/libmeterfeeder.so')
    elif platform == "darwin":
        # OS X
        METER_FEEDER_LIB = cdll.LoadLibrary(os.getcwd() + '/libmeterfeeder.dylib')
    elif platform == "win32":
        # Windows
        METER_FEEDER_LIB = cdll.LoadLibrary(os.getcwd() + '/meterfeeder.dll')
    METER_FEEDER_LIB.MF_Initialize.argtypes = c_char_p,
    METER_FEEDER_LIB.MF_Initialize.restype = c_int
    METER_FEEDER_LIB.MF_GetNumberGenerators.restype = c_int
    METER_FEEDER_LIB.MF_GetBytes.argtypes = c_int, POINTER(c_ubyte), c_char_p, c_char_p,
    METER_FEEDER_LIB.MF_RandUniform.argtypes = c_char_p, c_char_p
    METER_FEEDER_LIB.MF_RandUniform.restype = c_double

    # Make driver initialize all the connected devices
    global med_error_reason
    med_error_reason = create_string_buffer(256)
    result = METER_FEEDER_LIB.MF_Initialize(med_error_reason)
    print("MeterFeeder::MF_Initialize: result: " + str(result) + ", error (if any): ", med_error_reason.value)
    if (len(med_error_reason.value) > 0):
        exit(result)

def get_devices():
    # Get the number of connected devices
    numGenerators = METER_FEEDER_LIB.MF_GetNumberGenerators()
    print("MeterFeeder::MF_GetNumberGenerators: " + str(numGenerators) + " connected device(s)")

    # Get the list of connected devices
    generatorsListBuffers = [create_string_buffer(58) for i in range(numGenerators)]
    generatorsListBufferPointers = (c_char_p*numGenerators)(*map(addressof, generatorsListBuffers))
    METER_FEEDER_LIB.MF_GetListGenerators(generatorsListBufferPointers)
    generatorsList = [str(s.value, 'utf-8') for s in generatorsListBuffers]
    print("MeterFeeder::MF_GetListGenerators: Device serial numbers and descriptions:")
    for i in range(numGenerators):
        kvs = generatorsList[i].split("|")
        devices[kvs[0]] = kvs[1]
        print("\t" + str(kvs[0]) + "->" + kvs[1])

class RandomWalkBiasAmplifier:
    def __init__(self, bound):
        self.bound = bound
        self.counter = 0

    def process_bit(self, bit):
        if bit == 1:
            self.counter += 1
        else:
            self.counter -= 1

        if self.counter >= self.bound:
            self.counter = 0
            return 1
        elif self.counter <= -self.bound:
            self.counter = 0
            return 0

        return None

class QuantumPulse:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Pulse")
        self.canvas = Canvas(self.root, bg="white", height=400, width=400)
        self.canvas.pack(pady=20)
        
        self.rwba = RandomWalkBiasAmplifier(5)

        self.pulse()

    def pulse(self):
        # Get a random frequency using MeterFeeder, taking the first device in the list (if multiple devices connected)
        firstDevice = next(iter(devices))
        frequency = METER_FEEDER_LIB.MF_RandUniform(firstDevice.encode("utf-8"), med_error_reason)
        print("MeterFeeder::MF_RandUniform: result: " + str(frequency) + ", error (if any): ", med_error_reason.value)
        
        # Apply bias amplification
        bit = int(frequency > 0.5)
        bias = self.rwba.process_bit(bit)
        if bias is not None:
            if bias == 1:
                frequency += 0.05
            else:
                frequency -= 0.05

        # Ensure frequency is within bounds
        frequency = max(0.1, min(0.9, frequency))

        # Draw the pulsating circle
        self.canvas.delete("circle")
        radius = 50 + (frequency * 100)
        self.canvas.create_oval(200-radius, 200-radius, 200+radius, 200+radius, fill="blue", tags="circle")

        # Schedule the next pulse
        self.root.after(int(1000 * frequency), self.pulse)

if __name__ == "__main__":
    load_library()
    get_devices()

    root = tk.Tk()
    app = QuantumPulse(root)
    root.mainloop()
