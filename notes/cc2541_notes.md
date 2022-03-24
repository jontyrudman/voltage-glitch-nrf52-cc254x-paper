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

When attaching the glitch wire to DCOUPL, I won't remove the $1\mu~F$ capacitor yet, as it may not prevent me from shorting to ground in a reliable quick time.

## Observations

Using basically the same code as for the nRF52832 and the giant plugged into the CC2541 VCC, there is a problem: the CC Debugger still trickles power to the chip through DC, DD, RST.
cc-tool also fails to detect target, which we need to check if the chip is unlocked.
I'll need to connect VCC on the CC2541 to the CC Debugger and only use RST to the giant.

With the following setup, applying a glitch during test_blink_state.c would skip either the delay (the state would switch immediately) or the XOR of P0_2 (skipping the switch of state).
Success with this model for glitching instructions! (TODO: insert scope images).

Even with a very wide glitch (TODO: measurement needed), it won't reset.

### The Setup

- RST on CC2541 to GPIO1_6 on giant (acts as trigger) and RST on CC Debugger.
- DCOUPL on CC2541 to T1 on giant (short with a transistor).
- VCC on CC2541 to VCC on CC Debugger adapter board.
- GND on CC2541 to GND on CC Debugger adapter board.
- DD on CC2541 to DD on CC Debugger adapter board.
- DC on CC2541 to DC on CC Debugger adapter board.

I've had issues with the CC Debugger not seeing the target if plugged into the giant for resetting.
It turns out that the CC Debugger is fine as long as it's also connected to RST and the giant has pulled RST high.
This allows the CC Debugger to pull RST low, making it detect the target properly.
Correction: it doesn't seem to reset in this configuration because it doesn't get RST completely to 0; the application keeps running.

Any operation with `cc-tool` tells us whether the chip is locked, even reading the info page:

```
$ cc-tool -i
  Programmer: CC Debugger
  Target: CC2540
  Target is locked.
  No operations allowed on locked target without erasing
```

We can use this as a CRP check when glitching.

Using `cc-tool --reset` takes about 15ms, so the glitch offset needs to take this into account.

Annoyingly, `cc-tool -i` also produces the same reset pattern, so the glitch occurs again.
Even using just `cc-tool` resets the chip.
There's a good chance I'll have to disarm the glitcher before checking the CRP.
No, that's silly, because any reset will have reset the CRP anyway; we need to not reset at all to keep CRP change intact.

Even just logging `cc-tool` and no operations with `cc-tool --log`, shows the resets (reset target):

```
[16.02 12:09:07:72777] main, cc-tool 0.26
[16.02 12:09:07:72777] main, command line: cc-tool --log 
[16.02 12:09:07:72786] usb, open device, VID: 0451h, PID: 16A2h
[16.02 12:09:07:72786] usb, set configuration 1
[16.02 12:09:07:72796] usb, claim interface 0
[16.02 12:09:07:72797] usb, get string descriptor 2, data: CC Debugger
[16.02 12:09:07:72797] programmer, request device state
[16.02 12:09:07:72797] usb, control read, request_type: C0h, request: C0h, value: 0000h, index: 0000h, count: 8
[16.02 12:09:07:72797] usb, control read, data: 40 25 CC 05 44 00 01 00
[16.02 12:09:07:72797] device, name: CC Debugger, ID: 0100, version: 05CCh, revision: 0044h
[16.02 12:09:07:72797] programmer, set debug interface speed 0
[16.02 12:09:07:72797] usb, control write, request_type: 40h, request: CFh, value: 0001h, index: 0000h, count: 0
[16.02 12:09:07:72797] programmer, connect target
[16.02 12:09:07:72797] programmer, enter debug mode
[16.02 12:09:07:72797] usb, control write, request_type: 40h, request: C5h, value: 0000h, index: 0000h, count: 0
[16.02 12:09:07:72798] usb, control write, request_type: 40h, request: C8h, value: 0001h, index: 0000h, count: 48
[16.02 12:09:07:72798] usb, control write, data: 43 43 32 35 34 30 20 20 20 20 20 20 20 20 20 20 44 49 44 3A 20 30 31 30 30 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
[16.02 12:09:07:72798] programmer, reset target, debug mode: 1
[16.02 12:09:07:72798] usb, control write, request_type: 40h, request: C9h, value: 0000h, index: 0001h, count: 0
[16.02 12:09:07:72809] programmer, read debug status
[16.02 12:09:07:72809] usb, bulk write, count: 2, data: 1F 34
[16.02 12:09:07:72809] usb, bulk read, count 1: data: 26
[16.02 12:09:07:72809] programmer, debug status, 26h
[16.02 12:09:07:72809] programmer, target is locked
[16.02 12:09:07:72809] main, start task processing
[16.02 12:09:07:72809] main, finish task processing
[16.02 12:09:07:72809] programmer, reset target, debug mode: 0
[16.02 12:09:07:72809] usb, control write, request_type: 40h, request: C9h, value: 0000h, index: 0000h, count: 0
```

