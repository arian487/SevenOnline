"""Data for a Player."""

import time
import constants
import card


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
    self.owned_cards = None
    self.hand = None
    self.military_strength = 0
    # Represents the science cards I have.
    self.science_value = {
      0: 0
      1: 0
      2: 0
      3: 0
    }
    self.points = 0
    self.left_player = None
    self.right_player = None
    self.free_set = [] # The set of cards I can take for free


    self.ping()
    self.SetName('player.%s' % puid[:4])

  def MakeWonder(num, side)
    self.wonder = Wonder(num, side)
    # Add a single resource of value 1 for a wonder.
    self.AddPermanentResources(self.wonder.resource, 1)

  def SetName(self, namee):
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

  def AddCard(card):
    """Add a card."""
    self.owned_cards.append(card)
    self.free_set.append(card.tech_to)

    if card.type == card.MILITARY_TYPE:
      self.military_strength += card.GetValue()
    elif card.type == card.BLUE:
      self.points += card.GetValue()
    elif card.type == card.SCIENCE:
      self.science_value[card.GetValue()] += 1

  def CalculateScience(self):
    # TODO: deal with the / science cards.
    points = 0
    # used for calculating sets
    min_type_count = 10000
    # First go through each science type.
    for type in xrange(0,2):
      min_type_count = min(self.science_value[type], min_type_count)
      points += self.science_value[type]**2
    # Now we need to see how many sets we have
    points += 7 * min_type_count

  def TotalPoints(self):
    # TODO: add calculation of other point types like wonders and shit.
    return self.points + self.CalculateScience()

  def CanAfford(card, type):
    """Returns a list of possibilities for card payment, or -1 if not possible."""
    cost = card.cost
    if type == 'wonder':
      cost = self.wonder.GetWonderCost()
    else:
      # Get it for free.
      if card.name in self.free_set:
        cost = None
    if cost is None:
      return constants.CAN_AFFORD_FREE



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


	
