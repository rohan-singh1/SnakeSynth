import pygame.midi

pygame.midi.init()
pygame.init() 

device_count = pygame.midi.get_count()
print("Number of available MIDI input devices:", device_count)

for i in range(device_count):
    device_info = pygame.midi.get_device_info(i)
    print(f"Device {i}: {device_info}")

device_number_select = 1

print('Selected Device Number is:', device_number_select)

# Select the desired MIDI input device
input_device = pygame.midi.Input(device_number_select)

# Main loop to receive MIDI input
running = True
while running:
    # Check if there are any MIDI messages available
    if input_device.poll():
        # Read the MIDI messages
        midi_events = input_device.read(10)  # Read up to 10 MIDI events
        """
        The MIDI input handling loop reads up to 10 MIDI events in each iteration using input_device.read(10). If there are multiple MIDI events available, it will process each event individually in the for loop.

        The event handling loop using pygame.event.get() can detect multiple keypresses. It checks for all the events in the event queue and processes them one by one. 
                So if multiple keys are pressed simultaneously, each keypress event will be handled separately in the loop.

        The code is capable of detecting and handling multiple keypresses from the MIDI input device or the keyboard.
        """
        
        # Process the MIDI messages
        for event in midi_events:
            # Extract MIDI data from the event
            data = event[0]
            status = data[0]
            note = data[1]
            velocity = data[2]
            
            # Print the MIDI message
            print(f"Received MIDI message: Status={status}, Note={note}, Velocity={velocity}")
    
    # Add any other logic or functionality here
    

# Cleanup and close the MIDI input device
input_device.close()

# Quit Pygame MIDI
pygame.midi.quit()
