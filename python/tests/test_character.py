import unittest

from mock import MagicMock
from mock import patch

from evercraft import Character, InvalidAlignmentException, ALIGNMENTS
from evercraft import roll

# NOTE: Look at all of these redundant property tests! Can we factor this logic
#       into a mixin or something? Aren't Python's annotations meant to handle
#       cases like this?

class DefaultCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character()

class TestName(DefaultCharacter):

    def test_name_property(self):
        self.assertEqual(self.character.name(),"Anonymous")

    def test_change_name_property(self):
        new_name = "Baron Harkonnen"
        self.character.name(new_name)
        self.assertEqual(self.character.name(), new_name)

class TestAlignment(DefaultCharacter):

    def test_alignment_property(self):
        self.assertEqual(self.character.alignment(),"Neutral")

    def test_alignment_property_changes(self):
        for alignment in ALIGNMENTS:
          self.character.alignment(alignment)
          self.assertEqual(self.character.alignment(),alignment)

    def test_invalid_alignment_exception(self):
        self.assertRaises(InvalidAlignmentException,
                          self.character.alignment,
                          "Accelerationist")

class TestArmorClass(DefaultCharacter):

    def test_armor_class_property(self):
        self.assertEqual(self.character.armor_class(),10)

    def test_change_armor_class_property(self):
        self.character.armor_class(15) 
        self.assertEqual(self.character.armor_class(),15)

class TestHitPoints(DefaultCharacter):

    def test_hit_points_property(self):
        self.assertEqual(self.character.hit_points(),5)

    def test_change_hit_points_property(self):
        self.character.hit_points(1000)
        self.assertEqual(self.character.hit_points(),1000)

class TestAttacking(unittest.TestCase):

    def setUp(self):
        self.character = Character()
        self.opponent = Character()
        self.opponent.damage = MagicMock()

    @patch("evercraft.roll", return_value=5)
    def test_attacking_rolls_a_d20(self,roll):
        self.character.attack(self.opponent)
        self.assertEqual(roll.call_count, 1)

    @patch("evercraft.roll", return_value=19)
    def test_hits_when_rolling_at_or_over_target_ac(self, roll):
        self.character.attack(self.opponent)
        self.assertEqual(self.opponent.damage.call_count, 1)

    @patch("evercraft.roll", return_value=2)
    def test_miss_when_rolling_below_target_ac(self, roll):
        self.character.attack(self.opponent)
        self.assertEqual(self.opponent.damage.call_count, 0)

class TestBeingHit(DefaultCharacter):
    pass
