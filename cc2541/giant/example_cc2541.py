"""
Applies a crowbar glitch to a CC2541 on DCOUPL,
triggered by a reset when cc-tool communicates.
Doesn't manage to bypass CRP, this code is for testing.
Requires cc-tool and a CC Debugger.

Wiring:

- DCOUPL to T1 on GIAnT
- VDD to GIAnT DAC out and CC Debugger voltage sense
- GND to GIAnT GND and CC Debugger GND
- RESET_N to CC Debugger RST
- Debug Data to CC Debugger Debug Data
- Debug Clock to CC Debugger Debug Clock
"""

import time
import serial as ser
import uu
from glitcher import glitcher
import logging
from fpga import *
from gpio import gpio
import subprocess
import os


def check_protected():
    """
    Returns True if the uc is still protected, or False if it isn't.

    Attempts to dump flash using cc-tool.
    """
    try:
        output = subprocess.check_output(
            ["cc-tool", "-f", "-r", "dump.bin", "--log"],
            stderr=subprocess.STDOUT
        )
        print(str(output))
        if "Target is locked." not in str(output) and os.path.exists("cc-tool.log"):
            with open("cc-tool.log", "r") as f:
                print(f.read())
        if "Reading info page..." in str(output):
            return False
    except Exception as e:
        print(e)
        if os.path.exists("cc-tool.log"):
            with open("cc-tool.log", "r") as f:
                print(f.read())
    return True


def main():
    logging.basicConfig(level = logging.INFO)

    gl = glitcher()
    gl.reset_fpga() 
    gl.dac.setTestModeEnabled(0)
    gl.dac.setRfidModeEnabled(0)
    
    io = gpio()

    # Muxes GPIO1_6 with FI_EXTERNAL_TRIGGER_IN and enables
    # the trigger for falling edge transitions (entering reset)
    io.setPinMux(GPIO_Pins.GPIO6.value, GPIO_Select_Bits.FI_EXTERNAL_TRIGGER_IN.value)
    io.updateMuxState()
    gl.dac.setTriggerEnableState(Register_Bits.FI_TRIGGER_CONTROL_EXT1.value, True)
    gl.dac.setTriggerOnFallingEdge(True)
    
    # Offsets
    offset_start = 1000
    offset_end = 8100000
    offset_step = 500
    
    w_start = 50
    w_end = 80
    w_step = 10
    
    # Repeat each attempt how many times?
    repeat = 2
    
    # Loop state
    run = True
    w = w_start
    offset = offset_start
    r = 0

    # Both fault voltage and normal voltage are 3.3V.
    # We want the fault on T1, not on DAC power.
    gl.set_voltages(3.3, 3.3, 0)
    gl.dac.setEnabled(True)

    while run:
        print("Attempting to glitch...")
        print("w = {:d}, o = {:d}, repeat = {:d}".format(w, offset, r))
        time.sleep(0.05)
        
        # Clean up any previous pulses
        gl.dac.clearPulses()
    
        # Set a pulse
        gl.add_pulse(offset, w)
        
        # Arm the fault
        gl.dac.arm()
        
        time.sleep(0.05)

        # The call to cc-tool will reset the CC2541, triggering the glitch
        protected = check_protected()
        
        if protected:
            print("Protected! Next parameter.")
            
            # Next param
            if r < repeat:
                r = r + 1
            elif w < w_end:
                r = 0
                w = w + w_step
            elif offset < offset_end:
                w = w_start
                offset = offset + offset_step
            else:
                w = w_start
                offset = offset_start
                r = 0
        else:
            print("Success!")
            run = False
    
    gl.close()


if __name__=="__main__":
    main()
