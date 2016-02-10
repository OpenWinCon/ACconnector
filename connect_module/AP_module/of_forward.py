# -*- coding: utf-8 -*-

from netfilterqueue import NetfilterQueue
from scapy.all import *
import subprocess 

def pkt_filter_callback(packet):
    print packet

    pkt = IP(packet.get_payload())

    try:
        if pkt[TCP].dport == 6633 or pkt[TCP].dport == 6653:
            packet.set_mark(30) 

    except:
        pass

    finally:
        packet.accept()


def of_forward_func():
    '''
    q = nfqueue.queue()
    q.open()
    q.bind(socket.AF_INET)
    q.set_callback(pkt_modify)
    q.create_queue(1)
    '''

    nfq = NetfilterQueue()
    nfq.bind(1, pkt_filter_callback)

    cmd = 'ip rule add fwmark 30 table of_forward'
    subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    cmd = 'ip route add default dev ppp0 table of_forward'
    subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    cmd = 'iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE'
    subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    try:
        print 'Full forward mode - Starting to forwarding Openflow packet'
        nfq.run()

    except KeyboardInterrupt:
        print 'Quitting Openflow packet forward mode'
        nfq.unbind()

        cmd = 'ip rule del table of_forward' 
        subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

        cmd = 'ip route flush table of_forward'
        subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

        cmd = 'iptables -t nat -D POSTROUTING 1'
        subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

