from random import randint
import asyncio
import logging
import socket
import os

from constants import *


async def send():
    global count

    while True:
        await asyncio.sleep(randint(300, 3000) / 1000)

        client.sendall(f'[{count}] PING\n'.encode())

        count += 1

        await asyncio.sleep(0)


async def recv():
    while True:
        message = ''

        while True:
            data = await eventLoop.sock_recv(client, 1)

            if data == b'\n':
                break

            message += data.decode()

        logging.info(message)


async def main():
    global eventLoop

    eventLoop = asyncio.get_event_loop()
    eventLoop.create_task(send())
    eventLoop.create_task(recv())

    await asyncio.gather(*asyncio.all_tasks())


if __name__ == '__main__':
    count = 0
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    client.setblocking(False)

    logging.basicConfig(filename=f"{__file__.split('/')[-1].split('.')[-2]}_{os.getpid()}.log", filemode='w', format='%(asctime)s %(message)s', level=logging.DEBUG)

    asyncio.run(main())