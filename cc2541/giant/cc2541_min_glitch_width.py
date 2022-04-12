import time
import serial as ser
import uu
from glitcher import glitcher
import logging
from fpga import *
from gpio import gpio
import subprocess


width = 50 # Change width until the glitch is successful


def cc_reset():
    output = subprocess.check_output(
        ["cc-tool", "--reset"],
        stderr=subprocess.STDOUT
    )
    if "No target" in str(output):
        raise Exception("Target not found")


def main():
    logging.basicConfig(level = logging.INFO)

    gl = glitcher()
    gl.reset_fpga() 
    gl.dac.setTestModeEnabled(0)
    gl.dac.setRfidModeEnabled(0)
    
    io = gpio()

    io.setPinMux(GPIO_Pins.GPIO6.value, GPIO_Select_Bits.FI_EXTERNAL_TRIGGER_IN.value)
    io.updateMuxState()

    gl.dac.setTriggerEnableState(Register_Bits.FI_TRIGGER_CONTROL_EXT1.value, True)
    gl.dac.setTriggerOnFallingEdge(True)

    offset = 7100000
    offset_step = 50000

    # Both fault voltage and normal voltage are 3.3V.
    # We want the fault on T1, not on DAC power.
    gl.set_voltages(3.3, 3.3, 0)
    
    for offset in range(offset, offset * 2, offset_step):
        print("Attempting to glitch...")
        print("w = {:d}, o = {:d}".format(width, offset))
        time.sleep(0.05)
        
        # Clean up any previous pulses
        gl.dac.clearPulses()

        # Set a pulse
        gl.add_pulse(offset, width)
        
        # Arm the fault
        gl.dac.arm()
        
        # Reset uc. This will also trigger the glitch
        cc_reset()
        time.sleep(0.5)
    
    gl.close()


if __name__=="__main__":
    main()
