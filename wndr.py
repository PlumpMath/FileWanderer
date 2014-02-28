#IMPORTS
import os, sys, time, random

#GLOBAL VARIABLES
current_directory = os.getcwd()
home_directory = current_directory
save_file_name = "wanderer.save"
world_objects = []
time_until_next_action = float("inf")

#ART
walking_animation = [
'''
       ,
  -0  /()
 _/|\/
   |/
  / \\
  |  -[
  -
''',
'''
       ,
  -0  /()
  ,|\/
   |/
   |
   |\\
   - '
''',
'''
      ,
  -0 /()
   |/
  `|
   |
   |
   -
''',
'''
     ,
  -0/()
   |\\
  `| '
   ^
  / \\
 `   '
''',
'''
    ,
  -0()
  /|\\
 `-| \\
  / |
 /   \\
`     `
''',
'''
     ,
  -0/()
   |\\
  `| '
   ^
  / \\
 `   '
''',
'''
      ,
  -0 /()
   |/
  `|
   |
   |
   -
''',
'''
       ,
  -0  /()
  ,|\/
   |/
   |
   |\\
   - '
'''
]

sleeping_animation = [
'''


  z
.      
0------"
''',
'''

    z
  
.      
0------"
''',
'''
       z
    
  
.      
0------"
'''
]

#FUNCTIONS
def get_root(directory):
	filePath = directory.split('/')
	root = ""
	for i in range(len(filePath)-1):
		root += filePath[i] + "/"
	root = root[:len(root)-1]
	if os.access(root, os.W_OK):
		return root
	else:
		return None #no access

def get_top_root(directory):
	prevDir = None
	nextDir = get_root(directory)
	while (nextDir != None):
		prevDir = nextDir
		nextDir = get_root(prevDir)
	return prevDir

def get_child_directories(directory):
	children = []
	for f in os.listdir(directory):
		if not os.path.isfile(f):
			child = directory + "/" + f
			if os.path.isdir(child) and f[0] != '.' and os.access(child, os.W_OK) and not(".app" in child):
				children.append(child)
	return children

def remove_from_list(base_list, remove_list):
	return [x for x in base_list if x not in remove_list]

def default_save_path():
	return os.path.join(home_directory, save_file_name)

def save_object(filepath, obj, parameters):
	f = open(filepath, 'a')
	f.write(make_object_string(obj, parameters) + os.linesep)
	f.close()

def make_object_string(obj, parameters):
	objectString = obj.__class__.__name__ + "("
	for p in parameters:
		objectString += p + ", "
	objectString = objectString[:-2]
	objectString += ")"
	return objectString

def load_objects(filepath = default_save_path()):
	objects = []
	f = open(filepath, 'r')
	for objectString in f.readlines():
		o = eval(objectString)
		objects.append(o)
	return objects

def clear_save_file(filepath = default_save_path()):
	f = open(filepath, 'w')
	f.close()

def quote(string):
	return "'" + string + "'"

def next_action(time):
	global time_until_next_action
	if time < time_until_next_action:
		time_until_next_action = time

def sleep_until_next_action():
	global time_until_next_action
	if (time_until_next_action != float("inf")):
		print("sleep " + str(time_until_next_action))
		time.sleep(time_until_next_action)
		time_until_next_action = float("inf") #reset	

def test_animation():
	a = AsciiAnimation(walking_animation)
	while True:
		for f in a.get_frame():
			print(f)
		time.sleep(0.1)	

def find_file_in_harddrive(filename):
	topDirectory = get_top_root(current_directory) + "/"
	print(topDirectory)
	try:
		for root, directories, files in os.walk(topDirectory):
			print(directories)
			for f in files:
				#print(f)
				if f == filename:
					print("found it!")
					return root
		return None
	except:
		print("help!")
		return None

def weighted_choice(choices):
	choiceList = []
	for choice, weight in choices:
		choiceList += [choice] * weight
	return random.choice(choiceList)

def get_random_directory(top_directory, max_depth):
	cur_dir = top_directory
	i = 0
	while i < max_depth:
		sub_directories = get_child_directories(cur_dir)
		if len(sub_directories) > 0:
			cur_dir = random.choice(sub_directories)
		i += 1
	return cur_dir

#CLASSES
class Timer(object):
	def __init__(self, length):
		self.startTime = time.time()
		self.length = length

	def progress(self):
		return (time.time() - self.startTime) / self.length

	def done(self):
		return self.progress() >= 1

	def restart(self):
		self.startTime = time.time()

class AsciiAnimation(object):
	def __init__(self, frames):
		self.frames = frames
		self.index = 0

	def get_frame(self):
		frame_array = self.frames[self.index].split(os.linesep)
		self.index = (self.index + 1) % len(self.frames)
		return frame_array

class MultiLineContent(object):
	def __init__(self, string_array):
		self.content = string_array

	def write_content(self, start_index, string_array):
		for i in range(len(string_array)):
			if start_index + i < len(self.content):
				self.content[start_index + i] = string_array[i]
			else:
				self.content.append(string_array[i])

	def remove_content(self, start_index, end_index):
		self.content = self.content[:start_index] + self.content[end_index:]

	def insert_content(self, index, string_array):
		self.content = self.content[:index] + string_array + self.content[index:]

	def __str__(self):
		all_content = ""
		for line in self.content:
			all_content += line + os.linesep
		return all_content


