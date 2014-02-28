#IMPORTS
from wndr import *

for obj in load_objects():
	try:
		obj.destroy()
		print("deleted " + obj.name)
	except:
		pass