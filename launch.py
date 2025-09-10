
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

greeting = "*************************************************\nHello Human Hands, I'm comin for y'all real soon.\n*************************************************\n"
print(greeting)

print(     "Press Ctrl + C to Exit.               -XXGurjot07\n")

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
print(f"Your Volume Range (dBs) - {volume.GetVolumeRange()}\n")


import main
detection1 = main.run_detection()


