#!/usr/bin/python

##################################
### Import necessary libraries ###
##################################
import sys
import os
import shutil
from shutil import copyfile

#####################
### Set variables ###
#####################
# IO
## The folder where you should place the input files.
input_folder = "./input/"
## Input formats to use.
LIST_input_formats = 'aif','wav'
## The folder where intermediate files should be placed (and eventually removed).
intermediate_folder = "./.intermediate/"
## Intermediate file name to use.
temporary_file_name = "tmp"
## Intermediate format to use.
intermediate_format = "aif"
## The folder where the output files are going to appear.
output_folder = "./output/"

# Options
## Meteronome
BOOLEAN_add_meteronome = True
meteronome_keywords = ['Meteronome','meteronome']
## Tutti
BOOLEAN_create_tutti_rehersal_files = True
## Dominant
BOOLEAN_create_dominant_rehersal_files = True
## Side
BOOLEAN_create_side_rehersal_files = True
## Mute
BOOLEAN_create_mute_rehersal_files = True
BOOLEAN_mute_whole_voice_group = False
## Post processing
BOOLEAN_normalize_output_files = True
BOOLEAN_convert_output_files_to_mp3 = True

#########################
### Class definitions ###
#########################
# IO class.
class CLASS_io():
	def __init__(self, input_folder, LIST_input_formats, intermediate_folder, temporary_file_name, intermediate_format, output_folder):
		self.input_folder = input_folder
		self.LIST_input_formats = LIST_input_formats
		self.intermediate_folder = intermediate_folder
		self.temporary_file_name = temporary_file_name
		self.intermediate_format = intermediate_format
		self.output_folder = output_folder

# Options classes.
## Global option class that holds global variables and suboptions classes.
class CLASS_options():
	def __init__(self, OBJECT_meteronome, OBJECT_tutti, OBJECT_dominant, OBJECT_options_side, OBJECT_mute, OBJECT_post_processing):
		self.OBJECT_meteronome = OBJECT_meteronome
		self.OBJECT_tutti = OBJECT_tutti
		self.OBJECT_dominant = OBJECT_dominant
		self.OBJECT_side = OBJECT_options_side
		self.OBJECT_mute = OBJECT_mute
		self.OBJECT_post_processing = OBJECT_post_processing

## Suboption class for meteronome options.
class CLASS_meteronome():
	def __init__(self, BOOLEAN_add_meteronome, meteronome_keyword):
		self.BOOLEAN_add_meteronome = BOOLEAN_add_meteronome
		self.meteronome_keywords = meteronome_keywords

## Suboption class for tutti rehersal files.
class CLASS_tutti():
	def __init__(self, BOOLEAN_create_tutti_rehersal_files):
		self.BOOLEAN_create_rehersal_files = BOOLEAN_create_tutti_rehersal_files

## Suboption class for dominant rehersal files.
class CLASS_dominant():
	def __init__(self, BOOLEAN_create_dominant_rehersal_files):
		self.BOOLEAN_create_rehersal_files = BOOLEAN_create_dominant_rehersal_files

## Suboption class for side rehersal files.
class CLASS_side():
	def __init__(self, BOOLEAN_create_side_rehersal_files):
		self.BOOLEAN_create_rehersal_files = BOOLEAN_create_side_rehersal_files

## Suboption class for mute rehersal files.
class CLASS_mute():
	def __init__(self, BOOLEAN_create_mute_rehersal_files, BOOLEAN_mute_whole_voice_group):
		self.BOOLEAN_create_rehersal_files = BOOLEAN_create_mute_rehersal_files
		self.BOOLEAN_mute_whole_voice_group = BOOLEAN_mute_whole_voice_group

## Suboption class for post processing.
class CLASS_post_processing():
	def __init__(self, BOOLEAN_normalize_output_files, BOOLEAN_convert_output_files_to_mp3):
		self.BOOLEAN_normalize = BOOLEAN_normalize_output_files
		self.BOOLEAN_convert_to_mp3 = BOOLEAN_convert_output_files_to_mp3

