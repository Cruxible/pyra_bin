import ephem
import os
import datetime

while True:
	this = input(' type moon or exit: ')
	if this == 'exit':
		break
	if this == 'moon':
		os.system("clear")
		print("\n")
		moon = ephem.Moon()
		moon.compute()
		phase = moon.moon_phase
		phase_percent = round(phase * 100)
		print(f' The moon is currently\n {phase_percent}% full')

		moon = ephem.Moon()
		moon.compute()
		constellation = ephem.constellation(moon)
		print(f' The moon is currently in\n {constellation[1]}')

		date = datetime.datetime.utcnow()
		moon = ephem.Moon()
		moon.compute(date)
		next_new_moon = ephem.next_new_moon(date)
		moon.compute(next_new_moon)
		print(' The next constellation it will be in is\n', ephem.constellation(moon))


	#The `ephem` library provides a number of features for computing the positions of celestial objects. In addition to the `compute()` method, the library can be used to find where a planet, comet, or asteroid is in the sky, determine where in the sky an object appears for a particular observer, compute when a body will rise, transit overhead, and set from a particular location, parse and use orbital data in either the traditional XEphem file format or the standard TLE format used for tracking Earth-orbiting satellites¹. 

	#You can also use `ephem` to compute the angular separation between two objects in the sky, determine the constellation in which an object lies, and find the times an object rises, transits, and sets².