It's very unlikely that CRP will stay off after reset if glitched successfully, so I'll need to edit the source of `cc-tool` to add a `--no-reset` option.

`CC_Unit_Driver::reset()` is called from `CC_Programmer::unit_connect()`, `CC_Programmer::unit_reset()` and `CC_Programmer::unit_close()`.
I'm not sure why it's trying to write anything because there's an early return in `CC_Flasher::process_tasks()` if `--erase` isn't passed and the device is locked, which is checked early.

I added the `--no-reset` parameter to `cc-tool` but it then can't enter debug mode.
Sifting through the User Guide reveals something I should've seen earlier in section 3.1:

"Debug mode is entered by forcing two falling-edge transitions on pin P2.2 (debug clock) while the RESET_N input is held low.
When RESET_N is set high, the device is in debug mode.
On entering debug mode, the CPU is in the halted state with the program counter reset to address 0x0000.
While in debug mode, pin P2.1 is the debug-data bidirectional pin, and P2.2 is the debug-clock input pin."

That explains why `cc-tool` always causes two dips in RESET_N: enabling and disabling debug mode requires the chip to be reset (while P2.2 receives two falling-edge transitions).
Maybe this is the critical section I need to glitch?
Debug mode is a state that the chip needs to be put in during a reset, and it remains in debug mode until reset again.
This means that, if I can glitch the chip while it's under reset and being put into debug mode, only the operation I want cc-tool to complete will be run before resetting again (unless I make `--enter-debug` and `--exit-debug` parameters to use with `--no-reset` for subsequent commands to avoid leaving debug mode)

It makes sense that, unlike the nRF52832 which can continue running normally in debug mode, the CC2541 should come out of debug mode immediately, as the program is always halted in debug mode.

Now all I'm doing is glitching from the first time RESET_N is pulled low (during `unit_connect()`) and until RESET_N is pulled low again (during `unit_close()`), which reduces the search space to 10ms.
This is based on the assumption that there is an instruction we can skip either while debug mode is being enabled or when the check of the lock occurs.

At about 3.5ms after the first falling edge, I get errors of `cc-tool` crashing.
I can't seem to unlock it during the reset.
Also at 4.5ms.

At 6.85ms I got the following:
```
Attempting to glitch...
w = 1800, o = 6910000, repeat = 1
b'  Programmer: CC Debugger\n  Target: CC2540\n  Target does not reading Info Page\n'
```
and it stopped.
Got it again at 6.94ms on another run.

It means the target does not support reading the info page, which only happens in `cc-tool`, which shows some response is wrong.
I need to only stop when I hit "Reading info page..." to make sure I only get the intended glitch.
This is observed to happen in when the last of the three sections of CPU activity is glitched, causing it to extend indefinitely.
The first two sections of activity are common on other operations, like erase.

I need to record the logs for the `cc-tool` crashes to see more of what happens before the crash, but it's likely that the chip becomes unresponsive during communication.

What we're looking for is something similar to the debug lock info in the following log:

