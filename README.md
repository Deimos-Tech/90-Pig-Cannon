# Minecraft 26.1 Pig Cannon Project Files

This repository collects the project files for a 26.1 pig teleporter cannon. The associated YouTube-Tutrial can be found at
https://youtu.be/_WBwPR8dpyo.

## Scripts
To calibrate your fire at least three shots and note the number of items in the item-transfer-timers as well as the landing position.
Then run the python script using in a terminal with
```
    python3 "calculate 2d.py"
```
The script will automatically run a fit to calibrate your change of basis.

You may then enter your target coordinates x and z seperately and the corresponding timer settings will be calculated.
Additionally the time of flight is calculated using known in game mechanics.

A visual interface will then show the calibration and the target position.
Confirm that the prediced positions marked with black circles overlap well with the calibration datapoints shown as crosses.

A red marker will show the target position and an associated red dot shows the predicted landing position for the counter settings calculated.

## GUI

pig-cannon.html is a standalone, dependency-free graphical interface for the same calibration math. Open it in any browser (no install, works offline).

- Enter your calibration shots: timer counts n1, n2 and the landing x, z.
- Optionally pin the cannon's launch coordinates, or leave them blank to infer the launch point from your shots.
- Click the map to aim, or type target coordinates. The 90 degree firing cone, predicted landing, and flight time update live.
- Calibration shots and settings can be saved to and loaded from a .json file.

The original calculate 2d.py is kept as a reference implementation.
