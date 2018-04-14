import unittest

import meowth.spelling as spelling


class TestSpelling(unittest.TestCase):
    def setUp(self):
        self.pokemon_list = [
            "bulbasaur",
            "ivysaur",
            "venusaur",
            "charmander",
            "charmeleon",
            "charizard",
            "squirtle",
            "wartortle",
            "blastoise",
        ]

    def tearDown(self):
        # Remove global variables
        spelling.WORDS = None
        spelling.N = None

    def test_dictionary_initialization(self):
        """Tests that WORDS is populated correctly"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        self.assertEqual(len(spelling.WORDS), 9)

    def test_words_generation(self):
        """Tests that text is properly split into words"""
        words = spelling.words("Bulbasaur, Charmander, Squirtle")

        # Test that 3 words were extracted
        self.assertEqual(len(words), 3)

        # Test that each word is properly extracted
        self.assertTrue("bulbasaur" in words)
        self.assertTrue("charmander" in words)
        self.assertTrue("squirtle" in words)

    def test_known_word(self):
        """Tests that a word can be found in the dictionary"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        known_words = spelling.known(["bulbasaur", "charmander", "pickachu"])

        self.assertEqual(len(known_words), 2)

    def test_word_with_no_dictionary(self):
        """Tests that None is returned if no dictionary present"""
        known_words = spelling.known(["bulbasaur", "charmander", "pickachu"])

        self.assertIsNone(known_words)

    def test_p_without_n(self):
        """Tests proper error handling if no N is set"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        # Remove N
        spelling.N = None

        self.assertEqual(spelling.P("bulbasaur"), 0)

    def test_edits1_added_letter(self):
        """Tests that edits1 corrects extra letter"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        edits = spelling.edits1("bulbasaurs")

        self.assertTrue("bulbasaur" in edits)

    def test_edits1_deleted_letter(self):
        """Tests that edits1 corrects missing letter"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        edits = spelling.edits1("bulbaaur")

        self.assertTrue("bulbasaur" in edits)

    def test_edits1_transposed_letter(self):
        """Tests that edits1 corrects transposed letters"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        edits = spelling.edits1("bublasaur")

        self.assertTrue("bulbasaur" in edits)

    def test_edits1_replaced_letter(self):
        """Tests that edits1 corrects transposed letters"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        edits = spelling.edits1("pulbasaur")

        self.assertTrue("bulbasaur" in edits)

    def test_edits2_added_letter(self):
        """Tests that edits1 corrects extra letter"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        edits = spelling.edits2("bulbasaurss")

        self.assertTrue("bulbasaur" in edits)

    def test_edits2_deleted_letter(self):
        """Tests that edits1 corrects missing letter"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        edits = spelling.edits2("bulbaur")

        self.assertTrue("bulbasaur" in edits)

    def test_edits2_transposed_letter(self):
        """Tests that edits1 corrects transposed letters"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        edits = spelling.edits2("bbulasaur")

        self.assertTrue("bulbasaur" in edits)

    def test_edits2_replaced_letter(self):
        """Tests that edits1 corrects transposed letters"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        edits = spelling.edits2("palbasaur")

        self.assertTrue("bulbasaur" in edits)

    def test_correction(self):
        """Tests that the proper correction is given"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        self.assertEqual(spelling.correction("palbasaur"), "bulbasaur")

    def test_correction_with_no_answer(self):
        """Tests that no correction is given"""
        # Load the dictionary
        spelling.set_dictionary(self.pokemon_list)

        self.assertEqual(spelling.correction("bbbbulbasaur"), "bbbbulbasaur")
