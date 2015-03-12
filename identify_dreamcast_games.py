#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2015, Matthew Brennan Jones <matthew.brennan.jones@gmail.com>
# A module for identifying Sega Dreamcast games with Python 2 & 3
# It uses a MIT style license
# It is hosted at: https://github.com/workhorsy/identify_dreamcast_games
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys, os
import json

BUFFER_SIZE = 1024 * 1024 * 10


def fix_mislabelled_db(f, title, serial_number):
	if serial_number == "T1402N": # Mr. Driller
		f.seek(0x159208)
		blob = f.read(15)
		if blob == "DYNAMITE COP":
			return ("Dynamite Cop!", "MK-51013")
	elif serial_number == "MK-51035": # Crazy Taxi
		f.seek(0x1617E654)
		blob = f.read(9)
		if blob == "Half-Life":
			return ("Half-Life", "T0000M")
	elif serial_number == "T43903M": # Culdcept II
		f.seek(0x264E1E5D)
		blob = f.read(10)
		if blob == "CHAOSFIELD":
			return ("Chaos Field", "T47801M")
	elif serial_number == "T0000M": # Unnamed
		f.seek(0x557CAB0)
		blob = f.read(13)
		if blob == "BALL BREAKERS":
			return ("Ball Breakers", "T0000M")

		f.seek(0x4BD5EEA)
		blob = f.read(6)
		if blob == "TOEJAM":
			return ("ToeJam and Earl 3", "T0000M")
	elif serial_number == "T0000": # Unnamed
		f.seek(0x162E20)
		blob = f.read(15)
		if blob == "Art of Fighting":
			return ("Art of Fighting", "T0000")

		f.seek(0x29E898B0)
		blob = f.read(17)
		if blob == "Art of Fighting 2":
			return ("Art of Fighting 2", "T0000")

		f.seek(0x26D5BCA8)
		blob = f.read(17)
		if blob == "Art of Fighting 3":
			return ("Art of Fighting 3", "T0000")

	return (title, serial_number)

unofficial_db = {
	"RDC-0123" : "Ball Breakers",
	"THALIA-005" : "Evolution: The World of Sacred Device",
	"GYPLIKSANG" : "Half-Life - Blue Shift",
	"NGDT-DC300" : "Last Hope",
	"NGDT300P" : "Last Hope - Pink Bullets",
	"NGDT-304DCRE" : "NEO XYX",
	"51081" : "Propeller Arena",
	"MK-51162" : "Propeller Arena",
	"DR001" : "Sturmwind",
}

with open('official_us_db.json', 'rb') as f:
	official_us_db = json.loads(f.read())

with open('official_jp_db.json', 'rb') as f:
	official_jp_db = json.loads(f.read())

with open('official_eu_db.json', 'rb') as f:
	official_eu_db = json.loads(f.read())


def is_cdi_file(game_file):
	# Skip if not file
	if not os.path.isfile(game_file):
		return False

	# Skip if not a CDI file
	if not os.path.splitext(game_file)[1].lower() == '.cdi':
		return False

	return True

def locate_string_in_file(f, file_size, string_to_find):
	string_length = len(string_to_find)

	f.seek(0)
	while True:
		# Read into the buffer
		rom_data = f.read(BUFFER_SIZE)

		# Check for the end of the file
		if not rom_data:
			break

		# Figure out if we need an offset
		file_pos = f.tell()
		use_offset = False
		if file_pos > string_length and file_pos < file_size:
			use_offset = True

		# Get the string to find location
		if string_to_find in rom_data:
			index = rom_data.index(string_to_find)
			string_file_location = (file_pos - len(rom_data)) + index
			#if use_offset:
			#	string_file_location += string_length
			return string_file_location

		# Move back the length of the string to find
		# This is done to stop the string to find from being spread over multiple buffers
		if use_offset:
			f.seek(file_pos - string_length)

	return -1

def get_dreamcast_game_info(game_file):
	# Get the full file name
	full_entry = os.path.abspath(game_file)

	# Open the game file
	f = open(full_entry, 'rb', buffering=BUFFER_SIZE)
	file_size = os.path.getsize(full_entry)

	# Get the location of the header
	header_text = "SEGA SEGAKATANA SEGA ENTERPRISES"
	index = locate_string_in_file(f, file_size, header_text)
	
	# Return None if not found
	if index == -1:
		return None

	# Read the header
	f.seek(index)
	header = f.read(256)

	# Parse the header info
	offset = len(header_text)
	disc_info = header[offset + 5 : offset + 5 + 11].strip()
	region = header[offset + 14 : offset + 14 + 10].strip()
	serial_number = header[offset + 32 : offset + 32 + 10].strip()
	version = header[offset + 42 : offset + 42 + 22].strip()
	boot = header[offset + 64 : offset + 64 + 16].strip()
	maker = header[offset + 80 : offset + 80 + 16].strip()
	sloppy_title = header[offset + 96 : ].strip()
	title = None
	
	# Check for unofficial releases
	if serial_number in unofficial_db:
		title = unofficial_db[serial_number]
	# Check for official releases
	# US
	elif serial_number in official_us_db:
		title = official_us_db[serial_number]
	# Europe
	elif serial_number in official_eu_db:
		title = official_eu_db[serial_number]
	# Japan
	elif serial_number in official_jp_db:
		title = official_jp_db[serial_number]

	# Check for mislabelled releases
	title, serial_number = fix_mislabelled_db(f, title, serial_number)

	f.close()

	# Return None if the title is not found in the database
	if not title:
		print('-----------------------------------------------------')
		print(game_file)
		print('serial_number', serial_number)
		print('header', header)
		print('index', index)
		return None

	print('title', title)
	print('disc_info', disc_info)
	print('region', region)
	print('serial_number', serial_number)
	print('version', version)
	print('boot', boot)
	print('maker', maker)
	print('title', title)
	print('sloppy_title', sloppy_title)
	print('header_index', index)
	#print(header)

	return None
'''
file_name = "E:/Sega/Dreamcast/Deep Fighter/deep_fighter_dist_01.cdi"
info = get_dreamcast_game_info(file_name)
print(info)
'''
#'''
# Look at all the games, and get their serial number and proper titles
games = "E:/Sega/Dreamcast"
for root, dirs, files in os.walk(games):
	for file in files:
		# Get the full path
		entry = root + '/' + file

		if not is_cdi_file(entry):
			continue

		info = get_dreamcast_game_info(entry)
		#print(info)
#'''
		