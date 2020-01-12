
//Get Method = Doesn't change contract state
//Returns value
MyContract.methods.MyMethod(params).call((error, result) => {console.log(result)});

Example : contract.methods.getCount().call((err, r) => {console.log(r)})

//Set Method = Changes contract state
//Returns created's block hash
MyContract.methods.MyMethod(params).send({from: account}, (error, result) => {console.log(result)});

Example : contract.methods.increaseCount().send({from:"0x6Dbe3006e1674ca32fb9A32e855c068dFd2259DB"}, (err, r) => {console.log(r)})


(error, result) => {console.log(result)} //Callback Function
