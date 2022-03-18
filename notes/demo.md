---
geometry: margin=1in
---

# Preparatory notes

## To do list for demo:

- Record video of glitching nRF chip
- Compile list of things I think Andrew will want to hear
- Write a shortlist for progress on the TI CC chip
- Talk about what I've learned so far
- Light, structural slides

## General structure:

- What the challenges have been, how I have approached them and why I chose those methods (think "related works", here).
- What I've learned, and am proud of (this is really important, there's a lot to be proud of, even if it's not a scientific contribution).
- What I would do differently.
- Success criteria and how they've changed.
- How I've followed a well-motivated and structured procedure.

## Challenges, in chronological order:

- Replicating stacksmashing's glitch on the nRF52832:
  - Tried on the Debug n Dump - didn't work, the glitch was showing but not shorting to ground or having any effect.
  - Tried on the GIAnT - took a long time to understand how to connect everything for what I wanted to do and understanding the API. David made a change to the GIAnT code which allowed the "crowbar" approach the DnD used, and I implemented it and submitted example code which is now in the repo, for the nRF52832. It worked!
  - I'd submitted an issue on the DnD repo and Thomas Roth (stacksmashing) responded, blaming a resistor of the incorrect spec, which apparently served a minor purpose and could be removed. I quickly got it to glitch successfully for the nRF52832 after removing said resistor. This was the last thing I did on the nRF52832, just before the Christmas holiday.
- Glitching the CC2541
  - Haven't managed to, but the following happened along the way.
  - Referring to the Data Sheet and User Guide throughout.
  - Hooked up wires, got CC Debugger connected and cc-tool working.
  - Analysed the behaviour of the CC Debugger and the CC2541 during various tasks, such as flipping the debug lock bit and reading the info page from the CC2541.
  - Identified potential critical sections to glitch, and brute-forced that space.
  - DPA to try and shed some light on it. Hasn't really worked, say why and whether it'd be practical or likely to help.
- All of the things I've had to learn how to use:
  - Absorbed loads of information from data sheets.
  - Two glitching kits, with different approaches (microcontroller, simple and FPGA, complex)
  - OpenOCD, GDB, cc-tool (which I also opened up to modify, fruitlessly), sdcc, etc.
  - Using an oscilloscope, reading data from an oscilloscope programmatically (!) (and show example output)
  - Understanding the inner workings of two different microcontrollers
- Running out of time and things I'd like to do.
  - Glitch VCC
  - Old RAM clearing vulnerability.

# Speaker notes

## Background

<!-- Breeze through this, you don't have long -->

Embedded systems based around microcontrollers are in everything now, from watches to washing machines.
Microcontroller firmware is often protected from being read by the consumer with code readout protection (CRP), usually in the form of disabling debugging access to the microcontroller.
This means that independent security researchers can't easily assess the firmware for security vulnerabilities and consumers of many IoT devices are left with e-waste they can't repurpose when the manufacturer goes bankrupt and can no longer provide them with the service they paid for.

There are many ways that this situation can be avoided, but I've been looking into fault injection methods to bypass the CRP and dump the firmware, specifically voltage injection.
Why?
Because:

- Legislative solutions are slow, expensive and require many people in order for them to gain traction and, even then, can fail easily. Right to repair, for example, is a movement that's gained more traction over the last year, but it's not a new debate, and I think it highlights the difficulty of this route.
- Fault injection can be a very reliable way (citation?) to put a microcontroller into a debugging state, which allows the full extraction of application firmware.
- Voltage glitching is an inexpensive and quickly repeatable fault injection method when compared to invasive methods such as using laser or UV-C light.

## Success criteria

I wanted to see if the same "crowbar" technique, where the CPU voltage is momentarily shorted to ground, applied to the nRF52 series in Thomas Roth's (AKA stacksmashing) video and LimitedResults' blog post could be easily replicated and applied to another family of microcontrollers.

Previously, my success criteria were very focussed on successfully glitching then dumping the firmware of the nRF52832 and the CC2541.
Since then, they have changed to be more oriented around learning about the process of investigation and the various activities that need to be executed to find a voltage glitch security vulnerability, should one exist.

The roadmap in my proposal and last inspection presentation was ambitious in terms of timing, especially for the CC2541, which---to my knowledge---has no documented voltage glitch attack of the kind I wish to carry out.

## Glitching nRF52832

There have been many challenges throughout my project, out of which have come many learning experiences.

### First attempt with the Debug'n'Dump

The Debug'n'Dump is a product created by Thomas Roth to make voltage glitching using the "crowbar" method straightforward.
It's a board based around the Raspberry Pico.

I spent a week or so getting everything set up and learning about flashing the Pico.
It didn't seem to have any effect on the nRF52832, but I was blind to what was happening without an oscilloscope.
I acquired an oscilloscope from David Oswald, and observed that there was just a tiny pulse where the glitch should happen; it wasn't shorting.
After creating an issue on the airtag-glitcher GitHub repo, documenting my findings, I moved on to using David's own FPGA-based glitching board, the GIAnT, to replicate the attack.

### Using GIAnT

