import multiprocessing
import time
import datetime

def run(q):
    q.put('HEYA')
    import nbt
    import discord
    import numpy
    import pyautogui
    import json
    import click
    import flask
    while True:
        print(datetime.datetime.today())
        time.sleep(1)
        print('THE THREAD LIVES')


if __name__ == '__main__':
    context = multiprocessing.get_context('spawn')
    q = context.Queue()
    process = context.Process(target=run, args=(q,))
    process.start()
    process.terminate()
    print(q.get())

    time.sleep(10)

    print()