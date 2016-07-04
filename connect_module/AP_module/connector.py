# -*- coding: utf-8 -*-


from netfilterqueue import NetfilterQueue
from scapy.all import *
import subprocess 
import os
import pickle


#from selective_forward import selective_forward_func
#from full_forward import full_forward_func
#from of_forward import of_forward_func


class SettingManager:
    file_name = '/etc/iproute2/forward.settings'

    def __init__(self):

        try:
            with open(self.file_name, 'r') as fp:
                self.settings = pickle.load(fp)

        except IOError:
            fp = open(self.file_name, 'w')
            fp.close()
            self.settings = {}

        except EOFError:
            self.settings = {}
        

    def print_settings(self):
        print 'Printing forward settings'

        for k, v in sorted(self.settings.iteritems()):
            print k, v['forward_inter'], v['mode']


    def update_setting(self):
        print 'Enter ethernet interface name: ',
        inter_name = raw_input()

        print 'Enter forwarding interface name: ',
        forward_inter = raw_input()

        print 'Enter forwarding mode: ',
        forward_mode = raw_input()

        self.settings[inter_name] = {'forward_inter': forward_inter, 'mode': forward_mode}

        with open(self.file_name, 'w') as fp:
            pickle.dump(self.settings, fp)


    def delete_setting(self):
        print 'Enter ethernet interface name: ',
        inter_name = raw_input()

        self.settings.pop(inter_name, None)

        with open(self.file_name, 'w') as fp:
            pickle.dump(self.settings, fp)


    def get_settings(self):
        return self.settings


def make_pkt_callback(idx):
    def pkt_callback(pkt):
        print pkt
        pkt.set_mark(idx)
        pkt.accept()
    return pkt_callback


def make_selective_pkt_callback(idx):
    def pkt_callback(pkt):
        #data = payload.get_data()
        pkt = IP(packet.get_payload())

        if pkt.proto in proto_filter:
            pkt_action = proto_filter[pkt.proto]
            if pkt_action == 'accept':
                packet.accept()

            elif pkt_action == 'drop':
                packet.drop()
                #payload.verdict(nfqueue.NF_DROP)

            elif pkt_action == 'reroute':
                print 'Packet Rerouting'
                packet.set_mark(idx)
                packet.accept()

        if pkt.src in src_addr_filter:
            pkt_src_port, pkt_action = src_addr_filter[pkt.src]
            if pkt_src_port == '*' or pkt_src_port == pkt.sport:
                if pkt_action == 'accept':
                    packet.accept()
                    #payload.set_verdict(nfqueue.NF_ACCEPT)

                elif pkt_action == 'drop':
                    packet.drop()
                    #payload.set_verdict(nfqueue.NF_DROP)

        if pkt.dst in dst_addr_filter:
            pkt_dst_port, pkt_action = dst_addr_filter[pkt.dst]
            if pkt_dst_port == '*' or pkt_dst_port == pkt.dport:
                if pkt_action == 'accept':
                    packet.accept()
                    #payload.set_verdict(nfqueue.NF_ACCEPT)

                elif pkt_action == 'drop':
                    packet.drop()
                    #payload.set_verdict(nfqueue.NF_DROP)

                elif pkt_action == 'reroute':
                    packet.set_mark(idx)
                    packet.accept()
    return pkt_callback  


def check_tables():
    fp = open('/etc/iproute2/rt_tables', 'r')

    lines = list(map(lambda x: x.replace('\n', ''), fp.readlines()))

    tables = {}

    if len(lines) > 11:
        for line in lines[11:]:
            if not line.startswith('#'):
                info = line.split('\t')
                table_code = int(info[0])
                table_name = info[1]
                
                tables[table_code] = table_name

    if 10 not in tables:
        tables[10] = 'full_forward'

    if 20 not in tables:
        tables[20] = 'selective_forward'

    if 30 not in tables:
        tables[30] = 'of_forward'

    fp = open('/etc/iproute2/rt_tables', 'w')
    for line in lines[:11]:
        fp.write(line + '\n')

    for k, v in sorted(tables.iteritems(), reverse=True):
        fp.write('%d\t%s\n' % (k, v))
    fp.close()


