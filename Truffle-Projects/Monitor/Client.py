import json
from web3 import Web3

web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

abi = json.loads('[ { "constant": true, "inputs": [ { "name": "", "type": "address" }, { "name": "", "type": "uint256" } ], "name": "Flows_id", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": false, "inputs": [ { "name": "_monitor", "type": "address" } ], "name": "Set_Monitor", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_host", "type": "string" }, { "name": "_destiny", "type": "string" }, { "name": "_protocol", "type": "string" } ], "name": "New_Flow", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "Increase_Count", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Id", "outputs": [ { "name": "", "type": "uint256[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "Get_Flow", "outputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "string" }, { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "Get_Flow_Qnt", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" } ]')

owner = '0xf631b1cC9CcF165eC0C161E4B85F03E68A081bef'
monitor = '0x9f963803EFAC3592ad63a1cD3ca736c9Eed5b9c2'

client1 = '0x9aEFb1F7DEdb7F9a1aC578B3Be7c63Db33b1c78b'
client2 = '0xe55A3Dc7a8947578dAd1B133175E45a873eF993e'
client3 = '0x75B15B69D98E577d6509bd5E7C3285C138A2d7ab'
client4 = '0x4B2D9Dc47a32956aEe120fa4df1Ab59f0F8FDC78'
client5 = '0xEF8Bdd60fcC4f35cc9BA47c754bAE0358d8224D8'

clients = [client1,client2,client3,client4,client5]

address = web3.toChecksumAddress('0x67784810D0C87E4eCd31C6beA38E2ac318BA97F4')
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
