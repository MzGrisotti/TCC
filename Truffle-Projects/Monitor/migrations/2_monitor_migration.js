const Monitor = artifacts.require("./Monitor");

module.exports = function(deployer) {
  deployer.deploy(Monitor);
};
