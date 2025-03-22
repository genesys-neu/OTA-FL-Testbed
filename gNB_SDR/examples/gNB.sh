#!/bin/bash

# Path to your Python programs
PROGRAM1="Receive.py"
PROGRAM2="OFDM_Custom_Rx.py"

# Open first program in a new terminal
gnome-terminal -- bash -c "python3 $PROGRAM1; exec bash"

sleep 3
# Open second program in another new terminal
gnome-terminal -- bash -c "python3 $PROGRAM2; exec bash"
