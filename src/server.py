import asyncio
import logging
import socket

from constants import *


async def keepConnection():
    global responseCount

    while True:
        await asyncio.sleep(5)

        for client in clients:
            client.sendall(f'[{responseCount}] keepalive\n'.encode())

            await asyncio.sleep(0)

            responseCount += 1


async def handle(client):
    global responseCount

    clients.append(client)

    while True:
        message = ''

        while True:
            data = await eventLoop.sock_recv(client, 1)

            if not data:
                clients.remove(client)

                return

            if data == b'\n':
                break

            message += data.decode()

        logging.info(message)

        answer = f'[{responseCount}] PONG'

        client.sendall((answer + '\n').encode())

        logging.info(answer)

        responseCount += 1

        await asyncio.sleep(0)


async def main():
    global eventLoop

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen(2)
    server.setblocking(False)

    eventLoop = asyncio.get_event_loop()
    eventLoop.create_task(keepConnection())

    while True:
        connection, _ = await eventLoop.sock_accept(server)

        eventLoop.create_task(handle(connection))


if __name__ == '__main__':
    clients = []
    responseCount = 0

    logging.basicConfig(filename=f"{__file__.split('/')[-1].split('.')[-2]}.log", filemode='w', format='%(asctime)s %(message)s', level=logging.DEBUG)

    asyncio.run(main())