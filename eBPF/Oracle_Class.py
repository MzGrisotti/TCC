from bcc import BPF
from bcc.utils import printb
from ctypes import *
from Flow_Class import Flow_Data
from Helper_Functions import *

import json
import time
import random
from web3 import Web3

import time
import sys
import uptime

class Oracle:
    def __init__(self, web3, contract):
        self.web3 = web3
        self.contract = contract

    def handle_event(event):
        receipt = self.web3.eth.waitForTransactionReceipt(event['transactionHash'])
        result = self.contract.events.greeting.processReceipt(receipt)
        print(result[0]['args'])

    def log_loop(event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                handle_event(event)
                time.sleep(poll_interval)
