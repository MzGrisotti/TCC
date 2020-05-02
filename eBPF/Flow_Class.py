from Helper_Functions import *
from ctypes import *
from web3 import Web3
import random
import uptime

# struct Flow_data {
#     u64 id;
#     u64 ip_src;
#     u64 ip_dst;
#     uint port_src;
#     uint port_dst;
#     u64 protocol;
#     u64 pktcnt;
#     u64 bytes;
#     u64 start_tstamp;
#     u64 end_tstamp;
#     u64 last_packet_tstamp;
#     u64 duration;
# };
#
# struct key_ {
#   u64 ip_src;
#   u64 ip_dst;
#   u64 port_src;
#   u64 port_dst;
#   u64 protocol;
# };

class Flow_Data:
    def __init__(self, *args):
        # Created with kernel Map object
        if(len(args) == 1):
            map = args[0]
            self.map = map
            self.id = map.id
            self.ip_src = hex_to_ip(map.ip_src)
            self.ip_dst = hex_to_ip(map.ip_dst)
            self.port_src = int(map.port_src)
            self.port_dst = int(map.port_dst)
            self.protocol = map.protocol
            self.pktcnt = int(map.pktcnt)
            self.bytes = int(map.bytes)
            self.start_tstamp = int(map.start_tstamp)
            self.end_tstamp = int(map.end_tstamp)
            self.last_packet_tstamp = int(map.last_packet_tstamp)
            self.duration = int(map.duration)
            self.fin = 0

        #Created with Blockchain Arguments
        elif(len(args) == 3):
            self.smart_contract = args[1]
            self.id = args[0][0]
            self.map = args[2]
            self.ip_src = args[0][1]
            self.ip_dst = args[0][2]
            self.port_src = args[0][3]
            self.port_dst = args[0][4]
            self.protocol = args[0][5]
            self.pktcnt = args[0][6]
            self.bytes = args[0][7]
            self.start_tstamp = int(uptime.uptime()*1e9)
            self.end_tstamp = 0
            self.last_export = int(uptime.uptime()*1e9)
            self.last_packet_tstamp = int((uptime.uptime() + 10)*1e9)
            self.duration = 0
            self.fin = 0
            # self.duration = args[9]


    def update_stats_from_collector(self, map):
        # self.protocol = hex(int(map.protocol))
        # if int(map.pktcnt) - self.pktcnt > 0:
        #      self.pktcnt += (int(map.pktcnt) - self.pktcnt)
        #
        # if int(map.bytes) - self.bytes > 0:
        #     self.bytes += (int(map.bytes) - self.bytes)

        self.pktcnt = int(map.pktcnt)
        self.bytes = int(map.bytes)
        # self.fin = map.fin
        self.last_packet_tstamp = int(map.last_packet_tstamp)
        self.duration = int(map.duration)


    def get_key(self):
        # Return Kernel's Key Object
        ip_src = ip_to_hex(self.ip_src)
        ip_dst = ip_to_hex(self.ip_dst)
        port_src = c_uint(self.port_src)
        port_dst = c_uint(self.port_dst)
        protocol = self.protocol
        return self.map.Key(ip_src, ip_dst, port_src, port_dst, protocol)

    def get_leaf(self):
        # Return Kernel's Leaft Object
        id = self.id
        ip_src = ip_to_hex(self.ip_src)
        ip_dst = ip_to_hex(self.ip_dst)
        port_src = c_uint(self.port_src)
        port_dst = c_uint(self.port_dst)
        protocol = self.protocol
        start_tstamp = c_ulong(self.start_tstamp)
        last_packet_tstamp = c_ulong(self.last_packet_tstamp)
        return self.map.Leaf(c_ulong(id),ip_src, ip_dst, port_src, port_dst, protocol,c_ulong(self.pktcnt),c_ulong(self.bytes),start_tstamp,c_ulong(0),last_packet_tstamp,c_ulong(0))

    def get_delta_time(self):
        return uptime.uptime() - (self.last_packet_tstamp/1e9)

    def convert_time(self, nanoseconds):
        print("convert_time")
        seconds, nanoseconds = divmod(nanoseconds, 1e9)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        print(hours, minutes, seconds, nanoseconds)

    def verify_export(self, web3, Smart_Contract):
        export = False
        export_time_limit = 10 #seconds

        # Export Tag fin
        if(self.fin == 1):
            export = True
            self.fin = 0

        # Export last packet tstamp
        delta = int(uptime.uptime()* 1e9) - self.last_packet_tstamp
        if(delta > export_time_limit * 1e9 and self.last_packet_tstamp > self.last_export):
            export = True

        if(export):
            self.export(web3, Smart_Contract)
            self.last_export = int(uptime.uptime()*1e9)

        return export

    def export(self, web3, Smart_Contract):
        #export flow data
        print("Exporting Flow {}:".format(self.id))
        monitor = '0x5267D97e8C44fd7a3D8FccC484b5038e39fa4b31'
        tx_hash = Smart_Contract.functions.Update_Flow(
        self.id,
        self.pktcnt,
        self.bytes,
        self.last_packet_tstamp,
        self.end_tstamp
        ).transact({'from': monitor})
        web3.eth.waitForTransactionReceipt(tx_hash)

    def show(self):
        print("id: {:3}, ip_src: {:10s}, ip_dst: {:10s}, port_src: {:5}, port_dst: {:5}, proto: {:3}, pktcnt: {:7}, bytes: {:10}, start: {}"
        .format( self.id, self.ip_src, self.ip_dst, self.port_src, self.port_dst, self.protocol, self.pktcnt, self.bytes, self.start_tstamp))
