import random

ALIGNMENTS = [ "Lawful", "Neutral", "Chaotic" ]


DEFAULT_STATS = ["str", "dex", "con", "wis", "int", "cha"]

DEFAULT_STAT_SCORE = 10
DEFAULT_DAMAGE = 1
DEFAULT_ARMOR_CLASS = 10
DEFAULT_HIT_POINTS = 10

XP_PER_HIT = 10

class InvalidAlignmentException(Exception):
  pass

class InvalidStatException(Exception):
  pass

def roll(sides):
  return random.randint(1,sides)

class Character:

  def __init__(self):
    self._stats = dict()
    self._xp = 0
    for name in DEFAULT_STATS:
      self._stats[name] = DEFAULT_STAT_SCORE
    self.name("Anonymous")
    self.alignment("Neutral")
    self.hit_points(self.ideal_hit_points())

  def name(self, new_name=None):
    if new_name != None:
      self._name = new_name
    return self._name

  def ideal_hit_points(self):
    return DEFAULT_HIT_POINTS + self.stat_mod("con")

  def alignment(self, new_alignment=None):
    if new_alignment != None:
      if new_alignment not in ALIGNMENTS:
        raise InvalidAlignmentException(new_alignment)
      else:
        self._alignment = new_alignment
    return self._alignment

  def armor_class(self):
    return DEFAULT_ARMOR_CLASS + self.stat_mod("dex")

  def hit_points(self, new_hp=None):
    if new_hp != None:
      self._hit_points = new_hp
    return self._hit_points

  def roll_stat(self, name):
    return roll(20) + self.stat_mod(name) + (self.level() - 1)

  def attack(self, other):
    result = self.roll_stat("str")
    damage_done = DEFAULT_DAMAGE + self.stat_mod("str")
    if result is 20:
      damage_done *= 2
    if result >= other.armor_class():
      self.add_experience(XP_PER_HIT)
      other.damage(damage_done)

  def damage(self, hp_amount):
    self.hit_points(self.hit_points() - hp_amount)

  def stat(self, name, new_val=None):
    if new_val != None:
      self._stats[name] = new_val
    val = self._stats.get(name, None)
    if val is None:
      raise InvalidStatException(name)
    return val

  def stat_mod(self, name):
    val = self.stat(name)
    return (val - 10) / 2

  def experience_points(self):
    return self._xp

  def add_experience(self, xp):
    self._xp += xp

  def level(self):
    return (self.experience_points() / 1000) + 1
