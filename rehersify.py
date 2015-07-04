#!/usr/bin/python

# Global structure of the program:
# 0. Import necessary libraries
# 1. Set global variables
# 2. Create lists
# 3. Create sox commands
# 	3.1 Individual rehersal files - volume increased. 
# 	3.2 Individual rehersal files - channel muted.
#	3.3 Tutti files.
# 4. Run sox commands.

###################################
## 0. Import necessary libraries ##
###################################
import sys
import os

#############################
## 1. Set global variables ##
#############################
# TO-DO: Create better handling of 
inputFolder = "./input/"
outputFolder = "./output/"
volumeFactor=1
panFactor=1
outputFormat="aif"

#####################
## 2. Create lists ##
#####################

# TO-DO: Add something that checks if the files are formated correctly.

# Create a list of the file names for all files.
fileNamesList=[]
# Create a list of the file endings for all files.
fileEndingsList=[]
# Create a list of the song names for all files.
songNamesList=[]
# Create a list of the voice names for all files.
voiceNamesList=[]
# Create a list of the voice numbers for all files.
voiceNumbersList=[]

# Fill in all the files created above.
for file in os.listdir(inputFolder):
    if file.endswith((".aif",".wav")):
        songName,voiceAndFileEnding=file.split(' @ ')
        voice,ending=voiceAndFileEnding.split('.')
        fileNamesList.append(file)
        fileEndingsList.append(ending)
        songNamesList.append(songName)
        if('-' in voice):
            voiceName,voiceNumber=voice.split('-')
            voiceNamesList.append(voiceName)
            voiceNumbersList.append(voiceNumber)
        else:
        	voiceName=voice
        	voiceNamesList.append(voiceName)
        	voiceNumbersList.append('NA')

# Create a list of unique song names.
uniqueSongNamesList=set(songNamesList)

# Create a list of number of voices for each unique song.
numberOfVoicesForUniqueSongNamesList=[]
for song in uniqueSongNamesList:
    numberOfVoicesForUniqueSong=0
    for i in range(1,len(fileNamesList)):
        if songNamesList[i] == song:
            numberOfVoicesForUniqueSong=numberOfVoicesForUniqueSong+1
    numberOfVoicesForUniqueSongNamesList.append(numberOfVoicesForUniqueSong)

############################
## 3. Create sox commands ##
############################
soxCommandsList = []
# Loop for each unique song.
for uniqueSong in uniqueSongNamesList:
	# Create high and low volume values for this song.
	# TO-DO: Generate these commands from input values.
	highVolume=0.80
	lowVolume=0.125
	# Used to make the tutti files.
	standardVolume=0.75
	# Used to make the muted files.
	zeroVolume=0
	standardPlusVolume=0.80
	# 3.1 Create individual rehersal files for each voice of the song where the voice in question is higher than the others.
	for a in range(0,len(fileNamesList)):
		if songNamesList[a] == uniqueSong:
			soxCommand = "sox -m"
			for b in range (0,len(fileNamesList)):
				if fileNamesList[b] == fileNamesList[a]:
					soxCommand = soxCommand + " -v " + str(highVolume) + " \"" + inputFolder + fileNamesList[b] + "\""
				elif songNamesList[b] == songNamesList[a]:
					soxCommand = soxCommand + " -v " + str(lowVolume)  + " \"" + inputFolder + fileNamesList[b] + "\""
			soxCommand = soxCommand + " \"" + outputFolder + songNamesList[a] + " - " + voiceNamesList[a] 
			if voiceNumbersList[a] is not 'NA':
				soxCommand = soxCommand + "-" + voiceNumbersList[a]
			soxCommand = soxCommand + "." + outputFormat + "\""
			soxCommandsList.append(soxCommand)
	# 3.2 Create individual rehersal files for each voice of the son where the voice in question is muted.
	for a in range(0,len(fileNamesList)):
		if songNamesList[a] == uniqueSong:
			soxCommand = "sox -m"
			for b in range (0,len(fileNamesList)):
				if fileNamesList[b] == fileNamesList[a]:
					soxCommand = soxCommand + " -v " + str(zeroVolume) + " \"" + inputFolder + fileNamesList[b] + "\""
				elif songNamesList[b] == songNamesList[a]:
					soxCommand = soxCommand + " -v " + str(standardPlusVolume)  + " \"" + inputFolder + fileNamesList[b] + "\""
			soxCommand = soxCommand + " \"" + outputFolder + songNamesList[a] + " - " + "Sans " + voiceNamesList[a] 
			if voiceNumbersList[a] is not 'NA':
				soxCommand = soxCommand + "-" + voiceNumbersList[a]
			soxCommand = soxCommand + "." + outputFormat + "\""
			soxCommandsList.append(soxCommand)
	# 3.3 Create a tutti file where all the voices of the song have the same volume.
	soxCommand = "sox -m"
	for c in range(0,len(fileNamesList)):
		if songNamesList[c] == uniqueSong:
			soxCommand = soxCommand + " -v " + str(standardVolume) + " \"" + inputFolder + fileNamesList[c] + "\""
	soxCommand = soxCommand + " \"" + outputFolder + uniqueSong + " - Tutti." + outputFormat + "\""
	soxCommandsList.append(soxCommand)
	
#########################
## 4. Run sox commands ##
#########################
# Uncomment the line below to print all the generated Sox commands.
# print("\n".join(soxCommandsList))
for soxCommand in soxCommandsList:
 	os.system(soxCommand)