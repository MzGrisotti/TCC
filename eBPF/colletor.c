
#include <bcc/proto.h>
#include <bcc/helpers.h>
#include <uapi/linux/ptrace.h>
#include <linux/ktime.h>
#include <linux/time.h>
#include <linux/timekeeping.h>
#include <linux/skbuff.h>

struct Flow_data {
    u64 id;
    u64 ip_src;
    u64 ip_dst;
    u64 port_src;
    u64 port_dst;
    u64 protocol;
    u64 pktcnt;
    u64 bytes;
    u64 start_tstamp;
    u64 end_tstamp;
    u64 last_packet_tstamp;
    u64 duration;
};

struct Flow_key {
    u64 ip_src;
    u64 ip_dst;
    u64 port_src;
    u64 port_dst;
    u64 protocol;
};

struct Info_data {
    u64 info1;
    u64 info2;
};

struct Debug_data {
    u64 info1;
    u64 info2;
    u64 info3;
};

#define IP_TCP    6
#define IP_UDP    17
//                1
#define IP_ICMP   1
#define ETH_HLEN  14

//10240000 max
BPF_HASH(Debug, u64, struct Debug_data, 10240);
BPF_HASH(Flow, struct Flow_key, struct Flow_data, 10240);
BPF_HASH(Info, u64, struct Info_data, 10240);

static void new_entry_map(struct Flow_key *key, u64 ip_len);
static void match_entry_map(struct Flow_key *key, u64 ip_len);

int colletor(struct __sk_buff *skb) {

    u64 zero = 0;
    u8 *cursor = 0;
    u64 next;

    struct Debug_data Debug_Zero = {zero, zero, zero};
    struct Info_data info_zero = {zero, zero};

    struct Info_data* info = Info.lookup_or_try_init(&zero, &info_zero);
    if(info){
        info->info1 = bpf_ktime_get_ns();
        info->info2 = bpf_ktime_get_ns() - info->info1;
    }

    struct ethernet_t *ethernet = cursor_advance(cursor, sizeof(*ethernet));
    //filter IP packets (ethernet type = 0x0800)
    if (ethernet->type == 0x0800) {
        struct ip_t *ip = cursor_advance(cursor, sizeof(*ip));

        struct Flow_key key;
        key.ip_src = ip->src;
        key.ip_dst = ip->dst;
        key.protocol = ip->nextp;

        if (ip->nextp == IP_TCP) {
            struct tcp_t *tcp = cursor_advance(cursor, sizeof(*tcp));
            key.port_src = tcp->src_port;
            key.port_dst = tcp->dst_port;
            match_entry_map(&key, ip->tlen);
        }
        if (ip->nextp == IP_UDP) {
            struct udp_t *udp = cursor_advance(cursor, sizeof(*udp));
            key.port_src = udp->sport;
            key.port_dst = udp->dport;
            match_entry_map(&key, ip->tlen);
        }
    }

    return -1;
}

static void match_entry_map(struct Flow_key *key, u64 ip_len){
    // Search for key in map
    struct Flow_data *flow = Flow.lookup(key);

    if(flow){ // Found entry
        flow->pktcnt++;
        flow->bytes += ip_len;
        flow->last_packet_tstamp = bpf_ktime_get_ns();
    }else{ // Not found entry
        new_entry_map(key, ip_len);
    }

}

static void new_entry_map(struct Flow_key *key, u64 ip_len){

    u64 zero = 0;
    struct Flow_data Flow_Zero = {zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero};

    // Create new entry
    struct Flow_data* flow = Flow.lookup_or_try_init(key, &Flow_Zero);
    if(flow){
        flow->ip_src = key->ip_src;
        flow->ip_dst = key->ip_dst;
        flow->port_src = key->port_src;
        flow->port_dst = key->port_dst;
        flow->protocol = key->protocol;
        flow->pktcnt++;
        flow->bytes += ip_len;
        flow->start_tstamp = bpf_ktime_get_ns();
        flow->last_packet_tstamp = bpf_ktime_get_ns();
    }
}
