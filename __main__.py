''''''

from self_sign_tls_cert import SelfSignTLSCert as SSTC

def get_cert():
    client_cert = SSTC().gen_cert(save_cert=True)
    server_cert = SSTC().gen_cert(cert_file_name='server', save_cert=True)

    return client_cert, server_cert


get_cert()
