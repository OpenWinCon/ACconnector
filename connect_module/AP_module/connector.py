# -*- coding: utf-8 -*-

import os
import subprocess

#from selective_forward import selective_forward_func
from full_forward import full_forward_func
from of_forward import of_forward_func


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


def control_delegation():
    check_tables()
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
        print '1. Full delegation'
        print '2. Selective delegation'
        print '3. Openflow forward (OVS needed)'
        print '4. Program Quit'

        try:
            print 'Select mode: ',
            selection = int(raw_input())

            if selection not in range(1, 5):
                raise ValueError

        except ValueError:
            print 'Enter proper number (1~4)'
            continue

        if selection == 1:
            full_forward_func()

        elif selection == 2:
            selective_forward_func()

        elif selection == 3:
            of_forward_func()

        elif selection == 4:
            print
            print 'Qutting connector program'
           
            return


if __name__ == '__main__':
    try:
        control_delegation()

    except:
        pass

    finally:
        cmd = 'iptables -D FORWARD 1'
        subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