# Input files information class
class CLASS_input_files_information():
	def __init__(self, OBJECT_io, OBJECT_options, LIST_input_files):
		self.OBJECT_io = OBJECT_io
		self.OBJECT_options = OBJECT_options
		# Create a file information table.
		self.TABLE = [['File','Song','Voice','Voice_group','Amount_in_voice_group','Total_number_of_voice_groups','Meteronome','File_ending']]
		
		# Go through each file and fill in information for all the lists created above.
		for file in LIST_input_files:
			song,voice_information_and_file_ending = file.split('@')
			voice_information,file_ending = voice_information_and_file_ending.split('.')
			voice_name,voice_group = voice_information.split('%')
			# Add an empty row to the information table.
			self.TABLE.append([None] * len(self.TABLE[0]))
			# Add information to the newly created row.
			self.TABLE[len(self.TABLE)-1][self.TABLE[0].index('File')] = file
			self.TABLE[len(self.TABLE)-1][self.TABLE[0].index('Song')] = song
			self.TABLE[len(self.TABLE)-1][self.TABLE[0].index('Voice')] = voice_name
			self.TABLE[len(self.TABLE)-1][self.TABLE[0].index('Voice_group')] = voice_group
			self.TABLE[len(self.TABLE)-1][self.TABLE[0].index('File_ending')] = file_ending

		# Extract and fill out amount in voice group variable for each file.
		Voice_group_column = extract_column_from_table(self.TABLE, 'Voice_group')
		for a in range(1,len(self.TABLE)):
			tmp = self.TABLE[a][self.TABLE[0].index('Voice_group')]
			self.TABLE[a][self.TABLE[0].index('Amount_in_voice_group')] = Voice_group_column.count(tmp)

		# Extract and fill out total number of voice groups for each file (this will be the same number for all files).
		tmp = extract_column_from_table(self.TABLE,'Voice_group')
		tmp2 = []
		for a in tmp:
			try:
				tmp2.append(int(a))
			except Exception:
				pass
		tmp3 = []
		for a in tmp2:
			if a not in tmp3:
				tmp3.append(a)
		for a in range(1,len(self.TABLE)):
			self.TABLE[a][self.TABLE[0].index('Total_number_of_voice_groups')] = len(tmp3)

		# Extract and fill out meteronome information for each file.
		for a in range(1,len(self.TABLE)):
			tmp = self.TABLE[a][self.TABLE[0].index('Voice_group')]
			if tmp in self.OBJECT_options.OBJECT_meteronome.meteronome_keywords:
				self.TABLE[a][self.TABLE[0].index('Meteronome')] = True
			else:
				self.TABLE[a][self.TABLE[0].index('Meteronome')] = False

# Output files information class
class CLASS_output_files_information():
	TABLE = [['File','File_without_ending','File_ending']]

	@staticmethod
	def add_file(self, file):
		file_without_ending,file_ending = file.split('.')
		self.TABLE.append([None] * len(self.TABLE[0]))
		self.TABLE[len(self.TABLE)-1][self.TABLE[0].index('File')] = file
		self.TABLE[len(self.TABLE)-1][self.TABLE[0].index('File_without_ending')] = file_without_ending
		self.TABLE[len(self.TABLE)-1][self.TABLE[0].index('File_ending')] = file_ending

# Song class.
class CLASS_song():
	def __init__(self, OBJECT_io, OBJECT_input_files_information, OBJECT_options):
		self.OBJECT_io = OBJECT_io
		self.OBJECT_input_files_information = OBJECT_input_files_information
		self.OBJECT_output_files_information = CLASS_output_files_information
		self.OBJECT_options = OBJECT_options

