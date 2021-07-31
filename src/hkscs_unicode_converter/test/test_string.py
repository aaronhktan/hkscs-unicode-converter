from unittest import TestCase

from hkscs_unicode_converter import converter


class TestValid(TestCase):
    # All the test cases from converter.convert_char() should work
    def test_posessive(self):
        res = converter.convert_string("")
        self.assertEqual(res, "嘅")

    def test_correct(self):
        res = converter.convert_string("")
        self.assertEqual(res, "啱")

    def test_blabber(self):
        res = converter.convert_string("")
        self.assertEqual(res, "噏")

    def test_posessive_chr(self):
        res = converter.convert_string(chr(0xECD1))
        self.assertEqual(res, "嘅")

    def test_weird_edge_case(self):
        res = converter.convert_string(chr(0xF327))
        self.assertEqual(res, "Ê̌")

    # And some more test cases for strings specifically...
    def test_lots_of_blabber(self):
        res = converter.convert_string("亂廿四")
        self.assertEqual(res, "亂噏廿四")

    def test_thats_not_right(self):
        res = converter.convert_string("唔牙")
        self.assertEqual(res, "唔啱牙")

    def test_lots(self):
        res = converter.convert_string("大")
        self.assertEqual(res, "大嗱嗱")

    def test_unicode_literal(self):
        res = converter.convert_string("唔\ue7d4牙")
        self.assertEqual(res, "唔啱牙")

    def test_python_chr(self):
        res = converter.convert_string("唔" + chr(0xE7D4) + "牙")
        self.assertEqual(res, "唔啱牙")

    def test_beginning_of_string(self):
        res = converter.convert_string("好")
        self.assertEqual(res, "啱啱好")

    def test_weird_edge_case_in_string(self):
        res = converter.convert_string("EEEEE\uF327")
        self.assertEqual(res, "EEEEEÊ̌")

    def test_weird_edge_case_in_string_again(self):
        res = converter.convert_string("EEEEE" + chr(0xF327))
        self.assertEqual(res, "EEEEEÊ̌")

    def test_mixed_latin_cjk(self):
        res = converter.convert_string("key")
        self.assertEqual(res, "啱key")

    def test_mixed_numbers_cjk(self):
        res = converter.convert_string("1")
        self.assertEqual(res, "1嚟")

    # In order: Arabic numbers, Latin letters, Hangul, diacritic edge case, Amharic, Chinese, HKSCS, Sinhala, Arabic, Emoji
    def test_many_writing_systems(self):
        res = converter.convert_string("1A한\uF327አ啱අاَ☃️")
        self.assertEqual(res, "1A한Ê̌አ啱咗අاَ☃️")


class TestInvalid(TestCase):
    def test_no_arg(self):
        with self.assertRaises(TypeError):
            converter.convert_string()

    def test_not_string(self):
        with self.assertRaises(TypeError):
            converter.convert_string(-1)


class TestNoChangeNeeded(TestCase):
    # All the test cases from converter.convert_char() should work
    def test_latin(self):
        res = converter.convert_string("a")
        self.assertEqual(res, "a")

    def test_chinese(self):
        res = converter.convert_string("亂")
        self.assertEqual(res, "亂")

    def test_number(self):
        res = converter.convert_string("1")
        self.assertEqual(res, "1")

    def test_emoji(self):
        res = converter.convert_string("❓")
        self.assertEqual(res, "❓")

    def test_punctuation(self):
        res = converter.convert_string("'")
        self.assertEqual(res, "'")

    def test_sinhala(self):
        res = converter.convert_string("අ")
        self.assertEqual(res, "අ")

    # String with more than one character should work
    def test_basic_string(self):
        res = converter.convert_string("Hi!")
        self.assertEqual(res, "Hi!")

    def test_cjk_string(self):
        res = converter.convert_string("啱啱好")
        self.assertEqual(res, "啱啱好")

    def test_lots_of_blabber(self):
        res = converter.convert_string("亂噏廿四")
        self.assertEqual(res, "亂噏廿四")

    def test_thats_not_right(self):
        res = converter.convert_string("唔啱牙")
        self.assertEqual(res, "唔啱牙")

    def test_unicode_literal(self):
        res = converter.convert_string("唔\u5571牙")
        self.assertEqual(res, "唔\u5571牙")

    def test_python_chr(self):
        res = converter.convert_string("唔" + chr(0x5571) + "牙")
        self.assertEqual(res, "唔\u5571牙")

    def test_string_with_num(self):
        res = converter.convert_string("on9")
        self.assertEqual(res, "on9")

    def test_string_with_latin_and_cjk(self):
        res = converter.convert_string("AA制")
        self.assertEqual(res, "AA制")

    def test_string_with_latin_cjk_num(self):
        res = converter.convert_string("AA制12345")
        self.assertEqual(res, "AA制12345")

    # Multicodepoint emoji should stay the same and not throw an error
    def test_multicodepoint_emoji(self):
        res = converter.convert_string("👍🏽")
        self.assertEqual(res, "👍🏽")

    def test_many_writing_systems(self):
        res = converter.convert_string("1A한Ê̌አ啱咗අاَ☃️")
        self.assertEqual(res, "1A한Ê̌አ啱咗අاَ☃️")
