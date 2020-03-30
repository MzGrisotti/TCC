pragma solidity >=0.4.21 <0.6.0;

contract Monitor{

    struct Flow{
        uint id;
        address client;
        string host;
        string destiny;
        uint protocol;
        uint256 pktcount;
        uint256 total_bytes;
        uint256 start_tstamp;
        uint256 end_tstamp;
        uint256 last_packet_tstamp;
        uint256 duration;
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

    function New_Flow(string memory _host, string memory _destiny, uint _protocol) public{
        uint actual = flows_qnt;
        flows_qnt++;
        Flows_id[msg.sender].push(actual);
        Flows[actual].id = actual;
        Flows[actual].client = msg.sender;

        //Set by client
        Flows[actual].host = _host;
        Flows[actual].destiny = _destiny;
        Flows[actual].protocol = _protocol;

        //Set to default
        Flows[actual].pktcount = 0;
        Flows[actual].total_bytes = 0;
        Flows[actual].start_tstamp = block.timestamp;
        Flows[actual].end_tstamp = 0;
        Flows[actual].last_packet_tstamp = 0;
        Flows[actual].duration = 0;

    }

    function Get_Flow_Id() public view returns(uint[] memory){
        return Flows_id[msg.sender];
    }

    function Get_Flow(uint _id) public view returns(uint, string memory, string memory, uint, uint256, uint256, uint256, uint256, uint256){
        require(Flows[_id].client == msg.sender || msg.sender == monitor, "Esse dado so pode ser acessado pelo cliente a quem ele pertence");
        Flow memory f = Flows[_id];
        return(f.id, f.host, f.destiny, f.protocol, f.pktcount, f.total_bytes, f.start_tstamp, f.last_packet_tstamp, f.duration);
    }

    function Get_Flow_Qnt() public view returns(uint){
        return flows_qnt;
    }


}
