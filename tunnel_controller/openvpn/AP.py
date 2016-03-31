# -*- coding: utf-8 -*-


import os
import connection_mode as cm
import setting_mode as sm


OPENVPN_FOLDER = '/etc/openvpn'


def tunnel_control():
    while True:
        print
        print 'Host AP Tunnel Controller'
        print '1. Setting mode'
        print '2. Connection mode'
        print '3. Quit'

        try:
            print 'Select mode: ',
            selection = int(raw_input())

        except ValueError:
            print 'Enter proper number (1~3)'
            continue

        if selection == 1:
            setting_mode() 
                    
        elif selection == 2:
            connection_mode() 

        elif selection == 3:
            print
            print 'Qutting tunnel controller'
            return 

        else:
            print 'Enter proper number (1~3)'



def setting_mode():
    while True:
        print
        print 'Host AP Tunnel Controller (OpenVPN) - Setting'
        print '1. List current OpenVPN settings'
        print '2. Add new OpenVPN server'
        print '3. Remove OpenVPN server'
        print '4. Quit'
        
        try:
            print 'Select mode: ',
            selection = int(raw_input())

        except ValueError:
            print 'Enter proper number'
            print
            continue
            
        if selection == 1:
            settings = sm.list_settings()

            print
            print 'Setting Name\tServer IP\tConnection Status'
            for k, v in settings.iteritems():
                print '%s\t\t%s\t%s' % (k, v['server_ip'], v['status'])
            print

        elif selection == 2:
            sm.add_setting()

        elif selection == 3:
            sm.del_setting()

        elif selection == 4:
            return
        
        else:
            print 'Enter proper number'
            print


def connection_mode():
    while True:
        print
        print 'Host AP Tunnel Controller (OpenVPN) - Connection'
        print '1. List current active OpenVPN connections'
        print '2. Activate connection'
        print '3. Deactive connection'
        print '4. Check connection status'
        print '5. Quit'

        try:
            print 'Select mode: ',
            selection = int(raw_input())

        except ValueError:
            print 'Enter proper number'
            print
            continue

        if selection == 1:
            connection_dic = cm.list_active_connections()

            print
            print 'Server IP      | status'
            for k, v in connection_dic.iteritems():
                print '%s | %s' % (v['server_ip'], v['status']) 
            print

        elif selection == 2:
            cm.add_active_connection()
        
        elif selection == 3:
            cm.del_active_connection()

        elif selection == 4:
            pass

        elif selection == 5:
            return

        else:
            print 'Enter proper number'
            print

#setting_mode()
#connection_mode()
