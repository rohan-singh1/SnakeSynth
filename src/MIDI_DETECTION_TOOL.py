### Module that contains Midi hardware detection and input message handling ###

import pygame.midi

def identify_and_select_midi_device():
    pygame.midi.init()  # Initialize the Pygame MIDI module

    device_count = pygame.midi.get_count()  # Get the number of available MIDI devices

    if device_count == 0:  # Check if no MIDI devices are detected
        print("No MIDI devices detected.")
        pygame.midi.quit()  # Quit Pygame MIDI module
        return

    print("Number of available MIDI input devices:", device_count)  # Print the number of available MIDI devices

    # Iterate over the MIDI devices and print information for each device
    for i in range(device_count):
        device_info = pygame.midi.get_device_info(i)
        device_name = device_info[1].decode('utf-8')  # Decode the device name from bytes to a string
        device_input = device_info[2]  # Check if the device supports input
        if device_input:
            print(f"Input ID: {i}, Name: {device_name}")  # Print the ID and name of the MIDI input device

    device_number_select = 1  # Select a specific MIDI device by its ID (e.g., 1)

    if device_number_select >= device_count:  # Check if the selected device number is valid
        print("Invalid device number selected.")
        pygame.midi.quit()  # Quit Pygame MIDI module
        return

    print('Selected Device Number is:', device_number_select)


    # Select the desired MIDI input device
    input_device = pygame.midi.Input(device_number_select)

    # Call the function to receive MIDI input
    receive_midi_input(input_device)

    # Cleanup and close the MIDI input device
    input_device.close()

    # Quit Pygame MIDI
    pygame.midi.quit()


def receive_midi_input(midi_input_device):  # continuous loop monitoring. Needs retooling. don't use this as is
    # Main loop to receive MIDI input
    running = True
    while running:
        # Check if there are any MIDI messages available
        if midi_input_device.poll():
            # Read the MIDI messages
            midi_events = midi_input_device.read(10)  # Read up to 10 MIDI events

            # Process the MIDI messages
            for event in midi_events:
                # Extract MIDI data from the event
                data = event[0]        # The MIDI data is stored in the first element of the event tuple

                # Extract the specific MIDI components from the data
                status = data[0]       # The first byte of the MIDI data represents the status byte
                note = data[1]         # The second byte of the MIDI data represents the note value
                velocity = data[2]     # The third byte of the MIDI data represents the velocity or intensity of the MIDI event

                # Print the MIDI message
                print(f"Received MIDI message: Status={status}, Note={note}, Velocity={velocity}")

        # Add any other logic or functionality here
identify_and_select_midi_device()  # debug line
