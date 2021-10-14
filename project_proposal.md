---
title: Project Proposal
author: Jonathan Rudman
geometry: margin=1in
---

# Problem Statement

Microcontroller units (MCUs) are found embedded in many commercially available devices, performing many functions as part of a greater device.
In order to protect intellectual property, avoid cloning, and prevent the discovery of software vulnerabilities, the firmware of a microcontroller is protected by disabling debugging and read/write of internal memory.

The different implementations of these protections have various weaknesses that can be exploited through implementation attacks, and it is important for manufacturers of MCUs to reduce the effectiveness or increase the difficulty of these attacks.
One such weakness which is common among MCUs is voltage glitching: the act of raising or lowering the operating voltage for a fraction of a second to cause instructions to be skipped or incorrectly executed.
This can be used to gain access to a debug interface and enable reading the firmware to allow the attacker to modify existing proprietary firmware or search for software vulnerabilities.

I will be attempting to employ implementation attacks such as voltage glitching to dump the protected firmware of microcontrollers.
This may be informed by binary analysis of an available bootloader source and software vulnerabilities to dump protected internal memory.

<!-- TODO: Write about what other people have (and haven't) done -->

# Challenges

# Planned Approach

# Milestones

# Degree Apprenticeship Specialisation
