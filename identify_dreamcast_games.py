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

official_db = {
	"T40201N" : "Aero Wings",
	"T40210N" : "Aero Wings 2: Airstrike",
	"T9501N" : "AirForce Delta",
	"MK-51171" : "Alien Front Online",
	"T15117N" : "Alone in the Dark: The New Nightmare",
	"T47110M" : "Baldr Force EXE",
	"T44102N" : "Bang! Gunship Elite",
	"T40217N" : "Bangai-O",
	"T38702M" : "Bangai-O",
	"T7011D  50" : "Bangai-O",
	"T20101M" : "Black Matrix AD",
	"T13001N" : "Blue Stinger",
	"MK-51065" : "Bomberman Online",
	"RDC-0117" : "Bomberman Online",
	"T46703M" : "Border Down",
	"T1215N" : "Cannon Spike",
	"T1218N" : "Capcom vs. SNK",
	"T1217M" : "Capcom vs. SNK: Millennium Fight 2000",
	"T1249M" : "Capcom vs. SNK 2: Millionaire Fighting 2001",
	"T5701N" : "Carrier",
	"T47801M" : "Chaos Field",
	"T15127N" : "Charge N Blast",
	"HDR-0039" : "ChuChu Rocket!",
	"HDR-0048" : "ChuChu Rocket!",
	"MK-51049" : "ChuChu Rocket!",
	"MK-51049  50" : "ChuChu Rocket!",
	"RDC-0140" : "ChuChu Rocket!",
	"MK-51160" : "Confidential Mission",
	"MK-51035" : "Crazy Taxi",
	"MK-51136" : "Crazy Taxi 2",
	"MK-5113650" : "Crazy Taxi 2",
	"T43903M" : "Culdcept II",
	"MK-51036" : "D2",
	"MK-51037" : "Daytona USA",
	"T19724M" : "Daytona USA",
	"T3601N" : "Dead or Alive 2",
	"T8116D-05" : "Dead or Alive 2",
	"T3602M" : "Dead or Alive 2",
	"T3601M" : "Dead or Alive 2 Limited Edition",
	"T2401N" : "Death Crimson OX",
	"T17705N" : "Deep Fighter",
	"T17704D" : "Deep Fighter",
	"T17704D 09" : "Deep Fighter",
	"T15112N" : "Demolition Racer: No Exit",
	"T1217N" : "Dino Crisis",
	"T40203N" : "Draconus - Cult of The Wyrm",
	"T17720N" : "Dragonriders Chronicles of Pern",
	"MK-51033" : "Ecco the Dolphin: Defender of the Future",
	"MK-51033  50" : "Ecco the Dolphin: Defender of the Future",
	"T41601N" : "Elemental Gimmick Gear",
	"T14302M" : "Elemental Gimmick Gear",
	"T46605D  71" : "Evil Twin: Cyprien's Chronicles",
	"T17705SD  50" : "Evolution: The World of Sacred Device",
	"T17706N" : "Evolution: The World of Sacred Device",
	"T17711N" : "Evolution 2: Far Off Promise",
	"T1711N" : "Evolution 2: Far Off Promise",
	"T45005D  50" : "Evolution 2: Far Off Promise",
	"T15104N" : "Expendable",
	"MK1014" : "Fast Striker",
	"T44306N" : "Fatal Fury - Mark of The Wolves",
	"T35801N" : "Fighting Force 2",
	"T36802D  05" : "Fighting Force 2",
	"HDR-0133" : "Fighting Vipers 2",
	"HDR-0133 -1" : "Fighting Vipers 2",
	"MK-51154  50" : "Fighting Vipers 2",
	"T34201M" : "Frame Gride",
	"T3108M" : "Garou - Mark of the Wolves",
	"T1222N" : "GigaWing 2",
	"T42102N" : "Grand Theft Auto 2",
	"T17716N" : "Grandia 2",
	"T2402M" : "Guilty Gear X",
	"T1214N" : "Gun Bird 2",
	"T13301N" : "Gundam Side Story 0079 - Rise From The Ashes",
	"MK-5104150" : "Head Hunter",
	"MK-51002" : "House of the Dead 2",
	"HDR-0007" : "House of the Dead 2",
	"HDR-0011" : "House of the Dead 2",
	"MK51002  50" : "House of the Dead 2",
	"MK51045 50" : "House of the Dead 2",
	"T9702N" : "Hydro Thunder",
	"T38706M" : "Ikaruga",
	"T46001N" : "Illbleed",
	"T12503N" : "Incoming",
	"MK-51058" : "Jet Grind Radio",
	"T1206N" : "JoJo's Bizarre Adventure",
	"T47803M" : "Karous",
	"T44302N" : "King of Fighters '99 Evolution, The",
	"T47303M" : "King of Fighters 2000, The",
	"T47304M" : "King of Fighters 2001, The",
	"T47305M" : "King of Fighters 2002, The",
	"T2106M" : "L.O.L. Lack Of Love",
	"T44305N" : "The Last Blade 2: Heart of the Samurai",
	"T36802N" : "Legacy of Kain - Soul Reaver",
	"T21501M" : "Macross M3",
	"MK-51050" : "Maken X",
	"T2201M" : "Marionette Handler",
	"T1221N" : "Mars Matrix",
	"T1202N" : "Marvel vs. Capcom: Clash of Super Heroes",
	"T1212N" : "Marvel vs. Capcom 2",
	"T12502N" : "MDK2",
	"T51012" : "Metropolis Street Racer",
	"" : "Millennium Soldier",
	"T40508D" : "Moho",
	"T9701N" : "Mortal Kombat Gold",
	"T1402N" : "Mr. Driller",
	"T9904M" : "Neo Golden Logres",
	"T9504N" : "Nightmare Creatures 2",
	"T36807N" : "Omikron - The Nomad Soul",
	"MK-51140" : "Ooga Booga",
	"MK-51102" : "Outtrigger",
	"MK-51100" : "Phantasy Star Online",
	"T1207N" : "Plasma Sword: Nightmare of Bilstein",
	"T1201N" : "Power Stone",
	"T1211N" : "Power Stone 2",
	"T1219N" : "Project Justice",
	"T31101N" : "Psychic Force 2012",
	"T9907M" : "Psyvariar 2: The Will to Fabricate",
	"MK-51061" : "Quake III Arena",
	"T47802M " : "Radirgy",
	"T9901M" : "Rainbow Cotton",
	"T17704N" : "Rayman 2: The Great Escape",
	"T17707D  50" : "Rayman 2: The Great Escape",
	"T17703M" : "Rayman: Kaizokufune Kara no Dasshutsu!",
	"T9704N" : "Ready 2 Rumble Boxing",
	"T9717N" : "Ready 2 Rumble Boxing: Round 2",
	"T40218N" : "Record of Lodoss War",
	"T40215N" : "Red Dog: Superior Firepower",
	"RDXRE-JP" : "Redux: Dark Matters",
	"T1204N" : "Resident Evil Code: Veronica",
	"T1205N" : "Resident Evil 2",
	"T1220N" : "Resident Evil 3: Nemesis",
	"MK-51192  50" : "Rez",
	"T9707N" : "San Francisco Rush 2049",
	"T9709D  61" : "San Francisco Rush 2049",
	"MK-51092" : "Samba De Amigo",
	"MK-51053" : "Sega GT",
	"MK-51019" : "Sega Rally Championship 2",
	"MK-51146" : "Sega Smash Pack vol 1",
	"" : "Sega Swirl",
	"HDR-0171" : "Segagaga",
	"T8106N" : "Shadow Man",
	"MK-51059" : "Shenmue",
	"MK-51184  50" : "Shenmue 2",
	"T47702M" : "Shikigami no Shiro II",
	"T9507N" : "Silent Scope",
	"MK-51062" : "Skies of Arcadia",
	"MK-51000" : "Sonic Adventure",
	"MK-51117" : "Sonic Adventure 2",
	"MK-51060" : "Sonic Shuffle",
	"T1401N" : "Soul Calibur",
	"HDR-0029" : "Space Channel 5",
	"MK-51051" : "Space Channel 5",
	"MK-51051  50" : "Space Channel 5",
	"T40209N" : "StarLancer",
	"T17723D  50" : "StarLancer",
	"T1213N" : "Street Fighter III: 3rd Strike",
	"T1210N" : "Street Fighter III: Double Impact",
	"T1203N" : "Street Fighter Alpha 3",
	"T40206N" : "Super Magnetic Neo",
	"T1250M" : "Super Puzzle Fighter II X for Matching Service",
	"T40216N" : "Surf Rocket Racers",
	"T36805N" : "Sword of the Berserk: Guts' Rage",
	"T1208N" : "Tech Romancer",
	"MK-51144" : "The Typing of the Dead",
	"MK-51011" : "Time Stalkers",
	"T40211N" : "Tokyo Xtreme Racer 2",
	"MK-51020" : "Toy Commander",
	"T29102M" : "Triggerheart Exelica",
	"T47901M" : "Trizeal",
	"T3103M" : "Twinkle Star Sprites",
	"T46705M" : "Under Defeat",
	"T1235M" : "Vampire Chronicle for Matching Service",
	"T13002N" : "Vigilante 8: 2nd Offense",
	"HDR-0061" : "Virtua Cop 2",
	"MK-51001" : "Virtua Fighter 3tb",
	"MK-51028" : "Virtua Striker 2",
	"MK-51054" : "Virtua Tennis",
	"T13004N" : "Cyber Troopers Virtual On: Oratorio Tangram",
	"T15113N" : "Wacky Racers",
	"T8111N" : "Wetrix+",
	"T20401M" : "Zero Gunner 2",
	"MK-51038" : "Zombie Revenge",
	"T43301M" : "Zusar Vasar",
}


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

	print('-----------------------------------------------------')
	print(game_file)

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
	elif serial_number in official_db:
		title = official_db[serial_number]

	# Check for mislabelled releases
	title, serial_number = fix_mislabelled_db(f, title, serial_number)

	f.close()

	# Return None if the title is not found in the database
	if not title:
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
		