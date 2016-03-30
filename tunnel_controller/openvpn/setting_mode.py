# -*- coding: utf-8 -*-

import os 
import subprocess

OPENVPN_FOLDER = '/etc/openvpn'


def add_setting(setting_name, server_ip, username):
    subprocess.call('mkdir /etc/openvpn/settings/%s' % setting_name, shell=True)
    subprocess.call('mkdir /etc/openvpn/settings/%s/keys' % setting_name, shell=True)

    subprocess.call('scp %s@%s:/etc/openvpn/client_keys.tar /etc/openvpn/settings/%s' % (username, server_ip, setting_name), shell=True)

    subprocess.call('tar -xvf /etc/openvpn/settings/%s/client_keys.tar -C /etc/openvpn/settings/%s/keys' % (setting_name, setting_name), shell=True)

    subprocess.call('cp /etc/openvpn/sample_client.conf /etc/openvpn/settings/%s/client.conf' % setting_name, shell=True)

    fp = open('/etc/openvpn/settings/%s/client.conf' % setting_name, 'r')

    lines = list(map(lambda x: x.replace('\n', ''), fp.readlines()))

    file_new_content = []
    for line in lines:
        if line.startswith('ca'):
            line = 'ca /etc/openvpn/settings/%s/keys/ca.cert' % setting_name

        elif line.startswith('cert'):
            line = 'cert /etc/openvpn/settings/%s/keys/client.cert' % setting_name

        elif line.startswith('key'):
            line = 'cert /etc/openvpn/settings/%s/keys/client.key' % setting_name

        file_new_content.append(line)
        
    fp = open('/etc/openvpn/settings/%s/clinet.conf' % setting_name, 'w')

    for line in file_new_content:
        fp.write(line + '\n')

    setting_lst = list_settings()

    fp = open('/etc/openvpn/settings/server.settings', 'w')
    for k, v in setting_lst.iteritems():
        fp.write('%s,%s,%s\n' % (k, v['server_ip'], v['status']))

    fp.write('%s,%s,%s\n' % (setting_name, server_ip, 'False'))


def list_settings():
    try:
        setting_file = open(os.path.join(OPENVPN_FOLDER, 'settings', 'server.settings'), 'r')

    except OSError:
        os.makedirs(os.path.join(OPENVPN_FOLDER, 'settings'))

    except IOError:
        setting_file = open(os.path.join(OPENVPN_FOLDER, 'settings', 'server.settings'), 'w')
        setting_file.close()
        return {}

    settings = {}
    lines = list(map(lambda x: x.replace('\n', ''), setting_file.readlines()))

    for line in lines:
        info = line.split(',')
        setting_name = info[0]
        server_ip = info[1]
        status = info[2]

        settings[setting_name] = {'server_ip': server_ip, 'status': status}

    return settings

    '''
    if len(settings) == 0:
        print 'No setting exists'

    else:
        for subfolder in settings:
            print subfolder
    '''     

