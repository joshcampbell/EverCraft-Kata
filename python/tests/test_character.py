import unittest

from evercraft import Character, InvalidAlignmentException, ALIGNMENTS

class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character()

    def test_name_property(self):
        self.assertEqual(self.character.name(),"Anonymous")

    def test_change_name_property(self):
        new_name = "Baron Harkonnen"
        self.character.name(new_name)
        self.assertEqual(self.character.name(), new_name)

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

    def test_armor_class_property(self):
        self.assertEqual(self.character.armor_class(),10)

    def test_change_armor_class_property(self):
        self.character.armor_class(15) 
        self.assertEqual(self.character.armor_class(),15)

# NOTE: Look at all of these redundant property tests! Can we factor this logic
#       into a mixin or something? Aren't Python's annotations meant to handle
#       cases like this?

# TODO: Combat test cases will require mocking. Need to read about it first.
