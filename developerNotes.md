# To-do
* Fix volume scaling!
* Add a normalization function to all files in the end (see [this](https://www.learnosity.com/blog/2009/11/normalising-audio-with-sox/) post).
* Add a scaling factor to the stereo panning that takes human perception into account.
* Add something that checks that the voicePlacementsList is correct.
* Add something that stops the script if only one voice is present for a certain song.
* Add something that checks that all input files are formated correctly.
* Change the whole program so that the remix command is used everywhere instead.
* Should there be stereo panning for the rehersal files as well? Maybe, but to a lesser degree.
* Create stereo output. Might take some work.
* Make it so that volumeFactor and panFactor affects the outcome.
* Create a program that sorts the output into separate folders. Maybe.
* Write a better and more comprehensive README with instructions of how to export sound files from popular DAWs and more. Include screenshots. See [this link](http://stackoverflow.com/questions/2304863/how-to-write-a-good-readme).
* Conform to the GitHub standard of writing README files. (What special functions can I use?)
* Create a helper program that rename the files for you or places them in folders. Maybe I should implement some kind of folder looking instead of just having everything in on big inputfolder. Hmm...
* Create better and more sensible handling of input from terminal.
* Make it so that it's possible to choose between passing values to the proram and just go with the default values. Se [http://www.tutorialspoint.com/python/python_command_line_arguments.htm](this) homepage.
* Check out if you can implement ogg vorbis support, for example with tags and stuff.
* Find segments where two or more voices are exactly the same. Mute all but one voice here. This would be nice, but it would probably take A LOT of time to implement (not even sure if Sox could help me here).
* Create a program that convert midi files to individual audio files (that then can be used in rehersify).

# Snippets

Detta kommando skapar en fil med vänster- och högerpanorering.

	sox -M "Då väntar jag vid vägarna @ B.aif" "Då väntar jag vid vägarna @ S.aif" Test.aif remix -m 1,2,3p-10,4p-10 1p-10,2p-10,3,4

	sox -M "Då väntar jag vid vägarna @ S $ 4.aif" "Då väntar jag vid vägarna @ A $ 3.aif" "Då väntar jag vid vägarna @ T $ 2.aif" "Då väntar jag vid vägarna @ B $ 1.aif" Test.aif remix -a 1v1.0,2v0.80,3v0.20,4v0.0 1v0.0,2v0.20,3v0.80,4v1.0

Detta kommando skapar en monofil

	sox "Då väntar jag vid vägarna @ S.aif" "Då väntar jag vid vägarna @ S.aif" remix -

# Resources

- [A Stack Exchange thread](http://stackoverflow.com/questions/14950823/sox-exe-mixing-mono-vocals-with-stereo-music) about mixing.


sox -M "./input/Då väntar jag vid vägarna @ A $ 3.aif" "./input/Då väntar jag vid vägarna @ B $ 1.aif" "./input/Då väntar jag vid vägarna @ S $ 4.aif" "./input/Då väntar jag vid vägarna @ T $ 2.aif" "./output/Då väntar jag vid vägarna - Tutti .aif" remix -p 1v0.16666666666666669,2v0.5,3v0.0,4v0.33333333333333337 1v0.3333333333333333,2v0.0,3v0.5,4v0.16666666666666666