def start_forwarding(settings):
    nfq = NetfilterQueue()
    idx = 1
    for inter_name, forward_dic in sorted(settings.iteritems()):
        forward_inter, forward_mode = forward_dic['forward_inter'], int(forward_dic['mode'])
        
        #nfq.bind(idx, lambda pkt: print pkt; pkt.set_mark(idx); pkt.accept())
        nfq.bind(idx, make_pkt_callback(idx))

        if forward_mode == 1:    
            cmd = 'iptables -t mangle -I PREROUTING -i %s -j NFQUEUE --queue-num %d' % (inter_name, idx)

        elif forward_mode == 3:
            cmd = 'iptables -t mangle -I PREROUTING -i %s -p tcp --dport 6633 -j NFQUEUE --queue-num %d' % (inter_name, idx)
        
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

        cmd = 'ip rule add fwmark %d table %d' % (idx, idx)
        subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)

        cmd = 'ip route add default dev %s table %d' % (forward_inter, idx)
        subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)

        cmd = 'iptables -t nat -I POSTROUTING -o %s -j MASQUERADE' % forward_inter
        subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)

        cmd = 'sysctl -w net.ipv4.conf.%s.rp_filter=2' % forward_inter
        subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)

        idx += 1

    try:
        print
        print 'Full forward mode - Starting to forwarding every packet'

        nfq.run()

    except KeyboardInterrupt:
        print
        print 'Qutting forwarding mode'

        idx = 1
        for inter_name, forward_dic in sorted(settings.iteritems()):
            forward_inter, forward_mode = forward_dic['forward_inter'], forward_dic['mode'] 
            
            cmd = 'iptables -t mangle -D PREROUTING -i %s -j NFQUEUE --queue-num %d' % (inter_name, idx)
            subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

            cmd = 'ip rule del table %d' % idx
            subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)

            cmd = 'ip route flush table %d' % idx
            subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)

            cmd = 'iptables -t nat -D POSTROUTING -o %s -j MASQUERADE' % forward_inter
            subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)

            idx += 1

    return 
            

def control_delegation():
    #check_tables()
    setting_manager = SettingManager()
    #setting_manager.print_settings()
    #setting_manager.update_setting()

    # cmd = 'iptables -A INPUT -i br-lan -j NFQUEUE --queue-num 1'
    # cmd = 'iptables -A FORWARD -i eth1 -j NFQUEUE --queue-num 1'
    # cmd = 'iptables -A OUTPUT -d 8.8.8.8 -j NFQUEUE --queue-num 1'

    #cmd = 'sysctl -w net.ipv4.conf.ppp0.rp_filter=2'
    #p2 = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    #p1.kill()
    #p2.kill()

    while True:
        print 
        print '(AP - controller) connector - Main mode'
        print 'Select mode'
        print '1. Check forward settings'
        print '2. Update forward setting'
        print '3. Delete forward setting'
        print '4. Start forwarding'
        print '5. Program quit'
        '''
        print '1. Full delegation'
        print '2. Selective delegation'
        print '3. Openflow forward (OVS needed)'
        print '4. Program Quit'
        '''

        try:
            print 'Select mode: ',
            selection = int(raw_input())

            if selection not in range(1, 6):
                raise ValueError

        except ValueError:
            print 'Enter proper number (1~4)'
            continue

        '''
        if selection == 1:
            full_forward_func()

        elif selection == 2:
            selective_forward_func()

        elif selection == 3:
            of_forward_func()
        '''

        if selection == 1:
            setting_manager.print_settings()

        elif selection == 2:
            setting_manager.update_setting()
        
        elif selection == 3:
            setting_manager.delete_setting()

        elif selection == 4:
            start_forwarding(setting_manager.get_settings())

        elif selection == 5:
            print
            print 'Qutting connector program'
           
            return


if __name__ == '__main__':
    try:
        control_delegation()

    except:
        pass

    finally:
        #cmd = 'iptables -D FORWARD 1'
        #subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        pass




