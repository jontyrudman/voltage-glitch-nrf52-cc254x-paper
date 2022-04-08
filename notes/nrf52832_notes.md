# Resources

- [nRF52832 Datasheet](https://infocenter.nordicsemi.com/pdf/nRF52832_PS_v1.4.pdf)
- [Pico Debug'n'Dump Info](https://pdnd.stacksmashing.net/)
- [ARMv7-M Architecture Reference Manual](https://developer.arm.com/documentation/ddi0403/d?lang=en)

# Wiring

| DnD          | nRF      | ST-LINK | Why                                   |
|--------------|----------|---------|---------------------------------------|
| Trig         | VCC      |         | Provides 3.3V and starts the nRF      |
| Glitch       | CPU Regu.|         | Sends a glitch voltage to the CPU     |
| GND(glitcher)| GND      |         | Grounds the nRF                       |
| In 0         | DEC4     |         | The DnD checks this to see if nRF on  |
|              | SWDIO    | SWDIO   | Serial wire debug IO to/from ST-LINK  |
|              | SWCLK    | SWCLK   | Serial wire clock                     |


To make sure the nRF chip and breakout board work, I assumed that code readout protection (CRP) was off, and connected it up to the ST-LINK. Using the constant 3.3V power supply from the DnD to the nRF and only the SWDIO and SWCLK pins on the nRF to the ST-LINK (the ST-LINK was supplied 3.3V), I've managed to power up the nRF chip and access it using `openocd`:

```
openocd -f interface/stlink.cfg -f testnrf.cfg -c "init;dump_image nrf52_dumped2.bin 0x0 0x1000; exit"
```

I've successfully loaded the dumped binary into Ghidra as **little endian thumb ARM Cortex** (M4) instruction set.

Next step is to find where I can connect a wire to the CPU power decoupler to provide the glitch voltage as outlined in stacksmashing's video.
This is so I only target the operation of the CPU, rather than the bluetooth core for example.
The QFN48 has four pins for supply decoupling:

- DEC1: 0.9V (digital supply)
- DEC2: 1.3V (radio supply)
- DEC3: for VDD
- DEC4: 1.3V (input from DC/DC reg., output from 1.3V LDO)

I'm assuming that I can glitch the CPU voltage using DEC1.
This also checks out with stacksmashing's video where he shows the CPU regulator as 0.9V.
There are several capacitors on the XL52832-D01 board, one of which appears to come directly out of DEC1 and this should provide a safe enough pad to solder a wire to.
I'm working under the assumption that this capacitor is for CPU voltage regulation.

# Using GDB on the nRF firmware

Run `openocd` without any commands and in another window run `gdb`.
Type the following in `gdb`:

```
tar ext :3333      # Connect to gdbserver hosted by openocd.
                   # Short for target extended-remote localhost:3333
monitor halt       # Halt execution.
                   # Can't reset because the reset is done through CTRL-AP
```

I prefer to open `gdb` using `-tui` so I can see the assembly.
Use `ni` and `si` to use next and step on purely the instructions, as this works without the symbols being loaded.
Jump and break at addresses by using `*` before the address.

# CTRL-AP (Control Access Port)

Custom access port that enables control of the device even if the other access ports in the Debug Access Port (DAP, which uses the SWDIO and SWDCLK lines) are being disabled by the access port protection.

It allows you to soft reset and disable access port protection.
Note that disabling access port protection through the CTRL-AP is done by issuing an ERASEALL command, **erasing the flash, UICR and RAM**.

# User Information Configuration Registers (UICR)

"The user information configuration registers (UICRs) are non-volatile memory (NVM) registers for configuring user specific settings."

## Writing

Write the same way as flash.
Configuration only effective after reset.
Can be written to **181 times before needing to use ERASEUICR or ERASEALL**.

# Enabling access port protection

To write to UICR, I need to write CONFIG.WEN.

The **UICR (base addr. 0x10001000) register *APPROTECT* (addr. offset 0x208) is used to enable access port protection**.
Any value other than 0xFF will enable the protection.

Done using `halt` and `flash fillw 0x10001208 0xFFFFFF00 0x01` over telnet.

# Bootloader location

| Usage                               | Memory range nRF52832 (S132 v6.0.x) |
| ----------------------------------- | ----------------------------------- |
| Bootloader settings                 | 0x0007 F000 - 0x0008 0000 (4 kB)    |
| MBR parameter storage               | 0x0007 E000 - 0x0007 F000 (4 kB)    |
| Bootloader                          | 0x0007 8000 - 0x0007 E000 (24 kB)   |
| Application area (incl. free space) | 0x0002 0000 - 0x0007 8000 (352 kB)  |
| SoftDevice                          | 0x0000 1000 - 0x0002 6000 (148 kB)  |
| Master Boot Record (MBR)            | 0x0000 0000 - 0x0000 1000 (4 kB)    |

# Running the glitch

I've enabled APPROTECT and now OpenOCD still dumps the firmware but it's an empty binary, so the check I now run to see if APPROTECT is on is if there are 0 breakpoints declared when running OpenOCD.
After a number of glitches using pyserial to send the commands to the pico, there is a serial write timeout on setting the delay.
This is the first step in glitching and when I disable the glitch command and just set delay and pulse, there is no problem.

I believe that in the `CMD_GLITCH` case, the following is looping forever:

```c
while(!gpio_get(1 + IN_NRF_VDD));
```

The above waits as long as the input pin for monitoring the nRF VDD is low.
It starts the glitch when the input pin is high.

I've found that this happens on the very first glitch and then it takes a while to fill up the pico's serial input buffer.
The power supply for the in/out pins must be off.

The **CPU clock speed is 64MHz**, which means likely 64000000 instructions every second.
I think the delay needs to start at 1.5ms.
An instruction takes $1.5625*10^{-8}$ seconds.

## Challenges

See above for the first major challenge.
The second is that, using the default parameters of 63000-84000 for delay and 7-8 for the pulse width, I haven't had any success or even differences in the openocd init messages.

I attached a wire to DEC4 and removed the capacitor after the wire on DEC1 to ensure that the glitch goes through fully but still haven't had any luck.
I'm trying 43000-63000 this time.

Now with the oscilloscope, I can see that my delay is far too big: pulses only seem to be occurring in every other power cycle.

## Observations

Pulses from the Glitch pin are around 450mV.
A pulse of 9 is about 0.8 microseconds.
A pulse of 30 is about 2 microseconds.
A delay of 0 can be about 20 ms into power on too.
A delay of 1000 is about 18-19 ms into power on.
A delay of 5000 is about 20 ms into power on.
A delay of 50000 is about 21.5 ms into power on.
A delay of 100000 is about 24.6 ms into power on.
150000 is about 29 ms.
200000 is about 33 ms.

The fuzzy activity before VCC is pulled low again is init OpenOCD.
These delays are too late for targeting the NVMC activity because the while loop for checking system power is taking too long.

The Glitch pin seems to have pretty much no effect on the CPU power.
I've observed that even when GPIO19 is pulled high, the mosfet doesn't allow flow from drain to source.
GPIO19 is 2.6V, not 3.3V, only due to its connection to the mosfet and resistors.
I know this because I tried using GPIO17 instead and it exhibited the same behaviour.
GlitchEn is connected directly to GPIO19 and comes before the current-limiting 100ohm resistor before the mosfet gate.
There is also a 100ohm resistor between the gate and ground.
The voltage on the gate never reads higher than 1.3V.

# Glitching Using GIAnT

I tried to use GIAnT, initially, to insert a glitch in the same manner as in previous examples for GIAnT: by connecting the DAC output to VCC on the nRF and lowering that to a fault voltage after an offset.
This is different to how the Debug'n'Dump was designed to work, where a constant voltage is applied on the VCC of the nRF chip and the glitch is done by a separate pin which momentarily shorts to ground.
This had no noticeable effect, presumably because the nRF's internal voltage regulators were smoothing out the voltage into the CPU, allowing it to continue functioning fairly normally.
I needed to target the CPU power regulator specifically and go back to the fault model used with the Pico Debug'n'Dump.

At that point, the GIAnT didn't have any means of shorting an input line to ground; it didn't have the MOSFET configuration the DnD has.
Luckily, the board was build with that kind of ability in mind for the future, with solder pads available for a resistor and MOSFET going to a pin on the board.
Adding the functionality involved updating the HDL to pull the trace going to the MOSFET gate high at the trigger point, and soldering a resistor and MOSFET to that trace.
David added HDL to do the inverse on an adjacent transistor, too.

The T1 output of GIAnT was then connected to the CPU power decoupler DEC1, where it could perform the same function as the Glitch pin on the Pico Debug 'n' Dump.
The trigger was set to be the DAC out being high (when the nRF is started) and then after the defined offset, the CPU power would be shorted to GND through T1.
To make sure the DAC power wouldn't be lowered at the glitch, the fault voltage was set to the same value as the standard voltage.

Shortly after starting the python script again with this configuration, I'd obtained debugging access and OpenOCD displayed "6 breakpoints".
Success!

## Retrospective Comments

For the most part, don't bother trying to calculate offset timings using expected cycles.
It's much easier to just use the oscilloscope, change the offset value and observe.
I did find targeting the critical section using GIAnT though, and it's worth checking in future whether the offset timings are even linear...
It's very hard to target a section based on its time after start up.

# Retry of Pico DnD

Write about the exchange on the GitHub issue.

I removed the culprit resistor and now it's properly shorting the CPU regulator.

- Using the system power into IN_0 on the DnD in order to satisfy breaking out of the while loop still seems to add a crazy long delay (measure this, but about 20ms); just remove the while loop altogether.

Talk about how the NVMC activity seems to jump around the fault. Why?

# Minimum glitch width experiment

Width of 1000ns causes the CPU to fail. Even 180 does that late in execution (for the NVMC glitch it's fine).
GIAnT has a min glitch width of 10ns.

Offset of 5ms causes it to break out of the while loop, minimum width 50ns.
Same with 8ms.

Maybe the reason it never skips a wiggle is because the skipping out of the delay subroutine puts the program counter into some other area of memory where nothing happens.
Whereas the CC2541 delay is just NOPs.
nrfx_coredep_delay_us is defined in modules/nrfx/soc/nrfx_coredep.h.

As low as 50 doesn't really work for the NVMC glitch, reason for success rates experiment.

Offset can change a bit based on environmental factors.
Can't really comment on success rates because the offset moves (so hard to be consistent), and in any given range it's only likely that there are a couple of places close together that the glitch will be successful in.
