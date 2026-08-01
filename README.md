# Minecraft 26.1 Pig Cannon Project Files

This repository collects the project files for a 26.1 pig teleporter cannon. The associated YouTube-Tutrial can be found at
(TBA).

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
