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


db = {
	"T40201N" : "Aero Wings",
	"T40210N" : "Aero Wings 2: Airstrike",
	"T9501N" : "AirForce Delta",
	"MK-51171" : "Alien Front Online",
	"T15117N" : "Alone in the Dark: The New Nightmare",
	"RDC-0123" : "Ball Breakers",
	"T47110M" : "Baldr Force EXE",
	"T44102N" : "Bang! Gunship Elite",
	"T40217N" : "Bangai-O",
	"T38702M" : "Bangai-O",
	"7011D  50" : "Bangai-O",
	"T20101M" : "Black Matrix AD",
	"T13001N" : "Blue Stinger",
	"MK-51065" : "Bomberman Online",
	"T46703M" : "Border Down",
	"T1215N" : "Cannon Spike",
	"T1218N" : "Capcom vs. SNK",
	"T1217M" : "Capcom vs. SNK: Millennium Fight 2000",
	"T1249M" : "Capcom vs. SNK 2: Millionaire Fighting 2001",
	"T5701N" : "Carrier",
	"T47801M" : "Chaos Field",
	"T15127N" : "Charge N Blast",
	"MK-51160" : "Confidential Mission",
	"MK-51035" : "Crazy Taxi",
	"MK-51136" : "Crazy Taxi 2",
	"MK-51036" : "D2",
	"MK-51037" : "Daytona USA",
	"T3601N" : "Dead or Alive 2",
	"T2401N" : "Death Crimson OX",
	"T177059" : "Deep Fighter",
	"T15112N" : "Demolition Racer",
	"T1217N" : "Dino Crisis",
	"T40203N" : "Draconus - Cult of The Wyrm",
	"T17720N" : "Dragonriders Chronicles of Pern",
	"MK-51013" : "Dynamite Cop",
	"T41601N" : "Elemental Gimmick Gear",
	"T14302M" : "Elemental Gimmick Gear",
	"T46605D  71" : "Evil Twin: Cyprien's Chronicles",
	"T17706N" : "Evolution - The World of Sacred Device",
	"T17711N" : "Evolution 2 - Far Off Promise",
	"T15104N" : "Expendable",
	"" : "Fast Striker",
	"T44306N" : "Fatal Fury - Mark of The Wolves",
	"T35801N" : "Fighting Force 2",
	"HDR-0133" : "Fighting Vipers 2",
	"MK-51154  50" : "Fighting Vipers 2",
	"T34201M" : "Frame Gride",
	"T3108M" : "Garou - Mark of the Wolves",
	"T1222N" : "GigaWing 2",
	"T42102N" : "Grand Theft Auto 2",
	"T17716N" : "Grandia 2",
	"T2402M" : "Guilty Gear X",
	"T1214N" : "Gun Bird 2",
	"T13301N" : "Gundam Side Story 0079 - Rise From The Ashes",
	"" : "Half-Life",
	"" : "Half-Life - Blue Shift",
	"MK-51041  50" : "Head Hunter",
	"MK-51002" : "House of the Dead 2",
	"T9702N" : "Hydro Thunder",
	"T38706M" : "Ikaruga",
	"T46001N" : "Illbleed",
	"T12503N" : "Incoming",
	"MK51058" : "Jet Grind Radio",
	"T1206N" : "JoJos Bizarre Adventure",
	"T47803M" : "Karous",
	"T44302N" : "King of Fighters '99 Evolution, The",
	"T47303M" : "King of Fighters 2000, The",
	"T47304M" : "King of Fighters 2001, The",
	"T47305M" : "King of Fighters 2002, The",
	"T2106M" : "L.O.L. Lack Of Love",
	"T44305N" : "The Last Blade 2: Heart of the Samurai",
	"" : "Last Hope",
	"" : "Last Hope - Pink Bullets",
	"T36802N" : "Legacy of Kain - Soul Reaver",
	"T21501M" : "Macross M3",
	"51050" : "Maken X",
	"T2201M" : "Marionette Handler",
	"T1221N" : "Mars Matrix",
	"T1202N" : "Marvel vs. Capcom: Clash of Super Heroes",
	"T1212N" : "Marvel vs. Capcom 2",
	"T12502N" : "MDK2",
	"T51012" : "Metropolis Street Racer",
	"" : "Millennium Soldier",
	"T40508D" : "Moho",
	"T9701N" : "Mortal Kombat Gold",
	"T1402N" : "Mr Driller",
	"T9904M" : "Neo Golden Logres",
	"NGDT-304DCRE" : "NEO XYX",
	"T9504N" : "Nightmare Creatures 2",
	"T36807N" : "Omikron - The Nomad Soul",
	"MK-51102" : "Outtrigger",
	"MK-51100" : "Phantasy Star Online",
	"T1207N" : "Plasma Sword: Nightmare of Bilstein",
	"T1201N" : "Power Stone",
	"T1211N" : "Power Stone 2",
	"T1219N" : "Project Justice",
	"51081" : "Propeller Arena",
	"T31101N" : "Psychic Force 2012",
	"T9907M" : "Psyvariar 2: The Will to Fabricate",
	"MK-51061" : "Quake III Arena",
	"HDR-0001" : "Radilgy",
	"T9901M" : "Rainbow Cotton",
	"T17704N" : "Rayman 2: The Great Escape",
	"T9704N" : "Ready 2 Rumble Boxing",
	"T9717N" : "Ready 2 Rumble Boxing: Round 2",
	"T40218N" : "Record of Lodoss War",
	"T40215N" : "Red Dog: Superior Firepower",
	"RDXRE-JP" : "Redux: Dark Matters",
	"T1204N" : "Resident Evil: Code Veronica",
	"T1205N" : "Resident Evil 2",
	"T1220N" : "Resident Evil 3: Nemesis",
	"MK-51192  50" : "Rez",
	"MK_51092" : "Samba De Amigo",
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
	"" : "Soul Calibur",
	"" : "Street Fighter 3 - 3rd Strike",
	"" : "Street Fighter 3 - Double Impact",
	"" : "Street Fighter Alpha 3",
	"" : "Sturmwind",
	"" : "Super Magnetic Neo",
	"" : "Super Puzzle Fighter 2",
	"" : "Surf Rocket Racers",
	"" : "Sword of The Berserk - Guts Rage",
	"" : "Tech Romancer",
	"" : "The Typing of the Dead",
	"" : "Time Stalkers",
	"" : "ToeJam and Earl 3",
	"" : "Tokyo Xtreme Racer 2",
	"" : "Toy Commander",
	"" : "Triggerheart Exelica",
	"" : "Trizeal",
	"" : "Twinkle Star Sprites",
	"" : "Under Defeat",
	"" : "Vampire Chronicle For Matching Service",
	"" : "Vigilante 8 2nd Offence",
	"" : "Virtua Cop 2",
	"" : "Virtua Fighter 3tb",
	"" : "Virtua Striker 2",
	"" : "Virtua Tennis",
	"" : "Virtual On - Oratorio Tangram",
	"" : "Wacky Racers",
	"" : "Wetrix+",
	"" : "Zero Gunner 2",
	"" : "Zombie Revenge",
	"" : "Zusar Vasar",
}

