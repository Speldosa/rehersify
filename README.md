# Name
Rehersify

# Version
alpha 0.1

# Author
Martin Larsson, to.martin.larsson@gmail.com, [www.martinlarsson.net](http://www.martinlarsson.net).

# License type
GNU Gen­eral Public Li­cense, ver­sion 3

# Description
This is rehersify, a small [python](https://www.python.org) script that uses [SoX](http://sox.sourceforge.net/) to create rehersal music files out of individual music files containing single voices.

The program is in the Alpha stage, meaning that the feature set is extremely limited, that the customization options are non-existent, that the progra is prone to break if not used exactly as intended, and that this readme file is incredibly sparse. However, 

# Dependencies
In order to run this script you need [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)), [Python](https://www.python.org) and [Sox](http://sox.sourceforge.net/) installed and ready to go.

# Basic usage
## Input files
Input files should be named "This is the songs name @ voice-number" (the '-number' is optional) and placed in the folder 'Input'.
## Output files
Output files are generated in the 'Output' folder.
## Operation
When you've placed your input files in the input folder, use the Terminal to navigate to the folder where you've placed the program and type

	python rehersify.py

## Change log
###alpha 0.1 (released 2015-07-04)
- Added the basic functionality.
