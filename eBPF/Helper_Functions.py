from ctypes import *

def ip_to_hex(ip):
    ip = ip.split(".")
    hex_ip ='0x'+'{:02x}{:02x}{:02x}{:02x}'.format(*map(int, ip))
    int_ip = c_uint(int(hex_ip[2:], 16))
    return int_ip

def hex_to_ip(ip):
    ip_ = str(hex(int(ip)))
    ip_ = ip_[2:]
    l = []
    while(len(ip_)!= 0):
        byte = ip_[-2:]
        ip_ = ip_[:-2]
        l.insert(0,int(byte, 16))

    ip = '.'.join(map(str, l))
    return ip

def convert_time(nanoseconds):
    print("convert_time")
    seconds, nanoseconds = divmod(info, 1e9)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(hours, minutes, seconds, nanoseconds)
