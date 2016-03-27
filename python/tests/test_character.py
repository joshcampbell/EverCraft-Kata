import unittest

from mock import MagicMock
from mock import patch

from evercraft import Character, InvalidAlignmentException, ALIGNMENTS
from evercraft import roll, DEFAULT_DAMAGE

# NOTE: Look at all of these redundant property tests! Can we factor this logic
#       into a mixin or something? Aren't Python's annotations meant to handle
#       cases like this?
#
#       (annotation => decorator)

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

    @patch("evercraft.roll", return_value=19)
    def test_hits_doing_default_damage(self, roll):
        self.character.attack(self.opponent)
        self.opponent.damage.assert_called_once_with(DEFAULT_DAMAGE)

    @patch("evercraft.roll", return_value=2)
    def test_miss_when_rolling_below_target_ac(self, roll):
        self.character.attack(self.opponent)
        self.assertEqual(self.opponent.damage.call_count, 0)

    @patch("evercraft.roll", return_value=20)
    def test_critical_hit_does_double_damage(self,roll):
        self.character.attack(self.opponent)
        self.opponent.damage.assert_called_once_with(DEFAULT_DAMAGE * 2)

class TestBeingHit(DefaultCharacter):

    def test_taking_damage(self):
        original_hp = self.character.hit_points()
        damage = DEFAULT_DAMAGE
        self.character.damage(DEFAULT_DAMAGE)
        self.assertEqual(self.character.hit_points(), 
                         original_hp - DEFAULT_DAMAGE)

class TestStatRanges(DefaultCharacter):

    def test_stat_modifiers(self):
        stats = ["str","dex","con","wis","int","cha"]
        ability_modifiers = {
            1: -5,
            2: -4,
            3: -4,
            4: -3,
            5: -3,
            6: -2,
            7: -2,
            8: -1,
            9: -1,
            10: 0,
            11: 0,
            12: 1,
            13: 1,
            14: 2,
            15: 2,
            16: 3,
            17: 3,
            18: 4,
            19: 4,
            20: 5
        }
        for stat in stats:
            for score in range(1,20):
              self.character.stat(stat,score)
              self.assertEqual(self.character.stat_mod(stat), 
                               ability_modifiers[score])

    def test_invalid_stat_access(self):
      pass
