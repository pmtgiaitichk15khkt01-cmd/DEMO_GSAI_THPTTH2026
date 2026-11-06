import os
import unittest
from unittest.mock import patch

from tests.test_expert_patch_regressions import load_function


class VoiceEndpointConfigTests(unittest.TestCase):
    def resolve(self, environment, secret):
        with patch.dict(os.environ, environment, clear=True):
            return load_function('get_voice_public_url', os=os,
                                 get_secret=lambda name, default: secret)()

    def test_streamlit_secrets_work_without_process_environment(self):
        self.assertEqual(self.resolve({}, ' https://voice.example/ '), 'https://voice.example')

    def test_process_environment_takes_precedence(self):
        self.assertEqual(self.resolve({'GSAI_VOICE_PUBLIC_URL': 'https://env.example/'},
                                      'https://secret.example'), 'https://env.example')

    def test_blank_environment_falls_back_and_missing_config_stays_empty(self):
        self.assertEqual(self.resolve({'GSAI_VOICE_PUBLIC_URL': ' '}, 'https://voice.example'),
                         'https://voice.example')
        for value in (None, {}, 3, ''):
            self.assertEqual(self.resolve({}, value), '')
