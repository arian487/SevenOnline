"""Data for a Player."""

import time
import constants


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

  def MakeWonder(num, side)
    self.wonder = Wonder(num, side)
    # Add a single resource of value 1 for a wonder
    self.AddPermanentResources(self.wonder.resource, 1)

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
  def __init__(self, wonder_num, side);
    self.wonder_num = wonder_num
    self.name = constants.WONDER_NAME[wonder_num] # name of wonder
    self.side = side # side of wonder
    self.resource = wonder_num #wonder's intrinsic resource
    self.wonder_cost = []
    self.wonder_cost = GetWonderCost(self.num, self.side) #array containing the wonders cost for each level
    self.wonder_level = 0 #wonder's current built level
			
				
 def GetWonderCost(num, side):
    """need some way to import the costs, or else hard code, should have an array for each of the levels"""
    return 
			
  def IncrementWonder(self):
    self.wonder_level += 1


	
