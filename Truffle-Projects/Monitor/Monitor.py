import json
import time
import random
from web3 import Web3

web3 = Web3(Web3.HTTPProvider('HTTP://10.0.0.112:7545'))

abi = json.loads('[ { "constant": true, "inputs": [ { "name": "", "type": "address" }, { "name": "", "type": "uint256" } ], "name": "Flows_id", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": false, "inputs": [ { "name": "_monitor", "type": "address" } ], "name": "Set_Monitor", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_host", "type": "string" }, { "name": "_destiny", "type": "string" }, { "name": "_protocol", "type": "string" } ], "name": "New_Flow", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "Increase_Count", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Id", "outputs": [ { "name": "", "type": "uint256[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "Get_Flow", "outputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Qnt", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" } ]')

monitor = '0x5267D97e8C44fd7a3D8FccC484b5038e39fa4b31'

address = web3.toChecksumAddress('0x16C8730b5abcaAa78457CE58a92775d7af9e5ed8')
contract = web3.eth.contract(address = address, abi=abi)

flows_qnt = 0
flows = list()

while(True):
    new_flow_qnt = contract.functions.Get_Flow_Qnt().call()
    if new_flow_qnt > flows_qnt:
        print("New Flow Detected")
        for x in range(new_flow_qnt-flows_qnt):
            new_flow = contract.functions.Get_Flow(flows_qnt + x).call({'from':monitor})
            flows.append(new_flow)
        flows_qnt = new_flow_qnt
    for flow in flows:
        print(flow)
    print()

    type = random.randint(1,4)
    print(type)
    if type == 1:
        protocol = 'http'
    elif type == 2:
        protocol = 'tcp'
    elif type == 3:
        protocol = 'tcp/ip'
    elif type == 4:
        protocol = 'IP'

    for flow in flows:
        if flow[3] == protocol:
            id = flow[0]
            tx_hash = contract.functions.Increase_Count(id).transact({'from': monitor})
            web3.eth.waitForTransactionReceipt(tx_hash)
            flow[4] = flow[4] + 1

    time.sleep(2)
