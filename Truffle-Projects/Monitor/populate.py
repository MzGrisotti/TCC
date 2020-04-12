import json
import random
from web3 import Web3
# method erode bacon income cross staff runway beef replace already unknown bundle
web3 = Web3(Web3.HTTPProvider('HTTP://10.0.0.112:7545'))

abi = json.loads('[ { "constant": true, "inputs": [ { "name": "", "type": "address" }, { "name": "", "type": "uint256" } ], "name": "Flows_id", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": false, "inputs": [ { "name": "_monitor", "type": "address" } ], "name": "Set_Monitor", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_host", "type": "string" }, { "name": "_destiny", "type": "string" }, { "name": "_protocol", "type": "uint256" }, { "name": "_hport", "type": "uint256" }, { "name": "_dport", "type": "uint256" } ], "name": "New_Flow", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_pktcnt", "type": "uint64" }, { "name": "_t_bytes", "type": "uint64" }, { "name": "_last_pkt_tstamp", "type": "uint64" }, { "name": "_end_tstamp", "type": "uint64" } ], "name": "Update_Flow", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Id", "outputs": [ { "name": "", "type": "uint256[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "Get_Flow", "outputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Qnt", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" } ]')

owner = '0xa803db32a7a3034F93478022Fcf9e58D96A840A8'
monitor = '0x5267D97e8C44fd7a3D8FccC484b5038e39fa4b31'

client1 = '0xB0439dAecDf803925dc37531dcbc8e9Ff4A97A6a'
client2 = '0x95BFa40fEe133E15e1379BC21aF554Fb94FedA91'
client3 = '0x1Aa329ed01CDfB77EC1d01d0Ecc234d0c40EC37f'
client4 = '0x5d28D02d031900Ef18A8653490cE99dD2B70df15'
client5 = '0x3eECC2bc23ed68d13A3459115599271a6183F182'

clients = [client1,client2,client3,client4,client5]

address = web3.toChecksumAddress('0x16C8730b5abcaAa78457CE58a92775d7af9e5ed8')
contract = web3.eth.contract(address = address, abi=abi)

tx_hash = contract.functions.Set_Monitor(monitor).transact({'from': owner})
web3.eth.waitForTransactionReceipt(tx_hash)
#print(contract.functions.Get_Flow_Qnt().call())
flows_qnt = int(input("Digite a quantidade de fluxos para inserir na blockchain: "))
for i in range(0, flows_qnt):
    account = random.randint(0,4)
    if random.randint(1,2) == 1:
        host = "10.0.0.112"
        dest = "10.0.0.105"
    else:
        host = "10.0.0.105"
        dest = "10.0.0.112"
    host_port = random.randint(9000, 55000)
    dest_port = random.randint(9000, 55000)
    if random.randint(1,2) == 1:
        protocol = 17
    else:
        protocol = 6
    tx_hash = contract.functions.New_Flow(host, dest, protocol, host_port, dest_port).transact({'from': clients[account]})
    web3.eth.waitForTransactionReceipt(tx_hash)
