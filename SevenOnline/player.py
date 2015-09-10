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


