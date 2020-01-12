pragma solidity >=0.4.21 <0.6.0;

contract HelloWorld {

  int count;

  constructor() public {
    count = 0;
  }

  function increaseCount() public{
      count += 1;
  }
  function decreaseCount() public{
      count -= 1;
  }

  function getCount() public view returns (int){
      return count;
  }
}
