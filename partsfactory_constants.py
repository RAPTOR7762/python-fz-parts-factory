#!/usr/bin/env python3

## Constant values for the parts factory.

# For warning message later

import sys

# part types

MALE_HEADER = "male-header"
FEMALE_HEADER = "female-header"

# reference files

MALE_HEADER_BREADBOARD_REFERENCE_FILE = ("svg.breadboard.male_1_pin-0.1in-"
                                         "cons-lines_breadboard.svg")

MALE_HEADER_SCHEMATIC_REFERENCE_FILE = ("svg.schematic.male_1_pin-0.1in_"
                                        "schematic.svg")

CIRCLE_PCB_REFERENCE_FILE = "svg.pcb.circle_1_pin-0.1in_0.038hole_pcb.svg"

OBLONG_PCB_REFERENCE_FILE = "svg.pcb.oblong_single-pin-0.1in_0.038hole_pcb.svg"

# colors

BRN = "#404040"  # default color brown.
RED = "#ff0000"
YEL = "#ffff00"
GRN = "#008000"
BLU = "#0000ff"

# Some common pitch values.Pitch is in 1/1000in (mm settings = mm / 2.54 
# to convert to inches.) This value * row or column gives the pitch value in
# 1/1000 of an inch.

PITCH_0_5MM     = 1         # base ref file pitch 0.5mm
PITCH_1MM       = 2         # 
PITCH_1_27MM    = 2.54      # converted to inches
PITCH_2MM       = 4         # converted to inches
PITCH_0_1IN     = 5.08
PITCH_0_11IN    = 5.588
PITCH_0_12IN    = 6.096
PITCH_0_13IN    = 6.604
PITCH_0_14IN    = 7.112
PITCH_0_15IN    = 7.62
PITCH_0_156IN   = 7.9248    # 1.56 x 5.08
PITCH_0_16IN    = 8.128
PITCH_0_17IN    = 8.636
PITCH_0_18IN    = 9.144
PITCH_0_19IN    = 9.652
PITCH_0_2IN     = 10.16
PITCH_1IN       = 50.8 

# set the row to 1 to only scale by pitch (not move position) the value.

SCALE_ONLY      = 1
PITCH_IN_THOU   = 19.6850     # 0.5mm in thousands of an inch.
PITCH_TO_THOU   = 0.0196850   # pitch to 1/1000s of an inch. The 0.5mm pitch
                              # value is 1, which is 0.0196850in.


# pcb pad types (start at 1 to avoid 0 in a true/false sense.)

RECTANGLE = "rectangle"                     # only valid SMD type!
CIRCLE = "circle"                           # THT only
OBLONG = "oblong"                           # THT only
OBLONG_SINGLE_ROW = "oblong_single_row"     # THT only
OBLONG_BOT = "oblong_bot"                   # THT only
OBLONG_MIDDLE = "oblong_middle"             # THT only
OBLONG_TOP = "oblong_top"                   # THT only

# pcb types

THT = "tht"                                 # through hole
SMD = "smd"                                 # SMD (only copper1 present)

# pin order

ROW = "row"
COLUMN = "column"

# svg types

BREADBOARD = "breadboard"
SCHEMATIC = "schematic"
PCB = "pcb"

# Warning message

if __name__ == "__main__":
  print("This file only has constants and variables.")
  print("Please run 'partsfactory.py' instead")
  sys.exit()
