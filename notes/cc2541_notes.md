# Connecting the CC Debugger

The breakout board has UART but I don't seem to be getting anything back from it.
[This website](http://www.martyncurrey.com/bluetooth-modules/) seems to have some info on these kinds of boards but I'm not getting any UART response.

## Observations

Using a Pi Zero (over SSH from my laptop) as the UART sender to the CC2541 board doesn't get any response.
The CC Debugger won't connect to UART anyway, so I need to find a way to connect DD (Debug Data) to P2_1, DC (Debug Clock) to P2_2 and RESETn to RESETn.
I'm assuming, for now, that the main VCC and GND pins on the breakout board will suffice for power and ground connections to the chip.

Some legs on the chip look bridged: AVDD1, AVDD2 and AVDD4, according to the datasheet.
Unless I can find a reason to think this was deliberate, I may try to clean these up if the CC Debugger still can't talk to the CC2541 once I've connected it.

There are 34 pads around the main board which the CC2541 is situated on, and 40 pins on the actual chip.
If the pins I need for debugging have continuity with the pads on the central breakout board, I'll solder to the pads around the edge of the board.
This will make sure that I'm less likely to make a mistake, because the pads are larger and further apart than the legs of the chip.

I soldered to the pads I'd found that are connected to the necessary legs for debugging, plugged these into the CC Debugger and I'm getting a solid light, which is a good sign.

## CC Tool

I needed some software to allow my laptop to communicate with the CC Debugger; the software that TI provides doesn't support Linux and is proprietary.
I got cc-tool from [here](https://github.com/dashesy/cc-tool) because it has a fix for the issue with the original's `./configure`.
I installed cc-tool but it doesn't detect a target. I'll try with a Windows VM first.

It turns out that I hadn't turned the adapter board for the CC Debugger on.
After turning it on I get a solid red light, which means "no device detected", but cc-tool now sees a target: CC2540.
cc-tool also tells me that the target is locket and "No operations allowed on locked target without erasing".
The main concern I have is that it's detected a CC2540 rather than CC2541 (I know it's a CC2541 because it's etched onto the top of the chip).
This may mean that the Debugger firmware is out of date.
I'll try again on Windows.

SmartRF Studio 7 on Windows also detects the target as CC2540.
Assuming everything else is fine, this should be too; [TI states that](https://www.ti.com/lit/ug/swru270c/swru270c.pdf?ts=1642609030440) the "main difference between the CC2540 and CC2541 is a peripheral hardware change; Where CC2540
has a USB interface, the CC2541 has an I2C interface" and "lower power consumption".

### Original Image

Without glitching, I couldn't read the original image because the chip was locked:

```
$ cc-tool -r original_image.bin
  Programmer: CC Debugger
  Target: CC2540
  Target is locked.
  No operations allowed on locked target without erasing
```

I wanted to go through the process of locking first and making sure that everything was connected properly before trying to glitch and unlock, so I erased it:

```
$ cc-tool -e
  Programmer: CC Debugger
  Target: CC2540
  Target is locked.
  Erasing flash...
  Completed   
```

Reading its MAC addresses and info page now works!

```
$ cc-tool -a
  Programmer: CC Debugger
  Target: CC2540
  MAC addresses, primary: 5C:F8:21:EB:A4:EA, secondary: FF:FF:FF:FF:FF:FF
```

```
$ cc-tool -i
  Programmer: CC Debugger
  Target: CC2540
  Reading info page...
  Completed (0.94 s.)
  Information page (2048 B):
CC03008D17FFFFFF01010101FFFFEAA4EB21F85CFFFFFFFFFFFFFFFF961759083217586C7FFC695C
2EDCFB00170865E814A85BA00007070B00050657FFFFFFFFFFFFFFFFFFFFFFFFE53D6ECAC53D62BE
B53DE2B9A53DCEB3853DF4A7753DC8A1653D209B553D0093F51A7BD7F53DC8D2F5659FCAF53D7FD2
D53DBBC3953DABAC453DF589353DBD80253DB57A153D9372053DB16BFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFA3275FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFF00000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000
```

You can see its MAC address bytes backwards (little endian) in the above dump: `EAA4EB21F85C`.

```
$ cc-tool --test
  Programmer: CC Debugger
  Target: CC2540
  Device info: 
   Name: CC Debugger
   Debugger ID: 0100
   Version: 0x05CC
   Revision: 0x0044

  Target info: 
   Name: CC2540
   Revision: 0x22
   Internal ID: 0x8D
   ID: 0x2540
   Flash size: 256 KB
   Flash page size: 2
   RAM size: 8 KB
   Lock data size: 16 B
```

And, the following locks debug access:

```
$ cc-tool --lock debug
  Programmer: CC Debugger
  Target: CC2540
  Lock data: FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F
  Writing  lock data...
  Completed

$ cc-tool -r out.bin
  Programmer: CC Debugger
  Target: CC2540
  Target is locked.
  No operations allowed on locked target without erasing
```

Gaining debug access is all that's needed to remove any other flash or page locks (see "Lock Bits" below).

## Lock Bits

From [section 3.4.1 "Lock Bits"](https://www.ti.com/lit/ug/swru191f/swru191f.pdf).
The main purpose of locking flash pages is to "prevent erroneous code from unintentionally altering code or constraints", and the debug lock is for disabling all debug commands apart from CHIP_ERASE, READ_STATUS (for reading the debug status byte), and GET_CHIP_ID.
The debug bit is bit 127 in the "upper available flash page".

Looking at how `cc-tool` sets the debug lock bit, we can see an example of what's stated in the mentioned section:

```
Lock data: FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F      # 128 bits
In binary: 11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111101111111
Logical in binary: 11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110
```

The last bit, bit 127, is set to 0, to disable debug commands.
Note that in ["25.3.3 RAM-Based Registers" of the User Guide](https://www.ti.com/lit/ug/swru191f/swru191f.pdf), it says: "Where bit numbering is used, bit 0 is the LSB and bit 7 is the MSB. Multi-byte fields are little-endian".
So the more logical way of viewing the above is after reversing each byte, bit-wise.

Locking the first two pages (index starts at 0):

```
$ cc-tool -l pages:1
  Programmer: CC Debugger
  Target: CC2540
  Lock data: FDFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
  Writing  lock data...
  Completed


Lock data: FDFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
In binary: 11111101111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
Logical:  10111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
```

```
$ cc-tool -l pages:0
  Programmer: CC Debugger
  Target: CC2540
  Lock data: FEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
  Writing  lock data...
  Completed

Lock data: FEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
In binary: 11111110111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
Logical:  01111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
```

# What I need to work out

There are a few questions I need to answer in order to be more targeted in my approach:

- Whether changing VCC is a possible glitch or whether it needs to be directly on DCOUPL.
- Whether there's a memory copy of the debug lock bit before code execution, which can be glitched.
- Whether there's a some kind of software check of the debug lock bit in the embedded bootloader, which can be glitched to skip when making specific requests to the chip.

To analyse what the MCU does, I'll be following a few experiments from [here](https://github.com/debug-silicon/C8051F34x_Glitch).

I was struggling to use the BLE stack examples without IAR Workbench using SDCC.
Standard I/O examples work with the library found [here](https://github.com/Grapsus/cc254x_sdcc), however.

## Planned approach to find glitch

Connect glitch wire to DCOUPL first; can always experiment with VCC later (different shapes to see if there's an effect), but due to the voltage regulator, glitching directly on DCOUPL is likely to be the straightforward way to glitch.
I'll try to apply a "crowbar" technique on the decoupling circuit, similar to the nRF chip, to glitch.

1. Long-glitch to see if the chip resets.
2. Glitch a "normal" program to see if it can be done without resetting.
3. Basic DPA between unlocked and locked after reset and communication.
4. Try different signals on VCC to see if it can be done without shorting DCOUPL. Do this only if successful on DCOUPL.


