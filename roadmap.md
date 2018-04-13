# (Possible) future features
• Oavsett hur många stämmor jag har och vilken viktning av dem som sker så ska den övergripande volymen för hela ljudfilen alltid vara densamma. Eller? Hur blir det med hårdpannorerade stämmor?
• Ska mute-filerna lista alla stämmor den tar bort? Typ @-T1-T2-T3? Det tycker jag.
• Ska jag köra Python 3 eller Python 2?
• Fixa en UML class diagram för hela programmet.
• Möjlighet att muta hela voice groups för mute-delen.
• Create a GUI for using the program (that basically just runs terminal commands).
• Create a object structure for getting information about file names. It should be possible to specify that you want just a subset of songs to be converted. And rehersify should tell you: "Working on song x" and do that whole song first.
• Create a strict check of the input syntax for all files.
• Create a --vertabim mode where specific output is given. Right now, everything is printed.
• Create rehersal files with the focus voice in the left channel only.
	• Extra feature: Have this voice be another instrument.
• Tracks within the same % group should together have the same volume as other % groups (assuming that all individual tracks are random noise with the same volume).
• Meteronome tracks.
• Rewrite all the code in Swift instead.
	• Can midi and audio procedures be done with Swift Core packages instead of with SOX and something else?
• Midi to output rather than wave to output (or both).
	• Different tempos (e.g., ••bpm [60,80,100]).
	• Open source sound font that can be bundled with the program.