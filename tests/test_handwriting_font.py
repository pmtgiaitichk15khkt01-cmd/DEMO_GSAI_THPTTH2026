import base64
import io
from pathlib import Path
import re
import string
import unicodedata
import unittest

from fontTools.ttLib import TTFont
from services.lesson_export import build_lesson_html, renderer_assets


class HandwritingFontTests(unittest.TestCase):
    def test_actual_embedded_font_covers_vietnamese_without_system_fallback(self):
        _, embedded, _ = renderer_assets()
        font = TTFont(io.BytesIO(base64.b64decode(embedded)))
        cmap = font.getBestCmap()
        letters = {unicodedata.normalize('NFC', vowel + tone)
                   for vowel in 'aăâeêioôơuưyAĂÂEÊIOÔƠUƯY'
                   for tone in ('', '\u0300', '\u0301', '\u0303', '\u0309', '\u0323')} | set('đĐ')
        self.assertEqual(len(letters), 146)
        missing = [f'U+{ord(char):04X}' for char in letters | set(string.ascii_letters + string.digits)
                   if ord(char) not in cmap or cmap[ord(char)] == '.notdef']
        self.assertEqual(missing, [])
        self.assertEqual(font['OS/2'].usWeightClass, 400)

    def test_export_embeds_static_handwriting_and_retains_math_typesetting(self):
        lesson = 'Kể lại trải nghiệm: Ốc, ếch, hươu, người, chữ viết. $x^2+1$'
        page = build_lesson_html('Ngữ văn', 6, 'Kiểm chữ tiếng Việt', lesson)
        self.assertIn('font-style:normal;font-weight:400', page)
        self.assertNotIn('font-weight:100 900', page)
        self.assertIn('.handwritten{font-family:GSAIHand,cursive;font-synthesis:none}', page)
        self.assertIn('.handwritten .lesson-source-review{font-family:GSAIHand,cursive', page)
        self.assertIn('data:font/ttf;base64,', page)
        self.assertIn('Patrick Wagesreiter', page)
        self.assertIn('$x^2+1$', page)
        self.assertNotRegex(page, r'https?://fonts\.(?:googleapis|gstatic)\.com')
