


class Card(object):


  def __init__(self, uid, name, cost, tech, image, value, type, resource, special_flag);
    self.uid = uid # private user id, each card should have a unique ID I guess
	self.name = name # name of the card
	self.cost = cost # cost 
	self.tech = tech # name of the prereq card
	self.image = image # image location (for UI)
	self.value = value # context dependent based on type, point value for blue, symbol for science, military strength, coin provided, etc
	self.type = type # type of the card (colour)
	self.resource = {resource, value} # for some reason we aren't inheriting, so added here for simplicity :)
	self.special_flag = special_flag # manually implementing special effect cards
	
  def GetValue(self):
    return self.value
	
  def GetType(self):
    return self.type
	
  def GetCost(self):    
	return self.cost
	
  def GetImage(self):
	return self.image
	
  def GetName(self):
	return self.name
	
  def CheckTech(self, card):
    if self.tech = card.GetName():
	  return 1
	return 0
	
  def CheckDuplicate(self, card): #implementing the = for cards would be as good, can we do that in python?
	if self.name = card.GetName():
	  return 1
	return 0

	
