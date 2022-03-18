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

- Legislative solutions are slow, expensive and require many people in order for them to gain momentum and, even then, can fail easily. Right to repair, for example, is a movement that's gained more traction over the last year, but it's not a new debate.
- Fault injection can be a very reliable way (citation?) to put a microcontroller into a debugging state, which allows the full extraction of application firmware.
- Voltage glitching is an inexpensive and quickly repeatable fault injection method when compared to invasive methods such as using laser or UV-C light.

## Success criteria

I wanted to see if the same "crowbar" technique, where the CPU voltage is momentarily shorted to ground, applied in stacksmashing's (AKA Thomas Roth) video and LimitedResults' blog post could be easily replicated and applied to another family of microcontrollers.

Previously, my success criteria were very focussed on successfully glitching then dumping the firmware of the nRF52832 and the CC2541.
Since then, they have changed to be more oriented around learning about the process of investigation and the various activities that need to be executed to give the best chance of finding a security vulnerability, should one exist.

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

Tried on the GIAnT - took a long time to understand how to connect everything for what I wanted to do and understanding the API. David made a change to the GIAnT code which allowed the "crowbar" approach the DnD used, and I implemented it and submitted example code which is now in the repo, for the nRF52832. It worked!

GIAnT has many more features than the Debug'n'Dump, thanks to its use of more circuits, and an FPGA.
Initially it was set up for a different type of voltage glitch, but David made a change to the FPGA code to utilise a transistor, which I soldered to the board, to short a pin to ground (the "crowbar").
After learning more about the Python library to configure my glitching application, I created and ran my application, which targeted a critical section identified by LimitedResults and confirmed by Thomas Roth.

### Video voice-over

This is the setup:

- a Raspberry Pi Model 3 acting as the main computer, sending commands to both the GIAnT and nRF52832.
- the GIAnT, a platform for the implementation analysis of embedded devices, powering
- an nRF52832 chip, the same as you'd see in an Apple AirTag.

Play the video.

The terminal window you'll see on the right is from my laptop, where I've SSH'd into the Pi to run the attack.
The application that I've started on the Pi configures the GIAnT's glitching parameters.
The glitch offset is configured to glitch the CPU of the nRF chip at around the same offset as the flash memory activity, which includes when the readout protection data is copied.

You can see on the oscilloscope that the GIAnT keeps shorting the CPU of the nRF chip to ground momentarily, at an increasing offset after the chip has started.
It repeats each glitch a few times, and with multiple pulse widths, to increase the likelihood of a successful glitch.

Once this memory copy is successfully glitched, the application on the Pi stops running, and a dump of the nRF52832's firmware is left in the working directory.

### Returning to the Debug'n'Dump

In the meantime, Thomas Roth had responded to my issue on GitHub, blaming a resistor of the incorrect spec, which apparently served a minor purpose and could be removed.
After removing it, I quickly got the glitch to work successfully.

## Glitching the CC2541

I haven't managed to, but I've learned a lot along the way and my method was as follows.
Say where you got inspiration for your method, citations.

### Connecting the CC2541

### Observations

Analysed the behaviour of the CC Debugger and the CC2541 during various tasks, such as flipping the debug lock bit and reading the info page from the CC2541.
Identified potential critical sections to glitch, and brute-forced that space.

### Glitch attempts

### DPA

Hasn't really worked, say why and whether it'd be practical or likely to help if completed properly.

## What I'd have done differently

## What I've learned along the way
