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

There are many ways that this can be remedied, but I've been researching fault injection methods to bypass the CRP and dump the firmware.
Specifically, using voltage injection.
Why?
Because:

- Legislative solutions are slow, expensive and require many people in order for them to gain traction and, even then, can fail easily. Right to repair, for example, is a movement that's gained more traction over the last year, but it's not a new debate, and I think that highlights the difficulty of this route.
- Fault injection can be a very reliable way (citation?) to put a microcontroller into a debugging state, which allows the full extraction of application firmware.
- Voltage glitching is an inexpensive and quickly repeatable fault injection method when compared to invasive methods such as using laser or UV-C light.

## Success criteria

Now, I don't have a full solution to that problem, but I see voltage glitching as a possible short term solution.
I wanted to add to the knowledge of which chips are vulnerable to these attacks, and judge how it might be made easier and more reliable to carry them out. <!-- answer this! -->

I also wanted to see if the same "crowbar" technique applied to the nRF52 series in Thomas Roth's (AKA stacksmashing) video and LimitedResults' blog post could be easily replicated and applied to another family of microcontrollers, the CC253x/4x series from Texas Instruments.
The "crowbar" technique involves momentarily shorting the CPU voltage to ground in order to miscalculate or skip an instruction.

Previously, my success criteria were very focussed on successfully glitching and then dumping the firmware of the nRF52832 and, later, the CC2541.
Since then, they have changed to be more oriented around learning about the process of investigation and the various activities that need to be executed to find a voltage glitch vulnerability, should one exist.

<!-- The roadmap in my proposal and last inspection presentation was ambitious in terms of timing, especially for the CC2541, which---to my knowledge---has no documented voltage glitch attack of the kind I wish to carry out. -->

## Glitching nRF52832

### First attempt with the Debug'n'Dump

The Debug'n'Dump is a product created by Thomas Roth (stacksmashing) to make voltage glitching using the "crowbar" method straightforward.

After flashing the glitching firmware to the Debug'n'Dump and wiring everything up, running it didn't seem to have any effect on the nRF52832, but at that point I was also blind to what was happening without an oscilloscope.
I acquired an oscilloscope from David Oswald, and observed that there was just a tiny pulse where the glitch should happen; it wasn't shorting.
After creating an issue on the airtag-glitcher GitHub repo documenting my findings, I moved on to using David's own FPGA-based glitching board, the GIAnT, to replicate the attack.

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

You can see on the oscilloscope that the GIAnT keeps shorting the CPU of the nRF chip to ground momentarily, at an increasing offset approaching the critical section after the chip has started.
It repeats each glitch a few times, and with multiple pulse widths, to increase the likelihood of a successful glitch.

Once this memory copy is successfully glitched, the application on the Pi stops running, and a dump of the nRF52832's firmware is left in the working directory.

### Returning to the Debug'n'Dump

By the time I'd glitched the nRF chip using the GIAnT, Thomas Roth had responded to my issue on GitHub, blaming a resistor of the incorrect spec, which apparently served a minor purpose and could be removed.
After removing it, I quickly got the glitch to work successfully.

## Glitching the CC2541

I haven't managed to glitch the Texas Instruments CC2541, but I've learned a lot along the way and this section covers my methods.
In many respects, I've followed many of the key methods outlined in the work linked on this slide:
Bootloader analysis---there is no default bootloader in the flash as far as I can tell---using simple power analysis to look for critical sections---areas to glitch---and differential power analysis to look deeper into potential critical sections for more differences between CRP enabled and CRP disabled CPU activity.

### Observations

After connecting everything, the first thing I did was use an oscilloscope to monitor the behaviour of the CC Debugger and the CC2541 during various tasks, such as setting the debug lock bit and reading the info page from the CC2541.
Looking at the CPU voltage trace, I then identified potential critical sections to glitch.

Those sections were:

- Immediately after a "cold boot" and just before the application starts visibly executing,
- While the chip is under reset (the CPU doesn't really do anything here as far as I can tell, though),
- As the chip comes out of reset and immediately after.

### Glitch attempts

I've noticed in the cases of after reset and on a cold boot, that there is no obvious section of different CPU activity before the application starts running.
I assume this is because there's no boot loader, which means there's no logic run by the CPU for checking the readout protection state that I can actually glitch.

This was confirmed by my systematic glitching at increased offsets in those areas and observing the outcomes.
I knew that the glitch I was applying should cause some different behaviour from the CPU, because it would cause instructions to be skipped in the test application I was running.
Glitching the potential critical sections saw no change in the outcome.
<!-- Drifting too far towards the USB reads and writes did cause a change, but it was always just a crash due to the data returned to the CC Debugger being zeroed. -->

<!-- ### DPA -->

<!-- To make sure there wasn't anything I'd missed, I carried out differential power analysis on those critical sections. -->
<!-- This was in order to highlight any differences between CPU activity with and without CRP enabled, to see if there were any areas I could glitch. -->
<!-- I've had issues collecting enough traces for this, as it takes a very long to transfer data from the oscilloscope I have to the Pi or my laptop; I can only capture about one trace every 18 minutes, and I need hundreds or ideally thousands, before I can see any results. -->
<!-- Comparing by eye so far, however, I've seen no significant differences in CPU voltage traces between CRP enabled and disabled. -->

<!-- Here you can see that after averaging the blue and orange traces, features disappear, because I haven't managed to line up the clock cycles of each of the traces yet. -->

## Conclusions

I believe the crowbar glitch is not possible on the CC2541 because there does not seem to be a firmware bootloader in protected memory that can be affected by glitching the CPU.

During this project, I've found that voltage glitching has been made more accessible with the Pico Debug ‘n’ Dump, due to the low cost and ease of use.
If the resistor was the correct spec, I’d have managed to glitch the nRF52832 with far less troubleshooting, probably within a few days, or even under an hour, with a basic setup guide and more comprehensive pin descriptions.
The GIAnT, on the other hand, is a much more complex and versatile device, which gives it a lot of value when it comes to discovering which type of glitch will work best for a microcontroller, but not ease of use.

## What I'd have done differently

For some things, it's hard to say, because I've learned a lot for the first time in this project.
Knowing what I know now, it would have been better to identify whether there was any bootloader code I could have targeted before blindly glitching potential critical sections (although this glitching didn't take long).
I would also have attempted DPA earlier on, but I did not know what the knowledge barriers for communicating with the oscilloscope would be, so it could have really slowed down the project if I had.

I'd also have set my success criteria from the start to be more focussed on learning, rather than trying to successfully glitch a chip I had very little information about at the time.

If I had more time, I would have worked on compiling a more conclusive differential power analysis.
I also would have tried glitching the main voltage for the CC2541 to see if I could set bits.
David also brought to my attention an old vulnerability with the CC2430, to see whether it still applied to the CC2541, which I would have also liked to investigate.
I'd have also liked to work on improving ease of use of voltage glitching, primarily by extending GIAnT and adding to the documentation.


# Feedback

Be very specific about structuring in my report: boundaries between experiments, little experiments like finding minimum pulse widths, success rates, etc.
