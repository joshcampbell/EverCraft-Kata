import unittest

from mock import MagicMock
from mock import patch

from evercraft import Character, InvalidAlignmentException, ALIGNMENTS
from evercraft import roll, DEFAULT_DAMAGE, DEFAULT_HIT_POINTS
from evercraft import DEFAULT_ARMOR_CLASS, DEFAULT_STAT_SCORE
from evercraft import InvalidStatException
from evercraft import XP_PER_HIT

# NOTE: Look at all of these redundant property tests! Can we factor this logic
#       into a mixin or something? Aren't Python's annotations meant to handle
#       cases like this?
#
#       (annotation => decorator)

STATS = ["str","dex","con","wis","int","cha"]
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

class TestHitPoints(DefaultCharacter):

    def test_hit_points_property(self):
        self.assertEqual(self.character.hit_points(),DEFAULT_HIT_POINTS)

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

    def test_boring_default_stats(self):
        for stat in STATS:
            self.assertEqual(self.character.stat(stat),
                             DEFAULT_STAT_SCORE)

    def test_stat_modifiers(self):
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
        for stat in STATS:
            for score in range(1,20):
              self.character.stat(stat,score)
              self.assertEqual(self.character.stat_mod(stat), 
                               ability_modifiers[score])

    def test_invalid_stat_access(self):
        self.assertRaises(InvalidStatException,
                          self.character.stat,
                          "vim")

class TestModifiersModifying(DefaultCharacter):

    def test_dex_adds_armor(self):
        for score in range(1,20):
            self.character.stat("dex",score)
            self.assertEqual(self.character.armor_class(),
                    DEFAULT_ARMOR_CLASS + self.character.stat_mod("dex"))

    @patch("evercraft.roll", return_value=10)
    def test_roll_str_modifier(self, __):
        for score in range(1,20):
            result = self.character.roll_stat("str")
            self.assertEqual(result, 10 + self.character.stat_mod("str"))

    @patch("evercraft.roll", return_value=19)
    def test_str_adds_damage(self, __):
        self.character.stat("str",20)
        self.opponent = Character()
        self.character.attack(self.opponent)
        self.assertEqual(self.opponent.hit_points(), 
                DEFAULT_HIT_POINTS - (DEFAULT_DAMAGE + 5))

    def test_con_adds_hit_points(self):
        for score in range(1,20):
            self.assertEqual(self.character.hit_points(),
                DEFAULT_HIT_POINTS + self.character.stat_mod("con"))

class TestExperience(unittest.TestCase):

    def setUp(self):
        self.character = Character()
        self.opponent = Character()

    @patch("evercraft.roll", return_value=20)
    def test_xp_gain_on_hit(self, __):
        self.character.attack(self.opponent)
        self.assertEqual(self.character.experience_points(), XP_PER_HIT)

    @patch("evercraft.roll", return_value=2)
    def test_xp_gain_on_miss(self, __):
        self.character.attack(self.opponent)
        self.assertEqual(self.character.experience_points(), 0)

    def test_calculate_level(self):
        cases = [(0,1), (999,1), (1000, 2), (1001, 2), (2000, 3), (3000, 4)]
        for xp, expected_level in cases:
          self.character = Character()
          self.character.add_experience(xp)
          self.assertEqual(self.character.level(), expected_level, 
                           "%s %s"%(xp, self.character.level()))
