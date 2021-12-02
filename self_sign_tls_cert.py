''' create a pair of self signed TLS certs

    *** ONLY VALID FOR LOCAL TESTING ***

'''

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from ipaddress import IPv4Address as ipv4
import socket
import os
import datetime

class SelfSignTLSCert():
    ''' Create self signed TLS certificate

        - certificate only valid for local testing.

    references:
        - https://cryptography.io/en/latest/x509/tutorial/#creating-a-self-signed-certificate
        - https://cryptography.io/en/latest/x509/tutorial/#determining-certificate-or-certificate-signing-request-key-type
        - https://www.electricmonk.nl/log/2018/06/02/ssl-tls-client-certificate-verification-with-python-v3-4-sslcontext/

    methods:
        - get_dt: return the current date and time
        - gen_pkey: generate a private key
        - gen_cert: generate a TLS certificate

    parameters:
        - cert_dir: <str>: name of the core folder for storing certs and keys:
        default <certs>
        - cert_file_name: <str>: name of the certificate folder and file:
        default: <client>

    properties:
        - save_cert -> _save_cert: Create the necessary file structure for
        saving a cert and or private key.

    notes:
        - One can use the same cert for the client and server in a two
        node network. However, if the network gets larger than two there
        will be issues distinguishing between nodes on the network.
        Furthermore, using this tactic greatly lessens the security of TLS
        overall by giving both the client and server access to the same private
        key. I highly discourge the user from doing this unless the cert will
        only be used once. I.e., for a one time proof of concept throw away
        app.
    '''
    def __init__(self, cert_dir='certs'):
        self.cert_path = None
        self.cert_dir = cert_dir
        self._save_cert = None
        self._save_key = None
        # self.save_cert = save_cert

    @property
    def save_cert(self):
        ''' Create the necessary file structure for saving a cert.

            info
                - If save_cert is at any time set to True a file
                structure will be created. This is true even if the user
                ultimately decides not to save a cert or key
        '''
        return self._save_cert

    @save_cert.setter
    def save_cert(self, value):
        self._save_cert = value
        if value is True:
            self.cert_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                          self.cert_dir,
                                          self.get_dt(format='%m%d%Y'))
            if os.path.exists(self.cert_path) is False:
                os.makedirs(self.cert_path)

    @property
    def save_key(self):
        ''' Create the necessary file structure for saving a private key.

            info
                - If save_key is at any time set to True a file
                structure will be created. This is true even if the user
                ultimately decides not to save a cert or key
        '''
        return self._save_key

    @save_key.setter
    def save_key(self, value):
        self._save_key = value
        if value is True:
            self.cert_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                          self.cert_dir,
                                          self.get_dt(format='%m%d%Y'))
            if os.path.exists(self.cert_path) is False:
                os.makedirs(self.cert_path)

    def get_dt(self, format='%m%d%Y%H%M%S'):
        ''' return the current UTC date and time

            input:
                -format: <str>: the date time format: default:
                <%m%d%Y%H%M%S> (month:day:year:hours:minutes:seconds)

            output:
                date time string : <str>

        '''
        return(datetime.datetime.utcnow().strftime(format))

    def gen_pkey(self, key_name='private_key', save_key=False, key_size=4096):
        ''' generate a private key

        input:
            - key_name: <str>: the key file name:~ default: 'private_key'
            - save_key: <bool>: user choice to save the private key: default
            <False>
            - key_size: <int>: the bit-length of the key:~ default: 4096

        output:
            - a private key of length 'key_size'
            - PEM encoded private key



        '''
        key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        print(save_key)
        self.save_key = save_key
        print(self.save_key)
        if self.save_key is True:
            # unique file name for each key generated
            pk_file_name = os.path.join(self.cert_path, f'{key_name}{self.get_dt()}.key')
            # save key in the same folder as this module
            with open(pk_file_name, 'wb') as pk_file:
                pk_file.write(key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()))

        return key, key.private_bytes(encoding=serialization.Encoding.PEM,
                                 format=serialization.PrivateFormat.PKCS8,
                                 encryption_algorithm=serialization.NoEncryption())

    def gen_cert(self,
                 country_name='US',
                 state_or_province_name='California',
                 locality_name='Los Angeles',
                 organization_name='org_name',
                 common_name='common_name',
                 cert_file_name='client',
                 save_cert=False):

        ''' generate a certificate use in a TLS connection

        input:
            - country_name: <str>: name of the country the certificate is being
            used in: default: <US>
            - state_or_province_name: <str>: default: <California>
            - locality_name: <str>: default: <Los Angeles>
            - organization_name: <str>: Name of the Orginization using the
            certificate: default: <org_name>
            - common_name: <str>: default: <common_name>
            - save_cert: <bool>: user choice to save the certificate: default
            <False>


        output:
            - a self signed TLS certificate and its private key (PEM encoded)
        '''
        self.save_cert = save_cert
        print(self.save_cert)
        if self.save_cert is True:
            print("we are in the save_key=True pkey gen")
            pkey = self.gen_pkey(key_name=cert_file_name, save_key=True)
        else:
            print("we are in the save_key=False pkey gen")
            pkey = self.gen_pkey(key_name=cert_file_name)

        common_name = socket.gethostname()

        subject = issuer = x509.Name([
          x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
          x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_or_province_name),
          x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
          x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
          x509.NameAttribute(NameOID.COMMON_NAME, common_name),
          ])

        cert = x509.CertificateBuilder().subject_name(
          subject
        ).issuer_name(
          issuer
        ).public_key(
          pkey[0].public_key()
        ).serial_number(
          x509.random_serial_number()
        ).not_valid_before(
          datetime.datetime.utcnow()
        ).not_valid_after(
          # Our certificate will be valid for 1825 days
          datetime.datetime.utcnow() + datetime.timedelta(days=730)
        ).add_extension(x509.BasicConstraints(ca=False, path_length=None),
                                              critical=True,
        ).add_extension(x509.SubjectAlternativeName([x509.IPAddress
                                                    (ipv4('127.0.0.1')),
                                                    x509.DNSName
                                                    (f'{common_name}'),
                                                    x509.DNSName
                                                    (f'*.{common_name}'),
                                                    x509.DNSName('localhost'),
                                                    x509.DNSName('*.localhost'),
                                                     ]), critical=False,
        ).sign(pkey[0], hashes.SHA256())
        if self.save_cert is True:
            cert_path = os.path.join(self.cert_path, f'{cert_file_name}{self.get_dt()}.crt')
            with open(cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))

        return (cert.public_bytes(serialization.Encoding.PEM),
                pkey[1])

def main():
    ''' create and save a pair of self signed client/server TLS certificates '''
    client_cert, client_pkey = SelfSignTLSCert().gen_cert(save_cert=True)
    server_cert, server_pkey = SelfSignTLSCert().gen_cert(cert_file_name='server', save_cert=True)


if __name__ == '__main__':
    main()