# Pre-processing
class CLASS_do_pre_processing():
	def __init__(self, OBJECT_song):
		self.OBJECT_song = OBJECT_song

	def run(self,this_object):
		self.remove_intermediate_folder()
		self.create_intermediate_folder()
		self.check_file_endings()
		self.copy_input_files_to_intermediate_folder()
		self.convert_input_files_to_mono()

	def remove_intermediate_folder(self):
		if os.path.exists(self.OBJECT_song.OBJECT_io.intermediate_folder):
			shutil.rmtree(self.OBJECT_song.OBJECT_io.intermediate_folder)

	def create_intermediate_folder(self):
		if not os.path.exists(self.OBJECT_song.OBJECT_io.intermediate_folder):
			os.makedirs(self.OBJECT_song.OBJECT_io.intermediate_folder)

	def check_file_endings(self):
		tmp = extract_column_from_table(self.OBJECT_song.OBJECT_input_files_information.TABLE, 'File_ending')
		for file_ending in tmp:
			if file_ending not in self.OBJECT_song.OBJECT_io.LIST_input_formats:
				raise ValueError('Input files need to be of the form: ' + ', '.join(self.OBJECT_song.OBJECT_io.LIST_input_formats))

	def copy_input_files_to_intermediate_folder(self):
		tmp = extract_column_from_table(self.OBJECT_song.OBJECT_input_files_information.TABLE, 'File')
		for file in tmp:
			copyfile(self.OBJECT_song.OBJECT_io.input_folder + file, self.OBJECT_song.OBJECT_io.intermediate_folder + file)

	def convert_input_files_to_mono(self):
		tmp = extract_column_from_table(self.OBJECT_song.OBJECT_input_files_information.TABLE, 'File')
		for file in tmp:
			sox_command = "sox \"" + self.OBJECT_song.OBJECT_io.intermediate_folder + file + "\" \"" + self.OBJECT_song.OBJECT_io.intermediate_folder + self.OBJECT_song.OBJECT_io.temporary_file_name + "." + self.OBJECT_song.OBJECT_io.intermediate_format + "\" remix -"
			os.system(sox_command)
			os.remove(self.OBJECT_song.OBJECT_io.intermediate_folder + file)
			os.rename(self.OBJECT_song.OBJECT_io.intermediate_folder + self.OBJECT_song.OBJECT_io.temporary_file_name + "." + self.OBJECT_song.OBJECT_io.intermediate_format, self.OBJECT_song.OBJECT_io.intermediate_folder + file)

