# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 19:41:17 2014

@author: Sven Riester
Adapted and updated for newer pyvisa from Rocking Wombat's work (http://www.rocking-wombat.de/PythonPyVisa.html) by Jonathan Rudman
"""

import sys
import numpy
import pyvisa as visa


# Konstanten
AUTO = 'AUTO'
NORMAL = 'NORM'
AVERages = 'AVER'
PEAK = 'PEAK'
HIGH_RESOLUTION = 'HRES'
BW_20M = '20M'
OFF = 'OFF'
ON = 'ON'
AC = 'AC'
DC = 'DC'
GND = 'GND'

CHANNEL_1 = 'CHAN1'
CHANNEL_2 = 'CHAN2'
CHANNEL_3 = 'CHAN3'
CHANNEL_4 = 'CHAN4'

# FFT-Fensterfunktionen
RECTANGLE = 'RECT'
BLACKMAN = 'BLAC'
HANNING = 'HANN'
HAMMING = 'HAMM'
FLATTOP = 'FLAT'
TRIANGLE = 'TRI'

dB = 'DB'
Vrms = 'VRMS'

# Mathe-Funktionen
ADD = 'ADD'
SUBT = 'SUBT'
MULT = 'MULT'
DIV = 'DIV'
AND = 'AND'
OR = 'OR'
XOR = 'XOR'
NOT = 'NOT'
FFT = 'FFT'
INTG = 'INTG'
DIFF = 'DIFF'
SQRT = 'SQRT'
LOG = 'LOG'
LN = 'LN'
EXP = 'EXP'
ABS = 'ABS'



def get_device_list():
    '''Gibt eine Liste mit den angeschlossenen Instrumenten zurück'''
    device_list = visa.ResourceManager().list_resources()
    return device_list


class DS1074Z(object):
    def __init__(self, device_id):
        self.scope = visa.ResourceManager().open_resource(device_id, timeout=10000)
        return
    
    def autoscale(self):
        self.scope.write(':AUT')
        return
        
    def run(self):
        self.scope.write(':RUN')
        return
        
    def stop(self):
        self.scope.write(':STOP')
        return
        
    def single(self):
        '''Set the oscilloscope to the single trigger mode.'''
        self.scope.write(':SING')
        return
        
    def force_trigger(self):
        '''Generate a trigger signal forcefully.'''
        self.scope.write(':TFOR')
        return
    
    def get_timescale(self):
        '''Gibt die Einstellung der Zeitbasis zurück'''
        return self.scope.query(":TIM:SCAL?")
        
    def set_timescale(self, timescale):
        '''Ändert die Einstellung der Zeitbasis'''
        self.scope.write(":TIM:SCAL "+str(timescale))
        return        

    def get_averages_nr(self):
        '''Query the number of averages under the average acquisition mode.'''
        return self.scope.query(':ACQ:AVER?')
        
    def set_averages_nr(self, value):
        '''Set the number of averages under the average acquisition mode.
        value = 2^n with n=1...10'''
        self.scope.write(':ACQ:AVER '+str(value))
        return

    def get_mem_depth(self):
        '''Query the number of averages under the average acquisition mode.'''
        return self.scope.query(':ACQ:MDEP?')
        
    def set_mem_depth(self, value):
        '''Set the number of averages under the average acquisition mode.
        value:
        When a single channel is on: {AUTO|12000|120000|1200000|12000000|24000000} 
        When dual channels are on: {AUTO|6000|60000|600000|6000000|12000000} 
        When four channels are on: {AUTO|3000|30000|300000|3000000|6000000} 
        Wherein, 24000000, 12000000 and 6000000 are options.'''
        self.scope.write(':ACQ:MDEP '+str(value))
        return

    def get_acquisition_mode(self):
        '''Query the acquisition mode when the oscilloscope samples.'''
        return self.scope.query(':ACQ:TYPE?')
        
    def set_acquisition_mode(self, value):
        '''Set the acquisition mode when the oscilloscope samples.'''
        self.scope.write(':ACQ:TYPE '+value)
        return

    def get_samplerate(self):
        '''Gibt die Abtastrate zurück'''
        return float(self.scope.query(':ACQ:SRAT?').strip())
        
    def set_samplerate(self, value):
        '''Set the acquisition mode when the oscilloscope samples.'''
        self.scope.write(':ACQ:SRAT '+value)
        return        
    
    # Seite 22 wurde vorerst ausgelassen
    
    def get_bandwidth_limit(self, channel):
        '''Gibt die Eingangsbandbreite zurück'''
        return self.scope.query(':CHAN'+str(channel)+':BWL?')
        
    def set_bandwidth_limit(self, channel, value):
        '''Änder die Eingangsbandbreite: value = OFF oder 20M'''
        self.scope.write(':CHAN'+str(channel)+':BWL '+value)
        return
        
    def get_coupling(self, channel):
        '''Gibt die Eingangskopplung zurück'''
        return self.scope.query(':CHAN'+str(channel)+':COUP?')
        
    def set_coupling(self, channel, value):
        '''Ändert die Eingangskopplung: value = AC, DC oder GND'''
        self.scope.write(':CHAN'+str(channel)+':COUP '+value)
        return

    def get_channel_state(self, channel):
        '''Gibt den Zustand des Kanal zurück: ON oder OFF'''
        return self.scope.query(':CHAN'+str(channel)+':DISP?')
        
    def set_channel_state(self, channel, value):
        '''Ändert die Eingangskopplung: value = AC, DC oder GND'''
        self.scope.write(':CHAN'+str(channel)+':DISP '+value)
        return
        
    def get_channel_inv(self, channel):
        '''Gibt zurück ob das Signal invertiert wird oder nicht'''
        return self.scope.query(':CHAN'+str(channel)+':INV?')
        
    def set_channel_inv(self, channel, value):
        '''Aktiviert/deaktiviert die Invertierung für den Kanal'''
        self.scope.write(':CHAN'+str(channel)+':INV '+value)
        return
        
    # Seite 25
        
    def get_voltscale(self, channel):
        '''Gibt die Einstellung der Vertikalablenkung zurück'''
        return self.scope.query(':CHAN'+str(channel)+':SCAL?')
        
    def set_voltscale(self, channel, voltscale):
        '''Ändert die Einstellung der Vertikalablenkung'''
        self.scope.write(':CHAN'+str(channel)+':SCAL '+str(voltscale))
        return  

    # Mathe
    
    def set_Math(self, state):
        '''Mathefunktion ein- bzw. ausschalten'''
        self.scope.write(':MATH:DISP '+state)
        return
        
    def set_Math_Operator(self, Operator):
        '''Anzuwendende Mathefunktion'''
        self.scope.write(':MATH:OPER '+Operator)
        return
    
    def set_Math_Source1(self, Source):
        '''Anzuwendende Mathefunktion'''
        self.scope.write(':MATH:SOUR1 '+Source)
        return
    
    def set_Math_Source2(self, Source):
        '''Anzuwendende Mathefunktion'''
        self.scope.write(':MATH:SOUR2 '+Source)
        return    
    
    def get_Math_Scale(self):
        '''Gibt zurück ob das Signal invertiert wird oder nicht'''
        return self.scope.query(':MATH:SCAL?')
        
    def set_Math_Scale(self, value):
        '''Aktiviert/deaktiviert die Invertierung für den Kanal'''
        self.scope.write(':MATH:SCAL '+value)
        return
        
    def get_Math_Offset(self):
        '''Gibt zurück ob das Signal invertiert wird oder nicht'''
        return self.scope.query(':MATH:OFFS?')
        
    def set_Math_Offset(self, value):
        '''Aktiviert/deaktiviert die Invertierung für den Kanal'''
        self.scope.write(':MATH:OFFS '+value)
        return
    
    def invert_Math(self, value):
        '''Aktiviert/deaktiviert die Invertierung für den Kanal'''
        self.scope.write(':MATH:INV '+value)
        return
    
    def Reset_Math(self):
        '''Aktiviert/deaktiviert die Invertierung für den Kanal'''
        self.scope.write(':MATH:RES')
        return
    
    def FFT_Window(self, window):
        '''FFT-Fensterung'''
        self.scope.write(':MATH:FFT:WIND '+window)
        return  

    def FFT_Splitscreen(self, state = ON):
        '''Schaltet für FFT auf Splitscreen'''
        self.scope.write(':MATH:FFT:SPL '+state)
        return 

    def FFT_Unit(self, Unit = dB):
        '''FFT-Einheit: dB oder Vrms'''
        self.scope.write(':MATH:FFT:UNIT '+Unit)
        return
        
    # Seite 55


    # Zusätzliche Funktionen für mehr Komfort
    def screenshot(self, path, name, suffix = 'png'):
        '''Speichert den aktuellen Bildschirm als Grafik-Datei unter dem
        angegebenen Pfad.'''
        self.scope.write(":DISP:DATA?")
        wave_data = self.scope.read_raw()[2+9:]
        with open(path+name+'.'+suffix, "wb") as f:
            f.write( wave_data )
        f.close()
        return

    def _clean_tmc_header(self, tmc_data):
        if sys.version_info >= (3, 0):
            n_header_bytes = int(chr(tmc_data[1]))+2
        else:
            n_header_bytes = int(tmc_data[1])+2
        
        n_data_bytes = int(tmc_data[2:n_header_bytes].decode('ascii'))

        return tmc_data[n_header_bytes:n_header_bytes + n_data_bytes]

        
    def get_data(self, channel):
        '''Holt Daten von Oszilloskop ab und gibt sie in einem Dictonary
        als Float-Array zusammen mit der Samplerate zurück.'''
        self.scope.write(":WAV:FORM ASC")
        self.scope.write(":WAV:FORM BYTES")
        self.scope.write(":WAV:SOUR CHAN1")
        self.scope.write(":WAV:MODE RAW")
        self.scope.write(":WAV:STAR 1")
        self.scope.write(":WAV:STOP 6000")
        self.scope.write(":WAV:DATA?")
        # raw_bytes = self.scope.read_binary_values(datatype="c")
        raw_bytes = self.scope.read_bytes(1)
        # print(raw_bytes.hex())
        # data = self._clean_tmc_header(raw_bytes).decode().split(',')
        data = raw_bytes[11:-1].decode().split(',')
        # print(len(data))
        # print(data)

        for x in range(len(data)):
            data[x]=float(data[x])
        
        return {'Samplerate': self.get_samplerate(), 'Data': data}
        
    def movingaverage(values,window):
        '''Bildet gleitenden Mittelwert'''
        weigths = numpy.repeat(1.0, window)/window
        avg = numpy.convolve(values, weigths, 'valid')
        return avg
