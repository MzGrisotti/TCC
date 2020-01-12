var Web3 = require('web3');

var web3 = new Web3('HTTP://127.0.0.1:7545');

var address = '0x941Ec482894e9f69f7407c245855073e61c65F28';

var teste = { abi: [
{
"inputs": [],
"payable": false,
"stateMutability": "nonpayable",
"type": "constructor"
},
{
"constant": true,
"inputs": [],
"name": "getName",
"outputs": [
{
"name": "",
"type": "string"
}
],
"payable": false,
"stateMutability": "view",
"type": "function"
},
{
"constant": false,
"inputs": [
{
"name": "_name",
"type": "string"
}
],
"name": "setName",
"outputs": [],
"payable": false,
"stateMutability": "nonpayable",
"type": "function"
},
{
"constant": false,
"inputs": [],
"name": "increaseCount",
"outputs": [],
"payable": false,
"stateMutability": "nonpayable",
"type": "function"
},
{
"constant": false,
"inputs": [],
"name": "decreaseCount",
"outputs": [],
"payable": false,
"stateMutability": "nonpayable",
"type": "function"
},
{
"constant": true,
"inputs": [],
"name": "getCount",
"outputs": [
{
"name": "",
"type": "int256"
}
],
"payable": false,
"stateMutability": "view",
"type": "function"
}
]};


module.exports = {teste,
                  address,
                  web3,
                  contract: new web3.eth.Contract(teste.abi, address)
                  };
