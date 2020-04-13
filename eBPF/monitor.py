from bcc import BPF
from bcc.utils import printb
from ctypes import *
from Flow_Class import Flow_Data
from Oracle_Class import Oracle
from Helper_Functions import *
from threading import Thread

import json
import time
import random
from web3 import Web3

import time
import sys
import uptime

interface = "enp0s3"

def load_ebpf_program():

    print("Loading program into Interface")
    mode = BPF.SOCKET_FILTER
    func_name = "colletor"

    #load eBPF program
    bpf = BPF(src_file = "colletor.c",debug = 8)

    #load function
    function = bpf.load_func(func_name, mode)

    #attach functino to network interface
    bpf.attach_raw_socket(function, interface)

    return bpf

def download_blockchain_data(bpf):

    print("Downloading Blockchain Data")

    web3 = Web3(Web3.HTTPProvider('HTTP://10.0.0.112:7545'))

    abi = json.loads('[ { "constant": true, "inputs": [ { "name": "", "type": "address" }, { "name": "", "type": "uint256" } ], "name": "Flows_id", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "id", "type": "uint256" } ], "name": "new_entry", "type": "event" }, { "constant": false, "inputs": [ { "name": "_monitor", "type": "address" } ], "name": "Set_Monitor", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_host", "type": "string" }, { "name": "_destiny", "type": "string" }, { "name": "_protocol", "type": "uint256" }, { "name": "_hport", "type": "uint256" }, { "name": "_dport", "type": "uint256" } ], "name": "New_Flow", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_pktcnt", "type": "uint64" }, { "name": "_t_bytes", "type": "uint64" }, { "name": "_last_pkt_tstamp", "type": "uint64" }, { "name": "_end_tstamp", "type": "uint64" } ], "name": "Update_Flow", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Id", "outputs": [ { "name": "", "type": "uint256[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "Get_Flow", "outputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Qnt", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" } ]')

    monitor = '0x5267D97e8C44fd7a3D8FccC484b5038e39fa4b31'
    contract_address = '0x16C8730b5abcaAa78457CE58a92775d7af9e5ed8'
    address = web3.toChecksumAddress(contract_address)
    Smart_Contract = web3.eth.contract(address = address, abi=abi)

    last_flow_id = Smart_Contract.functions.Get_Flow_Qnt().call()

    Flows = dict()
    map = bpf.get_table("Flow")

    oracle = Oracle(web3, Smart_Contract, map)
    oracle.start()

    for i in range(last_flow_id):
        new_flow = Smart_Contract.functions.Get_Flow(i).call({'from':monitor})
        Flows[new_flow[0]] = Flow_Data(new_flow, Smart_Contract, map)

    update_ebpf_map(bpf, Flows)

    return web3, Smart_Contract, Flows, oracle

def update_ebpf_map(bpf, Flows):

    map = bpf.get_table("Flow")

    print("Exporting Flows to kernel memory")
    for key in Flows:
        map_key = Flows[key].get_key()
        map_leaf = Flows[key].get_leaf()
        map[map_key] = map_leaf

def main():

    bpf = load_ebpf_program()
    web3, Smart_Contract, Flows, oracle = download_blockchain_data(bpf)

    main_loop(bpf, Flows, web3, Smart_Contract, oracle)


def export_all(Flows, web3, smart_contract):
    for flow in Flows:
        Flows[flow].export(web3, smart_contract)


def main_loop(bpf, Flows, web3, Smart_Contract, oracle):
    flow_data = bpf.get_table("Flow")
    info_data = bpf.get_table("Info")
    print("Collecting Data")
    # new_key(bpf)
    export_time_limit = 300 #seconds
    last_export_tstamp = uptime.uptime()
    while 1:

        new_flows = oracle.get_new_entries()
        if(len(new_flows) > 0):
            print("Merging New Flows")
            update_ebpf_map(bpf, new_flows)
            Flows.update(new_flows)
        try:
            print("\nFlows:\n")
            for k in flow_data.keys():
                map = flow_data[k]
                id = map.id
                Flows[id].update_stats_from_collector(map)
                a = Flows[id].verify_export(web3, Smart_Contract)
                Flows[id].show()

            time.sleep(1)

        except KeyboardInterrupt:
            print("Removing filter from device")
            break;

    export_all(Flows, web3, Smart_Contract)
    bpf.remove_xdp(interface)
    oracle.stop_t()


if __name__ == "__main__":
    main()
