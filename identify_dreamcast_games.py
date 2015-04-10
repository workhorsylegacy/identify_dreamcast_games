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

IS_PY2 = sys.version_info[0] == 2


def _strip_comments(data):
	lines = data.split(b"\r\n")
	data = []
	for line in lines:
		if b'/*' not in line and b'*/' not in line:
			data.append(line)

	return b"\r\n".join(data)

root = os.path.dirname(os.path.realpath(__file__))

# Fix bug in py2exe that makes the exe name the dirname
if root.endswith('.exe'):
	root = os.path.dirname(root)


with open(os.path.join(root, 'db_dreamcast_unofficial.json'), 'rb') as f:
	unofficial_db = json.loads(_strip_comments(f.read()).decode('utf8'))

with open(os.path.join(root, 'db_dreamcast_official_us.json'), 'rb') as f:
	official_us_db = json.loads(_strip_comments(f.read()).decode('utf8'))

with open(os.path.join(root, 'db_dreamcast_official_jp.json'), 'rb') as f:
	official_jp_db = json.loads(_strip_comments(f.read()).decode('utf8'))

with open(os.path.join(root, 'db_dreamcast_official_eu.json'), 'rb') as f:
	official_eu_db = json.loads(_strip_comments(f.read()).decode('utf8'))


# Convert the keys from strings to bytes
dbs = [
	unofficial_db,
	official_us_db,
	official_jp_db,
	official_eu_db,
]
for db in dbs:
	keys = db.keys()
	for key in keys:
		# Get the value
		val = db[key]

		# Remove the unicode key
		db.pop(key)

		# Add the bytes key and value
		if IS_PY2:
			db[bytes(key)] = val
		else:
			db[bytes(key, 'utf-8')] = val


def _read_blob_at(file, start_address, size):
	file.seek(start_address)
	blob = file.read(size)
	return blob

def _fix_games_with_same_serial_number(f, title, serial_number):
	if serial_number == 'T-8111D-50':
		if title == "ECW HARDCORE REVOLUTION": # EU ECW Hardcore Revolution
			return ("ECW Hardcore Revolution", "T-8111D-50")
		elif title == "DEAD OR ALIVE 2": # EU Dead or Alive 2
			return ("Dead or Alive 2", "T-8111D-50")
	elif serial_number == 'T-8101N':
		if title == "QUARTERBACK CLUB 2000": #US NFL Quarterback Club 2000
			return ("NFL Quarterback Club 2000", "T-8101N")
		elif title == "JEREMY MCGRATH SUPERCROSS 2000": #US Jeremy McGrath Supercross 2000
			return ("Jeremy McGrath Supercross 2000", "T-8101N")
	'''
	elif serial_number == 'T9706D  61':
		EU 18 Wheeler: American Pro Trucker
		EU 4-Wheel Thunder

	elif serial_number == 'T1214M':
		JP BioHazard Code: Veronica Trial Edition
		JP BioHazard 2

	elif serial_number == 'MK-51062':
		US Skies of Arcadia
		US NFL 2K1

	elif serial_number == 'MK-51168':
		US NFL 2K2
		US Confidential Mission
	elif serial_number == 'T30001M':
		JP D2 Shock
		JP Kaze no Regret Limited Edition
	elif serial_number == 'MK51038  50':
		EU Sega WorldWide Soccer 2000 Euro Edition
		EU Zombie Revenge
	'''
	return (title, serial_number)

def _fix_games_that_are_mislabeled(f, title, serial_number):
	if serial_number == b"T1402N": # Mr. Driller
		if _read_blob_at(f, 0x159208, 12) == b"DYNAMITE COP":
			return (u"Dynamite Cop!", "MK-51013")
	elif serial_number == b"MK-51035": # Crazy Taxi
		if _read_blob_at(f, 0x1617E652, 9) == b"Half-Life":
			return (u"Half-Life", "T0000M")
		elif _read_blob_at(f, 0x1EA78B5, 10) == b"Shadow Man":
			return (u"Shadow Man", "T8106N")
	elif serial_number == b"T43903M": # Culdcept II
		if _read_blob_at(f, 0x264E1E5D, 10) == b"CHAOSFIELD":
			return (u"Chaos Field", "T47801M")
	elif serial_number == b"T0000M": # Unnamed
		if _read_blob_at(f, 0x557CAB0, 13) == b"BALL BREAKERS":
			return (u"Ball Breakers", "T0000M")
		elif _read_blob_at(f, 0x4BD5EE5, 6) == b"TOEJAM":
			return (u"ToeJam and Earl 3", "T0000M")
	elif serial_number == b"T0000": # Unnamed
		if _read_blob_at(f, 0x162E20, 15) == b"Art of Fighting":
			return (u"Art of Fighting", "T0000")
		elif _read_blob_at(f, 0x29E898B0, 17) == b"Art of Fighting 2":
			return (u"Art of Fighting 2", "T0000")
		elif _read_blob_at(f, 0x26D5BCA4, 17) == b"Art of Fighting 3":
			return (u"Art of Fighting 3", "T0000")
		elif _read_blob_at(f, 0x295301F0, 5) == b"Redux":
			return (u"Redux: Dark Matters", "T0000")
	elif serial_number == b"MK-51025": # NHL 2K1
		if _read_blob_at(f, 0x410CA8, 14) == b"READY 2 RUMBLE":
			return (u"Ready 2 Rumble Boxing", "T9704N")
	elif serial_number == b"T36804N": # Walt Disney World Quest: Magical Racing Tour
		if _read_blob_at(f, 0x245884, 6) == b"MakenX":
			return (u"Maken X", "MK-51050")
	elif serial_number == b"RDC-0117": # The king of Fighters '96 Collection (NEO4ALL RC4)
		if _read_blob_at(f, 0x159208, 16) == b"BOMBERMAN ONLINE":
			return (u"Bomberman Online", "RDC-0120")
	elif serial_number == b"RDC-0140": # Dead or Alive 2
		if _read_blob_at(f, 0x15639268, 13) == b"CHUCHU ROCKET":
			return (u"ChuChu Rocket!", "RDC-0139")
	elif serial_number == b"T19724M": # Pizzicato Polka: Suisei Genya
		if _read_blob_at(f, 0x3CA16B8, 7) == b"DAYTONA":
			return (u"Daytona USA", "MK-51037")
	elif serial_number == b"MK-51049": # ChuChu Rocket!
		if _read_blob_at(f, 0xC913DDC, 13) == b"HYDRO THUNDER":
			return (u"Hydro Thunder", "T9702N")
		elif _read_blob_at(f, 0x2D096802, 17) == b"MARVEL VS. CAPCOM":
			return (u"Marvel vs. Capcom 2", "T1212N")
		elif _read_blob_at(f, 0x1480A730, 13) == b"POWER STONE 2":
			return (u"Power Stone 2", "T-1211N")
	elif serial_number == b"T44304N": # Sports Jam
		if _read_blob_at(f, 0x157FA8, 9) == b"OUTRIGGER":
			return (u"OutTrigger: International Counter Terrorism Special Force", "MK-51102")
	elif serial_number == b"MK-51028": # Virtua Striker 2
		if _read_blob_at(f, 0x1623B0, 12) == b"zerogunner 2":
			return (u"Zero Gunner 2", "MK-51028")
			return (u"OutTrigger: International Counter Terrorism Special Force", "MK-51102")
	elif serial_number == b"T1240M": # BioHazard Code: Veronica Complete
		if _read_blob_at(f, 0x157FAD, 14) == b"BASS FISHING 2":
			return (u"Sega Bass Fishing 2", "MK-51166")
	elif serial_number == b"MK-51100": # Phantasy Star Online
		if _read_blob_at(f, 0x52F28A8, 26) == b"Phantasy Star Online Ver.2":
			return (u"Phantasy Star Online Ver. 2", "MK-51166")

	return (title, serial_number)


