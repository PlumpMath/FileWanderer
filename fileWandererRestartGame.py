#IMPORTS
from wndr import *

for obj in load_objects():
	try:
		obj.destroy()
		print("deleted " + obj.name)
	except:
		pass

os.remove(default_save_path())
print("deleted save file")