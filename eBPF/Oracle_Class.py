from bcc import BPF
from bcc.utils import printb
from ctypes import *
from Flow_Class import Flow_Data
from Helper_Functions import *
from threading import *

import json
import time
import random
from web3 import Web3

import time
import sys
import uptime

class Oracle(Thread):
    def __init__(self, web3, contract, map):
        Thread.__init__(self)
        self.web3 = web3
        self.contract = contract
        self.map = map
        self.event_filter = self.contract.events.new_entry.createFilter(fromBlock='latest')
        self.new = dict()
        self.lock = Lock()
        self.stop = False

    def handle_event(self, event):
        new_id = event.args.id
        print("New Flow Entry Detected, ID: {:4}".format(new_id))
        new_flow = self.contract.functions.Get_Flow(new_id).call({'from':'0x5267D97e8C44fd7a3D8FccC484b5038e39fa4b31'})
        self.lock.acquire()
        self.new[new_flow[0]] = Flow_Data(new_flow, self.contract, self.map)
        self.lock.release()

    def run(self):
        print("Starting Oracle")
        while not self.stop:
            for event in self.event_filter.get_new_entries():
                self.handle_event(event)
            # time.sleep(5)
        print("Stoping Oracle")

    def get_new_entries(self):

        self.lock.acquire()
        new_copy = dict()
        new_copy.update(self.new)
        self.new.clear()
        self.lock.release()

        return new_copy

    def stop_t(self):
        self.stop = True
