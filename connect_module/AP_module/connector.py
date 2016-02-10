# -*- coding: utf-8 -*-

import os
import subprocess

from selective_forward import selective_forward_func
from full_forward import full_forward_func
from of_forward import of_forward_func


def control_delegation():
    # cmd = 'iptables -A INPUT -i br-lan -j NFQUEUE --queue-num 1'
    cmd = 'iptables -A OUTPUT -d 8.8.8.8 -j NFQUEUE --queue-num 1'
    p1 = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    cmd = 'sysctl -w net.ipv4.conf.ppp0.rp_filter=2'
    p2 = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    p1.kill()
    p2.kill()

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
            try:
                full_forward_func()

            except KeyboardInterrupt:
                pass

        elif selection == 2:
            selective_forward_func()

        elif selection == 3:
            of_forward_func()

        elif selection == 4:
            print 'Qutting connector program'
           
            cmd = 'iptables -D OUTPUT 1'
            subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

            # TODO: 현재는 이 코드가 실행되면서 프로그램이 종료됨.
            sys.exit(1)


if __name__ == '__main__':
    try:
        control_delegation()

    except:
        pass

    finally:
        cmd = 'iptables -D OUTPUT 1'
        subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
