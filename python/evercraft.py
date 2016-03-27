import random

ALIGNMENTS = [ "Lawful", "Neutral", "Chaotic" ]

class InvalidAlignmentException(Exception):
  pass

def roll(sides):
  return random.randint(1,sides)

class Character:

  def __init__(self):
    self.name("Anonymous")
    self.alignment("Neutral")
    self.armor_class(10)
    self.hit_points(5)

  def name(self, new_name=None):
    if new_name != None:
      self._name = new_name
    return self._name

  def alignment(self, new_alignment=None):
    if new_alignment != None:
      if new_alignment not in ALIGNMENTS:
        raise InvalidAlignmentException(new_alignment)
      else:
        self._alignment = new_alignment
    return self._alignment

  def armor_class(self, new_ac=None):
    if new_ac != None:
      self._armor_class = new_ac
    return self._armor_class

  def hit_points(self, new_hp=None):
    if new_hp != None:
      self._hit_points = new_hp
    return self._hit_points

  def attack(self, other):
    result = roll(20)
    if result >= other.armor_class():
      other.damage(1)

  def damage(self, hp_amount):
    self.hit_points(self.hit_points() - hp_amount)
