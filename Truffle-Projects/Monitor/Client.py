import json
from web3 import Web3

web3 = Web3(Web3.HTTPProvider('HTTP://10.0.0.112:7545'))

abi = json.loads('[ { "constant": true, "inputs": [ { "name": "", "type": "address" }, { "name": "", "type": "uint256" } ], "name": "Flows_id", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": false, "inputs": [ { "name": "_monitor", "type": "address" } ], "name": "Set_Monitor", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_host", "type": "string" }, { "name": "_destiny", "type": "string" }, { "name": "_protocol", "type": "string" } ], "name": "New_Flow", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "Increase_Count", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Id", "outputs": [ { "name": "", "type": "uint256[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "Get_Flow", "outputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Qnt", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" } ]')

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

while(True):
    num = 0
    for i in clients:
        print(num,"-",i)
        num = num + 1
    account = int(input("Select account to use [0-4]: "))
    print("Select Method to use:")
    print("1 - New Flow")
    print("2 - Get Flow Info")
    print("3 - Get Flows you own")
    print("4 - Get Flows Qnt")
    method = int(input("Answer: "))
    print()
    if method == 1:
        host = input("Enter host: ")
        dest = input("Enter destiny: ")
        protocol = input("Enter protocol: ")
        tx_hash = contract.functions.New_Flow(host, dest, protocol).transact({'from': clients[account]})
        web3.eth.waitForTransactionReceipt(tx_hash)
    elif method == 2:
        id = int(input("Enter Flow ID: "))
        print(contract.functions.Get_Flow(id).call({'from':clients[account]}))
    elif method == 3:
        print(contract.functions.Get_Flow_Id().call({'from':clients[account]}))
    elif method == 4:
        print(contract.functions.Get_Flow_Qnt().call())
    print()
