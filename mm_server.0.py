''' run an echo server using the built in asyncio framework

    references:



'''
import asyncio
import ssl


async def client_connected(reader, writer):
    print(writer.get_extra_info('socket'))
    message = input('What woud you like to say?: ')
    writer.write(bytes(message, 'utf-8'))
    writer.close()


def main():
    sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    sslcontext.verify_mode = ssl.CERT_REQUIRED
    sslcontext.load_cert_chain(certfile=".\\client_server_certs\\server033142.crt",
                               keyfile=".\\client_server_certs\\server033142.key")

    sslcontext.load_verify_locations(".\\client_server_certs\\client033142.crt")

    print(sslcontext.cert_store_stats())
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(asyncio.start_server(client_connected,
                                               "127.0.0.1",
                                               1234,
                                               ssl=sslcontext))

    loop.run_forever()


if __name__ == '__main__':
    main()