def is_cdi_file(game_file):
	# Skip if not file
	if not os.path.isfile(game_file):
		return False

	# Skip if not a CDI file
	if not os.path.splitext(game_file)[1].lower() == '.cdi':
		return False

	return True

def get_dreamcast_game_info(game_file):
	BUFFER_SIZE = 1024 * 1024 * 10
	
	print(game_file)

	# Get the full file name
	full_entry = os.path.abspath(game_file)

	# Read the ROM file
	f = open(full_entry, 'rb', buffering=BUFFER_SIZE)
	file_size = os.path.getsize(full_entry)

	# Quickly check the serial numbers at common memory locations :)
	for common in [1408872, 1413576]:
		f.seek(common)
		rom_data = f.read(10)
		for serial_number, name in db.iteritems():
			if serial_number and serial_number in rom_data:
				index = rom_data.index(serial_number)
				print(('FAST', serial_number, name, f.tell() - 10))
				f.close()
				return (serial_number, name)
				
	# Slowly check the serial number throughout the entire binary :(
	f.seek(0)
	while True:
		# Read into the buffer
		rom_data = f.read(BUFFER_SIZE)

		# Check for the end of the file
		if not rom_data:
			break

		# Move back the length of the serial number
		# This is done to stop the serial number from being spread over multiple buffers
		file_pos = f.tell()
		if file_pos > 10 and file_pos < file_size:
			f.seek(file_pos - 10)

		# Get the serial number location
		for serial_number, name in db.iteritems():
			if serial_number and serial_number in rom_data:
				index = rom_data.index(serial_number)
				#print(rom_data[index-10 : index+10])
				print(('SLOW', serial_number, name, f.tell() - BUFFER_SIZE + index + 10))
				f.close()
				return (serial_number, name)

	f.close()
	return None


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

		