def _locate_string_in_file(f, file_size, string_to_find):
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
			return string_file_location

		# Move back the length of the string to find
		# This is done to stop the string to find from being spread over multiple buffers
		if use_offset:
			f.seek(file_pos - string_length)

	return -1

def _get_track_01_from_gdi_file(file_name):
	path = os.path.dirname(file_name)
	if IS_PY2:
		path = bytes(path)
	else:
		path = bytes(path, 'utf-8')

	with open(file_name, 'rb') as f:
		track_01_line = f.read().split(b"\r\n")[1]
		track_01_file = track_01_line.split(b' ')[4]
		track_01_file = os.path.join(path, track_01_file)
		return track_01_file

def is_dreamcast_file(game_file):
	# Skip if not file
	if not os.path.isfile(game_file):
		return False

	# FIXME: Make it work with .mdf/.mds, .nrg, and .ccd/.img
	# Skip if not a usable file
	if not os.path.splitext(game_file)[1].lower() in ['.cdi', '.gdi', '.iso']:
		return False

	return True

def get_dreamcast_game_info(game_file):
	# Get the full file name
	full_entry = os.path.abspath(game_file)

	# If it's a GDI file read track 01
	if os.path.splitext(full_entry)[1].lower() == '.gdi':
		full_entry = _get_track_01_from_gdi_file(full_entry)

	# Open the game file
	f = open(full_entry, 'rb', buffering=BUFFER_SIZE)
	file_size = os.path.getsize(full_entry)

	# Get the location of the header
	header_text = b"SEGA SEGAKATANA SEGA ENTERPRISES"
	index = _locate_string_in_file(f, file_size, header_text)
	
	# Throw if index not found
	if index == -1:
		raise Exception("Failed to find Sega Dreamcast Header.")

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

	# Check for different types of releases

	# Unofficial
	if serial_number in unofficial_db:
		title = unofficial_db[serial_number]
	# US
	elif serial_number in official_us_db:
		title = official_us_db[serial_number]
	# Europe
	elif serial_number in official_eu_db:
		title = official_eu_db[serial_number]
	# Japan
	elif serial_number in official_jp_db:
		title = official_jp_db[serial_number]

	# Check for games with the same serial number
	title, serial_number = _fix_games_with_same_serial_number(f, title, serial_number)

	# Check for mislabeled releases
	title, serial_number = _fix_games_that_are_mislabeled(f, title, serial_number)

	f.close()

	# Throw if the title is not found in the database
	if not title:
		raise Exception("Failed to find game in database.")

	return {
		'title' : title,
		'disc_info' : disc_info,
		'region' : region,
		'serial_number' : serial_number,
		'version' : version,
		'boot' : boot,
		'maker' : maker,
		'title' : title,
		'sloppy_title' : sloppy_title,
		'header_index' : index,
	}

def main():
	# Just return if there are no args
	if len(sys.argv) < 2:
		return

	# Just return if not a Dreamcast file
	game_file = sys.argv[1]
	if not is_dreamcast_file(game_file):
		return

	# Return 1 if fails to find game info
	info = None
	try:
		info = get_dreamcast_game_info(game_file)
	except:
		sys.exit(1)

	# Convert any binary strings to normal strings to be JSON friendly
	for key in info.keys():
		value = info[key]
		if type(value) is bytes:
			value = value.decode('utf-8')
		info[key] = value

	# If the game is found, return the info as JSON
	print(json.dumps(info))


if __name__ == "__main__":
	main()

