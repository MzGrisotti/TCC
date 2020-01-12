from bcc import BPF
from bcc.utils import printb
from ctypes import *
from Flow_Class import Flow_Data
from Helper_Functions import *
import time
import sys

interface = "enp0s3"

def new_key(bpf):
    print("Creating New Key")
    #map[key] = map.Leaf(c_ulong(arguments))
    # map[c_ulong(1)] = map.Leaf(c_ulong(5),c_ulong(2), c_ulong(3))
    # flow_data[flow_data.Key(c_ulong(5),c_ulong(5),c_ulong(5),c_ulong(4),c_ulong(5))] = flow_data.Leaf(c_ulong(1),c_ulong(2), c_ulong(3),c_ulong(4),c_ulong(5),c_ulong(6),c_ulong(7),c_ulong(8))
    map = bpf.get_table("Flow")

    flow = Flow_Data(map, "192.0.0.1", "80.101.30.20", 8080, 3999, 10)
    key = flow.get_key()
    leaf = flow.get_leaf()
    map[key] = leaf

    ip_src = ip_to_hex("10.0.0.1")
    ip_dst = ip_to_hex("192.23.50.3")
    port_src = c_ulong(1000)
    port_dst = c_ulong(3999)
    protocol = c_ulong(6)
    # protocol = c_ulong(int(hex(6), 16))
    print("ip_src: {}, ip_dst: {}, port_src: {}, port_dst: {}, protocol: {}".format(ip_src, ip_dst, port_src, port_dst, protocol))
    map[map.Key(ip_src, ip_dst, port_src, port_dst, protocol)] = map.Leaf(c_ulong(0),ip_src, ip_dst, port_src, port_dst, protocol,c_ulong(0),c_ulong(0))

def load_ebpf_program():

    print("Loading program into Interface")
    mode = BPF.SOCKET_FILTER
    func_name = "colletor"

    #load eBPF program
    bpf = BPF(src_file = "colletor.c",debug = 8)

    #load function
    function = bpf.load_func(func_name, mode)

    #attach functino to network interface
    bpf.attach_raw_socket(function, interface)

    return bpf

def main():

    bpf = load_ebpf_program()
    main_loop(bpf)
    # debug(bpf)

def debug(bpf):
    debug = bpf.get_table("Debug")
    print("Debugging")
    # hex_to_ip(0)
    # ip_to_hex(0)
    while 1:
        try:
            # (task, pid, cpu, flags, ts, msg) = bpf.trace_fields()
            for k in debug.keys():
                 val = debug[k]
                 val1 = int(val.info1)
                 val2 = int(val.info2)
                 val3 = int(val.info3)

                 print("debug: {}, {}, tstamp: {}".format(val1, val2, val3))
            time.sleep(1)
        except ValueError:
            continue
        except KeyboardInterrupt:
             print("Removing filter from device")
             break;
        # printb(b"%s" % (msg))
    bpf.remove_xdp(interface)

def main_loop(bpf):
    flow_data = bpf.get_table("Flow")
    print("Printing data")
    new_key(bpf)
    while 1:
        try:
            print("\nFlows:\n")
            for k in flow_data.keys():
                map = flow_data[k]
                flow = Flow_Data(map)
                flow.show()

            time.sleep(1)
        except KeyboardInterrupt:
            print("Removing filter from device")
            break;

    bpf.remove_xdp(interface)


if __name__ == "__main__":
    main()
