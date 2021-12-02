''''''

from self_sign_tls_cert import SelfSignTLSCert as SSTC

def get_cert():
    client_cert, client_pkey = SSTC().gen_cert(save_cert=True)
    server_cert, server_pkey = SSTC().gen_cert(cert_file_name='server', save_cert=True)

    return client_cert, client_pkey, server_cert, server_pkey


get_cert()
