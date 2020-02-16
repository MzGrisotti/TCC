from bcc import BPF
from bcc.utils import printb
from ctypes import *
from Flow_Class import Flow_Data
from Helper_Functions import *
import time
import sys
import uptime

interface = "enp0s3"

def new_key(bpf):
    print("Creating New Key")
    map = bpf.get_table("Flow")

    flow = Flow_Data(map, "192.0.0.1", "80.101.30.20", 8080, 3999, 10, uptime.uptime())
    key = flow.get_key()
    leaf = flow.get_leaf()
    map[key] = leaf

    flow = Flow_Data(map, "127.0.0.1", "127.0.0.1", 9400, 9500, 17, uptime.uptime())
    key = flow.get_key()
    leaf = flow.get_leaf()
    map[key] = leaf

def convert_time(nanoseconds):
    print("convert_time")
    seconds, nanoseconds = divmod(info, 1e9)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(hours, minutes, seconds, nanoseconds)

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

def export_all(map):
    i = 0

def main_loop(bpf):
    flow_data = bpf.get_table("Flow")
    info_data = bpf.get_table("Info")
    print("Printing data")
    new_key(bpf)
    export_time_limit = 300 #seconds
    export_time = uptime.uptime()
    while 1:
        if(uptime.uptime() - export_time > export_time_limit):
            export_all(flow_data)
        try:
            print("\nFlows:\n")
            for k in flow_data.keys():
                map = flow_data[k]
                flow = Flow_Data(map)
                # if(flow.verify_export()):
                    # flow_data.__delitem__(k)
                flow.show()

            # for k in info_data.keys():
            #     info1 = info_data[k].info1
            #     info2 = info_data[k].info2
            #     up = uptime.uptime()
            #     print("time since last packet:{}, last packet:{}, delta time:{}".format(up - (info1/1e9), info1, info2))
            # print(count)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Removing filter from device")
            break;

    bpf.remove_xdp(interface)


if __name__ == "__main__":
    main()
