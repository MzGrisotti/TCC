pragma solidity >=0.4.21 <0.6.0;

contract Monitor{

    struct Flow{
        uint id;
        address client;
        string host;
        string destiny;
        uint host_port;
        uint destiny_port;
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

    uint private next_flow_id;

    event new_entry(uint id);

    constructor() public{
        owner = msg.sender;
        next_flow_id = 0;
    }

    function Set_Monitor(address _monitor) public{
        require(msg.sender == owner, "Esse metodo so pode ser acessado pelo owner");
        monitor = _monitor;

    }

    function New_Flow(string memory _host, string memory _destiny, uint _protocol, uint _hport, uint _dport) public{
        uint actual = next_flow_id;
        next_flow_id++;
        Flows_id[msg.sender].push(actual);
        Flows[actual].id = actual;
        Flows[actual].client = msg.sender;

        //Set by client
        Flows[actual].host = _host;
        Flows[actual].destiny = _destiny;
        Flows[actual].host_port = _hport;
        Flows[actual].destiny_port = _dport;
        Flows[actual].protocol = _protocol;

        //Set to default
        Flows[actual].pktcount = 0;
        Flows[actual].total_bytes = 0;
        Flows[actual].start_tstamp = block.timestamp;
        Flows[actual].end_tstamp = 0;
        Flows[actual].last_packet_tstamp = 0;
        Flows[actual].duration = 0;

        emit new_entry(actual);

    }

    function Update_Flow(uint _id, uint64 _pktcnt, uint64 _t_bytes, uint64 _last_pkt_tstamp, uint64 _end_tstamp) public{
        /* require(msg.sender == monitor, "Metodo só pode ser acessado pelo monitor"); */
        if(Flows[_id].id >= 0){
            Flows[_id].pktcount += (uint256(_pktcnt) - Flows[_id].pktcount);
            Flows[_id].total_bytes += (uint256(_t_bytes) - Flows[_id].total_bytes);
            Flows[_id].end_tstamp = uint256(_end_tstamp);
            Flows[_id].last_packet_tstamp = uint256(_last_pkt_tstamp);
            Flows[_id].duration = block.timestamp - Flows[_id].start_tstamp;
        }

    }

    function Get_Flow_Id() public view returns(uint[] memory){
        return Flows_id[msg.sender];
    }

    function Get_Flow(uint _id) public view returns(uint, string memory, string memory, uint, uint, uint, uint256, uint256, uint256, uint256, uint256){
        require(Flows[_id].client == msg.sender || msg.sender == monitor, "Esse dado so pode ser acessado pelo cliente a quem ele pertence");
        Flow memory f = Flows[_id];
        return(f.id, f.host, f.destiny, f.host_port, f.destiny_port, f.protocol, f.pktcount, f.total_bytes, f.start_tstamp, f.last_packet_tstamp, f.duration);
    }

    function Get_Flow_Qnt() public view returns(uint){
        return next_flow_id;
    }


}
