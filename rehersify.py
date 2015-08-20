#!/usr/bin/python

# Global structure of the program:
# 0. Import necessary libraries
# 1. Set global variables
# 3. Create lists
# 4. Create sox commands
#	4.0 Define functions.
#	4.1 Go through each song individual song.
# 		4.2 Create individual rehersal files - volume increased. 
# 		4.3 Create individual rehersal files - channel muted.
#		4.4 Create tutti file.
# 5. Run sox commands.
# 6. Normalize all files.
# 7. Convert all files to mp3.

#####################################
### 0. Import necessary libraries ###
#####################################
import sys
import os

###############################
### 1. Set global variables ###
###############################
inputFolder = "./input/"
outputFolder = "./output/"
outputFormat = "aif"
temporaryFileName = "tmp.aif"
temporaryMP3fileName = "tmp.mp3"
volumeDownScale = 0.90


##########################################
### 2. Convert all input files to mono ###
##########################################
for file in os.listdir(inputFolder):
    if file.endswith((".aif",".wav")):
    	soxCommand = "sox \"" + inputFolder + file + "\" \"" + inputFolder + temporaryFileName + "\" remix -"
    	os.system(soxCommand)
    	os.remove(inputFolder + file)
    	os.rename(inputFolder + temporaryFileName, inputFolder + file)


#######################
### 3. Create lists ###
#######################
# Create a list of the file names for all files.
fileNamesList = []
# Create a list of the file endings for all files.
fileEndingsList = []
# Create a list of the song names for all files.
songNamesList = []
# Create a list of the voice names for all files.
voiceNamesList = []
# Create a list of the voice numbers for all files.
voiceNumbersList = []
# Create a list of the voice placement (relative to all other voices) for all files.
voicePlacementsList = []

# Fill in all the files created above.
for file in os.listdir(inputFolder):
    if file.endswith((".aif",".wav")):
        songName,voiceInformationAndFileEnding=file.split('@')
        voiceInformation,ending=voiceInformationAndFileEnding.split('.')
        # IF $ IS IN voiceInformation
        if '%' in voiceInformation:
        	voice,voicePlacement=voiceInformation.split('%')
        	voicePlacementsList.append(voicePlacement)
        else:
        	voice = voiceInformation
        	voicePlacementsList.append("center")
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
uniqueSongNamesList = set(songNamesList)

# Create a list of number of voices for each unique song.
numberOfVoicesForUniqueSongNamesList=[]
for song in uniqueSongNamesList:
    numberOfVoicesForUniqueSong=0
    for i in range(0,len(fileNamesList)):
        if songNamesList[i] == song:
            numberOfVoicesForUniqueSong=numberOfVoicesForUniqueSong+1
    numberOfVoicesForUniqueSongNamesList.append(numberOfVoicesForUniqueSong)

# Create a list of number of uniqe voice placements for each unique song.
numberOfUniqueVoicePlacementsForUniqueSongNamesList = []
for song in uniqueSongNamesList:
	voicePlacementsForUniqueSongList = []
	for i in range(0,len(fileNamesList)):
		if songNamesList[i] == song:
			voicePlacementsForUniqueSongList.append(voicePlacementsList[i])
	# Count instances of voice placements for each song if center placement is removed.
	tmp = [value for value in voicePlacementsForUniqueSongList if value != "center"]
	numberOfUniqueVoicePlacementsForUniqueSongNamesList.append(len(set(tmp)))

##############################
### 4. Create sox commands ###
##############################
# 4.0 Define functions.

