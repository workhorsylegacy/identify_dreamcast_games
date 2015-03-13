identify_dreamcast_games
==========

A module for identifying Sega Dreamcast games with Python 2 &amp; 3


Example use:
-----
~~~python

from identify_dreamcast_games import get_dreamcast_game_info

info = get_dreamcast_game_info("E:\Sega\Dreamcast\Power Stone 2\power_stone_2.cdi")
		
print('title', info['title'])
print('disc_info', info['disc_info'])
print('region', info['region'])
print('serial_number', info['serial_number'])
print('version', info['version'])
print('boot', info['boot'])
print('maker', info['maker'])
print('title', info['title'])
print('sloppy_title', info['sloppy_title'])
print('header_index', info['header_index'])

~~~


