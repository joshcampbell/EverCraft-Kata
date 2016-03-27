ALIGNMENTS = [ "Lawful", "Neutral", "Chaotic" ]

class InvalidAlignmentException(Exception):
  pass

class Character:

  def __init__(self):
    self.name("Anonymous")
    self.alignment("Neutral")
    self.armor_class(10)

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
