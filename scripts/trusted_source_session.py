"""Use Windows trust anchors alongside certifi without disabling TLS checks."""
import os
from pathlib import Path
import ssl
import tempfile

import certifi
import requests


def source_session():
    session = requests.Session()
    if os.name != 'nt' or os.environ.get('REQUESTS_CA_BUNDLE'):
        return session
    pem = Path(certifi.where()).read_text(encoding='ascii')
    for name in ('ROOT', 'CA'):
        for certificate, encoding, trust in ssl.enum_certificates(name):
            if encoding == 'x509_asn' and (trust is True or ssl.Purpose.SERVER_AUTH.oid in trust):
                pem += ssl.DER_cert_to_PEM_cert(certificate)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', prefix='gsai-source-ca-',
                                     encoding='ascii', delete=False) as stream:
        stream.write(pem)
        session.verify = stream.name
    original_close = session.close

    def close():
        original_close()
        Path(session.verify).unlink(missing_ok=True)
    session.close = close
    return session
