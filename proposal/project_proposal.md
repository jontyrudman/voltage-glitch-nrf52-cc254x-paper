---
title: Project Proposal
author: Jonathan Rudman
bibliography: project_proposal.bib
csl: harvard-cite-them-right.csl
geometry: margin=1in
---

# Problem Statement

Microcontroller units (MCUs) are found embedded in many commercially available devices, performing many functions as part of a greater device.
In order to protect intellectual property, avoid cloning and prevent the discovery of software vulnerabilities, the firmware of a microcontroller is protected by disabling debugging and read/write of internal memory.

The different implementations of these protections have various weaknesses that can be exploited through implementation attacks, and it is important for manufacturers of MCUs to reduce the effectiveness or increase the difficulty of these attacks.
One such weakness which is common among MCUs is voltage glitching: the act of raising or lowering the operating voltage for a fraction of a second to cause instructions to be skipped or incorrectly executed.
This can be used to gain access to a debug interface and enable reading the firmware to allow the attacker to modify existing proprietary firmware or search for software vulnerabilities.

I will be attempting to employ implementation attacks such as voltage glitching to dump the protected firmware of microcontrollers.
This may be informed by binary analysis of an available bootloader source and software vulnerabilities to dump protected internal memory.

# Related Work

@rothHowAppleAirTags2021 has shown how the nRF52832 in Apple AirTags can be glitched to skip its code readout protection (CRP) check, which I aim to replicate at the start of this project.
Roth also cites earlier work from a blog, @limitedresultsNRF52DebugResurrection2020, which focuses on a similar system-on-a-chip (SoC), the nRF52840, and presents information from the nRF52 family in the context of voltage glitching and CRP.

@vandenherrewegenFillYourBoots2020 describe voltage glitching in conjunction with binary analysis---a grey-box approach---on embedded bootloaders.
Although the nRF52832---the SoC I intend to attack first---has a CRP check before the bootloader (which is stored on flash memory), Van Den Herrewegen et al. outline voltage glitches on three different MCUs.
In the aforementioned paper the GIAnT, @oswaldGiantrevBGIAnTFault, is also used for the attacks, which is a device that I plan to use and develop further.

# Challenges

There are a number of challenges that this project will present:

- I've never done this much with electronics before. I did physics A level but I've never attempted power analysis on integrated circuits and I've only flashed firmware based on specific instructions.
- Reducing the glitch parameter space could involve binary analysis and/or power monitoring; the alternative is to use brute force, which is time consuming. 
- There are many microcontrollers for which voltage glitching hasn't been attempted or successful yet. As a "stretch" goal I'd like to attempt to glitch an MCU without any form of guide. For example, I'm not aware of a successful voltage glitch attack on the Texas Instruments CC2541.
- Automating the parameter space can be done in various different ways and can make voltage glitching more accessible, leading to the potential for more complex attacks. Extending and developing software to do this more effectively is a challenge that intrigues me.

# Planned Approach

I plan to connect a device for running voltage glitching attacks---such as the Pico Debug'n'Dump (@rothPicoDebugDump) or GIAnT---to microcontrollers to gain access to a debugging interface.
This will likely be done with some supplementary binary analysis, depending on whether the bootloader is on ROM, to determine how many cycles into the boot process the instructions for checking debug and read/write flags are.
I also plan to extend GIAnT with support for more MCUs and research the possibility of reducing the number of glitches required to find the correct glitch offset, width and voltage for a successful attack.

# Milestones

## Semester One

### 18th October 2021

Successfully replicate the voltage glitch attack on the nRF52832.
At the time of writing (15/10/2021) I have set up the hardware with an nRF52832 development board, Pico Debug'n'Dump and an ST-LINK V2 serial debugger and dumped firmware from the nRF52832 without code readout protection enabled.

### 8th Nov 2021 (Project inspection)

Should have made contributions to GIAnT to add nRF52832 support.
Be able to demonstrate/show results from a successful voltage glitch attack.
If the previous deadline is met, show contributions to GIAnT and be able to answer questions.

### 19th Nov 2021

Should have tested and compiled a list of success rates for glitching with various parameters on the nRF52832 and made notes on findings and lessons learned from multiple glitch attempts.

### 10th Dec 2021

Should have begun researching and reading the datasheet for an MCU which hasn't experienced a documented glitch (e.g. CC2541).

## Semester Two

### 21st Jan 2022

Should have successfully glitched the chosen MCU from the last deadline and made notes on findings.

### 25th Feb 2022

Should have investigated ways to automate---or adjust current automation methods for---voltage glitching effectively with MCUs which haven't yet been successfully glitched.
Should have used findings to propose mitigations for voltage glitching and any other techniques used throughout the project.

### 11th Apr 2022 (Final submission)

Should have created the report for final submission.

# Degree Apprenticeship Specialisation

This project will focus on developing skills and knowledge listed under the "Software Engineering Specialist" section of the Digital and Technology Solutions Professional degree apprenticeship standard outlined by the Institute for Apprenticeships.

## Skills

I plan to meet the following skills criteria:

- Create effective and secure software solutions using contemporary software development languages to deliver the full range of functional and non-functional requirements using relevant development methodologies.
- Undertake analysis and design to create artefacts, such as use cases to produce robust software designs.
- Produce high quality code with sound syntax in at least one language following best practices and standards.
- Perform code reviews, debugging and refactoring to improve code quality and efficiency.
- Test code to ensure that the functional and non-functional requirements have been met.
- Deliver software solutions using industry standard build processes, and tools for configuration management, version control and software build, release and deployment into enterprise environments.

## Knowledge

I plan to meet the following technical knowledge criteria:

- How to operate at all stages of the software development lifecycle.
- How teams work effectively to develop software solutions embracing agile and other development approaches.
- How to apply software analysis and design approaches.
- How to interpret and implement a design, compliant with functional, non-functional and security requirements.
- How to perform functional and unit testing.
- How to use and apply the range of software tools used in Software engineering.


# Reference List
