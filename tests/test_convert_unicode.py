from unittest import TestCase
from nico_tools import convunichrs

unicode_string = "\u3086\u3086\u5f0f\u306f\u5fa9\u6d3b\u3059\u308b\u3093\u3060"
converted_string = "ゆゆ式は復活するんだ"


class TestConvertUnicode(TestCase):

    def test_convert_unicode(self):
        converted = convunichrs.convert_unichars(unicode_string)
        self.assertEqual(converted, converted_string)