# Rehersal files creator
class CLASS_do_rehersal_files():
	def __init__(self, OBJECT_song):
		self.OBJECT_song = OBJECT_song

	def run(self,this_object):
		self.create_tutti_files()
		self.create_dominant_files()
		self.create_side_files()
		self.create_mute_files()

	def create_tutti_files(self):
		if self.OBJECT_song.OBJECT_options.OBJECT_tutti.BOOLEAN_create_rehersal_files:
			LIST_pan_factors_left = []
			LIST_pan_factors_right = []
			LIST_volume_factors = []
			for a in range(1,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)):
				LIST_volume_factors.append(volume_factor_calculator(self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Amount_in_voice_group')]))
				LIST_pan_factors_left.append(pan_factor_calculator(1,self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')],self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Total_number_of_voice_groups')], 'left'))
				LIST_pan_factors_right.append(pan_factor_calculator(1,self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')],self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Total_number_of_voice_groups')], 'right'))
			sox_command = "sox -M "
			for file in extract_column_from_table(self.OBJECT_song.OBJECT_input_files_information.TABLE, 'File'):
				sox_command = sox_command + "\"" + self.OBJECT_song.OBJECT_io.intermediate_folder + file + "\" "
			new_file_name = self.OBJECT_song.OBJECT_input_files_information.TABLE[1][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Song')] + "@Tutti." + self.OBJECT_song.OBJECT_io.intermediate_format
			sox_command = sox_command + "\"" + self.OBJECT_song.OBJECT_io.intermediate_folder + new_file_name + "\" "
			sox_command = sox_command + 'remix -p '
			# Add left channel.
			for a in range(0,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)-1):
				sox_command = sox_command + str(a+1) + 'v' + str(1 * LIST_volume_factors[a] * LIST_pan_factors_left[a]) + ','
			# Add right channel.
			sox_command = sox_command + ' '
			for a in range(0,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)-1):
				sox_command = sox_command + str(a+1) + 'v' + str(1 * LIST_volume_factors[a] * LIST_pan_factors_right[a]) + ','
			print(sox_command)
			os.system(sox_command)
			self.OBJECT_song.OBJECT_output_files_information.add_file(self.OBJECT_song.OBJECT_output_files_information, new_file_name)

	def create_dominant_files(self):
		if self.OBJECT_song.OBJECT_options.OBJECT_dominant.BOOLEAN_create_rehersal_files:
			for x in range(1,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)):
				current_file = self.OBJECT_song.OBJECT_input_files_information.TABLE[x][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('File')]
				current_voice = self.OBJECT_song.OBJECT_input_files_information.TABLE[x][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice')]
				current_voice_group = self.OBJECT_song.OBJECT_input_files_information.TABLE[x][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')]
				LIST_pan_factors_left = []
				LIST_pan_factors_right = []
				LIST_volume_factors = []
				for a in range(1,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)):
					LIST_volume_factors.append(volume_factor_calculator(self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Amount_in_voice_group')]))
					LIST_pan_factors_left.append(pan_factor_calculator(1,self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')],self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Total_number_of_voice_groups')], 'left'))
					LIST_pan_factors_right.append(pan_factor_calculator(1,self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')],self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Total_number_of_voice_groups')], 'right'))
					if current_voice == self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice')]:
						LIST_pan_factors_left[a-1] = 0.5
						LIST_pan_factors_right[a-1] = 0.5
						LIST_volume_factors[a-1] = 4

				sox_command = "sox -M "
				for file in extract_column_from_table(self.OBJECT_song.OBJECT_input_files_information.TABLE, 'File'):
					sox_command = sox_command + "\"" + self.OBJECT_song.OBJECT_io.intermediate_folder + file + "\" "
				new_file_name = self.OBJECT_song.OBJECT_input_files_information.TABLE[1][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Song')] + "@+" + current_voice + "." + self.OBJECT_song.OBJECT_io.intermediate_format
				sox_command = sox_command + "\"" + self.OBJECT_song.OBJECT_io.intermediate_folder + new_file_name + "\" "
				sox_command = sox_command + 'remix -p '
				# Add left channel.
				for a in range(0,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)-1):
					sox_command = sox_command + str(a+1) + 'v' + str(LIST_volume_factors[a] * LIST_pan_factors_left[a]) + ','
				# Add right channel.
				sox_command = sox_command + ' '
				for a in range(0,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)-1):
					sox_command = sox_command + str(a+1) + 'v' + str(LIST_volume_factors[a] * LIST_pan_factors_right[a]) + ','
				print(sox_command)
				os.system(sox_command)
				self.OBJECT_song.OBJECT_output_files_information.add_file(self.OBJECT_song.OBJECT_output_files_information, new_file_name)


	def create_side_files(self):
		if self.OBJECT_song.OBJECT_options.OBJECT_side.BOOLEAN_create_rehersal_files:
			for x in range(1,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)):
				current_file = self.OBJECT_song.OBJECT_input_files_information.TABLE[x][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('File')]
				current_voice = self.OBJECT_song.OBJECT_input_files_information.TABLE[x][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice')]
				current_voice_group = self.OBJECT_song.OBJECT_input_files_information.TABLE[x][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')]
				LIST_pan_factors_left = []
				LIST_pan_factors_right = []
				LIST_volume_factors = []
				for a in range(1,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)):
					LIST_volume_factors.append(volume_factor_calculator(self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Amount_in_voice_group')]))
					LIST_pan_factors_left.append(pan_factor_calculator(1,self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')],self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Total_number_of_voice_groups')], 'left'))
					LIST_pan_factors_right.append(pan_factor_calculator(1,self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')],self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Total_number_of_voice_groups')], 'right'))
					if current_voice == self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice')]:
						LIST_pan_factors_left[a-1] = 1
						LIST_pan_factors_right[a-1] = 0
						LIST_volume_factors[a-1] = 4
					else:
						LIST_pan_factors_left[a-1] = 0
						LIST_pan_factors_right[a-1] = 1			

				sox_command = "sox -M "
				for file in extract_column_from_table(self.OBJECT_song.OBJECT_input_files_information.TABLE, 'File'):
					sox_command = sox_command + "\"" + self.OBJECT_song.OBJECT_io.intermediate_folder + file + "\" "
				new_file_name = self.OBJECT_song.OBJECT_input_files_information.TABLE[1][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Song')] + "@left_" + current_voice + "." + self.OBJECT_song.OBJECT_io.intermediate_format
				sox_command = sox_command + "\"" + self.OBJECT_song.OBJECT_io.intermediate_folder + new_file_name + "\" "
				sox_command = sox_command + 'remix -p '
				# Add left channel.
				for a in range(0,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)-1):
					sox_command = sox_command + str(a+1) + 'v' + str(LIST_volume_factors[a] * LIST_pan_factors_left[a]) + ','
				# Add right channel.
				sox_command = sox_command + ' '
				for a in range(0,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)-1):
					sox_command = sox_command + str(a+1) + 'v' + str(LIST_volume_factors[a] * LIST_pan_factors_right[a]) + ','
				print(sox_command)
				os.system(sox_command)
				self.OBJECT_song.OBJECT_output_files_information.add_file(self.OBJECT_song.OBJECT_output_files_information, new_file_name)


	def create_mute_files(self):
		if self.OBJECT_song.OBJECT_options.OBJECT_mute.BOOLEAN_create_rehersal_files:
			for x in range(1,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)):
				current_file = self.OBJECT_song.OBJECT_input_files_information.TABLE[x][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('File')]
				current_voice = self.OBJECT_song.OBJECT_input_files_information.TABLE[x][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice')]
				current_voice_group = self.OBJECT_song.OBJECT_input_files_information.TABLE[x][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')]
				LIST_pan_factors_left = []
				LIST_pan_factors_right = []
				LIST_volume_factors = []
				for a in range(1,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)):
					LIST_volume_factors.append(volume_factor_calculator(self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Amount_in_voice_group')]))
					LIST_pan_factors_left.append(pan_factor_calculator(1,self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')],self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Total_number_of_voice_groups')], 'left'))
					LIST_pan_factors_right.append(pan_factor_calculator(1,self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')],self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Total_number_of_voice_groups')], 'right'))
					if current_voice_group == self.OBJECT_song.OBJECT_input_files_information.TABLE[a][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Voice_group')]:
						LIST_pan_factors_left[a-1] = 0
						LIST_pan_factors_right[a-1] = 0
				sox_command = "sox -M "
				for file in extract_column_from_table(self.OBJECT_song.OBJECT_input_files_information.TABLE, 'File'):
					sox_command = sox_command + "\"" + self.OBJECT_song.OBJECT_io.intermediate_folder + file + "\" "
				new_file_name = self.OBJECT_song.OBJECT_input_files_information.TABLE[1][self.OBJECT_song.OBJECT_input_files_information.TABLE[0].index('Song')] + "@-" + current_voice + "." + self.OBJECT_song.OBJECT_io.intermediate_format
				sox_command = sox_command + "\"" + self.OBJECT_song.OBJECT_io.intermediate_folder + new_file_name + "\" "
				sox_command = sox_command + 'remix -p '
				# Add left channel.
				for a in range(0,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)-1):
					sox_command = sox_command + str(a+1) + 'v' + str(1 * LIST_volume_factors[a] * LIST_pan_factors_left[a]) + ','
				# Add right channel.
				sox_command = sox_command + ' '
				for a in range(0,len(self.OBJECT_song.OBJECT_input_files_information.TABLE)-1):
					sox_command = sox_command + str(a+1) + 'v' + str(1 * LIST_volume_factors[a] * LIST_pan_factors_right[a]) + ','
				print(sox_command)
				os.system(sox_command)
				self.OBJECT_song.OBJECT_output_files_information.add_file(self.OBJECT_song.OBJECT_output_files_information, new_file_name)