#base class for objects that are part of the world of the game
class WorldObject(object):
	def __init__(self, name, content = "", directory = os.getcwd()):
		self.name = name
		self.content = content
		self.directory = directory
		self.hidden = False
		self.create()

	def __str__(self):
		return str(self.content)

	def path(self):
		return os.path.join(self.directory, self.name + ".txt")

	def create(self):
		f = open(self.path(), 'w')
		f.write(str(self))
		f.close()
		self.hidden = False

	def destroy(self):
		os.remove(self.path())
		self.hidden = True

	def move(self, directory = os.getcwd()):
		oldDirectory = self.directory
		try:
			self.destroy()
			self.directory = directory
			self.create()
			return True
		except:
			print("can't move to " + directory)
			self.directory = oldDirectory
			self.create()
			return False

	def update(self):
		pass

	def save(self, filepath = default_save_path()):
		save_object(filepath, self, [quote(self.name), quote(self.content), quote(self.directory)])

class Wanderer(WorldObject):
	MODE_EXPLORING = 0
	MODE_SLEEPING = 1
	MODE_QUESTING = 2

	DIRECTION_DOWN = 0
	DIRECTION_UP = 1

	#persistence = how long the wanderer goes in one direction
	min_persistence = 3
	max_persistence = 6

	def __init__(self, directory = os.getcwd()):
		super(Wanderer, self).__init__("wanderer", "exploring", directory)
		self.mode = Wanderer.MODE_EXPLORING

		#exploration
		self.exploring_timer = Timer(10) #move every 10 seconds
		self.direction = random.choice(range(2))
		self.persistence = self.random_persistence()
		self.visited_locations = []
		self.total_visits = 0
		self.status = ["exploring", "sleeping", "questing for "]
		self.quest_goal = None

		#sleeping
		self.tiredness = 0
		self.max_tiredness = 3
		self.sleeping_timer = Timer(30) #sleep for a minute

		#animation
		self.anim_timer = Timer(1)
		self.animations = [AsciiAnimation(walking_animation), AsciiAnimation(sleeping_animation), AsciiAnimation(walking_animation)]
		self.create()

		self.content = MultiLineContent([self.status[self.mode]] + self.animations[self.mode].get_frame())

	def update(self):
		global world_objects

		if os.path.isfile(self.path()):
			print("status " + self.status[self.mode])
			self.content.write_content(0, [self.status[self.mode]])

			#logic
			if self.mode == Wanderer.MODE_EXPLORING:
				if self.exploring_timer.done():
					self.explore()
					self.exploring_timer.restart()
					#next_action(self.exploring_timer.length)
			elif self.mode == Wanderer.MODE_SLEEPING:
				if self.sleeping_timer.done():
					world_objects.append(WorldObject("ashes", "the cold remains of a campfire", self.directory))
					self.mode = weighted_choice([(Wanderer.MODE_EXPLORING,3),(Wanderer.MODE_QUESTING,1)])
					self.exploring_timer.restart()
					self.content.remove_content(1, len(self.content.content))
					self.tiredness = 0
					if self.mode == Wanderer.MODE_QUESTING:
						print("QUESTING")
						self.quest_goal = get_random_directory(get_top_root(current_directory), random.randrange(1,4))
			elif self.mode == Wanderer.MODE_QUESTING:
				self.content.write_content(0, [self.status[self.mode] + self.quest_goal])
				print(self.directory + " --> " + self.quest_goal)
				if self.directory == self.quest_goal:
					#found goal!
					print("FOUND GOAL!")
					world_objects.append(WorldObject("flag", "a pennant flaps fitfully in the breeze", self.directory))
					#switch modes
					self.mode = Wanderer.MODE_EXPLORING
					self.tiredness = 0
				elif self.exploring_timer.done():
					self.explore()
					self.exploring_timer.restart()

			#animation
			if self.anim_timer.done():
				self.content.write_content(1, self.animations[self.mode].get_frame())
				self.anim_timer.restart()
				self.create()
				next_action(self.anim_timer.length)
		else:
			print("can't find wanderer")
			newDir = find_file_in_harddrive("wanderer.txt")
			if newDir != None:
				raw_input("waiting")
				self.directory = newDir
				self.create()

	def random_persistence(self):
		return random.choice(range(Wanderer.min_persistence, Wanderer.max_persistence))

	def explore(self):
		global world_objects
		print("exploring")
		#print("persistence " + str(self.persistence))

		#find a destiation
		destination = None
		if self.direction == Wanderer.DIRECTION_DOWN: #go deeper
			print("down")
			possible_destinations = get_child_directories(self.directory)
			possible_destinations = remove_from_list(possible_destinations, self.visited_locations)
			if len(possible_destinations) > 0:
				destination = random.choice(possible_destinations)
		elif self.direction == Wanderer.DIRECTION_UP: #climb higher
			print("up")
			destination = get_root(self.directory)

		if destination != None: #travel to the destination, if you find one
			print("new destination")
			prev_location = self.directory
			if self.move(destination):
				print("moved to " + destination)
				footprints = WorldObject("footprints" + str(self.total_visits), "a trail of muddy footprints lead toward " + destination, prev_location)
				world_objects.append(footprints)
				self.visited_locations.append(destination)
				self.persistence -= 1
				self.total_visits += 1
		else: #switch directions if you don't
			print("wanderer has nowhere to go")
			self.direction = not self.direction
			self.persistence = self.random_persistence()

		#change directions once persistence fades
		if self.persistence <= 0:
			print("new direction")
			self.direction = random.choice(range(2))
			self.persistence = self.random_persistence()

		self.tiredness += 1
		if self.tiredness >= self.max_tiredness:
			self.mode = Wanderer.MODE_SLEEPING
			self.content.remove_content(1, len(self.content.content))
			self.sleeping_timer.restart()
			print("SLEEPING")

	def save(self, filepath = default_save_path()):
			save_object(filepath, self, [quote(self.directory)])

