# Name
rehersify

# Version
alpha 0.5 (released 2019-01-05)

# Author
Martin Asperholm, martin.asperholm@gmail.com, [www.asperholm.net](http://www.asperholm.net).

# License type
[GNU Gen­eral Public Li­cense, ver­sion 3](https://www.gnu.org/licenses/gpl-3.0.en.html)

# Description
This is rehersify, a small [python](https://www.python.org) script that uses [SoX](http://sox.sourceforge.net/) and [lame](http://lame.sourceforge.net/) to create rehersal music files out of individual music files containing single voices.

The program is in the Alpha stage, meaning that the feature set is extremely limited, that the customization options are non-existent, that the program is prone to break if not used exactly as intended, and that this readme file is incredibly sparse. However, given that one follows the instructions below, it should be usable.

# Dependencies
In order to run this script you need [Python](https://www.python.org), [Sox](http://sox.sourceforge.net/), and [lame](http://lame.sourceforge.net/) installed and ready to go.

# Basic usage
## Input files
Input files should be named "This is the songs name@voice%voiceGroup" (with voiceGroup starting at 1 and counting upwards and where several files can be inside the same voice group) and placed in the folder 'input' that is placed in the same folder that rehersify.py is placed. Input formats that are accepted are WAW and AIF. The voice group command tells rehersify two things: 
    
    1. In what order the different parts should be placed in stereo space. Lower numbers are placed more to the left and higher numbers are placed more to the right.
    2. How the volume of each voice should be adjusted. Volumes of individual voices (that aren't the focus of that particular rehersal file) are adjusted so that their combined volume is the same as each other individual voice group.

## Output files
Output files are generated in the 'output' folder. Output files have the format 'mp3'.

## Operation
When you've placed your input files in the input folder, use the Terminal to navigate to the folder where you've placed the program and type

	python rehersify.py

## Change log
### alpha 0.5 (released 2019-01-05)
- Made it so that voices that belongs to the same voice group together have the same volume (when not being the primary rehersal voice of the file) if you assume that they are uncorrelated and have the same input volume.
- Added rehersal files where the voice in question is placed to the left in the stereo field with the other voices placed to the right.
- Cleaned up and optimized the code in general.

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