# Post-processing
class CLASS_do_post_processing():
	def __init__(self, OBJECT_song):
		self.OBJECT_song = OBJECT_song

	def run(self,this_object):
		self.normalize_files()
		self.convert_files_to_mp3()
		self.create_output_folder()
		self.copy_files_to_output_folder()
		self.remove_intermediate_folder()

	def normalize_files(self):
		if self.OBJECT_song.OBJECT_options.OBJECT_post_processing.BOOLEAN_normalize:
			for a in range(1,len(self.OBJECT_song.OBJECT_output_files_information.TABLE)):
				file = self.OBJECT_song.OBJECT_output_files_information.TABLE[a][self.OBJECT_song.OBJECT_output_files_information.TABLE[0].index('File')]
				sox_command = "sox --norm=-3 \"" + self.OBJECT_song.OBJECT_io.intermediate_folder + file + "\" \"" + self.OBJECT_song.OBJECT_io.intermediate_folder + self.OBJECT_song.OBJECT_io.temporary_file_name + "." + self.OBJECT_song.OBJECT_io.intermediate_format + "\""
				os.system(sox_command)
				os.remove(self.OBJECT_song.OBJECT_io.intermediate_folder + file)
				os.rename(self.OBJECT_song.OBJECT_io.intermediate_folder + self.OBJECT_song.OBJECT_io.temporary_file_name + "." + self.OBJECT_song.OBJECT_io.intermediate_format, self.OBJECT_song.OBJECT_io.intermediate_folder + file)

	def convert_files_to_mp3(self):
		if self.OBJECT_song.OBJECT_options.OBJECT_post_processing.BOOLEAN_convert_to_mp3:
			for a in range(1,len(self.OBJECT_song.OBJECT_output_files_information.TABLE)):
				file = self.OBJECT_song.OBJECT_output_files_information.TABLE[a][self.OBJECT_song.OBJECT_output_files_information.TABLE[0].index('File')]
				file_without_ending = self.OBJECT_song.OBJECT_output_files_information.TABLE[a][self.OBJECT_song.OBJECT_output_files_information.TABLE[0].index('File_without_ending')]
				lame_command = lame_command = "lame -V2 -h --silent \"" + self.OBJECT_song.OBJECT_io.intermediate_folder + file + "\" \"" + self.OBJECT_song.OBJECT_io.intermediate_folder + file_without_ending + ".mp3" + "\""
				os.system(lame_command)
				os.remove(self.OBJECT_song.OBJECT_io.intermediate_folder + file)
				# Update the output files information object with the newly created files.
				self.OBJECT_song.OBJECT_output_files_information.TABLE[a][self.OBJECT_song.OBJECT_output_files_information.TABLE[0].index('File')] = file_without_ending + ".mp3"
				self.OBJECT_song.OBJECT_output_files_information.TABLE[a][self.OBJECT_song.OBJECT_output_files_information.TABLE[0].index('File_without_ending')] = file_without_ending     
				self.OBJECT_song.OBJECT_output_files_information.TABLE[a][self.OBJECT_song.OBJECT_output_files_information.TABLE[0].index('File_ending')] = 'mp3'

	def create_output_folder(self):
		if not os.path.exists(self.OBJECT_song.OBJECT_io.output_folder):
			os.makedirs(self.OBJECT_song.OBJECT_io.output_folder)

	def copy_files_to_output_folder(self):
		tmp = extract_column_from_table(self.OBJECT_song.OBJECT_output_files_information.TABLE, 'File')
		for file in tmp:
			copyfile(self.OBJECT_song.OBJECT_io.intermediate_folder + file, self.OBJECT_song.OBJECT_io.output_folder + file)

	def remove_intermediate_folder(self):
		if os.path.exists(self.OBJECT_song.OBJECT_io.intermediate_folder):
			shutil.rmtree(self.OBJECT_song.OBJECT_io.intermediate_folder)

