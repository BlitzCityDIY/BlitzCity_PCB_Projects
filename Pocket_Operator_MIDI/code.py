# SPDX-FileCopyrightText: Copyright (c) 2025 Liz Clark
#
# SPDX-License-Identifier: MIT
import board
import digitalio
import time
import usb_midi
import adafruit_midi
import adafruit_mcp4728
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# Define pins for each synth voice button
button_pins = [
    board.TX,
    board.RX,
    board.D2,
    board.D3,
    board.D4,
    board.D6,
    board.D7,
    board.D8,
    board.D9,
    board.D10,
    board.MOSI,
    board.MISO,
    board.SCK,
    board.A0,
    board.A1
]

# Set up all pins as outputs
synth_voices = []
for pin in button_pins:
    voice = digitalio.DigitalInOut(pin)
    voice.direction = digitalio.Direction.OUTPUT
    voice.value = False
    time.sleep(1)
    voice.value = True  # Initialize as not pressed
    time.sleep(0.5)
    voice.value = False
    synth_voices.append(voice)
    print(pin)

# Set up status LED
led = digitalio.DigitalInOut(board.A3)
led.direction = digitalio.Direction.OUTPUT

# Set up DAC
i2c = board.I2C()  # uses board.SCL and board.SDA
mcp4728 = adafruit_mcp4728.MCP4728(i2c, adafruit_mcp4728.MCP4728_DEFAULT_ADDRESS)

# Set up MIDI over USB
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    in_channel=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
)

# Track active notes for each channel
active_notes = {}

# Map MIDI channels to synth voices
channel_to_voice = {}
for i in range(min(len(synth_voices), 16)):
    channel_to_voice[i] = i

# Define MIDI note numbers for the measured notes
# Map MIDI note numbers to voltage values (in volts)
note_to_voltage = {
    33: 0.0,   # A1 - 0V
    35: 0.35,   # B1 - 0.2V
    36: 0.53,   # C1 - 0.3V
    38: 0.78,   # D1 - 0.5V
    40: 1.0,   # E1 - 0.7V
    41: 1.25,   # F1 - 0.8V
    43: 1.5,   # G1 - 1.0V
    45: 1.7,  # A2 - 1.15V
    47: 1.9,   # B2 - 1.3V
    48: 2.15,   # C2 - 1.5V
    50: 2.3,   # D2 - 1.7V
    52: 2.55,   # E2 - 1.8V
    53: 2.78,   # F2 - 2.0V
    55: 2.9,   # G2 - 2.2V
    57: 3.2,  # A3 - 2.45V
}

# Function to convert a voltage (0-2.5V) to DAC raw value (0-4095)
# Assuming DAC reference voltage is 3.3V
def voltage_to_dac_value(voltage):
    # Calculate proportion of full scale (3.3V)
    proportion = voltage / 3.3
    # Convert to 12-bit DAC value (0-4095)
    return int(proportion * 4095)

# Function to set DAC output based on MIDI note
def set_dac_for_note(note):
    if note in note_to_voltage:
        voltage = note_to_voltage[note]
        dac_value = voltage_to_dac_value(voltage)
        print(f"Note {note} -> {voltage}V -> DAC value {dac_value}")
        mcp4728.channel_a.raw_value = dac_value

# Initialize DAC to A1 (0V)
mcp4728.channel_a.raw_value = 0

print("MIDI synth voice controller with pitch control started")

while True:
    # Check for MIDI messages
    msg = midi.receive()
    
    if msg is not None:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            # Note On event with velocity > 0
            set_dac_for_note(msg.note)
            channel = msg.channel
            note = msg.note
            
            # Blink LED to indicate MIDI activity
            led.value = True
            
            # Set the DAC value based on the note
            
            
            # If this channel maps to a synth voice, activate it
            if channel in channel_to_voice:
                voice_index = channel_to_voice[channel]
                if voice_index < len(synth_voices):
                    print(f"Channel {channel+1} -> Voice {voice_index}, Note {note}")
                    
                    # Track this note as active for this channel
                    if channel not in active_notes:
                        active_notes[channel] = set()
                    active_notes[channel].add(note)
                    set_dac_for_note(note)
                    #time.sleep(0.1)
                    # Activate the corresponding synth voice
                    synth_voices[voice_index].value = True
                    
                    
            
        elif isinstance(msg, NoteOff):
            # Note Off event (or Note On with velocity 0, which is equivalent)
            channel = msg.channel
            note = msg.note
            
            # If this note was active on this channel, process it
            if channel in active_notes and note in active_notes[channel]:
                active_notes[channel].remove(note)
                
                # If no more active notes for this channel, turn off the voice
                if not active_notes[channel] and channel in channel_to_voice:
                    voice_index = channel_to_voice[channel]
                    if voice_index < len(synth_voices):
                        print(f"Voice {voice_index} off")
                        synth_voices[voice_index].value = False
    
    # Turn off LED after processing MIDI events
    led.value = False
    
    # Small delay to avoid hogging the CPU
    #time.sleep(0.001)
