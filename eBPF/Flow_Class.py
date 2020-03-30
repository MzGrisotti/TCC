from Helper_Functions import *
from ctypes import *
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
            # ip_src = int(map.ip_src)
            # ip_dst = hex(int(map.ip_src))
            self.port_src = int(map.port_src)
            self.port_dst = int(map.port_dst)
            self.protocol = map.protocol
            # self.protocol = hex(int(map.protocol))
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
            self.port_src = 0
            self.port_dst = 0
            self.protocol = c_ulong(args[0][5])
            # self.start_tstamp = int(args[6]*1e9)
            self.start_tstamp = int(uptime.uptime()*1e9)
            # self.end_tstamp = args[7]
            # self.last_packet_tstamp = int(args[6]*1e9)
            self.last_packet_tstamp = int(uptime.uptime()*1e9)
            self.fin = 0
            # self.duration = args[9]

        # Created with User Space Arguments
        else:
            self.id = 9999
            self.map = args[0]
            self.ip_src = args[1]
            self.ip_dst = args[2]
            self.port_src = args[3]
            self.port_dst = args[4]
            self.protocol = c_ulong(args[5])
            # self.start_tstamp = int(args[6]*1e9)
            self.start_tstamp = int(uptime.uptime()*1e9)
            # self.end_tstamp = args[7]
            # self.last_packet_tstamp = int(args[6]*1e9)
            self.last_packet_tstamp = int(uptime.uptime()*1e9)
            self.fin = 0
            # self.duration = args[9]

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
        return self.map.Leaf(c_ulong(id),ip_src, ip_dst, port_src, port_dst, protocol,c_ulong(0),c_ulong(0),start_tstamp,c_ulong(0),last_packet_tstamp,c_ulong(0))

    def get_delta_time(self):
        return uptime.uptime() - (self.last_packet_tstamp/1e9)

    def convert_time(self, nanoseconds):
        print("convert_time")
        seconds, nanoseconds = divmod(nanoseconds, 1e9)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        print(hours, minutes, seconds, nanoseconds)

    def verify_export(self):
        export = False
        export_time_limit = 30 #seconds

        if(self.fin == 1):
            export = True
            self.fin = 0

        delta = int(uptime.uptime()* 1e9) - self.last_packet_tstamp
        if(delta > export_time_limit * 1e9):
            export = True

        if(export):
            self.export()

        return export

    def export(self):
        #export flow data
        i = 1 #ignore

    def show(self):
        print("ip_src: {:16s}, ip_dst: {:16s}, port_src: {:5}, port_dst: {:5}, proto: {:4}, pktcnt: {:3}, bytes: {:10}, id: {}, start: {:15}, last: {:15}"
        .format(self.ip_src, self.ip_dst, self.port_src, self.port_dst, self.protocol, self.pktcnt, self.bytes, self.id, self.start_tstamp, self.last_packet_tstamp))
