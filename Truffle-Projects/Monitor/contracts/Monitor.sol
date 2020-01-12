pragma solidity >=0.4.21 <0.6.0;

contract Monitor{

    struct Flow{
        uint id;
        string host;
        string destiny;
        string protocol;
        address client;
        uint count;
    }

    mapping(uint => Flow) private Flows;
    mapping(address => uint[]) public Flows_id;
    address private owner;
    address private monitor;

    uint private flows_qnt;

    constructor() public{
        owner = msg.sender;
        flows_qnt = 0;
    }

    function Set_Monitor(address _monitor) public{
        require(msg.sender == owner, "Esse metodo so pode ser acessado pelo owner");
        monitor = _monitor;

    }

    function New_Flow(string memory _host, string memory _destiny, string memory _protocol) public{
        uint actual = flows_qnt;
        flows_qnt++;
        Flows_id[msg.sender].push(actual);
        Flows[actual].id = actual;
        Flows[actual].host = _host;
        Flows[actual].destiny = _destiny;
        Flows[actual].count = 0;
        Flows[actual].protocol = _protocol;
        Flows[actual].client = msg.sender;
    }

    function Increase_Count(uint _id) public{
        require(msg.sender == monitor, "Esse metodo so pode ser acessado pelo monitor");
        Flows[_id].count++;
    }

    function Get_Flow_Id() public view returns(uint[] memory){
        return Flows_id[msg.sender];
    }

    function Get_Flow(uint _id) public view returns(uint, string memory, string memory, string memory, uint){
        require(Flows[_id].client == msg.sender || msg.sender == monitor, "Esse dado so pode ser acessado pelo cliente a quem ele pertence");
        Flow memory f = Flows[_id];
        return(f.id, f.host, f.destiny, f.protocol, f.count);
    }

    function Get_Flow_Qnt() public view returns(uint){
        return flows_qnt;
    }


}
