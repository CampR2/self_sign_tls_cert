
# ***readme in progress***
# self_sign_tls_cert (SSTC)
## Intro: Generate self signed TLS certificate, Generate RSA key pairs, Optional to save either to disk, Documented

- SSTC is designed to make it easy to create and save self signed TLS certs
        Tags: TLS, Self-Signed TLS, Security, Python, cryptography, Socket, Simple Socket, Client, Server
# Repository Notes
- Branch Notes
    - "stable" will hold the latest release as it becomes availiable.
        - this branch should work out of the box 
        - STABLE
    - "test" this branch will be an experimental working branch used for
       testing and debugging before a stable release
        - UNSTABLE
    
# Installing and Running
SSTC is designed to be a drop in package. After download, drop the package into
an application's folder structure where it can be accessed by the necessary module.
Then, import the self_sign_tls_cert package for use in said module.
The \__init__.py file inside the self_sign_tls_cert package is designed to make
it easy to import the SelfSignTLSCert object

within your application ...
```
from .self_sign_tls_cert import SSTC
```
Depending on your file structure you may need to use an absolute path for
the import instead of a relative path.
E.g.,
```
from app_root_folder.sub_folder.self_sign_tls_cert import SSTC
```

Refer to the helper client server example scripts included in the repo

If SSTC is run as a stand alone package,
E.g.
```
python self_sign_tls_cert
```
 it will create and save a pair of client/server certificates and keys inside
 a certs folder within this package


# Program Execution
import selfSignedTLSCerts object

**Robert Camp (CampR2)**
# ***readme in progress***
