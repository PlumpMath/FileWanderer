#IMPORTS
from wndr import *

wanderer = None

#FUNCTIONS
def save():
	global world_objects
	clear_save_file()
	for obj in world_objects:
		obj.save()
	print("save successful!")

def start():
	global world_objects, wanderer
	#load all objects from save file
	if os.path.isfile(default_save_path()):
		world_objects = load_objects()
		#if there exists a wanderer object, make it THE wanderer
		all_wanderers = [obj for obj in world_objects if type(obj) == Wanderer]
		if len(all_wanderers) > 0:
			wanderer = all_wanderers[0]
			print("found an existing wanderer")
	#make a new wanderer to start the game, if there are no wanderers yet
	if wanderer == None:
		wanderer = Wanderer()
		world_objects.append(wanderer)
		print("new wanderer")

def main():
	global world_objects, wanderer, time_until_next_action
	try:
		save_timer = Timer(5) #save once every 30 seconds

		while True:
			#time_until_next_action = float("inf")

			for obj in world_objects:
				obj.update()

			if save_timer.done():
				save()
				save_timer.restart()

			sleep_until_next_action()

	except KeyboardInterrupt:
		end()

def end():
	save()
	print("exitting game")

#START GAME LOOP
start()
main()