```
[17.02 20:52:09:55375] main, cc-tool 0.26
[17.02 20:52:09:55376] main, command line: ./cc-tool -i --log 
[17.02 20:52:09:55385] usb, open device, VID: 0451h, PID: 16A2h
[17.02 20:52:09:55385] usb, set configuration 1
[17.02 20:52:09:55393] usb, claim interface 0
[17.02 20:52:09:55394] usb, get string descriptor 2, data: CC Debugger
[17.02 20:52:09:55394] programmer, request device state
[17.02 20:52:09:55394] usb, control read, request_type: C0h, request: C0h, value: 0000h, index: 0000h, count: 8
[17.02 20:52:09:55395] usb, control read, data: 40 25 CC 05 44 00 01 00
[17.02 20:52:09:55395] device, name: CC Debugger, ID: 0100, version: 05CCh, revision: 0044h
[17.02 20:52:09:55395] programmer, set debug interface speed 0
[17.02 20:52:09:55395] usb, control write, request_type: 40h, request: CFh, value: 0001h, index: 0000h, count: 0
[17.02 20:52:09:55395] programmer, connect target
[17.02 20:52:09:55395] programmer, enter debug mode
[17.02 20:52:09:55395] usb, control write, request_type: 40h, request: C5h, value: 0000h, index: 0000h, count: 0
[17.02 20:52:09:55395] usb, control write, request_type: 40h, request: C8h, value: 0001h, index: 0000h, count: 48
[17.02 20:52:09:55395] usb, control write, data: 43 43 32 35 34 30 20 20 20 20 20 20 20 20 20 20 44 49 44 3A 20 30 31 30 30 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
[17.02 20:52:09:55396] programmer, reset target, debug mode: 1
[17.02 20:52:09:55396] usb, control write, request_type: 40h, request: C9h, value: 0000h, index: 0001h, count: 0
[17.02 20:52:09:55407] programmer, read debug status
[17.02 20:52:09:55407] usb, bulk write, count: 2, data: 1F 34
[17.02 20:52:09:55407] usb, bulk read, count 1: data: 22
[17.02 20:52:09:55407] programmer, debug status, 22h
[17.02 20:52:09:55407] programmer, write debug config, 22h
[17.02 20:52:09:55407] usb, bulk write, count: 3, data: 4C 1D 22
[17.02 20:52:09:55407] programmer, read xdata memory at 6276h, count: 2
[17.02 20:52:09:55407] usb, bulk write, count: 47, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 62 76 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:09:55410] usb, bulk read, count 2: data: 4C 07
[17.02 20:52:09:55410] programmer, read xdata memory, data: 4C 07
[17.02 20:52:09:55410] programmer, read xdata memory at 6249h, count: 1
[17.02 20:52:09:55410] usb, bulk write, count: 41, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 62 49 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:09:55413] usb, bulk read, count 1: data: 22
[17.02 20:52:09:55413] programmer, read xdata memory, data: 22
[17.02 20:52:09:55413] programmer, read xdata memory at 624Ah, count: 1
[17.02 20:52:09:55413] usb, bulk write, count: 41, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 62 4A 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:09:55416] usb, bulk read, count 1: data: 8D
[17.02 20:52:09:55416] programmer, read xdata memory, data: 8D
[17.02 20:52:09:55416] target, name: CC2540, chip ID: 8Dh, rev. 22h, flash: 256, ram: 8, flags: 07h
[17.02 20:52:09:55416] main, start task processing
[17.02 20:52:09:55416] programmer, check if unit locked
[17.02 20:52:09:55416] programmer, read debug status
[17.02 20:52:09:55416] usb, bulk write, count: 2, data: 1F 34
[17.02 20:52:09:55418] usb, bulk read, count 1: data: 22
[17.02 20:52:09:55418] programmer, debug status, 22h
[17.02 20:52:09:55418] programmer, read info page
[17.02 20:52:09:55418] programmer, read xdata memory at 7800h, count: 128
[17.02 20:52:09:55418] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 78 00 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:09:55477] usb, bulk read, count 128: data: CC 03 00 8D 17 FF FF FF 01 01 01 01 FF FF EA A4 EB 21 F8 5C FF FF FF FF FF FF FF FF 96 17 59 08 32 17 58 6C 7F FC 69 5C 2E DC FB 00 17 08 65 E8 14 A8 5B A0 00 07 07 0B 00 05 06 57 FF FF FF FF FF FF FF FF FF FF FF FF E5 3D 6E CA C5 3D 62 BE B5 3D E2 B9 A5 3D CE B3 85 3D F4 A7 75 3D C8 A1 65 3D 20 9B 55 3D 00 93 F5 1A 7B D7 F5 3D C8 D2 F5 65 9F CA F5 3D 7F D2 D5 3D BB C3 95 3D AB AC
[17.02 20:52:09:55477] programmer, read xdata memory, data: CC 03 00 8D 17 FF FF FF 01 01 01 01 FF FF EA A4 EB 21 F8 5C FF FF FF FF FF FF FF FF 96 17 59 08 32 17 58 6C 7F FC 69 5C 2E DC FB 00 17 08 65 E8 14 A8 5B A0 00 07 07 0B 00 05 06 57 FF FF FF FF FF FF FF FF FF FF FF FF E5 3D 6E CA C5 3D 62 BE B5 3D E2 B9 A5 3D CE B3 85 3D F4 A7 75 3D C8 A1 65 3D 20 9B 55 3D 00 93 F5 1A 7B D7 F5 3D C8 D2 F5 65 9F CA F5 3D 7F D2 D5 3D BB C3 95 3D AB AC
[17.02 20:52:09:55477] programmer, read xdata memory at 7880h, count: 128
[17.02 20:52:09:55477] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 78 80 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:09:55537] usb, bulk read, count 128: data: 45 3D F5 89 35 3D BD 80 25 3D B5 7A 15 3D 93 72 05 3D B1 6B FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF A3 27 5F FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:09:55537] programmer, read xdata memory, data: 45 3D F5 89 35 3D BD 80 25 3D B5 7A 15 3D 93 72 05 3D B1 6B FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF A3 27 5F FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:09:55537] programmer, read xdata memory at 7900h, count: 128
[17.02 20:52:09:55537] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 79 00 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:09:55597] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:09:55598] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:09:55598] programmer, read xdata memory at 7980h, count: 128
[17.02 20:52:09:55598] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 79 80 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:55658] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55658] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55658] programmer, read xdata memory at 7A00h, count: 128
[17.02 20:52:10:55658] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7A 00 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:55718] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55718] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55718] programmer, read xdata memory at 7A80h, count: 128
[17.02 20:52:10:55718] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7A 80 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:55778] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55778] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55778] programmer, read xdata memory at 7B00h, count: 128
[17.02 20:52:10:55778] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7B 00 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:55838] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55838] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55838] programmer, read xdata memory at 7B80h, count: 128
[17.02 20:52:10:55838] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7B 80 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:55898] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55898] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55898] programmer, read xdata memory at 7C00h, count: 128
[17.02 20:52:10:55899] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7C 00 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:55959] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55959] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:55959] programmer, read xdata memory at 7C80h, count: 128
[17.02 20:52:10:55959] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7C 80 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:56019] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56019] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56019] programmer, read xdata memory at 7D00h, count: 128
[17.02 20:52:10:56019] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7D 00 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:56079] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56079] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56079] programmer, read xdata memory at 7D80h, count: 128
[17.02 20:52:10:56079] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7D 80 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:56139] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56139] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56139] programmer, read xdata memory at 7E00h, count: 128
[17.02 20:52:10:56139] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7E 00 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:56199] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56199] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56199] programmer, read xdata memory at 7E80h, count: 128
[17.02 20:52:10:56199] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7E 80 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:56260] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56260] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56260] programmer, read xdata memory at 7F00h, count: 128
[17.02 20:52:10:56260] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7F 00 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:56320] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56320] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
[17.02 20:52:10:56320] programmer, read xdata memory at 7F80h, count: 128
[17.02 20:52:10:56320] usb, bulk write, count: 803, data: 40 55 00 72 56 E5 92 BE 57 75 92 00 74 56 E5 83 76 56 E5 82 BE 57 90 7F 80 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4E 55 E0 5E 55 A3 4F 55 E0 5E 55 A3 D4 57 90 C2 57 75 92 90 56 74
[17.02 20:52:10:56380] usb, bulk read, count 128: data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF E1 C1 FF FF 22 18 91 56 B4 0A 94 1C AA 55 AA 55
[17.02 20:52:10:56380] programmer, read xdata memory, data: FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF E1 C1 FF FF 22 18 91 56 B4 0A 94 1C AA 55 AA 55
[17.02 20:52:10:56381] main, finish task processing
[17.02 20:52:10:56381] programmer, reset target, debug mode: 0
[17.02 20:52:10:56381] usb, control write, request_type: 40h, request: C9h, value: 0000h, index: 0000h, count: 0
```

