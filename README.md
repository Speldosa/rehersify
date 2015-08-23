# Name
rehersify

# Version
alpha 0.4 (released 2015-08-21)

# Author
Martin Larsson, to.martin.larsson@gmail.com, [www.martinlarsson.net](http://www.martinlarsson.net).

# License type
GNU Gen­eral Public Li­cense, ver­sion 3

# Description
This is rehersify, a small [python](https://www.python.org) script that uses [SoX](http://sox.sourceforge.net/) and [lame](http://lame.sourceforge.net/) to create rehersal music files out of individual music files containing single voices.

The program is in the Alpha stage, meaning that the feature set is extremely limited, that the customization options are non-existent, that the program is prone to break if not used exactly as intended, and that this readme file is incredibly sparse. However, given that one follows the instructions, it should be usable.

# Dependencies
In order to run this script you need [Python](https://www.python.org), [Sox](http://sox.sourceforge.net/), and [lame](http://lame.sourceforge.net/) installed and ready to go.

# Basic usage
## Input files
Input files should be named "This is the songs name@voice%voicePlacement" (the '%voicePlacement' option is optional) and placed in the folder 'input'. Input formats that are accepted are wav and aif. The voice placement command tells the program in what order the different parts should be placed in stereo space. Lower numbers are placed more to the left and higher numbers are placed more to the right. Counting starts at "1".

## Output files
Output files are generated in the 'output' folder. Output files have the format 'mp3'.

## Operation
When you've placed your input files in the input folder, use the Terminal to navigate to the folder where you've placed the program and type

	python rehersify.py

## Change log
### alpha 0.4 (released 2015-08-23)
- Changed the naming of output files.
- Bug fixes.

### alpha 0.3 (released 2015-08-16)
- Bug fixes.
- Changed the syntax of input files.
- Added a normalization process at the end to all the output files.
- Tweaked volume parameters.
- Added a final step where all output files are converted to mp3 files with the help of [lame](http://lame.sourceforge.net/).

### alpha 0.2 (released 2015-07-12)
- Implemented a behind the scenes function so that every input file is converted to a mono file (regardless if it already is a mono file or not).
- Added an automatic scaling to avoid clipping in the final mix.
- Added stereo feature: Voices can now be spread out in stereo space.

### alpha 0.1 (released 2015-07-04)
- Added the basic functionality: Taking a number of sound files and combining them into rehersal files where the volume is mixed differently.
