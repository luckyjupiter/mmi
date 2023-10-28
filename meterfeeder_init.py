import os
from sys import platform
from ctypes import *

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