Specifically, a debug status of 22h rather than 26h.
On `cc-tool` crashes, I've noticed it's 00h and then "halt failed", presumably because debug lock isn't really off.
I've also noticed with these that on the scope, which is hard to freeze at the right point in time, the CPU basically dies and its voltage stays at ground.
Maybe the pulse width is too large (18000 and 19000).
I'll reduce it to 1000-1200 in the hope that it doesn't happen so much.
Doesn't seem to make much difference.

Next steps:

- Look into logs for the info page glitch. See below, done.
- Glitch on a flash read rather than info page (target the read activity).
- Glitch on cold boot, in case there's any debug lock setup there. There is much more interesting activity on cold boot (see pic, connected to CC Debugger at the time). So far, I'm fairly sure nothing glitchable is happening under reset.
- Perform DPA on both reset to debug mode 1 and cold boot.

## CPU Activity Pulses

When reading the info page, the following USB activity takes place:

1. A write, under reset.
2. A write then read to read the debug status.
3. Bulk write then bulk read to read the info page.

I think the 3rd section of CPU activity is for processing that last point.
Also, if I'm going to glitch that last section, I have to do it for every read in the bulk read, which is a pain.

Sometimes I get the following in that 3rd section of CPU activity:

```
Attempting to glitch...
w = 1000, o = 7050000, repeat = 2
b'  Programmer: CC Debugger\n  Target: CC2540\n  Target does not reading Info Page\n'
[21.02 12:54:51:17157] main, cc-tool 0.26
[21.02 12:54:51:17157] main, command line: cc-tool -i --log 
[21.02 12:54:51:17166] usb, open device, VID: 0451h, PID: 16A2h
[21.02 12:54:51:17166] usb, set configuration 1
[21.02 12:54:51:17175] usb, claim interface 0
[21.02 12:54:51:17176] usb, get string descriptor 2, data: CC Debugger
[21.02 12:54:51:17176] programmer, request device state
[21.02 12:54:51:17176] usb, control read, request_type: C0h, request: C0h, value: 0000h, index: 0000h, count: 8
[21.02 12:54:51:17176] usb, control read, data: 40 25 CC 05 44 00 01 00
[21.02 12:54:51:17176] device, name: CC Debugger, ID: 0100, version: 05CCh, revision: 0044h
[21.02 12:54:51:17176] programmer, set debug interface speed 0
[21.02 12:54:51:17176] usb, control write, request_type: 40h, request: CFh, value: 0001h, index: 0000h, count: 0
[21.02 12:54:51:17176] programmer, connect target
[21.02 12:54:51:17176] programmer, enter debug mode
[21.02 12:54:51:17176] usb, control write, request_type: 40h, request: C5h, value: 0000h, index: 0000h, count: 0
[21.02 12:54:51:17177] usb, control write, request_type: 40h, request: C8h, value: 0001h, index: 0000h, count: 48
[21.02 12:54:51:17177] usb, control write, data: 43 43 32 35 34 30 20 20 20 20 20 20 20 20 20 20 44 49 44 3A 20 30 31 30 30 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
[21.02 12:54:51:17177] programmer, reset target, debug mode: 1
[21.02 12:54:51:17177] usb, control write, request_type: 40h, request: C9h, value: 0000h, index: 0001h, count: 0
[21.02 12:54:51:17188] programmer, read debug status
[21.02 12:54:51:17188] usb, bulk write, count: 2, data: 1F 34
[21.02 12:54:51:17188] usb, bulk read, count 1: data: 26
[21.02 12:54:51:17189] programmer, debug status, 26h
[21.02 12:54:51:17189] programmer, target is locked
[21.02 12:54:51:17189] main, start task processing
[21.02 12:54:51:17189] programmer, check if unit locked
[21.02 12:54:51:17189] programmer, read debug status
[21.02 12:54:51:17189] usb, bulk write, count: 2, data: 1F 34
[21.02 12:54:51:17189] usb, bulk read, count 1: data: 23
[21.02 12:54:51:17189] programmer, debug status, 23h
[21.02 12:54:51:17189] main, finish task processing
[21.02 12:54:51:17189] programmer, reset target, debug mode: 0
[21.02 12:54:51:17189] usb, control write, request_type: 40h, request: C9h, value: 0000h, index: 0000h, count: 0
```

