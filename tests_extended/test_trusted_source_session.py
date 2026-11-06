import os
from pathlib import Path
import ssl
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import trusted_source_session as sources


class TrustedSourceTests(unittest.TestCase):
    @unittest.skipUnless(os.name=='nt','Windows trust integration')
    def test_system_trust_keeps_verification_and_cleans_temp_file(self):
        with patch.dict(os.environ), patch.object(ssl,'enum_certificates',return_value=[]):
            os.environ.pop('REQUESTS_CA_BUNDLE',None)
            session=sources.source_session()
            path=Path(session.verify)
            self.assertTrue(path.is_file())
            self.assertIn('BEGIN CERTIFICATE',path.read_text(encoding='ascii'))
            self.assertNotEqual(session.verify,False)
            session.close()
            self.assertFalse(path.exists())

    def test_explicit_ca_configuration_is_respected(self):
        with patch.dict(os.environ,REQUESTS_CA_BUNDLE='configured-ca.pem'):
            with sources.source_session() as session:
                self.assertTrue(session.verify)
                self.assertIs(session.verify,True)
