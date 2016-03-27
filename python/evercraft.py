import random

ALIGNMENTS = [ "Lawful", "Neutral", "Chaotic" ]

DEFAULT_DAMAGE = 1

DEFAULT_STATS = ["str", "dex", "con", "wis", "int", "cha"]

DEFAULT_STAT_VALUE = 10

class InvalidAlignmentException(Exception):
  pass

def roll(sides):
  return random.randint(1,sides)

class Character:

  def __init__(self):
    self._stats = dict()
    for name in DEFAULT_STATS:
      self._stats[name] = DEFAULT_STAT_VALUE
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
    hp_amount = DEFAULT_DAMAGE
    if result is 20:
      hp_amount *= 2
    if result >= other.armor_class():
      other.damage(hp_amount)

  def damage(self, hp_amount):
    self.hit_points(self.hit_points() - hp_amount)

  def stat(self, name, new_val=None):
    if new_val != None:
      self._stats[name] = new_val
    val = self._stats.get(name, None)
    return val

  def stat_mod(self, name):
    val = self.stat(name)
    return (val - 10) / 2
