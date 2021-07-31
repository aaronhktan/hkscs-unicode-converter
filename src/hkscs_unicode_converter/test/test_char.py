from unittest import TestCase

from hkscs_unicode_converter import converter


class TestValid(TestCase):
    def test_posessive(self):
        res = converter.convert_char("")
        self.assertEqual(res, "嘅")

    def test_correct(self):
        res = converter.convert_char("")
        self.assertEqual(res, "啱")

    def test_blabber(self):
        res = converter.convert_char("")
        self.assertEqual(res, "噏")

    def test_posessive_chr(self):
        res = converter.convert_char(chr(0xECD1))
        self.assertEqual(res, "嘅")

    def test_weird_edge_case(self):
        res = converter.convert_char(chr(0xF327))
        self.assertEqual(res, "Ê̌")


class TestInvalid(TestCase):
    def test_no_arg(self):
        with self.assertRaises(TypeError):
            converter.convert_char()

    def test_not_string(self):
        with self.assertRaises(TypeError):
            converter.convert_char(-1)

    def test_arg_too_long(self):
        with self.assertRaises(ValueError):
            converter.convert_char("Hi!")

    def test_multicodepoint_emoji(self):
        with self.assertRaises(ValueError):
            converter.convert_char("👋🏿")


class TestNoChangeNeeded(TestCase):
    def test_latin(self):
        res = converter.convert_char("a")
        self.assertEqual(res, "a")

    def test_chinese(self):
        res = converter.convert_char("亂")
        self.assertEqual(res, "亂")

    def test_number(self):
        res = converter.convert_char("1")
        self.assertEqual(res, "1")

    def test_emoji(self):
        res = converter.convert_char("❓")
        self.assertEqual(res, "❓")

    def test_punctuation(self):
        res = converter.convert_char("'")
        self.assertEqual(res, "'")

    def test_sinhala(self):
        res = converter.convert_string("අ")
        self.assertEqual(res, "අ")
