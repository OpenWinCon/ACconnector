# -*- coding: utf-8 -*-

import os
import subprocess
import setting_mode as sm


DEVNULL = open(os.devnull, 'w')


def list_active_connections():
    try:
        fp = open('/etc/openvpn/connection.settings', 'r')

    except IOError:
        fp = open('/etc/openvpn/connection.settings', 'w')
        fp.close()
        fp = open('/etc/openvpn/connection.settings', 'r')

    lines = list(map(lambda x: x.replace('\n', ''), fp.readlines()))
    
    connection_dic = {}
    for line in lines:
        info = line.split(',')
        connection_name, server_ip, status = info[0], info[1], info[2]

        if status == 'True':
            connection_dic[connection_name] = {'server_ip': server_ip, 'status': status}

    '''
    fd = subprocess.Popen("ps -ax | grep 'openvpn'", shell=True, stdout=subprocess.PIPE)

    results = list(map(lambda x: x.replace('\n', ''), fd.stdout.readlines()))

    for line in results:
        if 'grep' not in line and 'sudo' not in line:
            info = line.split(' ')[12:]

            setting = info[2].split('/')
            settings[3]
    '''

    return connection_dic


def add_active_connection():
    settings = sm.list_settings()
    connections = list_active_connections() 

    fp = open('/etc/openvpn/connection.settings', 'w')

    print
    for k, v in settings.iteritems():
        print k, v['server_ip'], v['status']
    print

    print 'Select connection to activate: ',
    setting_name = raw_input()
    
    if setting_name not in settings:
        print '%s does not exist in settings folder' % setting_name

    elif setting_name in connections:
        print '%s is active connection' % setting_name
        
    else:
        command = "sudo openvpn --config /etc/openvpn/settings/%s/client.conf &" % setting_name
        subprocess.call(command, shell=True, stdout=DEVNULL)
        
        connection_result = subprocess.Popen("ps -ax | grep '/etc/openvpn/settings/%s'" % setting_name, shell=True, stdout=subprocess.PIPE)

        connection_result = connection_result.stdout.readlines()

        if len(connection_result) == 0:
            print 'Failed to connect'
            print

        else:
            print 'Connection successful'
            print 
            connections[setting_name] = {'server_ip': settings[setting_name]['server_ip'], 'status': True} 
            settings[setting_name] = {'server_ip': settings[setting_name]['server_ip'], 'status': True}


    for k, v in connections.iteritems():
        fp.write('%s,%s,%s\n' % (k, v['server_ip'], v['status']))

    fp = open('/etc/openvpn/settings/server.settings', 'w')
    
    for k, v in settings.iteritems():
        fp.write('%s,%s,%s\n' % (k, v['server_ip'], v['status']))
        

def del_active_connection():
    connections = list_active_connections()

    print
    for k, v in connections.iteritems():
        print k, v['server_ip'], v['status']
    print

    print 'Select connection to remove: ',
    connection_name = raw_input()

    if connection_name not in connections:
        print '%s connection is not active or does not exist in settings' % connection_name

    else:
        result_process = subprocess.Popen("ps -ax | grep 'openvpn --config /etc/openvpn/settings/%s'" % connection_name, shell=True, stdout=subprocess.PIPE)

        lines = result_process.stdout.readlines()
        result_process_id = int(lines[1].split(' ')[0])

        subprocess.Popen("kill -9 %d" % result_process_id, shell=True)

        connections.pop('%s' % connection_name, None)
    
    fp = open('/etc/openvpn/connection.settings', 'w')

    for k, v in connections.iteritems():
        fp.write('%s,%s,%s\n' % (k, v['server_ip'], v['status']))

    fp.close()