I can get it to say the debug status is 23h (useless to me), but that doesn't mean it actually is, so even if I got it to say 22h, when `cc-tool` tries to move forward it will fail because the lock is still on.

I get much more frequent debug status glitches with the longer pulse widths, with a wider range of debug statuses returned (TODO: Expand, need stats).

David has also given me some info about another avenue to try (TODO):
"If you trigger a flash erase and overwrite to disable CRP but do not reset/power cycle afterwards, it will keep RAM contents".

# Differential Power Analysis

I've managed to, with some tweaks, use x's code for reading values from the DS1074Z scope to perform DPA on the section with the reset followed by command execution from cc-tool.
I also want to perform DPA on a cold boot to look for differences.
This is difficult because I need to be able to turn the chip on and off, so it needs to be connected to giant DAC (USB power toggle is notoriously messy and I don't have the tools right now).
While the DAC is on, the CC Debugger connects to the chip fine, but the CC Debugger is giving power to the CPU over the reset wire, which would mess up results.
Without the reset wire being connected to the CC Debugger, the CC Debugger won't recognise anything.

Or I could wire up a custom USB cable with VCC and GND breakouts and be done with it?
Nope, just looked at the CC Debugger instructions and I can connect VCC from the target (and giant) to the target voltage sense pin, and turn off the power from the adapter board (to stop it sending power over RST)!
Now, when the giant DAC is on, CC Debugger detects the target and cc-tool works normally, and when it's off it doesn't detect the target.
This works as long as the CC Debugger is manually reset with its button when the CC2541 is receiving power, and the CC Debugger is not then later manually reset while the CC2541 is off.

TODO: Add picture of wiring setup.
TODO: Add picture of cold boot.
TODO: Add pictures of DPA graphs.

I've been told by David to improve DPA with two things (TODO):

- Align all the traces before averaging based on common features (spike when reset pulled high) to make sure nothing is cancelled out and cycles are aligned.
- Record many more traces (think 1000s and 10000s).

Most of my power traces were using giant to supply power to the CC, which was unnecessary as I wasn't glitching, so there's a lot of noise for no reason...

# Glitching a cold boot

I'm using cold boot to describe starting with the chip completely off (VCC = 0V), rather than resetting while the chip is receiving power.
I hoped that it would be similar to the nRF52832, where I could glitch a memory copy of the lock status.
After DPA and brute forcing the whole search space of the first x ms of cold boot with the "crowbar" on CPU power with no unique output, I don't think it's possible to do here.

# 15 March Update

This morning I learned a few things...

- CC was getting power from the giant for all my traces so far, adding unnecessary noise.
- I still hadn’t tried removing the decoupling capacitor, which made a huge difference to the trace on the scope
- I was slightly too forceful when removing the capacitor, thought everything was fine and then realised the wire I’d connected had pulled off the pad. I managed to attach it to the DCOUPL leg though

David also sent me [this paper](https://eprint.iacr.org/2022/328.pdf), outlining a glitching campaign on ARM Cortex-based CC SoCs.

I don't believe there's a bootloader hidden on the CC2541, for the following reasons:

- It's not mentioned in the User Guide or the Data Sheet.
- Without an application flashed, there is no CPU activity (TODO: Capture this).
- No time difference between CRP enabled and disabled (TODO: Capture this).
- The CC Debugger is required for flashing the chip, unless your own serial or BLE OTA bootloader is present in the flash.