GIAnT has many more features than the Debug'n'Dump, thanks to its use of more circuits, and an FPGA.
Initially it was set up for a different type of voltage glitch, but David made a change to the FPGA code to utilise a transistor, which I soldered to the board, to short a pin to ground (the "crowbar").
After learning more about the Python library to configure my glitching application, I created and ran this application, which targeted a critical section identified by LimitedResults and confirmed by Thomas Roth.

There's a demonstration of the setup running successfully in the video on the next slide.

### Video voice-over

This is the setup:

- a Raspberry Pi Model 3 acting as the main computer, sending commands to both the GIAnT and nRF52832.
- the GIAnT, a platform for the implementation analysis of embedded devices, powering
- an nRF52832 chip, the same as you'd see in an Apple AirTag.

Play the video.

The terminal window you'll see on the right is from my laptop, where I've SSH'd into the Pi to run the attack.
The application that I've started on the Pi configures the GIAnT's glitching parameters.
The glitch offset is configured to glitch the CPU of the nRF chip at around the same offset as what is assumed to be flash memory activity, which includes when the readout protection data is copied.

You can see on the oscilloscope that the GIAnT keeps shorting the CPU of the nRF chip to ground momentarily, at an increasing offset after the chip has started.
It repeats each glitch a few times, and with multiple pulse widths, to increase the likelihood of a successful glitch.

Once this memory copy is successfully glitched, the application on the Pi stops running, and a dump of the nRF52832's firmware is left in the working directory.

### Returning to the Debug'n'Dump

In the meantime, Thomas Roth had responded to my issue on GitHub, blaming a resistor of the incorrect spec, which apparently served a minor purpose and could be removed.
After removing it, I quickly got the glitch to work successfully.

## Glitching the CC2541

I haven't managed to, but I've learned a lot along the way and this section covers my methods.
In many respects, I've followed in the footsteps of methods outlined in Fill your Boots and SiLabs C8051F34x code protection bypass, with "On the susceptibility of Texas Instruments SimpleLink platform microcontrollers to non-invasive physical attacks" more recently affirming these methods. (that was arm-based, which most of the newer CC chips are, whereas this was 8051).

### Connecting the CC2541

The setup here is similar to that of the nRF52832, but with a CC Debugger instead of the ST-LINK V2.
If powering the CC2541 from the GIAnT, which is needed for properly turning it off and on (cold boot) rather than resetting, the CC Debugger's voltage sense pin needs to also be connected to VCC and the power supply for the adapter board turned off in order for the CC Debugger to communicate with the CC2541.

### Observations

After connecting everything, the first thing I did was use the oscilloscope to monitor the behaviour of the CC Debugger and the CC2541 during various tasks, such as setting the debug lock bit and reading the info page from the CC2541.
Looking at the CPU voltage trace, I then identified potential critical sections to glitch.

Those critical sections were:

- Immediately after a "cold boot" and just before the application starts visibly executing,
- While the chip is under reset (the CPU doesn't really do anything here as far as I can tell, though),
- As the chip comes out of reset and immediately after.

### Glitch attempts

I've noticed in the cases of after reset and on a cold boot, that there is no section of different CPU activity before the application starts running.
I assume this is because there's no boot loader, which means there's no logic run by the CPU for checking the readout protection state that I can actually glitch.

This was confirmed by my systematic glitching at increased offsets in those areas and observing the outcomes.
I knew that the glitch I was applying should cause some different behaviour, because it would cause instructions to be skipped in the test application I was running.
Glitching the critical sections saw no change in the outcome.
Drifting too far towards reads and writes over USB did cause a change, but it was always just a crash due to the data returned to the CC Debugger being zeroed.

### DPA

To make sure there wasn't anything I'd missed, I carried out differential power analysis on those critical sections.
This was in order to highlight any differences between CPU activity with and without CRP enabled, to see if there were any areas I could glitch.
I've had issues collecting enough traces for this, as it takes a very long to transfer data from the oscilloscope I have to the Pi or my laptop; I can only capture about one trace every 18 minutes, and I need hundreds or ideally thousands, before I can see any results.
Comparing by eye so far, however, I've seen no significant differences in CPU voltage traces between CRP enabled and disabled.

## What I'd have done differently

For some things, it's hard to say, because I've learned a lot for the first time in this project.
Generally speaking, and knowing what I know now, it would have been better to identify whether there was any bootloader code I could have targeted before blindly glitching critical sections (although this glitching didn't take long).
I would also have attempted DPA earlier on, but I did not know what the bottlenecks were, so it could have really slowed down the project if I had.

I'd have set my success criteria from the start to be more focussed on learning, rather than trying to successfully glitch a chip I had very little information about at the time.

If I had more time, I would have worked on compiling a more conclusive differential power analysis.
I also would have tried glitching the main voltage for the CC2541 to see if I could set bits.
David also brought to my attention an old vulnerability with the CC2430, to see whether it still applied to the CC2541, which I would have also liked to investigate.

## What I've learned along the way

I've had to learn a lot, about a domain I initially knew nothing about, during this project.

I've absorbed lots of information from various data sheets to understand the inner workings of two different microcontrollers, learned how to use two glitching kits which have different approaches, various software and APIs to communicate with a number of devices.
Using an oscilloscope was something I'd never done before, let alone read data from one programmatically.

I'm quite pleased to have chosen this project because, although I haven't managed to get the achievement of finding a security vulnerability, I have much more knowledge than when I started.
