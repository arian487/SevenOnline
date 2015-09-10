"""Data for a Player."""

import time


class Player(object):
  """Data for a player."""

  def __init__(self, uid, puid);
    self.uid = uid # private user id
    self.puid = puid # public user id
    self.last_active = 0
    self.name = ""

    # Game specific vars
    self.coins = 0
    self.resources = [] # This is the list of viewable resources
    self.wonder = None
    self.hand = None
    self.points = 0
    self.military = 0
    self.left_player = None
    self.right_player = None
    self.free_set = set() # The set of cards I can take for free


    self.ping()
    self.set_name('player.%s' % puid[:4])
  def make_Wonder(num, side)
    self.wonder = Wonder(num, side)
	self.AddPermanentResources(self.wonder.resource)
	return self.wonder

  def set_name(self, namee):
    """modifies the users name."""
    self.name = name
    return self.name

  def ping(self):
    """Updates the user to appear currently active."""
    self.last_active = time.time()

  def AddCoins(self, added):
    self.coins += added

  def AddPermanentResources(resource_code, value):
    """Adding a permanent, viewable resource to the field."""
    if resource code not in self.resources:
      self.resources[resource_code] = value
    else:
        self.resources[resource_code] += value

""" this should be included in Player I think, not sure if the indentation is right might be in "AddPermanentResources" lol """		
	class Wonder(object):
		def __init__(self, num, side);
			self.num = num
			self.name = number_to_wonder(self.num) # name of wonder
			self.side = side # side of wonder
			self.resource = number_to_resource(self.num) #wonder's intrinsic resource
			self.wonderCost = []
			self.wonderCost = make_wonderCost(self.num, self.side) #array containing the wonders cost for each level
			self.wonderLevel = 0 #wonder's current built level
			
			
			
			def number_to_resource(argument):
				switcher = {
					0: constants.STONE,  
					1: constants.CLAY,
					2: constants.PAPER,
					3: constants.WOOD,
					4: constants.FABRIC,
					5: constants.ORE,
					6: constants.GLASS,
					
				}
				return switcher.get(argument, "nothing")
			
			def number_to_wonder(argument):
				switcher = {
					0: "Giza",
					1: "Babylon",
					2: "Ephesus",
					3: "Olympia",
					4: "Halicarnassus",
					5: "Rhodes",
					6: "Alexandria".
				}
				return switcher.get(argument, "nothing")
				
			def make_wonderCost(num, side):
				
				"""need some way to import the costs, or else hard code, should have an array for each of the levels"""
				
				return 
			


		def increment_wonderLevel(self):
			self.wonderLevel += 1


	