#################################
# Function: generateSoxCommands #
#################################
# Description: Generates a set of sox commands (one for each voice, unless 'volumeFactor' is set to 1, in which case only one command is created) used to build the individual rehersal files.
# Input:
#	volumeFactor: A scaling factor deciding how much higher the main voice should be compared to the other voices. Can take on a number between 0 (the main voice is as high as all the other voice) and 1 (the main voice is the only voice that can be heard). If set to "mute", the main voice will be muted. 
# 	panFactor: A scaling factor deciding how spread out all the voices will be. Can take on a number between 0 (all the voices are centered) and 1 (the voices are maximally spread out).
def generateSoxCommands(volumeFactor,panFactor):
	outputList = []
	partCounter = 0
	leftChannelMix = ""
	rightChannelMix = ""
	soxCommand = "sox -M"
	for b in range (0,len(fileNamesList)):
		# Main voice case.
		if fileNamesList[b] == fileNamesList[a]:
			soxCommand = soxCommand + " \"" + inputFolder + fileNamesList[b] + "\""
			partCounter = partCounter + 1
			if partCounter != 1:
				leftChannelMix = leftChannelMix + ","
				rightChannelMix = rightChannelMix + ","
			leftChannelMix = leftChannelMix + str(partCounter)
			rightChannelMix = rightChannelMix + str(partCounter)
			if volumeFactor == "mute":
				leftChannelMix = leftChannelMix + "v0"
				rightChannelMix = rightChannelMix + "v0"
			else:
				panning = panFactorCalculator(panFactor,voicePlacementsList[b],numberOfUniqueVoicePlacementsForUniqueSongNamesList[uniqueSongCounter],"left")
				leftChannelMix = leftChannelMix + "v" + str(panning * volumeDownScale)
				panning = panFactorCalculator(panFactor,voicePlacementsList[b],numberOfUniqueVoicePlacementsForUniqueSongNamesList[uniqueSongCounter],"right")
				rightChannelMix = rightChannelMix + "v" + str(panning * volumeDownScale)
		# Other voice case.
		elif songNamesList[b] == songNamesList[a]:
			soxCommand = soxCommand + " \"" + inputFolder + fileNamesList[b] + "\""
			partCounter = partCounter + 1
			if partCounter != 1:
				leftChannelMix = leftChannelMix + ","
				rightChannelMix = rightChannelMix + ","
			if volumeFactor == "mute":
				volume = 1
			else:
				volume = volumeCalculator(volumeFactor,numberOfVoicesForUniqueSongNamesList[uniqueSongCounter])
			panning = panFactorCalculator(panFactor,voicePlacementsList[b],numberOfUniqueVoicePlacementsForUniqueSongNamesList[uniqueSongCounter],"left")
			leftChannelMix = leftChannelMix + str(partCounter) + "v" + str(panning * volume * volumeDownScale)
			panning = panFactorCalculator(panFactor,voicePlacementsList[b],numberOfUniqueVoicePlacementsForUniqueSongNamesList[uniqueSongCounter],"right")
			rightChannelMix = rightChannelMix + str(partCounter) + "v" + str(panning * volume * volumeDownScale)
	soxCommand = soxCommand + " \"" + outputFolder + songNamesList[a] + "@"
	if volumeFactor == 1:
		soxCommand = soxCommand + "Tutti"
	else: 
		if volumeFactor == "mute":
			soxCommand = soxCommand + "-"
		else:
			soxCommand = soxCommand + "+"
		soxCommand = soxCommand + voiceNamesList[a]
		if voiceNumbersList[a] is not 'NA':
			soxCommand = soxCommand + voiceNumbersList[a]
	soxCommand = soxCommand + "." + outputFormat + "\"" + " remix -p " + leftChannelMix + " " + rightChannelMix
	soxCommandsList.append(soxCommand)
	# soxCommand = "sox −−norm=−3 " + infile + " " + outfile
	# soxCommandsList.append(soxCommand)


