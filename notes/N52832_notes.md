# Resources

- [nRF52832 Datasheet](https://infocenter.nordicsemi.com/pdf/nRF52832_PS_v1.4.pdf)
- [Pico Debug'n'Dump Info](https://pdnd.stacksmashing.net/)
- [ARMv7-M Architecture Reference Manual](https://developer.arm.com/documentation/ddi0403/d?lang=en)

# Wiring

| DnD          | nRF      | ST-LINK | Why                                   |
|--------------|----------|---------|---------------------------------------|
| Trig         | VCC      |         | Provides 1.8V and starts the nRF      |
| Glitch       | CPU Regu.|         | Sends a glitch voltage to the CPU     |
| GND(glitcher)| GND      |         | Grounds the nRF                       |
| In 0         | GND      |         | The DnD checks this to see if nRF on  |
|              | SWDIO    | SWDIO   | Serial wire debug IO to/from ST-LINK  |
|              | SWCLK    | SWCLK   | Serial wire clock                     |


To make sure the nRF chip and breakout board work, I assumed that code readout protection (CRP) was off, and connected it up to the ST-LINK. Using the constant 1.8V power supply from the DnD to the nRF and only the SWDIO and SWCLK pins on the nRF to the ST-LINK (the ST-LINK was supplied 3.3V), I've managed to power up the nRF chip and access it using `openocd`:

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

The **UICR (base addr. 0x10001000) register *APPROTECT* (addr. offset 0x208) is used to enable access port protection**.
Any value other than 0xFF will enable the protection.

# Bootloader location

| Usage                               | Memory range nRF52832 (S132 v6.0.x) |
| ----------------------------------- | ----------------------------------- |
| Bootloader settings                 | 0x0007 F000 - 0x0008 0000 (4 kB)    |
| MBR parameter storage               | 0x0007 E000 - 0x0007 F000 (4 kB)    |
| Bootloader                          | 0x0007 8000 - 0x0007 E000 (24 kB)   |
| Application area (incl. free space) | 0x0002 0000 - 0x0007 8000 (352 kB)  |
| SoftDevice                          | 0x0000 1000 - 0x0002 6000 (148 kB)  |
| Master Boot Record (MBR)            | 0x0000 0000 - 0x0000 1000 (4 kB)    |
