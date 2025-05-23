---
layout: default
---

## About these Python scripts

This is an improved version of the [Fritzing](https://fritzing.org) Parts Factory that generate parts such as coloured headers and multi row headers. These scripts use the `PySide6` library to work with Qt, so for those who don't have C++/Qt coding skills, you can contribute to tgis repo. The scripts are written in Python!

### Installing the scripts

#### Windows (Python Interpreter)

In command prompt (assuming you have installed python and added it to path!), run

```bash
pip install PySide6
```

With the PySide6 library installed, cd to the location where you have stored the scripts, and run

```
python partsfactory.py
```

You might need to change the parameters

```python
import partsfactory_constants as constants
import getopt
import os
import os.path
import sys
import logging
from datetime import date
from PySide6.QtCore import QCryptographicHash, QUuid, QByteArray

# ...

# set test parameters

rows = 4

columns = 4

part_type = constants.MALE_HEADER

pitch = constants.PITCH_0_5MM

#pitch = constants.PITCH_1MM

#pitch = constants.PITCH_1_27MM

#pitch = constants.PITCH_2MM

#pitch = constants.PITCH_0_1IN
#pitch = constants.PITCH_0_11IN
#pitch = constants.PITCH_0_12IN
#pitch = constants.PITCH_0_13IN
#pitch = constants.PITCH_0_14IN
#pitch = constants.PITCH_0_15IN
#pitch = constants.PITCH_0_16IN
#pitch = constants.PITCH_0_17IN
#pitch = constants.PITCH_0_18IN
#pitch = constants.PITCH_0_19IN

#pitch = constants.PITCH_0_156IN

#pitch = constants.PITCH_0_2IN

#pitch = constants.PITCH_1IN

pcb_type = constants.THT

pad_type = constants.CIRCLE

pin_order = constants.COLUMN

#pin_order = constants.ROW

color = constants.BRN


ref_file = constants.MALE_HEADER_BREADBOARD_REFERENCE_FILE
```
