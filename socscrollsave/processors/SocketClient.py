import multiprocessing
from time import time

import socket
import websocket

from socscrollsave.core.constants import Constants
from socscrollsave.common.logger import Logger as Log


TAG = "Socket"


class SocketProcess(multiprocessing.Process):
    """
    Socket client
    """
    def __init__(self, parser_process):


        """
        Initialises values for process.
        :param parser_process: Reference to a ParserProcess instance.
        :type parser_process: ParserProcess


        """

        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._parser = parser_process
        self._socket_client = websocket.WebSocket()



        Log.i(TAG, "Process Ready")

    def open(self, port='ger', speed='million', timeout=0.01):


        try:

            self._socket_client.connect("ws://192.168.4.1:81/")

            Log.i(TAG, "Socket open")
            return True
        except TimeoutError:
            Log.w(TAG, "Error")
        return False

    def run(self):
        """
        Reads the socket until a stop call is made.
        :return:
        """
        buffer_size = 20
        Log.i(TAG, "Process starting...")
        timestamp = time()

        while not self._exit.is_set():
            stamp = time() - timestamp
            try:
                data = self._socket_client.recv()
                #print(data)
                if len(data) > 0:
                    self._parser.add([stamp, data])
            except:
                print("Data_error")
        Log.i(TAG, "Process finished")

    def stop(self):
        """
        Signals the process to stop acquiring data.
        :return:
        """
        Log.i(TAG, "Process finishing...")
        self._socket_client.close()
        self._exit.set()