#################################
# Function: panFactorCalculator #
#################################
# Description: Calculates the panning value for an individual voice based on the input values.
# Input:
#	panFactor: The desired amount of spread between the different voices. Can take a value between 0 (meaning that all voices are placed in the center) and 1 (meaning that voices are spread out as much as possible).
#	currentVoicePlacement: The voice placement that the current voice has.
#	numberOfUniqueVoicePlacements: The number of unique voice placements there are in the song in total.
#	channel: A variable that says whether the calculation should be done for the left or the right channel. Can take on the values "left" or "right".
def panFactorCalculator(panFactor,currentVoicePlacement,numberOfUniqueVoicePlacements,channel):
	if currentVoicePlacement == "center":
		return(0.5)
	else:
		currentVoicePlacement = int(currentVoicePlacement)
	if channel == "left":
		return(0.5+(panFactor/2)-(currentVoicePlacement-1)*(panFactor/(numberOfUniqueVoicePlacements-1)))
	elif channel == "right":
		return(0.5-(panFactor/2)+(currentVoicePlacement-1)*(panFactor/(numberOfUniqueVoicePlacements-1)))
	else:
		print("Error!")

##############################
# Function: volumeCalculator #
##############################
def volumeCalculator(volumeFactor,numberOfPartsForSong):
	volumeFactor = float(volumeFactor)
	numberOfPartsForSong = float(numberOfPartsForSong)
	correctionFactor = 0
	if numberOfPartsForSong == 1:
		correctionFactor = 1
	elif numberOfPartsForSong == 2:
		correctionFactor = 0.60
	elif numberOfPartsForSong == 3:
		correctionFactor = 0.40
	elif numberOfPartsForSong == 4:
		correctionFactor = 0.25
	elif numberOfPartsForSong == 5:
		correctionFactor = 0.20
	elif numberOfPartsForSong == 6:
		correctionFactor = 0.15
	elif numberOfPartsForSong == 7:
		correctionFactor = 0.125
	elif numberOfPartsForSong == 8:
		correctionFactor = 0.10
	elif numberOfPartsForSong == 9:
		correctionFactor = 0.10
	elif numberOfPartsForSong == 10:
		correctionFactor = 0.10
	elif numberOfPartsForSong == 11:
		correctionFactor = 0.10
	elif numberOfPartsForSong == 12:
		correctionFactor = 0.10
	elif numberOfPartsForSong == 13:
		correctionFactor = 0.10
	elif numberOfPartsForSong == 14:
		correctionFactor = 0.10
	return(volumeFactor*correctionFactor)

# 4.1 Go through each individual song.
soxCommandsList = []
uniqueSongCounter = -1
# Loop for each unique song.
for uniqueSong in uniqueSongNamesList:
	uniqueSongCounter = uniqueSongCounter + 1
	# 4.1 Create individual rehersal files for each voice of the song where the voice in question is higher than the others.
	for a in range(0,len(fileNamesList)):
		if songNamesList[a] == uniqueSong:
			generateSoxCommands(0.60,0)
			
	# 4.2 Create individual rehersal files for each voice of the song where the voice in question is muted.
	for a in range(0,len(fileNamesList)):
		if songNamesList[a] == uniqueSong:
			generateSoxCommands("mute",1)

	# 4.3 Create a tutti file of the song.
	for a in range(0,len(fileNamesList)):
		if songNamesList[a] == uniqueSong:
			generateSoxCommands(1,0.8)
	
###########################
### 5. Run sox commands ###
###########################
# Uncomment the line below to print all the generated Sox commands.
# print("\n".join(soxCommandsList))
for soxCommand in soxCommandsList:
	print(soxCommand)
	os.system(soxCommand)


##############################
### 6. Normalize all files ###
##############################
for file in os.listdir(outputFolder):
    if file.endswith((".aif",".wav")):
    	soxCommand = "sox --norm=-3 \"" + outputFolder + file + "\" \"" + outputFolder + temporaryFileName + "\""
    	os.system(soxCommand)
    	os.remove(outputFolder + file)
    	os.rename(outputFolder + temporaryFileName, outputFolder + file)

###################################
### 7. Convert all files to mp3 ###
###################################
for file in os.listdir(outputFolder):
    if file.endswith((".aif",".wav")):
    	fileName,fileEnding=file.split('.')
    	lameCommand = "lame -V2 \"" + outputFolder + file + "\" \"" + outputFolder + fileName + ".mp3" + "\""
    	os.system(lameCommand)
    	os.remove(outputFolder + file)