############################
### Function definitions ###
############################
# Function to extract a column from the table constructs that are used in this program.
def extract_column_from_table(table, column):
	if isinstance(column, basestring):
		tmp = []
		for a in range(1,(len(table))):
			tmp.append(table[a][table[0].index(column)])
		return(tmp)
	elif isinstance(column, int):
		tmp = []
		for a in range(1,(len(table))):
			tmp.append(table[a][column])
		return(tmp)
	else:
		raise ValueError('Column input is not an integer or a string.')

def pan_factor_calculator(pan_factor, voice_group, total_number_of_voice_groups, channel):
# # Description: Calculates the panning value for an individual voice based on the input values.
# # Input:
# ## pan_factor: The desired amount of spread between the different voices. Can take a value between 0 (meaning that all voices are placed in the center) and 1 (meaning that voices are spread out as much as possible).
# ## voice_group: The voice group that the current voice belongs to.
# ## total_number_of_voice_groups: The number of unique voice groups there are in the song in total.
# ## channel: A variable that says whether the calculation should be done for the left or the right channel. Can take on the values "left" or "right".
	try:
		pan_factor = float(pan_factor)
		voice_group = float(voice_group)
		total_number_of_voice_groups = float(total_number_of_voice_groups)
		if channel == "left":
			#print(pan_factor/(total_number_of_voice_groups-1))
			return(0.5 + (pan_factor / 2) - (voice_group - 1) * (pan_factor / (total_number_of_voice_groups - 1)))
		elif channel == "right":
			return(0.5 - (pan_factor / 2) + (voice_group - 1) * (pan_factor / (total_number_of_voice_groups - 1)))
	except Exception:
		return(0.5)

