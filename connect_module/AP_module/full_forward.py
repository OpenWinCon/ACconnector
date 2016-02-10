# -*- coding: utf-8 -*-

from netfilterqueue import NetfilterQueue
from scapy.all import *
import subprocess 
import sys

def pkt_filter_callback(packet):
    print packet

    packet.set_mark(10) 
    packet.accept()


def full_forward_func():
    '''
    q = nfqueue.queue()
    q.open()
    q.bind(socket.AF_INET)
    q.set_callback(pkt_modify)
    q.create_queue(1)
    '''

    nfq = NetfilterQueue()
    nfq.bind(1, pkt_filter_callback)

    cmd = 'ip rule add fwmark 10 table full_forward'
    subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    cmd = 'ip route add default dev ppp0 table full_forward'
    subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    cmd = 'iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE'
    subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    cmd = 'sysctl -w net.ipv4.conf.ppp0.rp_filter=2'
    subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    try:
        print 'Full forward mode - Starting to forwarding every packet'
        nfq.run()

    except KeyboardInterrupt:
        print 'Quitting full forward mode'
        nfq.unbind()

        cmd = 'ip rule del table full_forward' 
        p1 = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

        cmd = 'ip route flush table full_forward'
        p2 = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

        cmd = 'iptables -t nat -D POSTROUTING 1'
        p3 = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

        p1.kill()
        p2.kill()
        p3.kill()
        
        raise KeyboardInterrupt

