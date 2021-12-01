''' run an echo client using the built in asyncio framework

    references:

'''
import asyncio
import ssl

'''


'''


async def connect():
    sslcontext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH,
                                            cafile=
                                            ".\\client_server_certs\\server033142.crt")
    sslcontext.check_hostname = True
    sslcontext.load_cert_chain(certfile=".\\client_server_certs\\client033142.crt",
                               keyfile=".\\client_server_certs\\client033142.key")

    while True:
        reader, writer = await asyncio.open_connection("127.0.0.1",
                                                       1234,
                                                       ssl=sslcontext)
        data = await reader.read()
        if data == b'kissitlightly':
            break
        print(data)

    return
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect())