def volume_factor_calculator(input):
	return(1)

#####################
### Main function ###
#####################
# Create an io object.
OBJECT_io = CLASS_io(input_folder, LIST_input_formats, intermediate_folder, temporary_file_name, intermediate_format, output_folder)

# Create suboptions objects that are going to be in the options object.
OBJECT_meteronome = CLASS_meteronome(BOOLEAN_add_meteronome, meteronome_keywords)
OBJECT_tutti = CLASS_tutti(BOOLEAN_create_tutti_rehersal_files)
OBJECT_dominant = CLASS_dominant(BOOLEAN_create_dominant_rehersal_files)
OBJECT_options_side = CLASS_side(BOOLEAN_create_side_rehersal_files)
OBJECT_mute = CLASS_tutti(BOOLEAN_create_mute_rehersal_files)
OBJECT_post_processing = CLASS_post_processing(BOOLEAN_normalize_output_files, BOOLEAN_convert_output_files_to_mp3)

# Create an options object.
OBJECT_options = CLASS_options(OBJECT_meteronome, OBJECT_tutti, OBJECT_dominant, OBJECT_options_side, OBJECT_mute, OBJECT_post_processing)

# Create a list of the file names in the input folder that ends with the allowable file name endings.
LIST_file_names = []
for file in os.listdir(OBJECT_io.input_folder):
    if file.endswith((OBJECT_io.LIST_input_formats)):
    	LIST_file_names.append(file)

# Create a list of all the song names.
LIST_song_names = [] 
for file in LIST_file_names:
	song_name,trash=file.split('@')
	LIST_song_names.append(song_name)

# Create a list of unique song names.
LIST_unique_song_names = set(LIST_song_names)

# Create a list of where all the files associated with each unique song name can be found.
LIST_unique_song_names_positions = []
for unique_song in LIST_unique_song_names:
	counter = -1
	tmp = []
	for song in LIST_song_names:
		counter = counter + 1
		if song == unique_song:
			tmp.append(counter)
	LIST_unique_song_names_positions.append((tmp))

# Create song objects for each song and create a list containing all song objects.
LIST_song_objects = []
for a in LIST_unique_song_names_positions:
	tmp = []
	for b in a:
		tmp.append(LIST_file_names[b])
	OBJECT_input_files_information = CLASS_input_files_information(OBJECT_io, OBJECT_options, tmp)
	LIST_song_objects.append(CLASS_song(OBJECT_io,OBJECT_input_files_information,OBJECT_options))

# Let each song object go through the processing chain.
for OBJECT_song in LIST_song_objects:
	OBJECT_do_pre_processing = CLASS_do_pre_processing(OBJECT_song)
	OBJECT_do_pre_processing.run(OBJECT_do_pre_processing)
	OBJECT_do_rehersal_files = CLASS_do_rehersal_files(OBJECT_song)
	OBJECT_do_rehersal_files.run(OBJECT_do_rehersal_files)
	OBJECT_do_post_processing = CLASS_do_post_processing(OBJECT_song)
	OBJECT_do_post_processing.run(OBJECT_post_processing)