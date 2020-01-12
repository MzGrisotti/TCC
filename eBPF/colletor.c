
#include <bcc/proto.h>
#include <bcc/helpers.h>
#include <uapi/linux/ptrace.h>
#include <linux/ktime.h>
#include <linux/time.h>
#include <linux/timekeeping.h>
#include <linux/skbuff.h>

struct flow_data {
    u64 id;
    u64 ip_src;
    u64 ip_dst;
    u64 port_src;
    u64 port_dst;
    u64 protocol;
    u64 pktcnt;
    u64 bytes;
};

struct flow_key {
    u64 ip_src;
    u64 ip_dst;
    u64 port_src;
    u64 port_dst;
    u64 protocol;
};

struct debug_data {
    u64 info1;
    u64 info2;
    u64 info3;
};

#define IP_TCP    6
#define IP_UDP    17
//                1
#define IP_ICMP   1
#define ETH_HLEN  14

BPF_HASH(debug, u64, struct debug_data, 10240);
//10240000 max
BPF_HASH(flow, struct flow_key, struct flow_data, 10240);
// BPF_HASH(flow, u64, struct flow_data, 1024);

static void new_entry_map(struct flow_key *Key, u64 ip_len);
static void match_entry_map(struct flow_key *Key, u64 ip_len);

int colletor(struct __sk_buff *skb) {

    u64 zero = 0;
    u8 *cursor = 0;
    u64 next;

    struct debug_data Debug_Zero = {zero, zero, zero};

    struct debug_data* Data = debug.lookup_or_try_init(&zero, &Debug_Zero);
    if(Data){
        Data->info3 = bpf_ktime_get_ns();
    }

    struct ethernet_t *ethernet = cursor_advance(cursor, sizeof(*ethernet));
    //filter IP packets (ethernet type = 0x0800)
    if (ethernet->type == 0x0800) {
        struct ip_t *ip = cursor_advance(cursor, sizeof(*ip));

        struct flow_key Key;
        Key.ip_src = ip->src;
        Key.ip_dst = ip->dst;
        Key.protocol = ip->nextp;

        if (ip->nextp == IP_TCP) {
            struct tcp_t *tcp = cursor_advance(cursor, sizeof(*tcp));
            Key.port_src = tcp->src_port;
            Key.port_dst = tcp->dst_port;
            match_entry_map(&Key, ip->tlen);
        }
        if (ip->nextp == IP_UDP) {
            struct udp_t *udp = cursor_advance(cursor, sizeof(*udp));
            Key.port_src = udp->sport;
            Key.port_dst = udp->dport;
            //new_entry_map(&Key, ip->tlen);
        }

    }

    return -1;
}

static void match_entry_map(struct flow_key *Key, u64 ip_len){
    // Search for key in map
    struct flow_data *Flow = flow.lookup(Key);

    if(Flow){ // Found entry
        Flow->pktcnt++;
        Flow->bytes += ip_len;
    }else{ // Not found entry
        new_entry_map(Key, ip_len);
    }

}

static void new_entry_map(struct flow_key *Key, u64 ip_len){

    u64 zero = 0;
    struct flow_data Flow_Zero = {zero, zero, zero, zero, zero, zero, zero, zero};

    // Create new entry
    struct flow_data* Flow = flow.lookup_or_try_init(Key, &Flow_Zero);
    if(Flow){
        Flow->ip_src = Key->ip_src;
        Flow->ip_dst = Key->ip_dst;
        Flow->port_src = Key->port_src;
        Flow->port_dst = Key->port_dst;
        Flow->protocol = Key->protocol;
        Flow->pktcnt++;
        Flow->bytes += ip_len;
    }
}
